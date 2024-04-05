import tkinter as tk
from CV_timer import score  # Импортируем переменную score из модуля CV_timer
import subprocess

leaderboard = {}  # Словарь для хранения результатов игроков (никнейм: счёт)


def leaders():
    # Функция для отображения таблицы лидеров
    leaders_window = tk.Toplevel(root)  # Открываем дочернее окно
    leaders_window.title("Таблица лидеров")  # Заголовок окна
    sorted_leaderboard = sorted(leaderboard.items(), key=lambda x: x[1], reverse=True)  # Сортируем результаты
    for i, (name, score1) in enumerate(sorted_leaderboard):
        tk.Label(leaders_window, text=f"#{i + 1}: {name} - {score1}").pack()  # Отображаем результаты в окне


def play():
    # Функция для начала игры
    player_name_window = tk.Toplevel(root)  # Открываем окно для ввода ника игрока
    player_name_window.title("Введите ваш игровой ник")
    player_name_window.geometry("200x200")
    tk.Label(player_name_window, text="Введите ваш игровой ник:").pack()
    entry_player_name = tk.Entry(player_name_window)
    entry_player_name.pack()

    def start_game():
        # Функция для запуска игры
        player_name = entry_player_name.get()  # Получаем ник игрока
        player_name_window.destroy()  # Закрываем окно ввода ника
        subprocess.Popen(["python", "D:/ДЗ/9 класс/IT/ТАУ/NTO FINAL/munktest (3).py", player_name])  # Запускаем игру

        save_score(player_name, score)  # Сохраняем результат игрока

    btn_start_game = tk.Button(player_name_window, text="Начать игру", command=start_game)
    btn_start_game.pack()


def save_score(player_name, score):
    # Функция для сохранения результата игрока
    leaderboard[player_name] = score  # Добавляем результат игрока в словарь leaderboard
    with open("leaderboard.txt", "a") as file:  # Открываем файл для сохранения результатов
        file.write(f"{player_name}: {score}\n")  # Записываем результат игрока в файл


def exit_app():
    root.quit()


root = tk.Tk()  # Создаём основное окно

root.geometry("600x360")
root.title("CUBITO")  # Устанавливаем заголовок окна

btn_menu = tk.Button(root, text="Таблица лидеров", width=50, height=5, command=leaders)
btn_menu.pack(pady=20)  # Кнопка для открытия таблицы лидеров

btn_play = tk.Button(root, text="Играть", width=50, height=5, command=play)
btn_play.pack(pady=10)  # Кнопка для начала игры

btn_settings = tk.Button(root, text="Выйти", width=50, height=5, command=exit_app)
btn_settings.pack(pady=10)  # Кнопка для выхода из приложения

root.mainloop()  # Запуск главного цикла обработки событий
