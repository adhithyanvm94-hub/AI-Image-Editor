import io
import re
import numpy as np
import cv2
import streamlit as st
from PIL import Image
from transformers import pipeline

st.set_page_config(page_title="Prompt Image Editor", layout="wide")

# ----------------------------
# LOAD MODEL
# ----------------------------
@st.cache_resource
def load_parser():
    return pipeline("image-segmentation", model="fashn-ai/fashn-human-parser")

parser = load_parser()

# ----------------------------
# COLOR MAP
# ----------------------------
COLOR_MAP = {
    "red": (180, 45, 45),
    "blue": (55, 95, 190),
    "green": (34, 92, 44),
    "yellow": (210, 190, 60),
    "black": (35, 35, 35),
    "white": (235, 235, 235),
    "pink": (210, 140, 170),
    "purple": (130, 85, 150),
    "orange": (210, 125, 55),
    "gray": (140, 140, 140),
    "grey": (140, 140, 140),
    "brown": (120, 90, 65),
}

CLOTH_LABELS = {"top", "dress", "skirt", "pants", "scarf", "belt"}

HUMAN_LABELS = {
    "face", "hair", "top", "dress", "skirt", "pants", "belt", "bag",
    "hat", "scarf", "glasses", "arms", "hands", "legs", "feet", "torso", "jewelry"
}

# ----------------------------
# HELPERS
# ----------------------------
def pil_to_bgr(img: Image.Image):
    return cv2.cvtColor(np.array(img.convert("RGB")), cv2.COLOR_RGB2BGR)

def bgr_to_pil(img):
    return Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))

def ensure_rgb(img: Image.Image):
    return img.convert("RGB")

def resize_preview(img: Image.Image, max_side=1024):
    w, h = img.size
    scale = min(max_side / max(w, h), 1.0)
    return img.resize((max(1, int(w * scale)), max(1, int(h * scale))), Image.LANCZOS)

def union_masks(seg_result, wanted_labels):
    final = None
    for item in seg_result:
        label = item["label"].lower().strip()
        if label in wanted_labels:
            mask = np.array(item["mask"].convert("L"))
            if final is None:
                final = mask
            else:
                final = np.maximum(final, mask)

    if final is None:
        return None

    _, final = cv2.threshold(final, 20, 255, cv2.THRESH_BINARY)
    kernel = np.ones((5, 5), np.uint8)
    final = cv2.morphologyEx(final, cv2.MORPH_OPEN, kernel)
    final = cv2.morphologyEx(final, cv2.MORPH_CLOSE, kernel)
    final = cv2.GaussianBlur(final, (7, 7), 0)
    return final

def apply_alpha_cutout(image: Image.Image, alpha_mask: np.ndarray):
    rgba = image.convert("RGBA")
    arr = np.array(rgba)
    arr[..., 3] = alpha_mask
    return Image.fromarray(arr)

def extract_background_color(prompt: str):
    p = prompt.lower()

    patterns = [
        r'background(?: color)?\s*(?:to|as|into)?\s*(red|blue|green|yellow|black|white|pink|purple|orange|gray|grey|brown)',
        r'(?:make|change|turn)\s+the?\s*background(?: color)?\s*(?:to|as|into)?\s*(red|blue|green|yellow|black|white|pink|purple|orange|gray|grey|brown)',
    ]

    for pat in patterns:
        m = re.search(pat, p)
        if m:
            return m.group(1)

    bg_match = re.search(
        r'background[^.,;]*\b(red|blue|green|yellow|black|white|pink|purple|orange|gray|grey|brown)\b',
        p
    )
    if bg_match:
        return bg_match.group(1)

    return None

def extract_cloth_color(prompt: str):
    p = prompt.lower()
    cloth_words = r'(dress|shirt|top|kurti|hoodie|jacket|coat|blazer|suit|pants|pant|trouser|skirt|clothes|cloth)'

    patterns = [
        rf'{cloth_words}\s*(?:to|as|into)?\s*(red|blue|green|yellow|black|white|pink|purple|orange|gray|grey|brown)',
        rf'(?:make|change|turn)\s+{cloth_words}\s*(?:to|as|into)?\s*(red|blue|green|yellow|black|white|pink|purple|orange|gray|grey|brown)',
        rf'(?:make|change|turn)\s+the?\s*{cloth_words}\s*(?:to|as|into)?\s*(red|blue|green|yellow|black|white|pink|purple|orange|gray|grey|brown)',
    ]

    for pat in patterns:
        m = re.search(pat, p)
        if m:
            return m.group(m.lastindex)

    cloth_match = re.search(
        rf'{cloth_words}[^.,;]*\b(red|blue|green|yellow|black|white|pink|purple|orange|gray|grey|brown)\b',
        p
    )
    if cloth_match:
        return cloth_match.group(cloth_match.lastindex)

    return None

def detect_cloth_target(prompt: str):
    p = prompt.lower()

    if "dress" in p:
        return {"dress"}
    if (
        "shirt" in p or "t-shirt" in p or "tshirt" in p or "top" in p or
        "kurti" in p or "hoodie" in p or "jacket" in p or "coat" in p or
        "blazer" in p or "suit" in p
    ):
        return {"top"}
    if "skirt" in p:
        return {"skirt"}
    if "pant" in p or "pants" in p or "trouser" in p:
        return {"pants"}

    return CLOTH_LABELS

def recolor_masked_region(image: Image.Image, mask: np.ndarray, target_rgb):
    original_alpha = None
    if image.mode == "RGBA":
        original_alpha = image.getchannel("A")

    rgb_image = image.convert("RGB")
    bgr = pil_to_bgr(rgb_image).astype(np.uint8)

    alpha = (mask.astype(np.float32) / 255.0)
    alpha = cv2.GaussianBlur(alpha, (9, 9), 0)
    alpha = np.clip(alpha * 0.95, 0, 1)[..., None]

    src_lab = cv2.cvtColor(bgr, cv2.COLOR_BGR2LAB).astype(np.float32)

    target_bgr = np.full_like(
        bgr,
        (target_rgb[2], target_rgb[1], target_rgb[0]),
        dtype=np.uint8
    )
    target_lab = cv2.cvtColor(target_bgr, cv2.COLOR_BGR2LAB).astype(np.float32)

    result_lab = src_lab.copy()
    color_strength = 0.72

    result_lab[..., 1] = (
        src_lab[..., 1] * (1 - alpha[..., 0] * color_strength)
        + target_lab[..., 1] * (alpha[..., 0] * color_strength)
    )
    result_lab[..., 2] = (
        src_lab[..., 2] * (1 - alpha[..., 0] * color_strength)
        + target_lab[..., 2] * (alpha[..., 0] * color_strength)
    )

    result_bgr = cv2.cvtColor(
        np.clip(result_lab, 0, 255).astype(np.uint8),
        cv2.COLOR_LAB2BGR
    )

    final_rgb = bgr_to_pil(result_bgr)

    if original_alpha is not None:
        final_rgba = final_rgb.convert("RGBA")
        final_rgba.putalpha(original_alpha)
        return final_rgba

    return final_rgb

# ----------------------------
# ONE-TIME MASK EXTRACTION
# ----------------------------
def get_all_masks(image: Image.Image, prompt: str):
    seg = parser(image.convert("RGB"))

    person_mask = union_masks(seg, HUMAN_LABELS)

    target_cloth_labels = detect_cloth_target(prompt)
    cloth_mask = union_masks(seg, target_cloth_labels)

    if cloth_mask is None:
        cloth_mask = union_masks(seg, CLOTH_LABELS)

    return person_mask, cloth_mask

# ----------------------------
# BACKGROUND / CLOTH OPERATIONS
# ----------------------------
def remove_background_with_mask(image: Image.Image, person_mask: np.ndarray):
    if person_mask is None:
        return image, None, "No person mask detected"

    out = apply_alpha_cutout(image, person_mask)
    return out, Image.fromarray(person_mask), "Background removed"

def change_background_with_mask(image: Image.Image, person_mask: np.ndarray, color_name: str):
    if person_mask is None:
        return image, None, "Could not detect subject"

    bgr = pil_to_bgr(image)
    bg_mask = cv2.bitwise_not(person_mask)

    color = COLOR_MAP[color_name]
    bg_color = np.full_like(
        bgr,
        (color[2], color[1], color[0]),
        dtype=np.uint8
    )

    alpha = (bg_mask.astype(np.float32) / 255.0)
    alpha = cv2.GaussianBlur(alpha, (15, 15), 0)
    alpha = np.clip(alpha, 0, 1)[..., None]

    result = (
        bg_color.astype(np.float32) * alpha +
        bgr.astype(np.float32) * (1 - alpha)
    ).astype(np.uint8)

    output = bgr_to_pil(result)
    return output, Image.fromarray(bg_mask), f"Background changed to {color_name}"

def change_clothes_with_mask(image: Image.Image, cloth_mask: np.ndarray, color_name: str):
    if cloth_mask is None:
        return image, None, "No clothing region detected"

    output = recolor_masked_region(image, cloth_mask, COLOR_MAP[color_name])
    return output, Image.fromarray(cloth_mask), f"Changed clothes color to {color_name}"

# ----------------------------
# CROP / RESIZE
# ----------------------------
def crop_center_to_ratio(image: Image.Image, ratio_w: int, ratio_h: int):
    w, h = image.size
    target_ratio = ratio_w / ratio_h
    current_ratio = w / h

    if current_ratio > target_ratio:
        new_w = int(h * target_ratio)
        left = (w - new_w) // 2
        return image.crop((left, 0, left + new_w, h))
    else:
        new_h = int(w / target_ratio)
        top = (h - new_h) // 2
        return image.crop((0, top, w, top + new_h))

def parse_crop_ratio(prompt: str):
    p = prompt.lower().strip()

    m = re.search(r'(\d+)\s*[:x]\s*(\d+)', p)
    if m:
        w = int(m.group(1))
        h = int(m.group(2))
        if w > 0 and h > 0:
            return (w, h)

    if "passport" in p:
        return (35, 45)
    if "square" in p or "instagram post" in p:
        return (1, 1)
    if "portrait" in p or "4:5" in p:
        return (4, 5)
    if "story" in p or "reel" in p or "9:16" in p:
        return (9, 16)
    if "landscape" in p or "youtube thumbnail" in p or "16:9" in p:
        return (16, 9)

    return None

def parse_resize_dims(prompt: str):
    p = prompt.lower()

    m = re.search(r'(\d{2,5})\s*[xX]\s*(\d{2,5})', p)
    if m and any(word in p for word in ["resize", "size", "make it", "convert to", "change size"]):
        return int(m.group(1)), int(m.group(2))

    if "512" in p and "square" in p:
        return (512, 512)
    if "1024" in p and "square" in p:
        return (1024, 1024)

    return None

# ----------------------------
# MULTI ACTION DETECTION
# ----------------------------
def has_bg_remove_request(prompt: str):
    p = prompt.lower()
    return any(k in p for k in [
        "remove background",
        "transparent background",
        "erase background",
        "cut out background"
    ])

def has_background_color_request(prompt: str):
    return extract_background_color(prompt) is not None

def has_color_change_request(prompt: str):
    return extract_cloth_color(prompt) is not None

def has_crop_request(prompt: str):
    p = prompt.lower()
    return (
        "crop" in p or
        "aspect" in p or
        "ratio" in p or
        "passport" in p or
        "square" in p or
        "story" in p or
        "reel" in p or
        "landscape" in p or
        "portrait" in p or
        re.search(r"\d+\s*[:x]\s*\d+", p) is not None
    )

def has_resize_request(prompt: str):
    p = prompt.lower()
    return (
        "resize" in p or
        "size" in p or
        "convert to" in p or
        "change size" in p
    )

def parse_actions(prompt: str):
    actions = []

    if has_bg_remove_request(prompt):
        actions.append("bg_remove")
    if has_background_color_request(prompt):
        actions.append("bg_color")
    if has_color_change_request(prompt):
        actions.append("color_change")
    if has_crop_request(prompt):
        actions.append("crop")
    if has_resize_request(prompt):
        actions.append("resize")

    return actions

# ----------------------------
# WRAPPER MODES
# ----------------------------
def remove_background_person(image: Image.Image):
    person_mask, _ = get_all_masks(image, "")
    return remove_background_with_mask(image, person_mask)

def change_background_color(image: Image.Image, prompt: str):
    color_name = extract_background_color(prompt)
    if not color_name:
        return image, None, "No background color found"

    person_mask, _ = get_all_masks(image, prompt)
    return change_background_with_mask(image, person_mask, color_name)

def change_clothes_color(image: Image.Image, prompt: str):
    color_name = extract_cloth_color(prompt)
    if not color_name:
        return image, None, "No clothing color found in prompt"

    _, cloth_mask = get_all_masks(image, prompt)
    return change_clothes_with_mask(image, cloth_mask, color_name)

def crop_by_prompt(image: Image.Image, prompt: str):
    ratio = parse_crop_ratio(prompt)
    if ratio is None:
        return image, "No crop ratio found in prompt"

    out = crop_center_to_ratio(image, ratio[0], ratio[1])
    return out, f"Cropped to {ratio[0]}:{ratio[1]}"

def resize_by_prompt(image: Image.Image, prompt: str):
    dims = parse_resize_dims(prompt)
    if dims is None:
        return image, "No resize size found in prompt"

    out = image.resize(dims, Image.LANCZOS)
    return out, f"Resized to {dims[0]}x{dims[1]}"

# ----------------------------
# SMART EDIT
# ----------------------------
def smart_edit(image: Image.Image, prompt: str):
    actions = parse_actions(prompt)

    current = image
    preview_mask = None
    messages = []

    if not actions:
        return image, None, "No supported instruction found"

    # Compute masks ONCE from the original image
    person_mask, cloth_mask = get_all_masks(image, prompt)

    # 1. background remove
    if "bg_remove" in actions:
        current, bg_mask_preview, msg = remove_background_with_mask(current, person_mask)
        if bg_mask_preview is not None:
            preview_mask = bg_mask_preview
        messages.append(msg)

    # 2. background color
    if "bg_color" in actions:
        bg_color = extract_background_color(prompt)
        current_for_bg = current.convert("RGB") if current.mode == "RGBA" else current
        current, bgc_mask, msg = change_background_with_mask(current_for_bg, person_mask, bg_color)
        if bgc_mask is not None:
            preview_mask = bgc_mask
        messages.append(msg)

    # 3. clothes color
    if "color_change" in actions:
        cloth_color = extract_cloth_color(prompt)
        current, cloth_mask_preview, msg = change_clothes_with_mask(current, cloth_mask, cloth_color)
        if cloth_mask_preview is not None:
            preview_mask = cloth_mask_preview
        messages.append(msg)

    # 4. crop
    if "crop" in actions:
        current, msg = crop_by_prompt(current, prompt)
        messages.append(msg)

    # 5. resize
    if "resize" in actions:
        current, msg = resize_by_prompt(current, prompt)
        messages.append(msg)

    return current, preview_mask, " | ".join(messages)

# ----------------------------
# UI
# ----------------------------
st.title("Prompt-Based Image Editor")
st.caption("Uses pretrained Hugging Face models. Best for single-person photos.")

mode = st.selectbox(
    "Mode",
    ["Smart Prompt", "Remove Background", "Change Background Color", "Change Clothes Color", "Crop", "Resize"]
)

uploaded = st.file_uploader("Upload image", type=["png", "jpg", "jpeg"])

prompt = st.text_area(
    "Prompt",
    placeholder=(
        "Examples:\n"
        "remove background and change dress to blue and crop to 1:1\n"
        "change background to blue and dress to red\n"
        "make background white and suit black\n"
        "change dress to red and crop 16:9\n"
        "resize to 512x512"
    )
)

col1, col2 = st.columns(2)

if uploaded:
    image = Image.open(uploaded)
    image = resize_preview(image, 1280)

    with col1:
        st.subheader("Input")
        st.image(image, use_column_width=True)

    if st.button("Generate"):
        with st.spinner("Processing..."):
            mask_preview = None

            if mode == "Remove Background":
                output, mask_preview, status = remove_background_person(image)

            elif mode == "Change Background Color":
                output, mask_preview, status = change_background_color(image, prompt)

            elif mode == "Change Clothes Color":
                output, mask_preview, status = change_clothes_color(image, prompt)

            elif mode == "Crop":
                output, status = crop_by_prompt(image, prompt)
                mask_preview = None

            elif mode == "Resize":
                output, status = resize_by_prompt(image, prompt)
                mask_preview = None

            else:
                output, mask_preview, status = smart_edit(image, prompt)

        with col2:
            st.subheader("Output")
            st.image(output, use_column_width=True)
            st.success(status)

        if mask_preview is not None:
            st.subheader("Mask Preview")
            st.image(mask_preview, clamp=True, use_column_width=True)

        buf = io.BytesIO()
        save_img = output

        if isinstance(save_img, Image.Image):
            save_img.save(buf, format="PNG")
            mime = "image/png"
            fname = "edited_output.png"

            st.download_button(
                "Download Output",
                data=buf.getvalue(),
                file_name=fname,
                mime=mime
            )