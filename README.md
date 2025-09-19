# Mini Tech Challenge – Customer Call Analyzer

## Overview
This is a **Python Flask app** that analyzes customer call transcripts.  
The app can:
- Summarize a customer call in 2–3 sentences using the Groq API.
- Detect the sentiment of the customer (Positive / Neutral / Negative).
- Save the transcript, summary, and sentiment into a CSV file (`call_analysis.csv`) for record-keeping.

---

## Features
- Simple web interface built with **Flask** and **Bootstrap**.
- Input a transcript in a text area and click **Analyze**.
- Displays results in a clean web UI (Bootstrap + colored badges)
- Displays the latest analysis and keeps a history of the last 5 transcripts.
- Automatically appends results to a CSV file for later reference.

---

## Demo
1. Run the server:
```bash
python app.py
```
2. Open your browser at: `http://127.0.0.1:5000/`
3. Paste a sample transcript, e.g.:  
   ```
   Hi, I tried booking a slot yesterday but the payment failed.
   ```
4. Click **Analyze**.  
5. View the summary, sentiment, and check `call_analysis.csv` for saved results.

---

## Installation
1. Clone the repository:
```bash
git clone https://github.com/Kavyasree856/mini-tech-call-analyzer.git
```
2. Navigate to the project folder:
```bash
cd mini-tech-call-analyzer
```
3. Install required packages:
```bash
pip install flask pandas groq
```
4. Set your Groq API key as an environment variable:
```bash
# Windows
set GROQ_API_KEY=your_api_key_here

# Mac/Linux
export GROQ_API_KEY=your_api_key_here
```

---

## Usage
- Start the Flask server:
```bash
python app.py
```
- Open your browser and go to `http://127.0.0.1:5000/`.
- Paste a transcript, click **Analyze**, and view results.

---

## Notes
- Do **not** commit your `.env` or `call_analysis.csv` with sensitive information.  
- The app uses the Groq API, so make sure your API key is valid.

---

## Author
**P. Kavya Sree**  
B.Tech CSE (Data Science), KL University
