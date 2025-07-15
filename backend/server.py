import os
import pandas as pd
from fastapi import FastAPI, UploadFile, HTTPException
from fastapi.responses import FileResponse
from classify import classify
import uuid

app = FastAPI()

@app.post("/classify/")
async def classify_logs(file: UploadFile):
    if not file.filename.endswith('.csv'):
        raise HTTPException(status_code=400, detail="File must be a CSV.")

    try:
        # Read uploaded CSV
        df = pd.read_csv(file.file)

        # Validate required columns
        if "source" not in df.columns or "log_message" not in df.columns:
            raise HTTPException(status_code=400, detail="CSV must contain 'source' and 'log_message' columns.")

        # Classify logs
        df["target_label"] = classify(list(zip(df["source"], df["log_message"])))

        # Save output to a unique temp file
        output_file = f"/tmp/output_{uuid.uuid4().hex}.csv"
        df.to_csv(output_file, index=False)

        return FileResponse(output_file, media_type='text/csv', filename="cascadelog_results.csv")
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
