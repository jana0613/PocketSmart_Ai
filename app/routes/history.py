import json
from fastapi import APIRouter, Depends, HTTPException
from ..dependencies import get_current_user
from ..db import get_history, get_recommendation

router = APIRouter(prefix="/api", tags=["History"])

@router.get("/history")
def history(user=Depends(get_current_user)):
    rows = get_history(int(user["sub"]))
    return [{"id": r["id"], "planner": r["planner"], "created_at": r["created_at"], "input": json.loads(r["input_json"]), "result": json.loads(r["result_json"])} for r in rows]

@router.get("/recommendations/{rec_id}")
def recommendation(rec_id: int, user=Depends(get_current_user)):
    row = get_recommendation(int(user["sub"]), rec_id)
    if not row:
        raise HTTPException(status_code=404, detail="Recommendation not found")
    return {"id": row["id"], "planner": row["planner"], "created_at": row["created_at"], "input": json.loads(row["input_json"]), "result": json.loads(row["result_json"])}
