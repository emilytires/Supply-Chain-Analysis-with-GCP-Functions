# Google Cloud Storage Data Processing with Cloud Functions

This project demonstrates an automated data processing pipeline using Google Cloud Storage and Cloud Functions. When a CSV file is uploaded to a designated Google Cloud Storage bucket, a Google Cloud Function is triggered, which processes the data, generates multiple Plotly charts, combines them into a single PDF, and optionally uploads the result back to the storage bucket.

## Prerequisites

- Google Cloud account
- Cloud Functions enabled
- Python 3.9 or above

## Setup Instructions

### 1. Clone the repository
   ```bash
   git clone https://github.com/yourusername/your-repo-name.git
   cd your-repo-name
   ```

### 2. Set up your Google Cloud credentials

	•	Create a service account in the Google Cloud Console with the necessary permissions and download the JSON key file.
	•	Place the JSON key file in your project directory.
	•	Copy config_example.py to config.py
	•	In config.py, specify the path to your JSON key file by replacing "your-credentials-file.json" with the name of your downloaded JSON file.

```bash
cp config_example.py config.py
```

### 3. Install required packages
```bash
pip install -r requirements.txt
```

### 4. Deploy the Cloud Function (if using Google Cloud)
	•	Zip main.py and requirements.txt
	•	Go to the Google Cloud Console and navigate to Cloud Functions.
	•	Create a new function:
	•	Set the Trigger type to Cloud Storage and choose the event type as Finalize/Create.
	•	Specify your Cloud Storage bucket.
	•	Upload the function_code.zip file as the source code.
	•	Set Entry Point to main.
```bash
zip function_code.zip main.py requirements.txt
```


Usage

Once the Cloud Function is deployed, upload a CSV file to the specified Cloud Storage bucket. The function will be triggered automatically, process the file, generate plots, and save the results as a PDF file back to the storage bucket.

Important Notes

	•	Billing: Be cautious of potential billing charges when running this on Google Cloud.
	•	Security: The config.py file is included in .gitignore to prevent accidental exposure of sensitive credentials.