from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional, List
from ..database.storage import Storage
from ..database.models import Result
from ..core.hash_utils import detect_algorithm

app = FastAPI(title="pyrehash API")
storage = Storage()

class CrackRequest(BaseModel):
    target: str
    mode: str
    algorithm: Optional[str] = None
    dictionary: Optional[str] = None
    length: Optional[int] = None
    charset: str = "lower"

class ResultResponse(BaseModel):
    hash_value: str
    password: str

@app.get("/results", response_model=List[ResultResponse])
def get_results():
    with storage.Session() as session:
        results = session.query(Result).all()
        return [{"hash_value": r.target.hash_value, "password": r.password} for r in results]

@app.get("/detect/{hash_str}")
def detect(hash_str: str):
    algo = detect_algorithm(hash_str)
    return {"hash": hash_str, "detected_algorithm": algo}

@app.post("/crack")
def start_crack(req: CrackRequest):
    # This would ideally start a background task
    return {"message": "Attack queued (not implemented in this demo POC)"}
