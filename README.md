<p align="center">
  <img src="https://readme-typing-svg.herokuapp.com?font=Fira+Code&size=28&duration=3000&pause=1000&color=3B82F6&center=true&vCenter=true&width=800&lines=Prompt-Based+Image+Editor;Edit+Images+Using+Natural+Language;No+Tools+Just+Type+Your+Prompt;AI-Powered+Image+Editing" />
</p>


# 🚀 Prompt-Based Image Editor

<p align="center">
  <img src="https://img.shields.io/badge/Streamlit-App-red?style=for-the-badge&logo=streamlit"/>
  <img src="https://img.shields.io/badge/Python-3.9+-blue?style=for-the-badge&logo=python"/>
  <img src="https://img.shields.io/badge/HuggingFace-Transformers-yellow?style=for-the-badge&logo=huggingface"/>
</p>

<p align="center">
  <b>Edit images using natural language — no tools, just prompts.</b>
</p>

---

## ✨ Overview

This project lets you **edit images by simply describing what you want**.

No complex UI. No manual tools.  
Just upload → type → get results.

Example:  
"remove background and change dress to blue and crop 1:1"

---

## 🖥️ App UI

<p align="center">
  <img src="./assets/ui.png" width="850"/>
</p>

<p align="center">
  <em>Clean Streamlit interface with real-time AI editing</em>
</p>

---

## ⚡ Features

- 🎯 Prompt-based editing (multi-action support)  
- 🎨 Background removal & color replacement  
- 👕 Clothing recolor with realistic shading  
- 📐 Smart crop & resize (1:1, 4:5, 16:9, custom)  
- 🧩 Mask preview for debugging  
- ⚡ Optimized pipeline (single segmentation pass)  

---

## 🧠 How it works

Upload Image → Enter Prompt → Segmentation Model → Mask Generation → Apply Edits → Final Output

Under the hood:

- Uses Hugging Face segmentation model  
- Extracts regions (person, clothes, background)  
- Applies edits using OpenCV + LAB color blending  
- Executes multiple actions from a single prompt  

---

## 🧪 Example Prompts

remove background  
change background to white  
change dress to red  
make shirt black  
crop 1:1  
resize to 512x512  
remove background and change suit to black and crop 4:5  

---

## 🛠️ Tech Stack

| Layer            | Tools |
|------------------|------|
| Language         | Python |
| UI               | Streamlit |
| AI Model         | Hugging Face Transformers |
| Image Processing | OpenCV, PIL |
| Data Handling    | NumPy |

---

## 📦 Installation

git clone https://github.com/your-username/prompt-image-editor.git  
cd prompt-image-editor  

pip install -r requirements.txt  
streamlit run app.py  

---

## 📥 Output

- High-quality PNG export  
- Supports transparent background (RGBA)  
- Preserves lighting and texture  

---

## 🚧 Roadmap

- Multi-person support  
- Gradient & image backgrounds  
- Better prompt understanding  
- Mobile UI improvements  

---

## 🤝 Contributing

Contributions are welcome.

Fork the repo → create a branch → open a PR.

---

## 🧑‍💻 Author

Adhithyan VM

---

## ⭐ Support

If you found this useful:

Star the repo  
Fork it  
Build something cool  

---

## ⚡ Final Thought

Editing images should feel like talking, not clicking.
