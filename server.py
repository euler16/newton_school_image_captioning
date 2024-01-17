from flask import Flask, request, jsonify, render_template
from transformers import pipeline
import base64
from PIL import Image
import io

app = Flask(__name__)

# Load the Hugging Face model for image captioning
caption_pipeline = pipeline("image-to-text", "Salesforce/blip-image-captioning-base")

def decode_image(image_b64):
    image_data = base64.b64decode(image_b64)
    image = Image.open(io.BytesIO(image_data))
    return image

@app.route('/')
def home():
    return render_template('index.html')

@app.route("/test", methods=['GET'])
def hello():
    return "HELLO HOW ARE YOU?"

@app.route('/caption', methods=['POST'])
def caption_image():
    # Extract base64 image from request
    data = request.json
    #print(data.keys())
    image_b64 = data['image']

    # Decode the base64 image
    image = decode_image(image_b64)

    # Generate caption
    try:
        caption = caption_pipeline(image)
        print(f"caption: {caption}")
        return jsonify({'caption': caption})
    except Exception as e:
        return jsonify({'error': str(e)})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8000)

