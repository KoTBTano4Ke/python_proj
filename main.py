import tkinter as tk
import openai
from sqlalchemy import create_engine, Column, String, Integer
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import socket

api_doc_name = 'api_key.txt'
with open(api_doc_name, 'r', encoding='utf-8') as file:
    apikey = file.read()
openai.api_key = apikey

Base = declarative_base()

# Определение модели пользователя
class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    login = Column(String)
    password = Column(String)
    email = Column(String)

# Создание соединения с базой данных и сессии
engine = create_engine('sqlite:///users.db', echo=True)
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()

# Функция для регистрации нового пользователя
def register():
    def save_user_info():
        new_login = new_nickname_entry.get()
        new_password = new_password_entry.get()
        new_email = new_email_entry.get()

        # Сохранение нового пользователя в базу данных
        new_user = User(login=new_login, password=new_password, email=new_email)
        session.add(new_user)
        session.commit()

        print("New login:", new_login)
        print("New password:", new_password)
        print("New mail:", new_email)

        register_screen.destroy()

    register_screen = tk.Toplevel(root)
    register_screen.title("Registration")

    new_nickname_label = tk.Label(register_screen, text="New login:")
    new_nickname_label.pack()

    new_nickname_entry = tk.Entry(register_screen)
    new_nickname_entry.pack()

    new_password_label = tk.Label(register_screen, text="New password:")
    new_password_label.pack()

    new_password_entry = tk.Entry(register_screen, show="*")
    new_password_entry.pack()

    new_email_label = tk.Label(register_screen, text="New mail:")
    new_email_label.pack()

    new_email_entry = tk.Entry(register_screen)
    new_email_entry.pack()

    save_button = tk.Button(register_screen, text="Save", command=save_user_info)
    save_button.pack()

def login():
    entered_login = nickname_entry.get()
    entered_password = password_entry.get()

    # Проверка введенного логина и пароля в базе данных
    user = session.query(User).filter_by(login=entered_login, password=entered_password).first()

    if user:
        print("Successful authorization:", user)
        root.withdraw()
        chat_page()
    else:
        show_error_mess()


def show_error_mess():
    error_screen = tk.Toplevel(root)
    error_screen.title("Error")
    
    error_label = tk.Label(error_screen, text="Wrong login or password")
    error_label.pack()

    ok_button = tk.Button(error_screen, text="OK", command=error_screen.destroy)
    ok_button.pack()

# Функция для отображения страницы чата
def chat_page():
    # Закрыть окно авторизации
    root.withdraw()

    # Отобразить страницу чата
    chat_window = tk.Toplevel(root)
    chat_window.title("Chat with bot")
    
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
        entry_field.delete(0, tk.END)
        # Получение ответа и отображение сообщения
        chat_display.insert(tk.END, "User: " + message + '\n')
        chat_display.insert(tk.END, "AI: " + response.choices[0].message.content + '\n')
    
    
    # Кнопка для отправки сообщения
    send_button = tk.Button(input_frame, text="Send", command=send_message)
    send_button.pack(side=tk.RIGHT)

root = tk.Tk()
root.title("Authorization")

nickname_label = tk.Label(root, text="Login:")
nickname_label.pack()

nickname_entry = tk.Entry(root)
nickname_entry.pack()

password_label = tk.Label(root, text="Password:")
password_label.pack()

password_entry = tk.Entry(root, show="*")
password_entry.pack()

login_button = tk.Button(root, text="Enter", command=login)
login_button.pack()

register_button = tk.Button(root, text="Registration", command=register)
register_button.pack()

def on_closing():
    session.close() 
    root.destroy()

root.protocol("WM_DELETE_WINDOW", on_closing)

root.mainloop()