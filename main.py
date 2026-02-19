from modules import app_obj
from modules.window import MainWindow

def main():
    # try:
        main_window = MainWindow (1920, 1080)
        main_window.show()
        app_obj.exec()
    # except Exception as error:
        # print(f"Помилка під час запуску проєкту: ")


if __name__ == "__main__":
    main()
