🚀 Prompt-Based Image Editor
<p align="center"> <img src="https://img.shields.io/badge/Streamlit-App-red?style=for-the-badge&logo=streamlit"> <img src="https://img.shields.io/badge/Python-3.9+-blue?style=for-the-badge&logo=python"> <img src="https://img.shields.io/badge/HuggingFace-Transformers-yellow?style=for-the-badge&logo=huggingface"> </p>
🎬 Demo Preview
<p align="center"> <img src="https://media.giphy.com/media/l0MYt5jPR6QX5pnqM/giphy.gif" width="700"/> </p>

✨ Edit images using simple text prompts like magic!

🧠 What This App Does

🔥 Upload an image
🧾 Type a prompt
⚡ Get AI-powered edits instantly

✨ Features

🎯 Smart Prompt Editing

"change background to blue and dress to red"
"remove background and crop 1:1"

🎨 Background Editing

Remove background
Replace with solid color

👕 Clothing Recolor

Detects clothes automatically
Applies realistic color blending

📐 Crop & Resize

Instagram, Passport, 16:9, 9:16
Custom dimensions like 512x512

🧩 Mask Preview

See AI segmentation in real-time
⚡ Live Workflow
🛠️ Tech Stack
🐍 Python
⚡ Streamlit
🤗 Hugging Face Transformers
🖼️ OpenCV + PIL
🔢 NumPy
📦 Installation
git clone https://github.com/your-username/prompt-image-editor.git
cd prompt-image-editor

pip install -r requirements.txt
streamlit run app.py
🧪 Example Prompts

💡 Try these:

remove background
change background to blue
change dress to red
crop 1:1
resize to 512x512
remove background and change suit to black and crop 4:5
🎥 UI Preview
<p align="center"> <img src="file_0000000034ac7208a93ff450c1158c88" width="800"/> </p>
🧩 How It Works

🧠 Uses:

fashn-ai/fashn-human-parser for segmentation
Mask processing with OpenCV
Prompt parsing via Regex
LAB color blending for realism
💡 Smart Prompt Engine

✔ Detects multiple actions
✔ Executes in correct order
✔ Applies masks only once (optimized ⚡)

📥 Output
PNG Download
Preserves transparency (RGBA)
High-quality resizing
🚧 Future Improvements
🎭 Multi-person support
🎨 Gradient / image backgrounds
🧠 Better prompt understanding (LLM integration)
📱 Mobile UI optimization
🤝 Contributing

Pull requests are welcome. For major changes, open an issue first.

⭐ Support

If you like this project:

🌟 Star the repo
🍴 Fork it
🧠 Build on top of it

🧑‍💻 Author

Adhithyan VM

⚡ Final Note

This isn’t just an editor — it’s a prompt-driven image engine.

Type less. Do more.
