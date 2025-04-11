document.addEventListener('DOMContentLoaded', () => {
    const fileInput = document.getElementById('fileInput');
    const fileNameDisplay = document.querySelector('.file-name');
    const uploadForm = document.getElementById('uploadForm');
    const settingsForm = document.getElementById('settingsForm');
    const saveSettingsButton = document.getElementById('saveSettings');
    const statusMessage = document.getElementById('statusMessage');
    const progressBar = document.getElementById('progressBar');
    const progress = document.querySelector('.progress');

    // Load saved settings from localStorage
    function loadSettings() {
        const settings = JSON.parse(localStorage.getItem('converterSettings') || '{}');
        document.getElementById('unitPriceCurrency').value = settings.unitPriceCurrency || 'USD';
        document.getElementById('taxCalculationType').value = settings.taxCalculationType || 'STANDARD';
        document.getElementById('thresholdNotification').value = settings.thresholdNotification || '5';
        document.getElementById('thresholdQuantity').value = settings.thresholdQuantity || '10';
        document.getElementById('componentQuantity').value = settings.componentQuantity || '1';
        document.getElementById('expirable').value = settings.expirable || 'No';
    }

    // Save settings to localStorage
    function saveSettings() {
        const settings = {
            unitPriceCurrency: document.getElementById('unitPriceCurrency').value,
            taxCalculationType: document.getElementById('taxCalculationType').value,
            thresholdNotification: document.getElementById('thresholdNotification').value,
            thresholdQuantity: document.getElementById('thresholdQuantity').value,
            componentQuantity: document.getElementById('componentQuantity').value,
            expirable: document.getElementById('expirable').value
        };
        localStorage.setItem('converterSettings', JSON.stringify(settings));
        showStatus('Settings saved successfully!', 'success');
    }

    // Update file name display when a file is selected
    fileInput.addEventListener('change', (e) => {
        const file = e.target.files[0];
        if (file) {
            fileNameDisplay.textContent = file.name;
        } else {
            fileNameDisplay.textContent = 'No file chosen';
        }
    });

    // Handle settings save
    saveSettingsButton.addEventListener('click', saveSettings);

    // Load settings when page loads
    loadSettings();

    // Handle form submission
    uploadForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        
        const file = fileInput.files[0];
        if (!file) {
            showStatus('Please select a file', 'error');
            return;
        }

        if (!file.name.endsWith('.csv')) {
            showStatus('Please upload a CSV file', 'error');
            return;
        }

        const formData = new FormData();
        formData.append('file', file);
        
        // Add settings to form data
        const settings = JSON.parse(localStorage.getItem('converterSettings') || '{}');
        formData.append('settings', JSON.stringify(settings));

        try {
            showStatus('Processing file...', 'info');
            progressBar.style.display = 'block';
            progress.style.width = '50%';

            const response = await fetch('/upload', {
                method: 'POST',
                body: formData
            });

            if (!response.ok) {
                const error = await response.text();
                throw new Error(error);
            }

            // Get the filename from the Content-Disposition header
            const contentDisposition = response.headers.get('Content-Disposition');
            const filename = contentDisposition
                ? contentDisposition.split('filename=')[1].replace(/"/g, '')
                : 'converted_skus.csv';

            // Create a blob from the response
            const blob = await response.blob();
            
            // Create a download link
            const url = window.URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = filename;
            document.body.appendChild(a);
            a.click();
            window.URL.revokeObjectURL(url);
            document.body.removeChild(a);

            showStatus('File processed successfully!', 'success');
            progress.style.width = '100%';
            
            // Reset form
            setTimeout(() => {
                uploadForm.reset();
                fileNameDisplay.textContent = 'No file chosen';
                progressBar.style.display = 'none';
                progress.style.width = '0';
            }, 2000);

        } catch (error) {
            showStatus(error.message, 'error');
            progressBar.style.display = 'none';
            progress.style.width = '0';
        }
    });

    function showStatus(message, type = 'info') {
        statusMessage.textContent = message;
        statusMessage.className = 'status-message';
        if (type !== 'info') {
            statusMessage.classList.add(type);
        }
    }
}); 