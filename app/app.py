from flask import Flask, request, render_template, jsonify
import segno
import os

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/uploads/'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit_form():
    # Get form data
    data = request.form.to_dict()
    print(data)  # Print the received data in the console

    qr_image_paths = []
    for index, text in enumerate(data.get('textInput[]', [])):
        if text:  # Check if the text is not empty
            # Create a QR code using Segno
            qr = segno.make(text)

            # Save the image
            image_path = os.path.join(app.config['UPLOAD_FOLDER'], f'qr_code_{index}.png')
            qr.save(image_path)

            qr_image_paths.append(image_path)

    # Return the generated QR code image paths as JSON response
    return jsonify({'qr_codes': qr_image_paths})
    # Process the data (for example, print it or return as JSON)
    return jsonify(data)  # Return the data as a JSON response

if __name__ == '__main__':
    if not os.path.exists(app.config['UPLOAD_FOLDER']):
        os.makedirs(app.config['UPLOAD_FOLDER'])
    app.run(debug=True)
