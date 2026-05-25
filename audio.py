import numpy as np
import sounddevice as sd
import soundfile as sf
import tempfile
import time
import sys
import os


def play_start_sound():
    """Двойной короткий звуковой сигнал — начало записи."""
    try:
        if sys.platform == "win32":
            import winsound
            winsound.Beep(1000, 100)
            time.sleep(0.1)
            winsound.Beep(1000, 100)
        else:
            print('\a', end='', flush=True)
            time.sleep(0.1)
            print('\a', end='', flush=True)
    except:
        pass


def play_end_sound():
    """Один длинный сигнал — конец записи."""
    try:
        if sys.platform == "win32":
            import winsound
            winsound.Beep(800, 300)
        else:
            print('\a', end='', flush=True)
    except:
        pass


def record_until_silence(
        sample_rate=16000,
        silence_threshold=500,  # RMS для int16
        silence_duration=1.5,  # секунд тишины до остановки
        max_duration=30  # максимальная длина записи в секундах
):
    """Записывает аудио с микрофона и останавливается после тишины.
    Возвращает путь к временному WAV-файлу."""

    print("🎤 Запись началась...")
    play_start_sound()

    # Параметры захвата
    chunk_size = 1024  # размер блока для анализа тишины
    audio_data = []
    silent_blocks = 0
    silence_blocks_needed = int(silence_duration * sample_rate / chunk_size)
    start_time = time.time()

    # Открываем поток
    stream = sd.InputStream(
        samplerate=sample_rate,
        channels=1,
        dtype='int16',
        blocksize=chunk_size
    )
    stream.start()

    try:
        while True:
            data, overflowed = stream.read(chunk_size)
            if overflowed:
                print("⚠️ Переполнение буфера, данные могут быть потеряны")
            audio_data.append(data.copy())

            # Расчёт RMS
            rms = np.sqrt(np.mean(data.astype(np.float32) ** 2))
            if rms < silence_threshold:
                silent_blocks += 1
            else:
                silent_blocks = 0

            # Прерывание по тишине или таймауту
            if silent_blocks >= silence_blocks_needed or (time.time() - start_time) > max_duration:
                break
    finally:
        stream.stop()
        stream.close()

    play_end_sound()
    print("✅ Запись завершена.")

    # Склеиваем все блоки в один массив
    full_audio = np.concatenate(audio_data, axis=0)

    # Сохраняем во временный WAV
    with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmpfile:
        sf.write(tmpfile.name, full_audio, sample_rate, subtype='PCM_16')
        return tmpfile.name