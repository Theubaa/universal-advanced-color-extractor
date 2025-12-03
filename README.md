# 🎨 Universal Advanced Colour Extractor API
### Perfect Color Extraction from JPG, PNG, SVG, AI, EPS, PDF & EPM — Powered by FastAPI

This repository provides a **high-performance colour extraction API** that detects accurate brand colours from images and vector files.  
It is built using **FastAPI + Python**, supports multiple formats, and generates **clean color palettes + preview assets** for designers, developers, and enterprises.

---

## ⭐ Key Features
- ✔ Extract accurate brand colors from **JPG, PNG, SVG, AI, EPS, PDF, EPM**
- ✔ Supports both **vector + raster** logo formats  
- ✔ FastAPI-based modern backend  
- ✔ Brand guideline automation  
- ✔ Generates preview images  
- ✔ Vector rendering using **CairoSVG, PyMuPDF, Ghostscript, ImageMagick**  
- ✔ Ubuntu production deployment guide included  
- ✔ MIT-Licensed → commercial & personal use allowed  

---

## 🔥 Who Is This For?
- **UI/UX Designers**
- **Developers**
- **Marketing Teams**
- **Automation Systems**
- **AI Projects needing colour metadata**

---

## 📌 Tech Stack
- FastAPI  
- Pillow  
- OpenCV  
- PyMuPDF  
- BeautifulSoup4  
- LXML  
- CairoSVG  
- Ghostscript  
- ImageMagick  

---

## 🖼 Supported Input Formats

| Format | Type | Supported |
|--------|------|-----------|
| JPG / PNG | Raster | ✅ |
| SVG | Vector | ✅ |
| AI | Vector | ✅ |
| EPS | Vector | ✅ |
| PDF | Vector | ✅ |
| EPM | Vector | ✅ |

---

# 🔧 Installation & Setup

## 1️⃣ Clone the Repository
```bash
git clone https://github.com/Theubaa/universal-advanced-color-extractor.git
cd universal-advanced-color-extractor
```

## 2️⃣ Create a Virtual Environment
```bash
python3 -m venv .venv
source .venv/bin/activate
```

## 3️⃣ Install Dependencies
```bash
pip install -r requirements.txt
```

---

# 🚀 Run in Development Mode

### Option 1: Run Directly
```bash
python app.py
```

### Option 2: Run with Uvicorn
```bash
uvicorn app:app --host 0.0.0.0 --port 8000 --reload
```

Now open:
```
http://localhost:8000/
```

---

# 🟢 Ubuntu Deployment Guide (Production Ready)

## 1️⃣ System Update
```bash
sudo apt update && sudo apt upgrade -y
sudo apt autoremove -y
```

## 2️⃣ Install Required Tools
```bash
sudo apt install -y build-essential curl wget git software-properties-common
```

## 3️⃣ Install Python Tools
```bash
sudo apt install -y python3 python3-pip python3-venv
```

## 4️⃣ Install System Libraries
```bash
sudo apt install -y \
libjpeg-dev zlib1g-dev libpng-dev libfreetype6-dev liblcms2-dev \
libwebp-dev tcl-dev tk-dev libxml2-dev libxslt1-dev libcairo2 libcairo2-dev \
libpango-1.0-0 libpangocairo-1.0-0 libffi-dev ghostscript imagemagick
```

## 5️⃣ Install PM2 (Process Manager)
```bash
curl -fsSL https://deb.nodesource.com/setup_20.x | sudo -E bash -
sudo apt install -y nodejs
sudo npm install -g pm2
```

## 6️⃣ Run App Under PM2
```bash
pm2 start "uvicorn app:app --host 0.0.0.0 --port 8000" \
--name colordetection \
--interpreter "$(pwd)/.venv/bin/python"
```

Enable auto-restart:
```bash
pm2 startup systemd
pm2 save
```

---

# 🎯 API Output Includes
- ✔ Hex color palette  
- ✔ Dominant colors  
- ✔ Color frequency  
- ✔ Preview palette image  
- ✔ Clean structured JSON  

---

# 🧩 Folder Structure
```
/universal-advanced-color-extractor
│── app.py
│── color_detection.py
│── utils/
│── uploads/
│── previews/
│── requirements.txt
│── README.md
│── LICENSE
│── .gitignore
```

---

# ⭐ Contributing
Contributions are welcome!

- ⭐ Star this repository  
- 🍴 Fork it  
- 🔧 Submit PRs  
- 🐞 Open issues  

---

# 📜 License — MIT
This project is licensed under the **MIT License**, which permits:

✔ Commercial use  
✔ Modification  
✔ Distribution  
✔ Private use  

Just credit the author.

---

# 👨‍💻 Author  
**Vibhanshu Kumar Shubham (Theubaa)**  
DevOps & AI Engineer  
GitHub: https://github.com/Theubaa

---

# 🚀 Enjoy the Universal Advanced Colour Extractor API!
