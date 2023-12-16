#ЕЩЕ ДОБАВИТЬ БАЗУ ДАННЫХ И БИБЛИОТЕКУ
import tkinter as tk
import openai
openai.api_key = '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'

# Инициализация окна
root = tk.Tk()
root.title("Чат")

def login():
    # Код для авторизации пользователя
    # СДЕЛАТЬ

    # Переход на страницу чата
    chat_page()

# Функция для отображения страницы чата
def chat_page():
    # Закрыть окно авторизации
    login_screen.destroy()

    # Отобразить страницу чата
    chat_window = tk.Toplevel(root)
    chat_window.title("Чат с ботом")

    # Окно чата
    chat_frame = tk.Frame(chat_window)
    chat_frame.pack(padx=10, pady=10)

    # Окно для отображения сообщений чата
    chat_display = tk.Text(chat_frame, height=20, width=50)
    chat_display.pack()

    # Окно для ввода сообщений
    input_frame = tk.Frame(chat_window)
    input_frame.pack(padx=10, pady=10)

    entry_field = tk.Entry(input_frame, width=40)
    entry_field.pack(side=tk.LEFT)

    # Функция для отправки сообщения
    def send_message():
        message = entry_field.get()
        prompt_text = "User: " + message + "\nAI:"
        response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo-1106",
        max_tokens=100,
        messages = [
            {"role": "user", "content": prompt_text}
        ]
        )
    
        # Получение ответа и отображение сообщения
        chat_display.insert(tk.END, "User: " + message + '\n')
        chat_display.insert(tk.END, "AI: " + response.choices[0].message.content + '\n')
    
    entry_field.delete(0, tk.END)
    # Кнопка для отправки сообщения
    send_button = tk.Button(input_frame, text="Send", command=send_message)
    send_button.pack(side=tk.RIGHT)

login_screen = tk.Frame(root)
login_screen.pack()

nickname_label = tk.Label(login_screen, text="Nickname:")
nickname_label.pack()

nickname_entry = tk.Entry(login_screen)
nickname_entry.pack()

password_label = tk.Label(login_screen, text="Password:")
password_label.pack()

password_entry = tk.Entry(login_screen, show="*")
password_entry.pack()

login_button = tk.Button(login_screen, text="Login", command=login)
login_button.pack()

register_button = tk.Button(login_screen, text="Register")
register_button.pack()

root.mainloop()