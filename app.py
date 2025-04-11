import os
import csv
from flask import Flask, render_template, request, send_file
from datetime import datetime
import tempfile
from collections import defaultdict
import io
import json

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# Ensure upload folder exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

def parse_additional_attributes(attr_string):
    if not attr_string:
        return {}
    result = {}
    try:
        pairs = [item.split('=', 1) for item in attr_string.split(',') if '=' in item]
        return dict(pairs)
    except:
        return {}

def get_last_category(category_string):
    if not category_string:
        return ''
    # Split by comma and get the last category path
    categories = category_string.split(',')
    last_category = categories[-1].strip()
    # Split by slash and get the last part
    parts = last_category.split('/')
    return parts[-1].strip()

def process_magento_data(csv_file, settings):
    # Read CSV data
    # Convert the file to text mode
    text_stream = io.StringIO(csv_file.read().decode('utf-8'))
    reader = csv.DictReader(text_stream)
    rows = list(reader)
    
    # Process rows
    fulfillment_rows = []
    
    for row in rows:
        # Skip empty rows
        if not any(row.values()):
            continue
            
        # Skip rows with missing SKUs
        if not row.get('sku'):
            continue
            
        # Parse additional attributes
        additional_attrs = parse_additional_attributes(row.get('additional_attributes', ''))
        
        # Get values from CSV or use settings
        unit_price_currency = row.get('unit_price_currency') or settings.get('unitPriceCurrency', 'USD')
        tax_calculation_type = row.get('tax_calculation_type') or settings.get('taxCalculationType', 'STANDARD')
        threshold_notification = row.get('threshold_for_notification') or settings.get('thresholdNotification', '5')
        threshold_quantity = row.get('threshold_quantity') or settings.get('thresholdQuantity', '10')
        component_quantity = row.get('component_quantity') or settings.get('componentQuantity', '1')
        expirable = row.get('expirable') or settings.get('expirable', 'No')
        
        # Create fulfillment row with exact column order
        fulfillment_row = {
            'CATEGORY_CODE': get_last_category(row.get('categories', '')),
            'PRODUCT_CODE': row.get('sku', ''),
            'NAME': row.get('name', ''),
            'DESCRIPTION': row.get('description', ''),
            'LENGTH': additional_attrs.get('length', ''),
            'WIDTH': additional_attrs.get('width', ''),
            'HEIGHT': additional_attrs.get('height', ''),
            'WEIGHT': row.get('weight', ''),
            'HS_CODE': additional_attrs.get('hs_code', ''),
            'UNIT_PRICE': additional_attrs.get('membership_price', row.get('price', '')),
            'UNIT_PRICE_CURRENCY': unit_price_currency,
            'BUNDLE_SKU': row.get('associated_skus', '') if row.get('product_type') == 'bundle' else '',
            'TAX_CALCULATION_TYPE': tax_calculation_type,
            'ACTIVE': 'Yes' if row.get('product_online') == '1' else 'No',
            'IMAGE_URL': row.get('base_image', ''),
            'THRESHOLD_FOR_NOTIFICATION': threshold_notification,
            'THRESHOLD_QUANTITY': threshold_quantity,
            'EAN': additional_attrs.get('ean', ''),
            'UPC': additional_attrs.get('upc', ''),
            'ISBN': additional_attrs.get('isbn', ''),
            'COLOR': additional_attrs.get('color', ''),
            'BRAND': additional_attrs.get('brand', ''),
            'SIZE': additional_attrs.get('size', ''),
            'COMPONENT_PRODUCT_CODE': row.get('associated_skus', '') if row.get('product_type') == 'bundle' else '',
            'COMPONENT_QUANTITY': component_quantity,
            'COMPONENT_PRICE': additional_attrs.get('membership_price', row.get('price', '')),
            'EXPIRABLE': expirable,
            'SHELF_LIFE': ''
        }
            
        fulfillment_rows.append(fulfillment_row)
    
    return fulfillment_rows

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return 'No file uploaded', 400
    
    file = request.files['file']
    if file.filename == '':
        return 'No file selected', 400
    
    if not file.filename.endswith('.csv'):
        return 'Please upload a CSV file', 400
    
    try:
        # Get settings from form data
        settings = {}
        if 'settings' in request.form:
            settings = json.loads(request.form['settings'])
        
        # Process the data
        processed_rows = process_magento_data(file, settings)
        
        # Create output file
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        output_filename = f'converted_skus_{timestamp}.csv'
        output_path = os.path.join(app.config['UPLOAD_FOLDER'], output_filename)
        
        # Define the exact column order
        fieldnames = [
            'CATEGORY_CODE', 'PRODUCT_CODE', 'NAME', 'DESCRIPTION', 'LENGTH', 'WIDTH', 'HEIGHT',
            'WEIGHT', 'HS_CODE', 'UNIT_PRICE', 'UNIT_PRICE_CURRENCY', 'BUNDLE_SKU',
            'TAX_CALCULATION_TYPE', 'ACTIVE', 'IMAGE_URL', 'THRESHOLD_FOR_NOTIFICATION',
            'THRESHOLD_QUANTITY', 'EAN', 'UPC', 'ISBN', 'COLOR', 'BRAND', 'SIZE',
            'COMPONENT_PRODUCT_CODE', 'COMPONENT_QUANTITY', 'COMPONENT_PRICE',
            'EXPIRABLE', 'SHELF_LIFE'
        ]
        
        # Write to CSV with exact column order
        if processed_rows:
            with open(output_path, 'w', newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(f, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(processed_rows)
        
        return send_file(
            output_path,
            as_attachment=True,
            download_name=output_filename,
            mimetype='text/csv'
        )
    
    except Exception as e:
        return f'Error processing file: {str(e)}', 500

if __name__ == '__main__':
    app.run(debug=True) 