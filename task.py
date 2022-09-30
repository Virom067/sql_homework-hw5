
from commands import commands
from database_query import CreateDB, DatabaseTask


def task(commands):
    try:
        create_db = CreateDB()
        data_base_task = DatabaseTask()
        mail_request = ["add_phone", "find_client", "delete_phone", "delete_client", "change_client"]
        cycle = True
        while cycle:
            query = input('\nВывести список возможных команд введите "help"\nВведите команду: ')
            if query == "help":
                for command, info in commands.items():
                    print(f'{command} - {info}')
            elif query == "stop":
                cycle = False
                print("[INFO] Программа остановлена")

            elif query == "create_table":
                create_db.open_connect_db()
                create_db.create_table()
                create_db.close_connect_db()

            elif query == "add_client":
                data_base_task.open_connect_db()
                data_base_task.add_client()
                data_base_task.close_connect_db()

            elif query in mail_request:
                email = input('Укажижете email клиента: ')
                if query == "add_phone":
                    data_base_task.open_connect_db()
                    data_base_task.add_phone(email)
                    data_base_task.close_connect_db()

                elif query == "find_client":
                    data_base_task.open_connect_db()
                    data_base_task.find_client(email)
                    data_base_task.close_connect_db()

                elif query == "delete_phone":
                    data_base_task.open_connect_db()
                    data_base_task.delete_phone(email)
                    data_base_task.close_connect_db()

                elif query == "delete_client":
                    data_base_task.open_connect_db()
                    data_base_task.delete_client(email)
                    data_base_task.close_connect_db()

                elif query == "change_client":
                    data_base_task.open_connect_db()
                    data_base_task.change_client(email)
                    data_base_task.close_connect_db()

    except Exception as _ex:
        print("[INFO] Error while working with task", _ex)


if __name__ == "__main__":
    task(commands)


