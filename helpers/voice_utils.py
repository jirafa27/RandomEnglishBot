import whisper


def transcribe(audio_path: str, model_name: str = "base") -> str:
    """
    Распознаёт речь в аудиофайле (ogg, mp3, wav и т.д.) с помощью модели OpenAI Whisper.

    :param audio_path: Путь к аудиофайлу (любого формата, поддерживаемого ffmpeg).
    :param model_name: Название модели Whisper (tiny, base, small, medium, large).
                      По умолчанию "base" — относительно небольшой размер (~500 МБ).
    :return: Распознанный текст (string).
    """
    # Загружаем модель (при первом запуске скачивается из интернета)
    model = whisper.load_model(model_name)

    # Выполняем транскрипцию
    result = model.transcribe(audio_path)

    # Результат — словарь, где ключ "text" содержит итоговую расшифровку
    recognized_text = result["text"].strip()
    return recognized_text
