from fastapi import FastAPI
import pandas as pd
import subprocess

app = FastAPI(title="Redrob AI Ranking API")


@app.get("/")
def home():
    return {
        "status": "Running",
        "project": "Redrob AI Candidate Ranking"
    }


@app.post("/rank")
def run_ranking():

    subprocess.run(["python", "rank.py"])

    return {
        "message": "Ranking completed successfully."
    }


@app.get("/top100")
def top100():

    df = pd.read_csv("submission.csv")

    return df.to_dict(orient="records")


@app.get("/candidate/{candidate_id}")
def candidate(candidate_id: str):

    df = pd.read_csv("submission.csv")

    result = df[df["candidate_id"] == candidate_id]

    if result.empty:
        return {"error": "Candidate not found"}

    return result.to_dict(orient="records")[0]