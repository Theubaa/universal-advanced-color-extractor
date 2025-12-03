#this code ouptu is in Hexadecimal format
from fastapi import FastAPI, UploadFile, File
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
import uvicorn
from color_detection import detect_colors
import os
from typing import Dict, Any, List
import base64
from io import BytesIO
import fitz  # PyMuPDF for PDF -> PNG conversion
import subprocess
import shutil
from PIL import Image
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Color Detection API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["#your    site name"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create uploads directory if it doesn't exist
os.makedirs("uploads", exist_ok=True)

@app.get("/", response_class=HTMLResponse)
async def get_upload_page():
    return """
    <!DOCTYPE html>
    <html>
        <head>
            <title>Color Detection</title>
            <style>
                body {
                    font-family: Arial, sans-serif;
                    max-width: 1200px;
                    margin: 0 auto;
                    padding: 20px;
                    background-color: #f5f5f5;
                }
                .container {
                    background-color: white;
                    padding: 20px;
                    border-radius: 8px;
                    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
                }
                h1 {
                    color: #333;
                    text-align: center;
                }
                .upload-form {
                    display: flex;
                    flex-direction: column;
                    gap: 20px;
                    align-items: center;
                }
                .file-input {
                    padding: 10px;
                    border: 2px dashed #ccc;
                    border-radius: 4px;
                    width: 100%;
                    max-width: 400px;
                    display: none;
                }
                .submit-btn {
                    background-color: #4CAF50;
                    color: white;
                    padding: 10px 20px;
                    border: none;
                    border-radius: 4px;
                    cursor: pointer;
                    font-size: 16px;
                }
                .submit-btn:hover {
                    background-color: #45a049;
                }
                #result {
                    margin-top: 20px;
                    padding: 20px;
                    border-radius: 4px;
                    display: none;
                }
                .color-box {
                    display: inline-block;
                    width: 20px;
                    height: 20px;
                    margin-right: 5px;
                    border: 1px solid #ccc;
                    vertical-align: middle;
                }
                .logo-result {
                    border: 1px solid #ddd;
                    padding: 20px;
                    margin: 20px 0;
                    border-radius: 8px;
                    background-color: white;
                }
                .logo-preview {
                    max-width: 200px;
                    max-height: 200px;
                    margin: 10px 0;
                }
                .colors-grid {
                    display: grid;
                    grid-template-columns: repeat(auto-fill, minmax(150px, 1fr));
                    gap: 10px;
                    margin-top: 10px;
                }
                .color-item {
                    display: flex;
                    align-items: center;
                    gap: 5px;
                }
                .drop-zone {
                    border: 2px dashed #ccc;
                    padding: 20px;
                    text-align: center;
                    border-radius: 4px;
                    cursor: pointer;
                    transition: border-color 0.3s ease;
                }
                .drop-zone:hover {
                    border-color: #4CAF50;
                }
                .drop-zone.dragover {
                    border-color: #4CAF50;
                    background-color: #f0f9f0;
                }
            </style>
        </head>
        <body>
            <div class="container">
                <h1>Color Detection</h1>
                <form class="upload-form" id="uploadForm">
                    <div class="drop-zone" id="dropZone">
                        <p>Drag and drop up to 100 logo files here or click to select</p>
                        <input type="file" 
                               class="file-input"
                               id="file-input"
                               accept=".png,.jpg,.jpeg,.svg,.pdf,.ai,.eps,.epm,application/pdf,application/postscript"
                               multiple>
                    </div>
                    <button type="submit" class="submit-btn" id="detectBtn">Detect Colors</button>
                </form>
                <div id="loading" style="display:none; text-align:center; margin-top:20px; font-weight:bold; color:#4CAF50;">Uploading and processing files...</div>
                <div id="result"></div>
            </div>
            <script>
                const dropZone = document.getElementById('dropZone');
                const fileInput = document.getElementById('file-input');
                const resultDiv = document.getElementById('result');

                // Drag and drop handlers
                dropZone.addEventListener('dragover', (e) => {
                    e.preventDefault();
                    dropZone.classList.add('dragover');
                });

                dropZone.addEventListener('dragleave', () => {
                    dropZone.classList.remove('dragover');
                });

                dropZone.addEventListener('drop', (e) => {
                    e.preventDefault();
                    dropZone.classList.remove('dragover');
                    fileInput.files = e.dataTransfer.files;
                });

                dropZone.addEventListener('click', () => {
                    fileInput.click();
                });

                document.getElementById('uploadForm').onsubmit = async (e) => {
                    e.preventDefault();
                    const detectBtn = document.getElementById('detectBtn');
                    const loadingDiv = document.getElementById('loading');
                    detectBtn.disabled = true;
                    loadingDiv.style.display = 'block';
                    
                    if (!fileInput.files.length) {
                        alert('Please select at least one file');
                        detectBtn.disabled = false;
                        loadingDiv.style.display = 'none';
                        return;
                    }

                    if (fileInput.files.length > 100) {
                        alert('Maximum 100 files allowed');
                        detectBtn.disabled = false;
                        loadingDiv.style.display = 'none';
                        return;
                    }

                    const formData = new FormData();
                    for (let file of fileInput.files) {
                        formData.append('files', file);
                    }

                    try {
                        const response = await fetch('/upload', {
                            method: 'POST',
                            body: formData
                        });
                        const data = await response.json();
                        
                        let resultsHtml = '<h2>Results:</h2>';
                        
                        data.results.forEach(result => {
                            resultsHtml += `
                                <div class="logo-result">
                                    <h3>${result.filename}</h3>
                                    <img src="${result.preview}" class="logo-preview" alt="${result.filename}">
                                    <p>Total Colors Detected: ${result.count}</p>
                                    <div class="colors-grid">
                                        ${result.colors.map(color => `
                                            <div class="color-item">
                                                <span class="color-box" style="background-color: ${color}"></span>
                                                <span>${color}</span>
                                            </div>
                                        `).join('')}
                                    </div>
                                </div>
                            `;
                        });
                        
                        resultDiv.innerHTML = resultsHtml;
                        resultDiv.style.display = 'block';
                    } catch (error) {
                        alert('Error uploading files');
                        console.error(error);
                    } finally {
                        detectBtn.disabled = false;
                        loadingDiv.style.display = 'none';
                    }
                };
            </script>
        </body>
    </html>
    """

def _convert_pdf_to_png(pdf_path: str) -> str:
    """
    Convert the first page of a PDF to a high-resolution PNG.
    Returns the path to the generated PNG file.
    """
    doc = fitz.open(pdf_path)
    if len(doc) == 0:
        doc.close()
        raise ValueError("PDF has no pages")
    page = doc[0]
    # Use a scaling matrix for higher resolution rendering
    matrix = fitz.Matrix(2.0, 2.0)
    pix = page.get_pixmap(matrix=matrix)
    png_path = os.path.splitext(pdf_path)[0] + "_page1.png"
    pix.save(png_path)
    doc.close()
    return png_path


def _convert_ai_to_png(ai_path: str) -> str:
    """
    Convert an Adobe Illustrator (.ai) file to PNG using a 3-level fallback:
    1) Try to open directly with PyMuPDF and treat as PDF.
    2) Fallback to Ghostscript to create a PDF, then reuse the PDF -> PNG pipeline.
    3) Final fallback to ImageMagick (`magick`) to rasterize directly to PNG.
    Returns the path to the generated PNG file.
    """
    # 1) Try to treat the file as a PDF-compatible AI using PyMuPDF directly
    try:
        doc = fitz.open(ai_path)
        if len(doc) == 0:
            doc.close()
        else:
            doc.close()
            return _convert_pdf_to_png(ai_path)
    except Exception:
        # PyMuPDF couldn't handle it as a PDF-compatible file; continue to next fallback
        pass

    # 2) Fallback: use Ghostscript to convert AI -> PDF, then reuse PDF -> PNG
    pdf_path = os.path.splitext(ai_path)[0] + ".pdf"
    gs_executable = shutil.which("gswin64c") or shutil.which("gswin32c") or shutil.which("gs")
    if gs_executable:
        cmd = [
            gs_executable,
            "-dSAFER",
            "-dBATCH",
            "-dNOPAUSE",
            "-sDEVICE=pdfwrite",
            f"-sOutputFile={pdf_path}",
            ai_path,
        ]
        result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if result.returncode == 0 and os.path.exists(pdf_path):
            try:
                png_path = _convert_pdf_to_png(pdf_path)
                return png_path
            finally:
                if os.path.exists(pdf_path):
                    os.remove(pdf_path)

    # 3) Final fallback: use ImageMagick (`magick`) to rasterize AI -> PNG directly
    magick_executable = shutil.which("magick") or shutil.which("convert")
    if magick_executable:
        png_path = os.path.splitext(ai_path)[0] + "_page1.png"
        cmd = [
            magick_executable,
            ai_path,
            png_path,
        ]
        result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if result.returncode == 0 and os.path.exists(png_path):
            return png_path

    # If all fallbacks fail, surface a clear, user-friendly error
    raise RuntimeError("This vector file is a raw Illustrator-only format and cannot be processed.")


def _convert_eps_to_png(eps_path: str) -> str:
    """
    Convert an EPS/EPM file to PNG using a 3-level fallback:
    1) Try to open directly with PyMuPDF and treat as PDF.
    2) Fallback to Ghostscript to create a PDF, then reuse the PDF -> PNG pipeline.
    3) Final fallback to ImageMagick (`magick`) to rasterize directly to PNG.
    Returns the path to the generated PNG file.
    """
    # 1) Try to treat the file as a PDF-compatible EPS/EPM using PyMuPDF directly
    try:
        doc = fitz.open(eps_path)
        if len(doc) == 0:
            doc.close()
        else:
            doc.close()
            return _convert_pdf_to_png(eps_path)
    except Exception:
        # PyMuPDF couldn't handle it as a PDF-compatible file; continue to next fallback
        pass

    # 2) Fallback: use Ghostscript to convert EPS/EPM -> PDF, then reuse PDF -> PNG
    pdf_path = os.path.splitext(eps_path)[0] + ".pdf"
    gs_executable = shutil.which("gswin64c") or shutil.which("gswin32c") or shutil.which("gs")
    if gs_executable:
        cmd = [
            gs_executable,
            "-dSAFER",
            "-dBATCH",
            "-dNOPAUSE",
            "-sDEVICE=pdfwrite",
            f"-sOutputFile={pdf_path}",
            eps_path,
        ]
        result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if result.returncode == 0 and os.path.exists(pdf_path):
            try:
                png_path = _convert_pdf_to_png(pdf_path)
                return png_path
            finally:
                if os.path.exists(pdf_path):
                    os.remove(pdf_path)

    # 3) Final fallback: use ImageMagick (`magick`) to rasterize EPS/EPM -> PNG directly
    magick_executable = shutil.which("magick") or shutil.which("convert")
    if magick_executable:
        png_path = os.path.splitext(eps_path)[0] + "_page1.png"
        cmd = [
            magick_executable,
            eps_path,
            png_path,
        ]
        result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if result.returncode == 0 and os.path.exists(png_path):
            return png_path

    # If all fallbacks fail, surface a clear, user-friendly error
    raise RuntimeError("This vector file is a raw Illustrator-only format and cannot be processed.")


def _prepare_raster_image_for_detection(image_path: str) -> str:
    """
    Normalize raster images (.png, .jpg, .jpeg) before passing them to detect_colors:
    - Open with PIL
    - Convert CMYK/LA/L/Palette/etc. to 3-channel RGB
    - Save as a temporary PNG and return its path
    """
    ext = os.path.splitext(image_path)[1].lower()
    if ext not in ('.png', '.jpg', '.jpeg'):
        return image_path

    img = Image.open(image_path)

    # Normalize color modes to 3-channel RGB
    if img.mode in ('CMYK', 'P'):
        img = img.convert('RGB')
    elif img.mode == 'LA':
        img = img.convert('RGBA').convert('RGB')
    elif img.mode == 'L':
        img = img.convert('RGB')
    elif img.mode == 'RGBA':
        # Strip alpha but keep RGB channels
        img = img.convert('RGB')

    rgb_path = os.path.splitext(image_path)[0] + "_rgb.png"
    img.save(rgb_path, format='PNG')
    return rgb_path


@app.post("/upload")
async def upload_files(files: List[UploadFile] = File(...)) -> Dict[str, Any]:
    results = []
    
    for file in files:
        # Save the uploaded file temporarily
        file_path = f"uploads/{file.filename}"
        with open(file_path, "wb") as buffer:
            content = await file.read()
            buffer.write(content)

        # Determine if this is a PDF/AI/EPS file that needs preprocessing
        ext = os.path.splitext(file.filename)[1].lower()
        processed_path = file_path
        is_pdf = ext == '.pdf'
        is_ai = ext == '.ai'
        is_eps = ext in ('.eps', '.epm')
        if is_pdf:
            # PDF -> PNG conversion happens here, before the existing pipeline
            processed_path = _convert_pdf_to_png(file_path)
        elif is_ai:
            # AI -> PNG conversion happens here, before the existing pipeline
            processed_path = _convert_ai_to_png(file_path)
        elif is_eps:
            # EPS/EPM -> PNG conversion happens here, before the existing pipeline
            processed_path = _convert_eps_to_png(file_path)
        elif ext in ('.png', '.jpg', '.jpeg'):
            # Raster images (PNG/JPG/JPEG) go directly through the raster loader
            # before entering the existing detect_colors pipeline.
            processed_path = _prepare_raster_image_for_detection(file_path)
        
        try:
            # Process the file using the existing color detection pipeline
            count, colors = detect_colors(processed_path)
            
            # Determine MIME type for preview (SVG keeps its type, others use PNG)
            if ext == '.svg':
                mime = 'image/svg+xml'
                preview_path = file_path
            else:
                mime = 'image/png'
                preview_path = processed_path

            # Create preview image
            with open(preview_path, "rb") as image_file:
                preview = f"data:{mime};base64," + base64.b64encode(image_file.read()).decode()
            
            results.append({
                "filename": file.filename,
                "count": count,
                "colors": list(colors),
                "preview": preview
            })
            
        except Exception as e:
            if os.path.exists(file_path):
                os.remove(file_path)
            if processed_path != file_path and os.path.exists(processed_path):
                os.remove(processed_path)
            raise e
        finally:
            # Clean up the temporary files
            if os.path.exists(file_path):
                os.remove(file_path)
            if processed_path != file_path and os.path.exists(processed_path):
                os.remove(processed_path)
    
    return {"results": results}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000) 