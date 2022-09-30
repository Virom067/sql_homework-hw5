import psycopg2
import random

from functools import partial
from config import user, password, host, port, database, customer_table
from customer_generate import custumer_generate
from phone_generate import gen_phone_numb



class CreateDB:

    def __init__(self):
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.port = port

    def open_connect_db(self):
        try:
            self.connection = psycopg2.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database,
                port=self.port
            )
            self.cursor = self.connection.cursor()
            print("[INFO] PostrgeSQL successful connection")
            return self.cursor

        except Exception as _ex:
            print("[INFO] Error while working with PostgeSQL", _ex)

    def close_connect_db(self):
        if self.connection:
            self.connection.close()
            print("[INFO] PostrgeSQL connection closed")

    def create_table(self):
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS %(customer_table)s(
        %(customer_table)s_id INTEGER NOT NULL GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
        first_name VARCHAR(50) NOT NULL,
        last_name VARCHAR(50) NOT NULL,
        email VARCHAR(60) NOT NULL
        );
        """ % {'customer_table': customer_table})
        self.connection.commit()

        # self.cursor.execute("""
        # CREATE DOMAIN rus_pnone_number AS VARCHAR(20)
        # CHECK(VALUE ~ '^((8|\+7)[\- ]?)?(\(?\d{3}\)?[\- ]?)?[\d\- ]{7,10}$'
        # );
        # """)
        # self.connection.commit()

        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS phone_numbers(
        phone_number_id INTEGER NOT NULL GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
        phone_number rus_pnone_number,
        %(customer_table)s_id INTEGER NOT NULL REFERENCES %(customer_table)s(%(customer_table)s_id)
        );
        """ % {'customer_table': customer_table})
        self.connection.commit()


class DatabaseTask:

    def __init__(self):
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.port = port

    def open_connect_db(self):
        try:
            self.connection = psycopg2.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database,
                port=self.port
            )
            self.cursor = self.connection.cursor()
            print("[INFO] PostrgeSQL successful connection")
            return self.cursor

        except Exception as _ex:
            print("[INFO] Error while working with PostgeSQL", _ex)

    def close_connect_db(self):
        if self.connection:
            self.connection.close()
            print("[INFO] PostrgeSQL connection closed")

    def add_client(self):
        customer = custumer_generate()
        first_name = customer[0]
        last_name = customer[1]
        phone_number = gen_phone_numb()
        email = f'{first_name}_{last_name}@gmail.com'
        a = partial(random.randint, 0, 1)
        self.cursor.execute("""
        INSERT INTO %(customer_table)s (first_name, last_name, email)
        VALUES ('%(first_name)s', '%(last_name)s', '%(email)s'
        );
        """ % {'customer_table': customer_table,
               'first_name': first_name,
               'last_name': last_name,
               'email': email})
        self.connection.commit()
        print(f"Добавлен новый клиент --> {first_name} {last_name}    {email}")


        if a():
            self.cursor.execute("""
                                SELECT customer_table_id FROM customer_table WHERE email='%(email)s';
                                """ % {'email': email})
            custumer_id = self.cursor.fetchall()
            for id in custumer_id:
                self.cursor.execute("""
                                    INSERT INTO phone_numbers (customer_table_id, phone_number)
                                    VALUES ('%(id)s', '%(phone_number)s');
                                    """ % {'id': id[0],
                                           'phone_number': phone_number})
                print(f"Номер {phone_number} добавлен клиенту {first_name} {last_name}")
                self.connection.commit()
        else:
            print('Клиент номер не указал')

    def add_phone(self, email):
        phone_number = gen_phone_numb()
        custumer_id = self.find_client(email)
        for id in custumer_id:
            self.cursor.execute("""
                                SELECT first_name, last_name FROM customer_table WHERE customer_table_id=%(id)s;
                                """ % {'id': id[0]})
            customer = self.cursor.fetchall()[0]
            first_name = customer[0]
            last_name = customer[1]
            self.cursor.execute("""
                                INSERT INTO phone_numbers (customer_table_id, phone_number)
                                VALUES ('%(id)s', '%(phone_number)s');
                                """ % {'id': id[0],
                                       'phone_number': phone_number})
            print(f"Номер {phone_number} добавлен клиенту {first_name} {last_name}")
            self.connection.commit()

    def find_client(self, email):
        self.cursor.execute("""
                            SELECT customer_table_id FROM customer_table WHERE email='%(email)s';
                            """ % {'email': email})
        custumer_id = self.cursor.fetchall()
        print(f"ID клиента: {custumer_id[0][0]}")
        return custumer_id

    def delete_phone(self, email):
        custumer_id = self.find_client(email)
        self.cursor.execute("""
                            SELECT phone_number FROM phone_numbers WHERE customer_table_id='%(custumer_id)s';
                            """ % {'custumer_id': custumer_id[0][0]})
        phone_bumbers = self.cursor.fetchall()
        if len(phone_bumbers) > 0:
            print(f"У данного клиента есть следующие номера:\n{phone_bumbers}")
            delete_phone_numb = input('Укажите номер телефона для удаления: ')
            self.cursor.execute("""
                                DELETE FROM phone_numbers 
                                WHERE customer_table_id=%(custumer_id)s 
                                AND phone_number='%(delete_phone_numb)s';
                                """ % {'custumer_id': custumer_id[0][0],
                                       'delete_phone_numb': delete_phone_numb})
            self.connection.commit()
            print('Номер удален')
        else:
            print("У данного клиента нет ни одного номера")

    def delete_client(self, email):
        custumer_id = self.find_client(email)
        self.cursor.execute("""
                            DELETE FROM phone_numbers WHERE customer_table_id='%(custumer_id)s';
                            """ % {'custumer_id': custumer_id[0][0]})
        self.connection.commit()
        self.cursor.execute("""
                            DELETE FROM customer_table WHERE customer_table_id='%(custumer_id)s';
                            """ % {'custumer_id': custumer_id[0][0]})
        self.connection.commit()
        print('Клиент удален')

    def change_client(self, email):
        custumer_id = self.find_client(email)
        for id in custumer_id:
            self.cursor.execute("""
                                SELECT first_name, last_name FROM customer_table 
                                WHERE customer_table_id=%(id)s;
                                """ % {'id': id[0]})
            customer = self.cursor.fetchall()[0]
            first_name = customer[0]
            self.cursor.execute("""
                                UPDATE customer_table SET first_name='%(first_name)s' 
                                WHERE customer_table_id='%(custumer_id)s';
                                """ % {'custumer_id': custumer_id[0][0],
                                       'first_name': first_name+'_new'})
            self.connection.commit()
            print('Имя клиента изменено')



if __name__ == "__main__":
    pass
