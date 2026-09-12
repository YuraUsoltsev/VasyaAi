"""
Интеллектуальное ядро Vasya Ai v3.0.
Содержит логику "настоящего" ИИ: эвристики, контекстный анализ и генерацию ответов.
"""
import random
import datetime
from user_profile import UserProfile

class VasyaBrain:
    def __init__(self, profile: UserProfile):
        self.profile = profile
        self.conversation_history = []
        self.max_history = 10  # Храним последние 10 реплик для контекста
        
        # База знаний расширена для глубоких ответов
        self.knowledge_base = {
            "приветствие": [
                "Здравствуй, {name}! Я готов погрузиться в решение твоих задач.",
                "Рад видеть тебя, {name}. Что будем исследовать сегодня?",
                "Приветствую! Твой знак зодиака ({zodiac}) подсказывает мне, что сегодня отличный день для начинаний."
            ],
            "код": {
                "python": "Python — мощный инструмент. Ошибка часто кроется в отступах или типах данных. Давай разберем стек вызова (traceback).",
                "js": "JavaScript асинхронен. Проверь промисы и цепочки async/await. Ошибки в консоли браузера — твой лучший друг.",
                "c++": "C++ требует управления памятью. Проверь указатели и выход за границы массивов. Используй умные указатели (smart pointers).",
                "ошибка": "Любая ошибка — это подсказка. Прочитай текст ошибки внимательно: он указывает на строку и тип проблемы."
            },
            "жизнь": [
                "Понимаю. Иногда нужно просто выдохнуть. Как твой знак зодиака ({zodiac}) советует: доверься интуиции, но проверяй факты.",
                "В возрасте {age} лет многие сталкиваются с этим. Главное — системный подход. Раздели проблему на мелкие шаги.",
                "Это сложная ситуация. Давай составим план действий из 3 пунктов прямо сейчас."
            ],
            "наука": "Научный метод требует гипотезы и проверки. Что именно вызывает сомнения? Физика, математика или логика?",
            "творчество": "Творческий кризис лечится сменой деятельности. Попробуй технику 'фрирайтинг' или смени обстановку."
        }

    def add_to_history(self, role, message):
        self.conversation_history.append({"role": role, "message": message, "time": datetime.datetime.now().isoformat()})
        if len(self.conversation_history) > self.max_history:
            self.conversation_history.pop(0)

    def analyze_intent(self, text):
        text_lower = text.lower()
        if any(word in text_lower for word in ["код", "программ", "ошибк", "баг", "python", "java", "c++"]):
            return "code"
        if any(word in text_lower for word in ["груст", "проблем", "стресс", "устал", "не знаю"]):
            return "life"
        if any(word in text_lower for word in ["формула", "теорема", "физик", "химия", "биология"]):
            return "science"
        if any(word in text_lower for word in ["рисова", "писать", "идея", "творчеств"]):
            return "creative"
        return "general"

    def generate_response(self, user_input):
        intent = self.analyze_intent(user_input)
        name = self.profile.name if self.profile.name else "друг"
        zodiac = self.profile.zodiac if self.profile.zodiac else "звезд"
        age = str(self.profile.age) if self.profile.age else "любом"
        
        response = ""
        
        # Логика формирования ответа в стиле "Настоящего ИИ"
        if intent == "code":
            response = f"👨‍💻 **Анализ кода:**\nВижу, ты столкнулся с технической задачей. Как {name}, ты наверняка справишься.\n\n"
            response += "1. **Диагностика:** Внимательно прочитай сообщение об ошибке. Оно содержит номер строки.\n"
            response += "2. **Изоляция:** Попробуй запустить этот кусок кода отдельно.\n"
            response += "3. **Решение:** Чаще всего проблема в синтаксисе или версии библиотеки.\n\n"
            response += "💡 *Совет Vasya Ai:* Используй отладчик (debugger), чтобы пройти по коду пошагово."
            
        elif intent == "life":
            response = f"❤️ **Эмоциональный интеллект:**\n{name}, я слышу тебя. В {age} лет жизнь полна вызовов.\n"
            response += f"Твой знак зодиака ({zodiac}) говорит о том, что у тебя есть внутренняя сила.\n\n"
            response += "Давай применим алгоритм решения проблем:\n"
            response += "- Шаг 1: Опиши проблему одним предложением.\n"
            response += "- Шаг 2: Назови 3 возможных решения, даже самых безумных.\n"
            response += "- Шаг 3: Выбери одно и сделай первый микро-шаг прямо сейчас."
            
        elif intent == "science":
            response = f"🔬 **Научный подход:**\nИнтересный вопрос, {name}!\n"
            response += "Наука строится на фактах. Давай разберем это явление через призму причинно-следственных связей.\n"
            response += "Какие вводные данные мы имеем? Есть ли противоречия с известными законами?"
            
        else:
            # Общий ответ с персонализацией
            templates = self.knowledge_base["приветствие"] if "привет" in user_input.lower() else [
                "Я анализирую твой запрос, {name}. Это требует глубокого понимания контекста.",
                "Интересная мысль. Учитывая твой возраст ({age}) и знак ({zodiac}), я предлагаю такой взгляд...",
                "Я обработал информацию. Вот мое резюме ситуации..."
            ]
            response = random.choice(templates).format(name=name, zodiac=zodiac, age=age)
            if "привет" not in user_input.lower():
                response += "\n\nРасскажи подробнее, какие детали ты считаешь ключевыми?"

        self.add_to_history("user", user_input)
        self.add_to_history("assistant", response)
        return response

    def get_context_summary(self):
        """Возвращает сводку контекста для 'памяти' бота."""
        if not self.conversation_history:
            return "История пуста."
        last_topics = [msg['message'][:50] for msg in self.conversation_history[-3:]]
        return f"Последние темы: {'; '.join(last_topics)}..."
