from flask import Flask, request, render_template, redirect, url_for, send_file, flash
import pandas as pd
import io, os, json
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = "excel_extractor_secret"

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        uploaded = request.files.get("file")
        if not uploaded or uploaded.filename == "":
            flash("Please upload a valid Excel file.")
            return redirect(url_for("index"))

        filename = secure_filename(uploaded.filename)
        try:
            df = pd.read_excel(uploaded, engine="openpyxl")
        except Exception as e:
            flash(f"Error reading Excel file: {e}")
            return redirect(url_for("index"))

        temp_id = os.urandom(8).hex()
        temp_path = f"/tmp/{temp_id}.pkl"
        df.to_pickle(temp_path)

        # Extract column names and up to 100 unique values
        column_values = {}
        for col in df.columns:
            try:
                unique_vals = df[col].dropna().astype(str).unique().tolist()[:100]
                column_values[col] = unique_vals
            except Exception:
                column_values[col] = []

        return render_template("index.html", uploaded=True, temp_id=temp_id, column_values=column_values)
    return render_template("index.html", uploaded=False)

@app.route("/extract", methods=["POST"])
def extract():
    temp_id = request.form.get("temp_id")
    temp_path = f"/tmp/{temp_id}.pkl"
    if not os.path.exists(temp_path):
        flash("Session expired or file missing.")
        return redirect(url_for("index"))

    df = pd.read_pickle(temp_path)
    os.remove(temp_path)

    selected_columns = request.form.getlist("columns")
    filters_json = request.form.get("filters")
    filters = json.loads(filters_json) if filters_json else {}

    # Apply filtering
    for col, vals in filters.items():
        if vals:
            df = df[df[col].astype(str).isin(vals)]

    # Apply column selection
    if selected_columns:
        df = df[selected_columns]

    out = io.BytesIO()
    with pd.ExcelWriter(out, engine="openpyxl") as writer:
        df.to_excel(writer, index=False, sheet_name="Filtered Data")
    out.seek(0)

    return send_file(out, as_attachment=True, download_name="filtered_data.xlsx")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
