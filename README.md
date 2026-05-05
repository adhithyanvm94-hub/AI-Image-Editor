🚀 Prompt-Based Image Editor
<p align="center"> <img src="https://img.shields.io/badge/Streamlit-App-red?style=for-the-badge&logo=streamlit"/> <img src="https://img.shields.io/badge/Python-3.9+-blue?style=for-the-badge&logo=python"/> <img src="https://img.shields.io/badge/HuggingFace-Transformers-yellow?style=for-the-badge&logo=huggingface"/> </p>
🎬 Demo Preview
<p align="center"> <img src="https://media.giphy.com/media/l0MYt5jPR6QX5pnqM/giphy.gif" width="700"/> </p>

✨ Edit images using simple text prompts like magic

🧠 What This App Does
🔥 Upload an image
🧾 Type a prompt
⚡ Get AI-powered edits instantly
✨ Features
🎯 Smart Prompt Editing
change background to blue and dress to red
remove background and crop 1:1
Multi-action execution in a single prompt
🎨 Background Editing
Remove background
Replace background with solid colors
👕 Clothing Recolor
Automatic clothing detection
Realistic color blending using LAB color space
📐 Crop & Resize
Presets: Instagram, Passport, 16:9, 9:16
Custom sizes: 512x512, 1024x1024
🧩 Mask Preview
Visualize segmentation masks in real-time
⚡ Workflow
🛠️ Tech Stack
Category	Tools Used
Language	Python 🐍
UI Framework	Streamlit ⚡
AI Models	Hugging Face 🤗
Image Processing	OpenCV + PIL 🖼️
Data Handling	NumPy 🔢
📦 Installation
git clone https://github.com/your-username/prompt-image-editor.git
cd prompt-image-editor

pip install -r requirements.txt
streamlit run app.py
🧪 Example Prompts
remove background
change background to blue
change dress to red
crop 1:1
resize to 512x512
remove background and change suit to black and crop 4:5
🎥 UI Preview
<p align="center"> <img src="file_0000000034ac7208a93ff450c1158c88" width="800"/> </p>
🧩 How It Works
🧠 Core Components
Segmentation Model
fashn-ai/fashn-human-parser
Mask Processing
OpenCV morphological operations + smoothing
Prompt Parsing
Regex-based action detection
Color Transformation
LAB color space blending for realistic results
💡 Smart Prompt Engine
✔ Detects multiple actions
✔ Executes operations in correct order
✔ Computes masks only once (performance optimized ⚡)
📥 Output
PNG download
Transparent background support (RGBA)
High-quality image resizing
🚧 Future Improvements
🎭 Multi-person support
🎨 Gradient / image backgrounds
🧠 Advanced prompt understanding (LLM integration)
📱 Mobile UI optimization
🤝 Contributing

Pull requests are welcome.
For major changes, please open an issue first.

⭐ Support

If you like this project:

🌟 Star the repo
🍴 Fork it
🧠 Build on top of it
🧑‍💻 Author

Adhithyan VM

⚡ Final Note

This isn’t just an editor — it’s a prompt-driven image engine

Type less. Do more.
