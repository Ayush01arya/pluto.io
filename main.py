from flask import Flask, request, jsonify, send_file
from rembg import remove
from PIL import Image
import io
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
# Endpoint for removing background from an image
@app.route('/remove-bg', methods=['POST'])
def remove_background():
    if 'image' not in request.files:
        return jsonify({'error': 'No image provided'}), 400

    # Get the image from the request
    image_file = request.files['image']

    try:
        # Open the image using PIL
        img = Image.open(image_file)

        # Remove the background using rembg
        img_without_bg = remove(img)

        # Convert the image to bytes to send back as a response
        img_byte_arr = io.BytesIO()
        img_without_bg.save(img_byte_arr, format='PNG')
        img_byte_arr.seek(0)

        return send_file(img_byte_arr, mimetype='image/png')

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
