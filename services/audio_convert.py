import os
import shutil
import subprocess
import tempfile
from typing import List


def _ensure_ffmpeg() -> None:
    if shutil.which("ffmpeg") is None:
        raise RuntimeError(
            "系统未找到 ffmpeg，请先安装 ffmpeg，并确保命令行可直接执行 ffmpeg。"
        )


def audio_file_to_pcm_chunks(file_bytes: bytes, suffix: str, work_dir: str = "tmp") -> List[bytes]:
    """
    把上传的音频文件转成 16k / 单声道 / 16bit little-endian PCM。
    返回值是 List[bytes]，为了兼容原项目 ASR 的 speech_to_text_wrapper(..., audio_format='pcm')
    """
    _ensure_ffmpeg()
    os.makedirs(work_dir, exist_ok=True)

    if not suffix:
        suffix = ".wav"
    if not suffix.startswith("."):
        suffix = "." + suffix

    input_path = None
    output_path = None

    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=suffix, dir=work_dir) as f:
            f.write(file_bytes)
            input_path = f.name

        with tempfile.NamedTemporaryFile(delete=False, suffix=".pcm", dir=work_dir) as f:
            output_path = f.name

        cmd = [
            "ffmpeg",
            "-y",
            "-i",
            input_path,
            "-f",
            "s16le",
            "-acodec",
            "pcm_s16le",
            "-ac",
            "1",
            "-ar",
            "16000",
            output_path,
        ]

        result = subprocess.run(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )

        if result.returncode != 0:
            raise RuntimeError(f"ffmpeg 转换失败：{result.stderr.strip()}")

        with open(output_path, "rb") as f:
            pcm_bytes = f.read()

        if not pcm_bytes:
            raise RuntimeError("音频转换完成，但 PCM 数据为空。")

        return [pcm_bytes]

    finally:
        if input_path and os.path.exists(input_path):
            try:
                os.remove(input_path)
            except Exception:
                pass

        if output_path and os.path.exists(output_path):
            try:
                os.remove(output_path)
            except Exception:
                pass