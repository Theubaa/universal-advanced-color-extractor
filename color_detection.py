from PIL import Image
import numpy as np
from bs4 import BeautifulSoup
import os
import re
import cv2

def count_png_colors(file_path, n_colors=5):
    image = Image.open(file_path).convert("RGBA")
    np_img = np.array(image)
    # Remove fully transparent pixels
    pixels = np_img[np_img[:, :, 3] != 0][:, :3]
    if len(pixels) == 0:
        return 0, set()
    # Use OpenCV k-means to find dominant colors
    Z = pixels.reshape((-1, 3)).astype(np.float32)
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 20, 1.0)
    K = min(n_colors, len(Z))
    _, labels, centers = cv2.kmeans(Z, K, None, criteria, 10, cv2.KMEANS_RANDOM_CENTERS)
    centers = np.uint8(centers)
    color_labels = set()
    for center in centers:
        if tuple(center) == (255, 255, 255):
            color_labels.add('white')
        else:
            color_labels.add('#{:02X}{:02X}{:02X}'.format(*center))
    return len(color_labels), color_labels

def extract_svg_colors(file_path):
    def is_white(color):
        color = color.strip().lower()
        if color in ['#fff', '#ffffff', '#FFF', '#FFFFFF', 'white']:
            return True
        rgb_match = re.match(r'rgb\s*\(\s*255\s*,\s*255\s*,\s*255\s*\)', color)
        if rgb_match:
            return True
        rgb_pct_match = re.match(r'rgb\s*\(\s*100%\s*,\s*100%\s*,\s*100%\s*\)', color)
        if rgb_pct_match:
            return True
        rgba_match = re.match(r'rgba\s*\(\s*255\s*,\s*255\s*,\s*255\s*,\s*1(\.0*)?\s*\)', color)
        if rgba_match:
            return True
        rgba_pct_match = re.match(r'rgba\s*\(\s*100%\s*,\s*100%\s*,\s*100%\s*,\s*1(\.0*)?\s*\)', color)
        if rgba_pct_match:
            return True
        return False

    def is_visible(tag):
        style = tag.get('style', '')
        if 'display:none' in style or 'visibility:hidden' in style or 'opacity:0' in style:
            return False
        if tag.get('display') == 'none' or tag.get('visibility') == 'hidden' or tag.get('opacity') == '0':
            return False
        return True

    def normalize_color(color):
        color = color.strip().lower()
        if is_white(color):
            return 'white'
        # Hex color
        if color.startswith('#'):
            if len(color) == 4:
                # e.g. #abc -> #aabbcc
                color = '#' + ''.join([c*2 for c in color[1:]])
            return color.upper()
        # rgb/rgba
        rgb_match = re.match(r'rgb\s*\(([^)]+)\)', color)
        if rgb_match:
            parts = rgb_match.group(1).split(',')
            if '%' in parts[0]:
                # rgb(100%,100%,100%)
                vals = [int(float(p.strip().replace('%','')) * 2.55) for p in parts[:3]]
            else:
                vals = [int(float(p.strip())) for p in parts[:3]]
            return '#{:02X}{:02X}{:02X}'.format(*vals)
        # named color
        return color

    with open(file_path, 'r', encoding='utf-8') as file:
        soup = BeautifulSoup(file.read(), 'xml')
    colors = set()
    # 1. Extract visible fill/stroke colors
    for tag in soup.find_all(True):
        if not is_visible(tag):
            continue
        for attr in ['fill', 'stroke']:
            val = tag.get(attr)
            if val and val.strip().lower() not in ['none', 'transparent'] and not val.startswith('url('):
                colors.add(normalize_color(val))
        style = tag.get('style')
        if style:
            for part in style.split(';'):
                if ':' in part:
                    prop, color_val = part.split(':', 1)
                    prop = prop.strip().lower()
                    color_val = color_val.strip()
                    if prop not in ['fill', 'stroke']:
                        continue
                    if color_val.lower() in ['none', 'transparent'] or color_val.startswith('url('):
                        continue
                    colors.add(normalize_color(color_val))
    # 2. Extract gradient stop colors
    for grad in soup.find_all(['linearGradient', 'radialGradient']):
        for stop in grad.find_all('stop'):
            stop_color = stop.get('stop-color')
            if stop_color:
                colors.add(normalize_color(stop_color))
            stop_style = stop.get('style')
            if stop_style:
                # Only add stop-color, ignore stop-opacity, offset, etc.
                for part in stop_style.split(';'):
                    if part.strip().startswith('stop-color:'):
                        color_val = part.split(':',1)[1].strip()
                        colors.add(normalize_color(color_val))
    return len(colors), colors

def detect_colors(file_path):
    ext = os.path.splitext(file_path)[1].lower()
    if ext == '.png':
        return count_png_colors(file_path)
    elif ext == '.svg':
        return extract_svg_colors(file_path)
    else:
        return 0, set()

if __name__ == "__main__":
    file_path = input("Enter path to image file (.png or .svg): ").strip()
    if not os.path.isfile(file_path):
        print("File not found. Please check the path.")
    else:
        count, colors = detect_colors(file_path)
        print(f"\n✅ Total Colors Detected: {count}")
        print("🎨 Unique Colors List:")
        for color in colors:
            print(color)