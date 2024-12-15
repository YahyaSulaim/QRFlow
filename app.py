from flask import Flask, request, render_template, send_file
import segno
import os
from PIL import Image, ImageFont, ImageDraw
import zipfile

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = '/tmp/uploads/' 

A4_WIDTH, A4_HEIGHT = (2480, 3508)  # A4 dimensions at 300 DPI
MARGIN = 50  # Margin around each QR code
GRID_COLUMNS = 3  # Number of QR codes per row

def clear_upload_folder():
    """Delete all files in the upload folder."""
    upload_folder = app.config['UPLOAD_FOLDER']
    # Create the upload folder if it does not exist
    if not os.path.exists(upload_folder):
        os.makedirs(upload_folder)

    for filename in os.listdir(upload_folder):
        file_path = os.path.join(upload_folder, filename)
        try:
            if os.path.isfile(file_path):
                os.remove(file_path)
        except Exception as e:
            print(f"Error deleting file {file_path}: {e}")


@app.route('/')
def index():
    clear_upload_folder()
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit_form():
    texts = request.form.getlist('textInput[]')
    numbers = request.form.getlist('numberInput[]')
    
    qr_image_paths = []
    qr_data = []

    for index, (text, number) in enumerate(zip(texts, numbers)):
        if text.strip() and number.strip():
            count = int(number)
            qr = segno.make(text, error='h')
            image_path = os.path.join(app.config['UPLOAD_FOLDER'], f'qr_code_{index}.png')
            qr.save(image_path, kind='png', scale=10, border=2)
            
            qr_image_paths.append(image_path)
            qr_data.append((image_path, count))

    # Create a list to hold the paths of generated A4 sheets
    a4_sheet_paths = create_a4_qr_sheets(qr_data)

    # Check the number of A4 sheets created
    if len(a4_sheet_paths) > 1:
        # Create a zip file if there are multiple sheets
        zip_file_path = os.path.join(app.config['UPLOAD_FOLDER'], 'qr_sheets.zip')
        with zipfile.ZipFile(zip_file_path, 'w') as zip_file:
            for sheet_path in a4_sheet_paths:
                zip_file.write(sheet_path, arcname=os.path.basename(sheet_path))
        return send_file(zip_file_path, as_attachment=True)
    else:
        # Send the single A4 sheet if only one was created
        return send_file(a4_sheet_paths[0], as_attachment=True)

def create_a4_qr_sheets(qr_data):
    cell_width = (A4_WIDTH - (GRID_COLUMNS + 1) * MARGIN) // GRID_COLUMNS
    cell_height = cell_width

    current_index = 0
    total_qrs = sum(count for _, count in qr_data)
    a4_sheet_paths = []

    while current_index < total_qrs:
        a4_canvas = Image.new('RGB', (A4_WIDTH, A4_HEIGHT), 'white')
        x_pos, y_pos = MARGIN, MARGIN
        current_column = 0
        font = ImageFont.load_default()

        for qr_path, count in qr_data:
            for i in range(count):
                if current_index >= total_qrs:
                    break

                qr_image = Image.open(qr_path).convert('RGB')
                qr_image = qr_image.resize((cell_width, cell_height), Image.LANCZOS)
                a4_canvas.paste(qr_image, (x_pos, y_pos))

                label_text = f"{os.path.basename(qr_path)}"
                draw = ImageDraw.Draw(a4_canvas)
                text_bbox = draw.textbbox((x_pos, y_pos + cell_height + 5), label_text, font=font)
                text_width = text_bbox[2] - text_bbox[0]
                text_height = text_bbox[3] - text_bbox[1]

                text_x = x_pos + (cell_width - text_width) // 2
                text_y = y_pos + cell_height + 5

                draw.text((text_x, text_y), label_text, fill="black", font=font)

                current_index += 1
                current_column += 1

                if current_column < GRID_COLUMNS:
                    x_pos += cell_width + MARGIN
                else:
                    x_pos = MARGIN
                    y_pos += cell_height + text_height + MARGIN
                    current_column = 0

                if y_pos + cell_height + text_height > A4_HEIGHT - MARGIN:
                    break

        # Save the A4 sheet to a temporary path
        sheet_filename = f'qr_sheet_{len(a4_sheet_paths) + 1}.png'
        sheet_path = os.path.join(app.config['UPLOAD_FOLDER'], sheet_filename)
        a4_canvas.save(sheet_path, 'PNG')
        a4_sheet_paths.append(sheet_path)

    return a4_sheet_paths

if __name__ == '__main__':

    if not os.path.exists(app.config['UPLOAD_FOLDER']):
        os.makedirs(app.config['UPLOAD_FOLDER'])
    app.run(debug=True)
