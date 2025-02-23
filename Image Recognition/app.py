import os
import logging
from flask import Flask, render_template, request, jsonify
from werkzeug.utils import secure_filename
from image_processor import ImageProcessor

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET")

# Configure upload settings
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max-limit

try:
    logger.info("Initializing ImageProcessor...")
    image_processor = ImageProcessor()
    logger.info("ImageProcessor initialized successfully")
except Exception as e:
    logger.error(f"Failed to initialize ImageProcessor: {str(e)}")
    image_processor = None

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/detect', methods=['POST'])
def detect_objects():
    if image_processor is None:
        return jsonify({'error': 'Image processing service is not available'}), 503

    if 'image' not in request.files:
        return jsonify({'error': 'No image provided'}), 400

    file = request.files['image']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    if not allowed_file(file.filename):
        return jsonify({'error': 'Invalid file type'}), 400

    try:
        logger.info(f"Processing image: {secure_filename(file.filename)}")
        predictions = image_processor.process_image(file)
        logger.info("Image processed successfully")
        return jsonify({'predictions': predictions})
    except Exception as e:
        logger.error(f"Error processing image: {str(e)}")
        return jsonify({'error': 'Error processing image: ' + str(e)}), 500

@app.route('/api/docs')
def api_docs():
    return render_template('api_docs.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)