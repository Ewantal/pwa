from flask import Flask, request, render_template, send_from_directory, jsonify, redirect, url_for
import os

app = Flask(__name__)

# Set up the directory where uploaded files will be saved
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Create the folder if it doesn’t exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# First page route
@app.route('/')
def first_page():
    return render_template('first_page.html')

# Second page route (current page with upload functionality)
@app.route('/second-page')
def second_page():
    return render_template('index.html')

# Endpoint to handle file uploads
@app.route('/upload', methods=['POST'])
def upload_file():
    # Check if the required files are in the request
    if 'image1' not in request.files or 'image2' not in request.files:
        return jsonify({"error": "Missing file(s)"}), 400

    # Access the files
    file1 = request.files['image1']
    file2 = request.files['image2']

    # Validate that files are not empty
    if file1.filename == '' or file2.filename == '':
        return jsonify({"error": "One or both files are empty"}), 400

    # Define new filenames
    front_filename = "front" + os.path.splitext(file1.filename)[1]  # Retain original file extension
    side_filename = "side" + os.path.splitext(file2.filename)[1]   # Retain original file extension

    # Save the files with new names
    filepath1 = os.path.join(app.config['UPLOAD_FOLDER'], front_filename)
    filepath2 = os.path.join(app.config['UPLOAD_FOLDER'], side_filename)
    file1.save(filepath1)
    file2.save(filepath2)

    # Provide a response with file paths or other data
    return jsonify({
        "success": True,
    }), 200

# New endpoint to handle model creation based on values
@app.route('/compute', methods=['POST'])
def compute_model():
    # Parse the incoming JSON data
    data = request.get_json()

    # Check if all required fields are present
    required_fields = ['shoulderDistance', 'armpitDistance', 'armpitHeight', 'chestHeight', 'neckHeight', 
                       'neckWidth', 'shoulderWidth', 'sleeveHeight', 'sleeveWidth', 'height', 'type']
    
    for field in required_fields:
        if field not in data or not data[field]:
            return jsonify({"error": f"Missing or invalid value for {field}"}), 400
    
    # Now you have all the form data and can process it as needed
    # For example, creating a model based on these values
    # Logic for model creation goes here
    
    print(f"Received data for model creation: {data}")  # Just logging for now

    # Respond with success
    return jsonify({"success": True}), 200

# Serve uploaded files for download
@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
