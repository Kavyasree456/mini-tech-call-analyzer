from flask import Flask, request, render_template_string
import pandas as pd
import os
from groq import Groq

# -------------------------------
# Initialize Groq client
# Make sure you set your GROQ_API_KEY in environment variables
# -------------------------------
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

app = Flask(__name__)

# -------------------------------
# Simple HTML template
# Using Bootstrap for quick styling
# -------------------------------
HTML_TEMPLATE = """
<!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <title>Customer Call Analyzer</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
  </head>
  <body class="bg-light">
    <div class="container py-5">
      <h2 class="mb-4 text-center">📞 Customer Call Analyzer</h2>

      <form method="post" class="mb-4">
        <div class="mb-3">
          <label class="form-label"><b>Enter Transcript</b></label>
          <textarea name="transcript" rows="5" class="form-control" placeholder="Paste customer call transcript here..."></textarea>
        </div>
        <button type="submit" class="btn btn-primary">Analyze</button>
      </form>

      {% if summary %}
      <div class="card mb-4 shadow-sm">
        <div class="card-body">
          <h5 class="card-title">✅ Latest Analysis</h5>
          <p><b>Transcript:</b> {{ transcript }}</p>
          <p><b>Summary:</b> {{ summary }}</p>
          <p><b>Sentiment:</b>
            {% if sentiment == "Positive" %}
              <span class="badge bg-success">{{ sentiment }}</span>
            {% elif sentiment == "Negative" %}
              <span class="badge bg-danger">{{ sentiment }}</span>
            {% else %}
              <span class="badge bg-secondary">{{ sentiment }}</span>
            {% endif %}
          </p>
        </div>
      </div>
      {% endif %}

      <h4>📊 Previous Analyses (Last 5)</h4>
      <table class="table table-striped table-bordered">
        <thead class="table-dark">
          <tr><th>Transcript</th><th>Summary</th><th>Sentiment</th></tr>
        </thead>
        <tbody>
        {% for row in history %}
          <tr>
            <td>{{ row[0] }}</td>
            <td>{{ row[1] }}</td>
            <td>
              {% if row[2] == "Positive" %}
                <span class="badge bg-success">{{ row[2] }}</span>
              {% elif row[2] == "Negative" %}
                <span class="badge bg-danger">{{ row[2] }}</span>
              {% else %}
                <span class="badge bg-secondary">{{ row[2] }}</span>
              {% endif %}
            </td>
          </tr>
        {% endfor %}
        </tbody>
      </table>
    </div>
  </body>
</html>
"""

# -------------------------------
# Function to get summary and sentiment
# -------------------------------
def analyze_transcript(text):
    # Generate a short summary (strictly about the transcript, no extra sentences)
    summary_prompt = f"Summarize this customer call in 2-3 sentences only about the transcript. Do NOT add extra information or polite follow-ups:\n{text}"
    summary = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{"role": "user", "content": summary_prompt}]
    ).choices[0].message.content.strip()

    # Detect sentiment
    sentiment_prompt = f"""
    Classify the overall sentiment of this transcript as one word only:
    Positive, Neutral, or Negative.
    Transcript: {text}
    """
    sentiment_resp = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{"role": "user", "content": sentiment_prompt}]
    ).choices[0].message.content.strip()

    # Keep only first word (in case model adds explanation)
    sentiment = sentiment_resp.split()[0]

    return summary, sentiment

# -------------------------------
# Flask routes
# -------------------------------
@app.route("/", methods=["GET", "POST"])
def home():
    transcript = ""
    summary = sentiment = None

    if request.method == "POST":
        transcript = request.form["transcript"]
        summary, sentiment = analyze_transcript(transcript)

        # Save to CSV
        df = pd.DataFrame([[transcript, summary, sentiment]],
                          columns=["Transcript", "Summary", "Sentiment"])
        df.to_csv("call_analysis.csv", mode="a", header=not os.path.exists("call_analysis.csv"), index=False)

    # Load last 5 analyses for display
    history = []
    if os.path.exists("call_analysis.csv"):
        df = pd.read_csv("call_analysis.csv").tail(5)
        df["Transcript"] = df["Transcript"].apply(lambda x: (x[:60] + "...") if len(x) > 60 else x)
        df["Summary"] = df["Summary"].apply(lambda x: (x[:80] + "...") if len(x) > 80 else x)
        history = df.values.tolist()

    return render_template_string(HTML_TEMPLATE, transcript=transcript, summary=summary, sentiment=sentiment, history=history)

# -------------------------------
# Run server
# -------------------------------
if __name__ == "__main__":
    app.run(debug=True)
