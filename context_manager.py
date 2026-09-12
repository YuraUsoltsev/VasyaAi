# -*- coding: utf-8 -*-
"""
Контекстный менеджер Vasya Ai
Управляет историей диалога, памятью о пользователе и контекстом беседы.
"""

import json
from datetime import datetime

class ConversationContext:
    """Класс для управления контекстом диалога."""
    
    def __init__(self, history_file="conversation_history.json"):
        self.history_file = history_file
        self.user_name = None
        self.user_mood = "нейтральное"
        self.conversation_history = []
        self.problem_topics = []
        self.load_history()
    
    def load_history(self):
        """Загружает историю из файла."""
        try:
            with open(self.history_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                self.user_name = data.get('user_name')
                self.user_mood = data.get('user_mood', 'нейтральное')
                self.conversation_history = data.get('history', [])
                self.problem_topics = data.get('problem_topics', [])
        except FileNotFoundError:
            self.conversation_history = []
    
    def save_history(self):
        """Сохраняет историю в файл."""
        data = {
            'user_name': self.user_name,
            'user_mood': self.user_mood,
            'history': self.conversation_history[-50:],  # Последние 50 сообщений
            'problem_topics': self.problem_topics
        }
        with open(self.history_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    
    def add_message(self, role, message):
        """Добавляет сообщение в историю."""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.conversation_history.append({
            'timestamp': timestamp,
            'role': role,
            'message': message
        })
        self.save_history()
    
    def set_user_name(self, name):
        """Устанавливает имя пользователя."""
        self.user_name = name
        self.save_history()
    
    def get_user_name(self):
        """Возвращает имя пользователя."""
        return self.user_name if self.user_name else "друг"
    
    def update_mood(self, mood):
        """Обновляет настроение пользователя."""
        self.user_mood = mood
        self.save_history()
    
    def add_problem_topic(self, topic):
        """Добавляет тему проблемы в список."""
        if topic not in self.problem_topics:
            self.problem_topics.append(topic)
            self.save_history()
    
    def get_history_summary(self):
        """Возвращает краткую сводку истории."""
        if not self.conversation_history:
            return "История пуста."
        
        summary = f"Всего сообщений: {len(self.conversation_history)}\n"
        if self.user_name:
            summary += f"Имя пользователя: {self.user_name}\n"
        if self.problem_topics:
            summary += f"Обсуждаемые темы: {', '.join(self.problem_topics)}\n"
        
        # Последние 3 сообщения
        recent = self.conversation_history[-3:]
        summary += "\nПоследние сообщения:\n"
        for msg in recent:
            summary += f"[{msg['timestamp']}] {msg['role']}: {msg['message'][:50]}...\n"
        
        return summary
    
    def clear_history(self):
        """Очищает историю."""
        self.conversation_history = []
        self.problem_topics = []
        self.save_history()
    
    def get_context_for_ai(self):
        """Возвращает контекст для улучшения ответов ИИ."""
        context = {
            'user_name': self.get_user_name(),
            'mood': self.user_mood,
            'recent_topics': self.problem_topics[-5:] if self.problem_topics else [],
            'message_count': len(self.conversation_history)
        }
        return context
