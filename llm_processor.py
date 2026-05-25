import ollama

def process_text_with_ollama(text, model="gemma4:e4b"):
    """Отправляет сырой текст в локальную LLM и возвращает литературно оформленный результат."""
    prompt = (
        "You are a text editing assistant. Convert the following informal spoken phrase "
        "into a well-written, grammatically correct, and stylistically beautiful text in Russian. "
        "Improve wording, fix mistakes, add necessary details to make it sound complete. "
        "Ответ должен быть ТОЛЬКО обработанным текстом без каких-либо пояснений.\n\n"
        f"Текст для обработки: {text}"
    )
    response = ollama.chat(model=model, messages=[
        {"role": "user", "content": prompt}
    ])
    return response['message']['content'].strip()