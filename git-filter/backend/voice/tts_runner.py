"""
voice/tts_runner.py
Converts the voice guide script to audio using TTS (Coqui TTS / TinyTTS).
Falls back to generating a plain text file if TTS is unavailable.
"""

import logging
import os
from pathlib import Path

from core.config import get_settings

logger = logging.getLogger(__name__)

_TTS_AVAILABLE = False
_tts_instance = None

try:
    from TTS.api import TTS as CoquiTTS
    _TTS_AVAILABLE = True
    logger.info("Coqui TTS available.")
except ImportError:
    logger.warning(
        "TTS (Coqui) not installed. Voice guide will generate a text script file instead. "
        "Install with: pip install TTS"
    )


def _get_tts():
    """Lazily initialize the TTS model (downloads on first use)."""
    global _tts_instance
    if _tts_instance is None and _TTS_AVAILABLE:
        try:
            _tts_instance = CoquiTTS(model_name="tts_models/en/ljspeech/tacotron2-DDC")
        except Exception as exc:
            logger.error(f"Failed to initialize TTS model: {exc}")
    return _tts_instance


def _save_text_fallback(
    script_sections: list[dict],
    output_path: Path,
) -> str:
    """Save the guide script as a plain .txt file when TTS is unavailable."""
    txt_path = output_path.with_suffix(".txt")
    with open(txt_path, "w", encoding="utf-8") as f:
        for section in script_sections:
            f.write(f"\n=== {section['section_title']} ===\n\n")
            f.write(section["script_text"])
            f.write("\n\n")
    return str(txt_path)


def generate_voice_guide(
    repo_id: str,
    script_sections: list[dict],   # [{section_title, script_text}, ...]
) -> str:
    """
    Convert the voice guide script to audio and save to disk.

    Returns the path to the generated audio file (MP3 or WAV),
    or to a .txt fallback if TTS is not available.
    """
    settings = get_settings()
    audio_dir = Path(settings.audio_cache_dir)
    audio_dir.mkdir(parents=True, exist_ok=True)
    output_path = audio_dir / f"{repo_id}_voice_guide.wav"

    if not _TTS_AVAILABLE:
        logger.info("TTS unavailable — saving script as text file.")
        return _save_text_fallback(script_sections, output_path)

    tts = _get_tts()
    if tts is None:
        return _save_text_fallback(script_sections, output_path)

    try:
        import wave

        # Generate audio for each section, then concatenate
        segment_paths = []
        for i, section in enumerate(script_sections):
            segment_path = audio_dir / f"{repo_id}_section_{i}.wav"
            tts.tts_to_file(
                text=section["script_text"],
                file_path=str(segment_path),
            )
            segment_paths.append(str(segment_path))

        if len(segment_paths) == 1:
            os.rename(segment_paths[0], output_path)
        else:
            _concatenate_wav_files(segment_paths, str(output_path))
            # Cleanup segments
            for p in segment_paths:
                try:
                    os.remove(p)
                except OSError:
                    pass

        logger.info(f"Voice guide generated: {output_path}")
        return str(output_path)

    except Exception as exc:
        logger.error(f"TTS generation failed: {exc}")
        return _save_text_fallback(script_sections, output_path)


def _concatenate_wav_files(input_paths: list[str], output_path: str):
    """Concatenate multiple WAV files into a single output file."""
    import wave

    with wave.open(output_path, "wb") as output_wav:
        for i, path in enumerate(input_paths):
            try:
                with wave.open(path, "rb") as input_wav:
                    if i == 0:
                        output_wav.setparams(input_wav.getparams())
                    output_wav.writeframes(input_wav.readframes(input_wav.getnframes()))
            except Exception as exc:
                logger.warning(f"Skipping segment {path}: {exc}")
