
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
                create_db.create_table()

            elif query == "add_client":
                data_base_task.add_client()

            elif query in mail_request:
                last_name = input('Укажижете фамилию клиента: ')
                if query == "add_phone":
                    data_base_task.add_phone(last_name)

                elif query == "find_client":
                    data_base_task.find_client(last_name)

                elif query == "delete_phone":
                    data_base_task.delete_phone(last_name)

                elif query == "delete_client":
                    data_base_task.delete_client(last_name)

                elif query == "change_client":
                    data_base_task.change_client(last_name)

    except Exception as _ex:
        print("[INFO] Error while working with task", _ex)


if __name__ == "__main__":
    task(commands)


