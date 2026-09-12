"""
Vasya Ai v3.0 — Главный файл запуска.
Интеллектуальный чат-бот с регистрацией пользователя и глубоким анализом.
Запускается в терминале Windows, Linux, macOS и Visual Studio.
"""
import sys
from user_profile import UserProfile
from ai_engine import VasyaBrain

def print_banner():
    print("=" * 60)
    print("🤖 VASYA AI v3.0 — Твой умный друг и помощник")
    print("=" * 60)

def register_user(profile: UserProfile):
    """Процедура регистрации нового пользователя."""
    print("\n📝 Давай познакомимся! Я хочу узнать о тебе всё.")
    
    if not profile.is_registered():
        name = input("Твоё имя: ").strip()
        surname = input("Твоя фамилия: ").strip()
        
        while True:
            try:
                age = int(input("Твой возраст: ").strip())
                break
            except ValueError:
                print("⚠️ Пожалуйста, введи число для возраста.")
        
        zodiac = input("Твой знак зодиака (например, Овен, Телец): ").strip()
        
        profile.name = name
        profile.surname = surname
        profile.age = age
        profile.zodiac = zodiac
        profile.save_profile()
        
        print(f"\n✨ Рад знакомству, {name} {surname}!")
        print(f"🔮 Знак {zodiac} наделяет тебя особыми качествами.")
        print("Я сохранил твой профиль. В следующий раз я сразу узнаю тебя.\n")
    else:
        print(f"\n👋 С возвращением, {profile.get_full_name()}!")
        print(f"🔮 Твой знак: {profile.zodiac}, Возраст: {profile.age}")
        print("Я помню тебя. Готов продолжать общение.\n")

def main():
    print_banner()
    
    # Инициализация профиля и мозга
    profile = UserProfile()
    register_user(profile)
    
    brain = VasyaBrain(profile)
    
    print("💡 Я готов решать любые твои проблемы.")
    print("   Напиши 'помощь' для списка команд или просто расскажи о проблеме.")
    print("-" * 60)
    
    while True:
        try:
            user_input = input("\n💬 Ты: ").strip()
            
            if not user_input:
                continue
            
            lower_input = user_input.lower()
            
            # Команды управления
            if lower_input in ["пока", "выход", "quit", "exit"]:
                print(f"\n🤖 Vasya Ai: До встречи, {profile.name}! Помни: ты способен на всё!")
                break
            
            if lower_input in ["помощь", "help"]:
                print("\n📚 **Команды Vasya Ai:**")
                print("   - помощь: показать это меню")
                print("   - пока / выход: завершить разговор")
                print("   - контекст: показать текущий контекст беседы")
                print("   - сброс: забыть историю переписки")
                print("   - анкета: показать мои данные")
                print("   Просто напиши о своей проблеме, и я помогу!")
                continue
            
            if lower_input == "контекст":
                print(f"\n🧠 **Контекст:** {brain.get_context_summary()}")
                continue
                
            if lower_input == "сброс":
                brain.conversation_history = []
                print("\n🗑️ История переписки очищена.")
                continue
            
            if lower_input == "анкета":
                print(f"\n📋 **Твои данные:**")
                print(f"   Имя: {profile.name}")
                print(f"   Фамилия: {profile.surname}")
                print(f"   Возраст: {profile.age}")
                print(f"   Знак зодиака: {profile.zodiac}")
                print(f"   Портрет: {profile.get_psycho_portrait()}")
                continue
            
            # Генерация ответа ИИ
            response = brain.generate_response(user_input)
            print(f"\n🤖 Vasya Ai: {response}")
            
        except KeyboardInterrupt:
            print(f"\n\n🤖 Vasya Ai: Прервано. Береги себя, {profile.name}!")
            sys.exit(0)
        except Exception as e:
            print(f"\n⚠️ Произошла ошибка: {e}. Попробуй еще раз.")

if __name__ == "__main__":
    main()
