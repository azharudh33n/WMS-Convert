# WMS Convert

A web application for converting Magento CSV data to fulfillment system format.

## Features

- Upload and process Magento CSV files
- Customizable settings for data conversion
- Automatic handling of additional attributes
- Flexible field mapping with fallback to default values

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/wms-convert.git
cd wms-convert
```

2. Create a virtual environment and activate it:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
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

3. Configure your default settings in the web interface
4. Upload your Magento CSV file
5. Download the converted file

## Settings

The application allows you to set default values for the following fields:
- Unit Price Currency (default: USD)
- Tax Calculation Type (default: STANDARD)
- Threshold for Notification (default: 5)
- Threshold Quantity (default: 10)
- Component Quantity (default: 1)
- Expirable (default: No)

These values can be overridden by data in the CSV file if available.

## License

MIT License 