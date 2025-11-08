# Excel Column & Value Extractor

Upload an Excel file, choose which columns and which values to extract, and download the filtered Excel.

## Deploy to Render (Free)
1. Push this folder to GitHub.
2. Go to [Render](https://render.com).
3. Create a new Web Service → Connect your repo.
4. Build: `pip install -r requirements.txt`
5. Start: `gunicorn app:app --bind 0.0.0.0:$PORT`
6. Get your URL like `https://excel-column-value-extractor.onrender.com`

## Local Run
```
pip install -r requirements.txt
python app.py
# open http://localhost:5000
```
