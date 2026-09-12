"""
Модуль управления профилем пользователя Vasya Ai.
Сохраняет личные данные и формирует психологический портрет.
"""
import json
import os

PROFILE_FILE = "user_data.json"

class UserProfile:
    def __init__(self):
        self.name = ""
        self.surname = ""
        self.age = 0
        self.zodiac = ""
        self.loaded = False
        self.load_profile()

    def load_profile(self):
        """Загрузка профиля из файла, если он существует."""
        if os.path.exists(PROFILE_FILE):
            try:
                with open(PROFILE_FILE, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.name = data.get("name", "")
                    self.surname = data.get("surname", "")
                    self.age = data.get("age", 0)
                    self.zodiac = data.get("zodiac", "")
                    self.loaded = True
            except Exception:
                self.loaded = False

    def save_profile(self):
        """Сохранение профиля в JSON файл."""
        data = {
            "name": self.name,
            "surname": self.surname,
            "age": self.age,
            "zodiac": self.zodiac
        }
        with open(PROFILE_FILE, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
        self.loaded = True

    def is_registered(self):
        return self.loaded and bool(self.name)

    def get_full_name(self):
        return f"{self.name} {self.surname}" if self.surname else self.name

    def get_psycho_portrait(self):
        """Формирует краткое описание личности для контекста ИИ."""
        if not self.loaded:
            return "Пользователь не зарегистрирован."
        
        traits = []
        # Примерная логика по знакам зодиака (для персонализации стиля)
        zodiac_traits = {
            "овен": "решителен, любит прямые ответы, ценит скорость",
            "телец": "практичен, любит конкретику и стабильность",
            "близнецы": "любит разнообразие, юмор и краткость",
            "рак": "эмоционален, нуждается в поддержке и эмпатии",
            "лев": "ценит уважение, похвалу и лидерский тон",
            "дева": "любит логику, детали и структурированные планы",
            "весы": "ищет баланс, вежлив, любит варианты выбора",
            "скорпион": "проницателен, любит глубину и тайны",
            "стрелец": "оптимист, любит масштабные идеи и путешествия",
            "козерог": "целеустремлен, ценит карьеру и дисциплину",
            "водолей": "креативен, любит нестандартные решения",
            "рыбы": "интуитивен, ценит творчество и мечты"
        }
        
        zodiac_key = self.zodiac.lower()
        trait = zodiac_traits.get(zodiac_key, "уникален и интересен")
        
        age_group = "молодой человек" if self.age < 30 else "опытный человек" if self.age < 60 else "мудрый наставник"
        
        return f"Пользователь: {self.get_full_name()}, {self.age} лет ({age_group}). Знак зодиака: {self.zodiac}. Характер: {trait}."
