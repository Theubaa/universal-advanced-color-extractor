## Perfect Colour Extractor for JPG, PNG, AI, SVG, EPS – FastAPI Color Palette API

This repository provides a **perfect colour extractor** API that detects and previews brand colours from logos, images, and vector files (`.jpg`, `.png`, `.ai`, `.svg`, `.eps`, `.epm`, and PDF).  
It is built with **Python**, **FastAPI**, and a robust image/vector processing pipeline to generate accurate color palettes and visual previews for designers, marketers, and developers.

> **Tip for personalization & SEO:** Replace `YOUR_NAME_HERE` in this README with your real name so that when people search for your name, this project appears in search results.

- **Project type**: Color detection / color palette extraction API  
- **Tech stack**: FastAPI, Pillow, OpenCV, PyMuPDF, CairoSVG, Ghostscript, ImageMagick  
- **Use cases**: Logo color extraction, brand guideline tools, automated color palette generation, design QA  
- **Input formats supported**: JPG, PNG, SVG, PDF, AI, EPS, EPM (and other common raster/vector logo formats)  
- **Output**: Hexadecimal color codes and preview images suitable for design tools and brand systems

**Author / Maintainer:** YOUR_NAME_HERE  

---

## Color Detection API – Ubuntu Setup & Deployment Guide

This guide walks you from a **fresh Ubuntu install** to a **production-style deployment** of this project, including:

- System update & base tools  
- Python, virtualenv, and project setup  
- System libraries required for image and vector processing  
- Running the FastAPI app (development & production)  
- **PM2** setup to keep the API running in the background and restart on reboot  

The instructions assume **Ubuntu 22.04+**, but they will also work (with minor differences) on other recent Ubuntu versions.

---

## 1. Update & Upgrade Ubuntu

Open a terminal and run:

```bash
sudo apt update
sudo apt upgrade -y
```

Optionally remove old packages:

```bash
sudo apt autoremove -y
```

---

## 2. Install Core System Tools

You need some basic tools and compilers:

```bash
sudo apt install -y \
  build-essential \
  curl \
  wget \
  git \
  software-properties-common
```

---

## 3. Install Python & Virtual Environment Tools

Install Python 3 and pip (Ubuntu usually already has them, but this ensures you are set up):

```bash
sudo apt install -y \
  python3 \
  python3-pip \
  python3-venv
```

Check versions:

```bash
python3 --version
pip3 --version
```

---

## 4. Install System Libraries Required by This Project

This project uses:

- **Pillow** and **OpenCV** → need image codecs and dev headers  
- **cairosvg** and **lxml** → need Cairo, Pango, and XML libraries  
- **Ghostscript** and **ImageMagick** → for vector formats (PDF/AI/EPS/EPM)  

Install the required system packages:

```bash
sudo apt install -y \
  libjpeg-dev \
  zlib1g-dev \
  libpng-dev \
  libfreetype6-dev \
  liblcms2-dev \
  libwebp-dev \
  tcl-dev tk-dev \
  libxml2-dev \
  libxslt1-dev \
  libcairo2 \
  libcairo2-dev \
  libpango-1.0-0 \
  libpangocairo-1.0-0 \
  libffi-dev \
  ghostscript \
  imagemagick
```

> **Note:** On some systems, ImageMagick may have security policies that restrict PDF/EPS/AI reading. If you get “not allowed by security policy” errors, you’ll need to adjust `/etc/ImageMagick-*/policy.xml` (outside the scope of this README).

---

## 5. Download the Project Code

You have two main ways to get the code onto your Ubuntu machine.

### 5.1. Clone via Git (recommended)

If your project is in a Git repo (e.g., GitHub, GitLab), run:

```bash
cd ~
git clone <YOUR_REPO_URL> colordetection
cd colordetection
```

Replace `<YOUR_REPO_URL>` with your actual repository URL.

### 5.2. Download ZIP (if no Git access)

1. From your local machine, zip the project folder or download it from its source.
2. Copy the ZIP to the Ubuntu server (via `scp`, SFTP, etc.).
3. On Ubuntu:

```bash
cd ~
unzip colordetection.zip -d colordetection
cd colordetection
```

Ensure you see files like `app.py`, `color_detection.py`, `requirements.txt`, and an `uploads/` directory (it will be auto-created if missing).

---

## 6. Create & Activate a Python Virtual Environment

Inside the project directory:

```bash
cd ~/colordetection
python3 -m venv .venv
```

Activate it:

```bash
source .venv/bin/activate
```

Your prompt should now start with `(.venv)` indicating the virtual environment is active.

To deactivate later:

```bash
deactivate
```

---

## 7. Install Python Dependencies

With the virtual environment activated and in the project directory:

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

This will install:

- `Pillow`, `numpy`, `opencv-python`  
- `beautifulsoup4`, `lxml`, `cairosvg`  
- `fastapi`, `uvicorn`, `python-multipart`  
- `PyMuPDF` and other required libraries  

If any installation fails, read the error carefully; often missing system libraries are the cause (covered in section 4).

---

## 8. Run the App in Development Mode

### 8.1. Using `python app.py`

From the project root with `.venv` active:

```bash
python app.py
```

This uses the `if __name__ == "__main__"` block in `app.py`, which starts Uvicorn on port **8000**.

Open your browser and navigate to:

```text
http://localhost:8000/
```

If you’re on a remote server, replace `localhost` with the server’s IP or domain and ensure port 8000 is allowed in your firewall.

### 8.2. Using `uvicorn` directly

Alternatively:

```bash
uvicorn app:app --host 0.0.0.0 --port 8000 --reload
```

The `--reload` flag is convenient for development (auto-restarts on code changes).

---

## 9. Preparing for Production Deployment

For production, you’ll typically want:

- The app to **run continuously** (and restart if it crashes).  
- Automatic **restart on reboot**.  
- Optional **reverse proxy** (e.g., Nginx) in front (not covered here).  

Here we’ll use **PM2**, a Node.js process manager, to manage the Uvicorn process.

---

## 10. Install Node.js & PM2

### 10.1. Install Node.js (via NodeSource)

Add NodeSource repository (example for Node 20.x – adjust as needed):

```bash
curl -fsSL https://deb.nodesource.com/setup_20.x | sudo -E bash -
sudo apt install -y nodejs
```

Verify:

```bash
node -v
npm -v
```

### 10.2. Install PM2 globally

```bash
sudo npm install -g pm2
```

Verify:

```bash
pm2 --version
```

---

## 11. Running the FastAPI App Under PM2

We want PM2 to manage the Uvicorn process. There are two clean approaches:

- Use PM2’s **`--interpreter`** to run a Python command.  
- Or wrap the Uvicorn command in a small shell script.

Below we use the **interpreter approach**.

> **Note:** Always ensure the virtual environment is set up and dependencies are installed before using PM2.

### 11.1. PM2 command for this project

From the project directory (`~/colordetection`):

```bash
pm2 start "uvicorn app:app --host 0.0.0.0 --port 8000" \
  --name colordetection \
  --interpreter "$(pwd)/.venv/bin/python"
```

Explanation:

- `uvicorn app:app ...` → runs your FastAPI app.  
- `--name colordetection` → a friendly process name in PM2.  
- `--interpreter` → ensures PM2 uses the **Python** from your virtualenv.  

Check status:

```bash
pm2 status
pm2 logs colordetection --lines 100
```

If something is wrong, use logs to debug:

```bash
pm2 logs colordetection
```

Restart and stop:

```bash
pm2 restart colordetection
pm2 stop colordetection
pm2 delete colordetection
```

---

## 12. Enable PM2 Startup on Reboot

PM2 can generate a startup script so your processes restart after a reboot.

Run:

```bash
pm2 startup systemd
```

PM2 will print a command. It typically looks like:

```bash
sudo env PATH=$PATH:/usr/bin pm2 startup systemd -u <your-username> --hp /home/<your-username>
```

Copy and run that exact command.

Then save your current process list:

```bash
pm2 save
```

Now, on every reboot:

- PM2 will start.  
- Your `colordetection` process will be restored automatically.

To test:

```bash
sudo reboot
```

After the machine comes back:

```bash
pm2 status
```

Your `colordetection` app should be listed as **online**.

---

## 13. Optional: Basic Hardening & Tips

- **Use a reverse proxy** like Nginx or Caddy to:
  - Terminate HTTPS.  
  - Forward traffic to `http://127.0.0.1:8000`.  
  - Add rate limiting and headers.

- **Firewall (UFW)**:

  ```bash
  sudo apt install -y ufw
  sudo ufw allow OpenSSH
  sudo ufw allow 8000/tcp   # or your reverse proxy port (80/443)
  sudo ufw enable
  sudo ufw status
  ```

- **Log rotation**: PM2 logs are stored under `~/.pm2/logs`. Monitor disk usage and rotate as needed.

---

## 14. Quick Command Reference

- **Initial setup (once)**:

  ```bash
  sudo apt update && sudo apt upgrade -y
  sudo apt install -y python3 python3-pip python3-venv git build-essential \
      libjpeg-dev zlib1g-dev libpng-dev libfreetype6-dev liblcms2-dev \
      libwebp-dev tcl-dev tk-dev libxml2-dev libxslt1-dev libcairo2 \
      libcairo2-dev libpango-1.0-0 libpangocairo-1.0-0 libffi-dev \
      ghostscript imagemagick
  ```

- **Project setup**:

  ```bash
  git clone <YOUR_REPO_URL> colordetection
  cd colordetection
  python3 -m venv .venv
  source .venv/bin/activate
  pip install -r requirements.txt
  ```

- **Run dev server**:

  ```bash
  python app.py
  # or
  uvicorn app:app --host 0.0.0.0 --port 8000 --reload
  ```

- **PM2 (after Node.js + PM2 install)**:

  ```bash
  pm2 start "uvicorn app:app --host 0.0.0.0 --port 8000" \
    --name colordetection \
    --interpreter "$(pwd)/.venv/bin/python"

  pm2 save
  pm2 startup systemd
  ```

You now have a complete path from **fresh Ubuntu** to a **production-style FastAPI color detection service** running under PM2.  


