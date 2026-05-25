import time
import os
import sys
from speech_to_text import STTModel
from llm_processor import process_text_with_ollama
from hotkey_manager import HotkeyManager
from audio import record_until_silence
import keyboard

# ================== КОНФИГУРАЦИЯ ==================
HOTKEY = "ctrl+alt+r"
WHISPER_MODEL_SIZE = "small"   # tiny / base / small / medium
WHISPER_DEVICE = "cpu"
WHISPER_COMPUTE_TYPE = "int8"
OLLAMA_MODEL = "gemma4"
# ===================================================

def on_hotkey():
    print("\n🔥 Горячая клавиша нажата!")
    audio_file = record_until_silence(silence_threshold=500, silence_duration=1.5)

    try:
        # 1. Распознавание
        raw_text = stt_model.transcribe(audio_file)
        print(f"📝 Распознано: {raw_text}")
        if not raw_text.strip():
            print("⚠️ Речь не обнаружена.")
            return

        # 2. Улучшение через нейросеть
        processed_text = process_text_with_ollama(raw_text, model=OLLAMA_MODEL)
        print(f"✨ Улучшено: {processed_text}")

        # 3. Вставка в активное поле
        time.sleep(0.2)          # чтобы гарантированно отпустились модификаторы
        keyboard.write(processed_text)
        print("📋 Текст вставлен в поле ввода.")
    except Exception as e:
        print(f"❌ Ошибка обработки: {e}")
    finally:
        if os.path.exists(audio_file):
            os.unlink(audio_file)

def main():
    global stt_model
    # Инициализация STT
    stt_model = STTModel(
        model_size=WHISPER_MODEL_SIZE,
        device=WHISPER_DEVICE,
        compute_type=WHISPER_COMPUTE_TYPE
    )

    # Проверка связи с Ollama
    try:
        import ollama
        ollama.list()
        print("🦙 Сервер Ollama доступен.")
    except Exception as e:
        print(f"⚠️ Не удалось подключиться к Ollama: {e}")

    # Запуск слушателя горячих клавиш
    hotkey_manager = HotkeyManager(HOTKEY, on_hotkey)
    hotkey_manager.start()

    print(f"🎙️ Ассистент запущен. Нажмите {HOTKEY} для записи и улучшения речи.")
    print("Для выхода нажмите Ctrl+C в терминале.\n")

    try:
        while True:
            time.sleep(0.1)
    except KeyboardInterrupt:
        print("\n👋 Завершение работы.")
        sys.exit(0)

if __name__ == "__main__":
    main()