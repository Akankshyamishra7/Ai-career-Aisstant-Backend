from typing import List, Dict, Any
from fastapi import APIRouter, HTTPException
from app.db import db_manager

router = APIRouter(prefix="/api/history", tags=["Analysis History"])

@router.get("", response_model=List[Dict[str, Any]])
async def get_all_analyses():
    """
    Returns list of all saved resume analyses from MongoDB (or persistent storage).
    """
    return db_manager.get_all_analyses()

@router.get("/status")
async def get_database_status():
    """
    Returns active database status (MongoDB vs persistent local storage).
    """
    return db_manager.get_status()

@router.get("/{analysis_id}")
async def get_analysis_by_id(analysis_id: str):
    """
    Returns a specific resume analysis by ID.
    """
    analysis = db_manager.get_analysis_by_id(analysis_id)
    if not analysis:
        raise HTTPException(status_code=404, detail="Analysis record not found.")
    return analysis

@router.delete("/{analysis_id}")
async def delete_analysis_by_id(analysis_id: str):
    """
    Deletes a specific resume analysis by ID.
    """
    success = db_manager.delete_analysis(analysis_id)
    if not success:
        raise HTTPException(status_code=404, detail="Analysis record not found or could not be deleted.")
    return {"message": "Record successfully deleted.", "id": analysis_id}
