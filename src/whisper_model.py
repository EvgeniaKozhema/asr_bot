import librosa
import torch
import time
import os
import soundfile as sf
from transformers import AutoModelForSpeechSeq2Seq, AutoProcessor, pipeline

# Загружаем модель
MODEL_NAME = "EvgeniaKozhema/whisper-small-ru"
model = AutoModelForSpeechSeq2Seq.from_pretrained(
    MODEL_NAME, torch_dtype=torch.float32, low_cpu_mem_usage=True, use_safetensors=True, attn_implementation="sdpa"
)
processor = AutoProcessor.from_pretrained(MODEL_NAME)

# Настраиваем пайплайн
pipe = pipeline(
    "automatic-speech-recognition",
    model=model,
    tokenizer=processor.tokenizer,
    feature_extractor=processor.feature_extractor,
    max_new_tokens=128,
    chunk_length_s=30,
    batch_size=16,
    generate_kwargs={'language': 'russian', 'task': 'transcribe'},
    torch_dtype=torch.float32,
)

def transcribe_audio(audio_path):
    """Обрабатывает аудио и возвращает текст."""
    waveform, sr = librosa.load(audio_path, sr=None)
    if sr != 16000:
        waveform = librosa.resample(waveform, orig_sr=sr, target_sr=16000)

    start_time = time.time()
    response = pipe(waveform)
    generation_time = time.time() - start_time

    print(f"Текст: {response['text']}, Время работы: {generation_time:.2f} сек.")
    return response["text"]
