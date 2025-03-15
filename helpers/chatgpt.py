from g4f.client import Client


class AIHelper:
    def __init__(self, model: str = "gpt-4o-mini"):
        self.client = Client()
        self.model = model

    def correct_text(self, text: str) -> str:
        """
        Исправляет ошибки в английском предложении и возвращает исправленный вариант.
        Текст, в котором необходимо исправить ошибки, передается в параметре text.
        Модель возвращает исправленный вариант, при этом слова, которые были исправлены, выделяются заглавными буквами.
        """
        prompt = (
            "Исправь в этом предложении на английском ошибки. Если ошибок нет, то так и напиши"
            "Напиши предложение без ошибок и укажи, что ты исправил с объяснениями. "
            "Формат ответа."
            "Исходный текст: text"
            "Исправленный текст: text"
            "Пояснения: text"
            f"{text}"
        )
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
            web_search=False,
        )
        print(response.choices[0].message.content)
        # Предполагается, что исправленный текст находится в response.choices[0].message.content
        return response.choices[0].message.content

    def check_language(self, text: str) -> str:
        prompt = (
            "Исправь в этом предложении на английском ошибки. Если ошибок нет, то так и напиши"
            "Напиши предложение без ошибок и укажи, что ты исправил с объяснениями. "
            "Формат ответа."
            "Исходный текст: text"
            "Исправленный текст: text"
            "Пояснения: text"
            f"{text}"
        )
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
            web_search=False,
        )
        print(response.choices[0].message.content)
        # Предполагается, что исправленный текст находится в response.choices[0].message.content
        return response.choices[0].message.content


if __name__ == "__main__":
    corrector = AIHelper()
    original_text = "I'm goig to school yesterday"
    corrected_text = corrector.correct_text(original_text)
    print("Исходное:", original_text)
    print("Исправленное:", corrected_text)
