# Excel Column & Value Extractor (No render.yaml)

This Flask app lets users upload an Excel file, pick columns and specific values to include, and download a filtered Excel file.

## Deploy to Render (manual, no render.yaml required)
1. Push this folder to GitHub.
2. On Render, create a **New -> Web Service** and connect the repo.
3. Use build command: `pip install -r requirements.txt`
4. Start command: `gunicorn app:app --bind 0.0.0.0:$PORT`
5. Choose Free plan and deploy.

## Local run
```
pip install -r requirements.txt
python app.py
# open http://localhost:5000
```
