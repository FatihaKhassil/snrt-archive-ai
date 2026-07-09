from datetime import datetime
from typing import Dict, Any
from app.core.constants import DocumentStatus
from pydantic import BaseModel, Field


class ProcessingSchema(BaseModel):

    transcription: bool = False

    summary: bool = False

    embedding: bool = False

    indexation: bool = False

    fingerprint: bool = False


class DocumentSchema(BaseModel):

    title: str

    original_filename: str

    stored_filename: str

    storage_path: str

    file_type: str

    mime_type: str

    file_size: int

    sha256: str

    status: str = DocumentStatus.UPLOADED

    ai_metadata: Dict[str, Any] = Field(default_factory=dict)

    processing: ProcessingSchema = Field(default_factory=ProcessingSchema)

    created_at: datetime = Field(default_factory=datetime.utcnow)

    updated_at: datetime = Field(default_factory=datetime.utcnow)