#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Vasya Ai - Умный чат-бот для решения любых проблем.
Версия 2.0: Модульная архитектура с расширенными возможностями.

Запуск в Visual Studio 2019:
1. Откройте этот файл
2. Убедитесь, что Python установлен
3. Нажмите F5 или кнопку "Run"
"""

import sys
from datetime import datetime
from context_manager import ConversationContext
from ai_engine import VasyaAiEngine


class VasyaAiBot:
    """Основной класс чат-бота Vasya Ai."""
    
    def __init__(self):
        self.context = ConversationContext()
        self.engine = VasyaAiEngine()
        self.is_running = True
        self.commands = ['помощь', 'история', 'очистить', 'контекст', 'темы', 'пока', 'выход']
    
    def start(self):
        """Запускает чат-бота."""
        self._print_welcome()
        
        while self.is_running:
            try:
                user_input = self._get_user_input()
                
                if not user_input:
                    continue
                
                # Проверка на команды
                if user_input.lower().strip() in self.commands:
                    response = self.engine.process_command(user_input, self.context)
                    if user_input.lower().strip() in ['пока', 'выход']:
                        self._say_goodbye()
                        break
                else:
                    # Попытка извлечь имя пользователя
                    name = self.engine.extract_user_name(user_input)
                    if name:
                        self.context.set_user_name(name)
                    
                    # Анализ и генерация ответа
                    category, params = self.engine.analyze_message(user_input, self.context)
                    response = self.engine.generate_detailed_response(category, params, self.context)
                
                # Добавление в историю
                self.context.add_message("пользователь", user_input)
                self.context.add_message("Vasya Ai", response)
                
                # Вывод ответа
                self._print_response(response)
                
            except KeyboardInterrupt:
                print("\n\n⚠️  Работа прервана пользователем.")
                self._say_goodbye()
                break
            except Exception as e:
                print(f"\n❌ Произошла ошибка: {e}")
                print("Попробуйте ещё раз или введите 'помощь'.")
    
    def _print_welcome(self):
        """Выводит приветственное сообщение."""
        welcome_art = r"""
 ____   ____  _____ ____  ______ 
|  _ \ / __ \|  __|___ ||____  |
| |_) | |  | | |__   / /    / / 
|  _ <| |  | |  __| / /    / /  
| |_) | |__| | |__ / /__  / /   
|____/ \____/|____|_____|/_/    
      Искусственный Интеллект
========================================
"""
        print(welcome_art)
        print("🤖 Привет! Я Vasya Ai — твой умный друг и помощник.")
        print("   Я здесь, чтобы помочь решить любые проблемы!")
        print("   Введи 'помощь' для списка команд.\n")
        
        # Персонализированное приветствие
        if self.context.get_user_name() != "друг":
            print(f"   С возвращением, {self.context.get_user_name()}! 👋\n")
    
    def _get_user_input(self):
        """Получает ввод от пользователя."""
        try:
            user_name = self.context.get_user_name()
            prompt = f"\n💬 {user_name}: " if user_name != "друг" else "\n💬 Ты: "
            return input(prompt).strip()
        except EOFError:
            return ""
    
    def _print_response(self, response):
        """Выводит ответ бота."""
        print(f"\n🤖 Vasya Ai: {response}")
        print("-" * 60)
    
    def _say_goodbye(self):
        """Выводит прощальное сообщение."""
        user_name = self.context.get_user_name()
        farewell = f"\n👋 До встречи, {user_name}!" if user_name != "друг" else "\n👋 До встречи!"
        print(farewell)
        print("   Помни: я всегда здесь, если понадобишься помощь.")
        print("   Возвращайся в любое время!\n")
        print("=" * 60)


def main():
    """Точка входа в приложение."""
    bot = VasyaAiBot()
    bot.start()


if __name__ == "__main__":
    main()
