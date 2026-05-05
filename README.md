# 🚀 Prompt-Based Image Editor

<p align="center">
  <img src="https://img.shields.io/badge/Streamlit-App-red?style=for-the-badge&logo=streamlit"/>
  <img src="https://img.shields.io/badge/Python-3.9+-blue?style=for-the-badge&logo=python"/>
  <img src="https://img.shields.io/badge/HuggingFace-Transformers-yellow?style=for-the-badge&logo=huggingface"/>
</p>

<hr/>

## 🧠 What this project does

This is a simple app where you can edit images just by typing what you want.

Upload a photo, write something like:  
**"change background to blue and dress to red"**

…and the app handles the rest.

<hr/>

## ✨ What you can do

### 🎯 Edit with plain English  
Just type what you want:
- remove background  
- change background to white  
- make shirt black  
- crop 1:1  
- resize to 512x512  

You can also combine multiple actions in one prompt.

---

### 🎨 Background editing  
- Remove background  
- Replace with solid colors  

---

### 👕 Change clothes color  
- Detects clothing automatically  
- Keeps natural lighting and shading  

---

### 📐 Crop & resize  
- Supports common ratios (1:1, 4:5, 16:9)  
- Custom sizes also supported  

---

### 🧩 Mask preview  
- View AI-detected regions  

<hr/>

## 🖥️ App UI

<p align="center">
  <img src="./assets/ui.png" width="800"/>
</p>

<p align="center">
  <em>Main interface of the Prompt-Based Image Editor</em>
</p>

<hr/>

## ⚡ How it works

1. Detects person and clothing using AI  
2. Generates masks for specific regions  
3. Applies edits only where needed  
4. Combines everything into final image  

<hr/>

## 🛠️ Built with

- Python  
- Streamlit  
- Hugging Face Transformers  
- OpenCV + PIL  
- NumPy  

<hr/>

## 📦 Installation

```bash
git clone https://github.com/your-username/prompt-image-editor.git
cd prompt-image-editor

pip install -r requirements.txt
streamlit run app.py
