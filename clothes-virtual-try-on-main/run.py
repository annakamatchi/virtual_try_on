import os
from PIL import Image
from flask import Flask, render_template, request
import base64

# --- Config ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
UPLOAD_CLOTH = os.path.join(BASE_DIR, 'assets', 'cloth')
UPLOAD_MODEL = os.path.join(BASE_DIR, 'assets', 'image')
TEST_PAIRS_PATH = os.path.join(BASE_DIR, 'inputs', 'test_pairs.txt')
OUTPUT_IMAGE_PATH = os.path.join(BASE_DIR, 'output', 'tryon.jpg')  # Simulated output image

# Create necessary directories
os.makedirs(UPLOAD_CLOTH, exist_ok=True)
os.makedirs(UPLOAD_MODEL, exist_ok=True)
os.makedirs(os.path.dirname(TEST_PAIRS_PATH), exist_ok=True)
os.makedirs(os.path.dirname(OUTPUT_IMAGE_PATH), exist_ok=True)

# --- Helper: Resize to standard dimensions (768x1024) ---
def resize_img(path):
    with Image.open(path) as im:
        im = im.resize((768, 1024))
        im.save(path)

# --- Flask App ---
app = Flask(__name__, template_folder='templates', static_folder='static')

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():
    cloth_file = request.files.get('cloth')
    model_file = request.files.get('model')

    if not cloth_file or not model_file:
        return "Both cloth and model images must be uploaded.", 400

    cloth_path = os.path.join(UPLOAD_CLOTH, cloth_file.filename)
    model_path = os.path.join(UPLOAD_MODEL, model_file.filename)

    cloth_file.save(cloth_path)
    model_file.save(model_path)

    resize_img(cloth_path)
    resize_img(model_path)

    # --- Save test pair ---
    with open(TEST_PAIRS_PATH, 'w') as f:
        f.write(f"{model_file.filename} {cloth_file.filename}\n")

    # --- Simulated: Call your virtual try-on model pipeline here ---
    # os.system("python test.py ...") or subprocess equivalent
    # For this example, we simulate the output

    # Simulate output (copy model image as dummy try-on result)
    from shutil import copyfile
    copyfile(model_path, OUTPUT_IMAGE_PATH)

    # --- Convert output to base64 ---
    with open(OUTPUT_IMAGE_PATH, "rb") as image_file:
        encoded_result = base64.b64encode(image_file.read()).decode('utf-8')

    return render_template('index.html', op=encoded_result)

if __name__ == '__main__':
    app.run(debug=True)
    
