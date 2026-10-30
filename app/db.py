import json
import uuid
from datetime import datetime
from typing import List, Optional, Dict, Any
from pathlib import Path
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure, ServerSelectionTimeoutError
from app.config import settings

FALLBACK_FILE = settings.DATA_DIR / "analyses.json"

class DatabaseManager:
    def __init__(self):
        self.use_mongo = False
        self.client = None
        self.db = None
        self.collection = None
        self._init_connection()

    def _init_connection(self):
        try:
            self.client = MongoClient(settings.MONGODB_URI, serverSelectionTimeoutMS=2000)
            # Test connection
            self.client.admin.command('ping')
            self.db = self.client[settings.DB_NAME]
            self.collection = self.db["resume_analyses"]
            self.use_mongo = True
            print("[Database] Successfully connected to MongoDB.")
        except (ConnectionFailure, ServerSelectionTimeoutError, Exception) as e:
            self.use_mongo = False
            print(f"[Database] MongoDB not reachable ({e}). Using persistent JSON local storage at {FALLBACK_FILE}")
            if not FALLBACK_FILE.exists():
                with open(FALLBACK_FILE, "w", encoding="utf-8") as f:
                    json.dump([], f)

    def _read_local(self) -> List[Dict[str, Any]]:
        if not FALLBACK_FILE.exists():
            return []
        try:
            with open(FALLBACK_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return []

    def _write_local(self, data: List[Dict[str, Any]]):
        with open(FALLBACK_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

    def save_analysis(self, record: Dict[str, Any]) -> Dict[str, Any]:
        if "id" not in record or not record["id"]:
            record["id"] = str(uuid.uuid4())
        if "created_at" not in record or not record["created_at"]:
            record["created_at"] = datetime.utcnow().isoformat()

        if self.use_mongo and self.collection is not None:
            try:
                # Mongo requires _id or uses record id
                mongo_doc = {**record, "_id": record["id"]}
                self.collection.replace_one({"_id": record["id"]}, mongo_doc, upsert=True)
                return record
            except Exception as e:
                print(f"[Database] MongoDB write failed ({e}), falling back to local file.")

        # Local fallback
        records = self._read_local()
        # Update or append
        existing_idx = next((i for i, r in enumerate(records) if r.get("id") == record["id"]), None)
        if existing_idx is not None:
            records[existing_idx] = record
        else:
            records.insert(0, record)
        self._write_local(records)
        return record

    def get_all_analyses(self) -> List[Dict[str, Any]]:
        if self.use_mongo and self.collection is not None:
            try:
                docs = list(self.collection.find().sort("created_at", -1))
                for d in docs:
                    if "_id" in d:
                        del d["_id"]
                return docs
            except Exception as e:
                print(f"[Database] MongoDB read failed ({e}), using local file.")
        
        return self._read_local()

    def get_analysis_by_id(self, analysis_id: str) -> Optional[Dict[str, Any]]:
        if self.use_mongo and self.collection is not None:
            try:
                doc = self.collection.find_one({"_id": analysis_id})
                if doc:
                    if "_id" in doc:
                        del doc["_id"]
                    return doc
            except Exception:
                pass
        
        records = self._read_local()
        for r in records:
            if r.get("id") == analysis_id:
                return r
        return None

    def delete_analysis(self, analysis_id: str) -> bool:
        deleted = False
        if self.use_mongo and self.collection is not None:
            try:
                res = self.collection.delete_one({"_id": analysis_id})
                deleted = res.deleted_count > 0
            except Exception:
                pass

        records = self._read_local()
        initial_len = len(records)
        records = [r for r in records if r.get("id") != analysis_id]
        if len(records) < initial_len:
            self._write_local(records)
            deleted = True
        return deleted

    def get_status(self) -> Dict[str, Any]:
        return {
            "engine": "MongoDB" if self.use_mongo else "Local Persistent JSON (Fallback)",
            "connected": self.use_mongo,
            "database_name": settings.DB_NAME if self.use_mongo else "analyses.json"
        }

db_manager = DatabaseManager()
