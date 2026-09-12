# -*- coding: utf-8 -*-
"""
Интеллектуальный движок Vasya Ai
Анализирует запросы, генерирует подробные ответы и адаптируется к пользователю.
"""

import re
from knowledge_base import get_category, get_response, KNOWLEDGE_BASE

class VasyaAiEngine:
    """Умный движок для обработки запросов пользователя."""
    
    def __init__(self):
        self.conversation_depth = 0
        self.last_topic = None
        self.detailed_mode = True
    
    def analyze_message(self, message, context):
        """
        Глубокий анализ сообщения пользователя.
        Возвращает категорию, подкатегорию и дополнительные параметры.
        """
        message_lower = message.lower()
        
        # Базовая категория
        category = get_category(message)
        
        # Дополнительные параметры
        params = {
            'is_question': '?' in message,
            'is_urgent': any(word in message_lower for word in ['срочно', 'быстро', 'помогите', 'беда']),
            'needs_code': any(word in message_lower for word in ['код', 'пример', 'скрипт', 'функция']),
            'emotional_tone': self._detect_emotion(message_lower),
            'specificity': self._measure_specificity(message)
        }
        
        # Обновление контекста
        if params['emotional_tone'] != 'нейтральное':
            context.update_mood(params['emotional_tone'])
        
        if category != 'приветствие' and category != 'неизвестно':
            context.add_problem_topic(category)
        
        return category, params
    
    def _detect_emotion(self, text):
        """Определяет эмоциональный тон сообщения."""
        positive_words = ['отлично', 'хорошо', 'рад', 'счастлив', 'спасибо', 'круто', 'супер']
        negative_words = ['плохо', 'грустно', 'устал', 'стресс', 'проблема', 'ошибка', 'беда', 'тревога']
        
        pos_count = sum(1 for word in positive_words if word in text)
        neg_count = sum(1 for word in negative_words if word in text)
        
        if neg_count > pos_count:
            return 'негативное'
        elif pos_count > neg_count:
            return 'позитивное'
        return 'нейтральное'
    
    def _measure_specificity(self, text):
        """Измеряет конкретность запроса (количество деталей)."""
        words = text.split()
        return len(words)
    
    def generate_detailed_response(self, category, params, context):
        """
        Генерирует развёрнутый и персонализированный ответ.
        """
        user_name = context.get_user_name()
        base_response = get_response(category)
        
        # Добавляем персонализацию
        personalized = self._personalize_response(base_response, user_name, params)
        
        # Добавляем дополнительные советы если запрос сложный
        if params['specificity'] > 10 or params['is_question']:
            additional_advice = self._generate_additional_advice(category, params)
            if additional_advice:
                personalized += f"\n\n💡 Дополнительно:\n{additional_advice}"
        
        # Если срочный запрос - добавляем поддержку
        if params['is_urgent']:
            personalized = "🚨 Срочно! " + personalized + "\n\nНе переживай, мы вместе это решим! Действуй по шагам."
        
        # Если нужны примеры кода
        if params['needs_code'] and category == 'проблемы_кодинг':
            code_example = self._get_code_example()
            if code_example:
                personalized += f"\n\n📝 Пример кода:\n{code_example}"
        
        self.conversation_depth += 1
        return personalized
    
    def _personalize_response(self, response, user_name, params):
        """Добавляет персонализацию к ответу."""
        # Обращение по имени
        if user_name != "друг":
            greeting_variants = [
                f"{user_name}, ",
                f"Дорогой {user_name}, ",
                f"{user_name}, послушай, "
            ]
            import random
            response = random.choice(greeting_variants) + response[0].lower() + response[1:]
        
        # Учёт эмоций
        if params['emotional_tone'] == 'негативное':
            response = "Понимаю твои чувства. " + response
        elif params['emotional_tone'] == 'позитивное':
            response = "Здорово, что у тебя всё хорошо! " + response
        
        return response
    
    def _generate_additional_advice(self, category, params):
        """Генерирует дополнительные советы в зависимости от категории."""
        advice_map = {
            'проблемы_кодинг': [
                "Используй print() для отладки или установи breakpoint().",
                "Проверь документацию библиотеки на официальном сайте.",
                "Создай минимальный воспроизводимый пример ошибки."
            ],
            'проблемы_учеба': [
                "Составь интеллект-карту (mind map) по теме.",
                "Найди практические задачи и реши их.",
                "Объясни тему кому-нибудь другому — это проверит понимание."
            ],
            'проблемы_жизнь': [
                "Разбей большую задачу на маленькие шаги.",
                "Сделай перерыв и прогуляйся на свежем воздухе.",
                "Запиши 3 вещи, за которые ты благодарен сегодня."
            ],
            'технологии': [
                "Изучи официальную документацию — там всегда актуальная информация.",
                "Посмотри проекты на GitHub для практики.",
                "Присоединись к профильным сообществам (Telegram, Discord)."
            ]
        }
        
        import random
        advice_list = advice_map.get(category, [
            "Попробуй подойти к проблеме с другой стороны.",
            "Ищи информацию в надёжных источниках.",
            "Не бойся задавать уточняющие вопросы."
        ])
        
        return random.choice(advice_list)
    
    def _get_code_example(self):
        """Возвращает пример кода для демонстрации."""
        examples = [
            "# Пример обработки ошибки в Python\n"
            "try:\n"
            "    result = 10 / 0\n"
            "except ZeroDivisionError as e:\n"
            "    print(f'Ошибка: {e}')\n"
            "    result = 0",
            
            "# Пример функции с документацией\n"
            "def solve_problem(problem_description):\n"
            "    '''Решает проблему пошагово'''\n"
            "    steps = [\n"
            "        '1. Пойми суть проблемы',\n"
            "        '2. Разбей на части',\n"
            "        '3. Реши каждую часть',\n"
            "        '4. Проверь результат'\n"
            "    ]\n"
            "    return steps"
        ]
        import random
        return random.choice(examples)
    
    def process_command(self, command, context):
        """Обрабатывает специальные команды."""
        commands = {
            'помощь': self._help_command,
            'история': lambda ctx: context.get_history_summary(),
            'очистить': lambda ctx: self._clear_command(context),
            'контекст': lambda ctx: str(context.get_context_for_ai()),
            'темы': lambda ctx: f"Обсуждаемые темы: {', '.join(context.problem_topics) if context.problem_topics else 'Нет'}"
        }
        
        command_lower = command.lower().strip()
        if command_lower in commands:
            return commands[command_lower](context)
        return None
    
    def _help_command(self, context):
        """Возвращает справку по командам."""
        return """
📚 СПРАВКА ПО КОМАНДАМ:

• помощь - показать эту справку
• история - показать историю переписки
• очистить - очистить историю диалога
• контекст - показать текущий контекст
• темы - показать обсуждаемые темы
• пока / выход - завершить работу

💡 СОВЕТЫ:
• Описывай проблему подробно для лучших ответов
• Упоминай имя: "меня зовут Александр"
• Задавай уточняющие вопросы
• Используй ключевые слова: код, ошибка, учёба, стресс
"""
    
    def _clear_command(self, context):
        """Очищает историю и возвращает подтверждение."""
        context.clear_history()
        return "✅ История диалога очищена. Начинаем с чистого листа!"
    
    def extract_user_name(self, message):
        """Пытается извлечь имя пользователя из сообщения."""
        patterns = [
            r"меня зовут\s+(\w+)",
            r"мое имя\s+(\w+)",
            r"я\s+(\w+)\s*[,\.]",
            r"зовут\s+(\w+)"
        ]
        
        for pattern in patterns:
            match = re.search(pattern, message.lower())
            if match:
                name = match.group(1).capitalize()
                if len(name) > 1 and len(name) < 20:  # Простая валидация
                    return name
        return None
