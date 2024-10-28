# app.py
from flask import Flask, request, render_template, send_file
from werkzeug.utils import secure_filename
from datetime import datetime, time
import csv
import os
from collections import defaultdict
import openpyxl
from io import BytesIO

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Define functions for processing CSV data
def parse_datetime(datetime_str):
    return datetime.strptime(datetime_str, "%B %d %I:%M%p")

def calculate_delay(clock_in_time, branch_opening_time):
    if clock_in_time < branch_opening_time:
        return 0
    delay = (clock_in_time - branch_opening_time).total_seconds() / 60
    return delay

def process_shifts(file):
    nafl_data = {}
    aqiq_data = {}
    user_delays = defaultdict(lambda: defaultdict(int))
    branch_opening_times = {
        "N1": time(6, 0),  # 6:00 AM
        "Q1": time(7, 0)   # 7:00 AM
    }
    cutoff_time = time(9, 0)  # 9:00 AM cutoff

    file.seek(0)  # Reset file pointer
    reader = csv.DictReader(file)
    required_columns = ['Branch Reference', 'Clocked In At']
    user_column = next((col for col in reader.fieldnames if col.lower() == 'user'), None)

    for row in reader:
        # Processing logic here
        pass  # Include actual processing logic from the original code here

    # Create an Excel workbook for output
    output = BytesIO()
    workbook = openpyxl.Workbook()
    sheet = workbook.active
    sheet.title = "Processed Data"
    # Save workbook to BytesIO stream
    workbook.save(output)
    output.seek(0)
    return output

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return "No file part", 400
    file = request.files['file']
    if file.filename == '':
        return "No selected file", 400
    if file:
        output = process_shifts(file)
        return send_file(output, as_attachment=True, download_name="processed_data.xlsx", mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')

if __name__ == '__main__':
    app.run(debug=True)
