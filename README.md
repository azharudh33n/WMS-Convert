# Magento to RSA Global WMS Converter

A web application for converting Magento CSV export data to RSA Global Warehouse Management System (WMS) format.

## Features

- Convert Magento CSV exports to RSA Global WMS format
- Customizable settings for data conversion
- Automatic handling of additional attributes
- Flexible field mapping with fallback to default values
- Support for bundle products
- Automatic category extraction
- Additional attributes parsing

## Installation

1. Clone this repository:
```bash
git clone https://github.com/azharudh33n/WMS-Convert.git
cd WMS-Convert
```

2. Create a virtual environment and activate it:
```bash
python -m venv venv
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

1. Start the Flask application:
```bash
python app.py
```

2. Open your web browser and navigate to:
```
http://127.0.0.1:5000
```

3. Configure your default settings in the web interface:
   - Unit Price Currency (default: USD)
   - Tax Calculation Type (default: STANDARD)
   - Threshold for Notification (default: 5)
   - Threshold Quantity (default: 10)
   - Component Quantity (default: 1)
   - Expirable (default: No)

4. Upload your Magento CSV export file
5. Download the converted RSA Global WMS format file

## Settings

The application allows you to set default values for various fields. These values can be overridden by data in the CSV file if available:

- Unit Price Currency (default: USD)
- Tax Calculation Type (default: STANDARD)
- Threshold for Notification (default: 5)
- Threshold Quantity (default: 10)
- Component Quantity (default: 1)
- Expirable (default: No)

## Project Structure

```
WMS-Convert/
├── static/
│   ├── css/
│   │   └── style.css
│   └── js/
│       └── main.js
├── templates/
│   └── index.html
├── app.py
├── requirements.txt
└── README.md
```

## License

MIT License 