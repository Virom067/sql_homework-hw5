import psycopg2
import random

from functools import partial
from config import user, password, host, port, database, customer_table
from customer_generate import custumer_generate
from phone_generate import gen_phone_numb


class CreateDB:

    def __init__(self):
        self.conn = psycopg2.connect(host=host, user=user, password=password, database=database, port=port)

    def create_table(self):
        with self.conn.cursor() as cur:
            cur.execute("""
            CREATE TABLE IF NOT EXISTS %(customer_table)s(
            %(customer_table)s_id INTEGER NOT NULL GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
            first_name VARCHAR(50) NOT NULL,
            last_name VARCHAR(50) NOT NULL,
            email VARCHAR(60) NOT NULL
            );
            """ % {'customer_table': customer_table})
            self.conn.commit()

            cur.execute("""
            CREATE DOMAIN rus_pnone_number AS VARCHAR(20)
            CHECK(VALUE ~ '^((8|\+7)[\- ]?)?(\(?\d{3}\)?[\- ]?)?[\d\- ]{7,10}$'
            );
            """)
            self.conn.commit()

            cur.execute("""
            CREATE TABLE IF NOT EXISTS phone_numbers(
            phone_number_id INTEGER NOT NULL GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
            phone_number rus_pnone_number,
            %(customer_table)s_id INTEGER NOT NULL REFERENCES %(customer_table)s(%(customer_table)s_id)
            );
            """ % {'customer_table': customer_table})
            self.conn.commit()


class DatabaseTask:

    def __init__(self):
        self.conn = psycopg2.connect(host=host, user=user, password=password, database=database, port=port)

    def add_client(self):
        customer = custumer_generate()
        first_name = customer[0]
        last_name = customer[1]
        phone_number = gen_phone_numb()
        email = f'{first_name}_{last_name}@gmail.com'
        a = partial(random.randint, 0, 1)
        with self.conn.cursor() as cur:
            cur.execute("""
            INSERT INTO %(customer_table)s (first_name, last_name, email)
            VALUES ('%(first_name)s', '%(last_name)s', '%(email)s'
            );
            """ % {'customer_table': customer_table,
                   'first_name': first_name,
                   'last_name': last_name,
                   'email': email})
            self.conn.commit()
            print(f"Добавлен новый клиент --> {first_name} {last_name}    {email}")

            if a():
                cur.execute("""
                SELECT customer_table_id FROM customer_table WHERE email='%(email)s';
                """ % {'email': email})
                custumer_id = cur.fetchall()
                for id in custumer_id:
                    cur.execute("""
                    INSERT INTO phone_numbers (customer_table_id, phone_number)
                    VALUES ('%(id)s', '%(phone_number)s');
                    """ % {'id': id[0],
                           'phone_number': phone_number})
                    print(f"Номер {phone_number} добавлен клиенту {first_name} {last_name}")
                    self.conn.commit()
            else:
                print('Клиент номер не указал')

    def add_phone(self, email):
        phone_number = gen_phone_numb()
        customer_id = self.find_client(email)
        for id in customer_id:
            with self.conn.cursor() as cur:
                cur.execute("""
                SELECT first_name, last_name FROM customer_table WHERE customer_table_id=%(id)s;
                """ % {'id': id[0]})
                customer = cur.fetchall()[0]
                first_name = customer[0]
                last_name = customer[1]
                cur.execute("""
                INSERT INTO phone_numbers (customer_table_id, phone_number)
                VALUES ('%(id)s', '%(phone_number)s');
                """ % {'id': id[0],
                       'phone_number': phone_number})
                print(f"Номер {phone_number} добавлен клиенту {first_name} {last_name}")
                self.conn.commit()

    def find_client(self, last_name):
        with self.conn.cursor() as cur:
            cur.execute("""
            SELECT customer_table_id 
            FROM customer_table 
            WHERE last_name LIKE '%%%(last_name)s%%'';
            """ % {'last_name': last_name})
            customer_id = cur.fetchall()
            print(f"ID клиента: {customer_id[0][0]}")
            return customer_id

    def delete_phone(self, email):
        customer_id = self.find_client(email)
        with self.conn.cursor() as cur:
            cur.execute("""
            SELECT phone_number FROM phone_numbers WHERE customer_table_id='%(customer_id)s';
            """ % {'customer_id': customer_id[0][0]})
            phone_numbers = cur.fetchall()
            if len(phone_numbers) > 0:
                print(f"У данного клиента есть следующие номера:\n{phone_numbers}")
                delete_phone_numb = input('Укажите номер телефона для удаления: ')
                cur.execute("""
                DELETE FROM phone_numbers 
                WHERE customer_table_id=%(customer_id)s 
                AND phone_number='%(delete_phone_numb)s';
                """ % {'customer_id': customer_id[0][0],
                       'delete_phone_numb': delete_phone_numb})
                self.conn.commit()
                print('Номер удален')
            else:
                print("У данного клиента нет ни одного номера")

    def delete_client(self, email):
        customer_id = self.find_client(email)
        with self.conn.cursor() as cur:
            cur.execute("""
            DELETE FROM phone_numbers WHERE customer_table_id='%(customer_id)s';
            """ % {'customer_id': customer_id[0][0]})
            self.conn.commit()
            cur.execute("""
            DELETE FROM customer_table WHERE customer_table_id='%(customer_id)s';
            """ % {'customer_id': customer_id[0][0]})
            self.conn.commit()
            print('Клиент удален')

    def change_client(self, email):
        customer_id = self.find_client(email)
        for id in customer_id:
            with self.conn.cursor() as cur:
                cur.execute("""
                SELECT first_name, last_name FROM customer_table 
                WHERE customer_table_id=%(id)s;
                """ % {'id': id[0]})
                customer = cur.fetchall()[0]
                first_name = customer[0]
                cur.execute("""
                UPDATE customer_table SET first_name='%(first_name)s' 
                WHERE customer_table_id='%(customer_id)s';
                """ % {'customer_id': customer_id[0][0],
                       'first_name': first_name + '_new'})
                self.conn.commit()
                print('Имя клиента изменено')


if __name__ == "__main__":
    pass
