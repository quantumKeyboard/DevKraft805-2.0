"""
api/routers/voice.py
GET /voice/{repo_id} — returns the audio file for the voice guide.
GET /voice/{repo_id}/script — returns the script sections as JSON.
"""

import os
from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse
from api.routers.analyze import REPO_STORE

router = APIRouter(prefix="/voice", tags=["voice"])


@router.get("/{repo_id}/script")
async def get_voice_script(repo_id: str):
    store = REPO_STORE.get(repo_id)
    if not store:
        raise HTTPException(status_code=404, detail="Repo ID not found.")
    if store.get("status") != "complete":
        raise HTTPException(status_code=202, detail="Analysis not yet complete.")

    return {
        "repo_id": repo_id,
        "sections": store.get("voice_script", []),
    }


@router.get("/{repo_id}")
async def get_voice_guide(repo_id: str):
    store = REPO_STORE.get(repo_id)
    if not store:
        raise HTTPException(status_code=404, detail="Repo ID not found.")
    if store.get("status") != "complete":
        raise HTTPException(status_code=202, detail="Analysis not yet complete.")

    voice_path = store.get("voice_guide_path", "")
    if not voice_path or not os.path.exists(voice_path):
        # Return the script as JSON if audio not available
        return {
            "repo_id": repo_id,
            "audio_available": False,
            "sections": store.get("voice_script", []),
            "message": "Audio file not available. TTS may not be installed.",
        }

    ext = os.path.splitext(voice_path)[1].lower()
    media_type = "audio/wav" if ext == ".wav" else "audio/mpeg"
    return FileResponse(path=voice_path, media_type=media_type, filename=f"{repo_id}_guide{ext}")
