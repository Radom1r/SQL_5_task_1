import psycopg2

with psycopg2.connect(database='SQL_5', user='appadmin', password='jdfh8jhtghnjkfrvhyu') as conn:
    def create_tables():
        with conn.cursor() as cur:
            cur.execute("""
            create table if not exists clients(
                id SERIAL primary key,
                first_name VARCHAR(100) not null,
                last_name VARCHAR(100) not null,
                email VARCHAR(100) unique not null
            );
            """)

            cur.execute("""CREATE unique INDEX IF NOT EXISTS unique_email on clients (email);""")

            cur.execute("""create table if not exists phones(
                id SERIAL primary key,
                phone_number VARCHAR(15),
                client_id int references clients(id)
            );""")
        
            cur.execute("""CREATE unique INDEX IF NOT EXISTS unique_phone_number on phones (phone_number);""")
            conn.commit()
        
    def fill_client_data():
        with conn.cursor() as cur:
            cur.execute(f"""INSERT INTO clients(first_name, last_name, email) VALUES ('{str(input("Enter first name:"))}', '{str(input("Enter last name:"))}', '{str(input("Enter the email:"))}') on conflict do nothing;""", )
            conn.commit()

    def enter_client_number():
        with conn.cursor() as cur:    
            cur.execute(f"""INSERT INTO phones(phone_number, client_id) VALUES ('{str(input("Enter phone number:"))}', '{str(input("Enter client id:"))}') on conflict do nothing;""")
            conn.commit()
    def change_client_data():
        with conn.cursor() as cur: 
            cur.execute("""UPDATE clients SET first_name=%s, last_name =%s, email=%s WHERE id=%s;""", (str(input("Enter new first name:")), str(input("Enter new second name:")), str(input("Enter new email:")), str(input("Enter client id:"))))
            conn.commit()
    def delete_phone_number():
        with conn.cursor() as cur:
            cur.execute("""DELETE FROM phones WHERE id=%s;""", (str(input("Enter phone id:")),))
            conn.commit()

    def delete_client():
        new_client_id = str(input("Enter client id:"))
        with conn.cursor() as cur:
            cur.execute("""DELETE FROM phones WHERE client_id=%s;""", (new_client_id,))
            cur.execute("""DELETE FROM clients WHERE id=%s;""", (new_client_id,))
            conn.commit()

    def find_client():
        with conn.cursor() as cur:
            query = str(input("Type '1' to use email, type '2' to use phone number: "))
            if query == '1':
                cur.execute("""select id from clients where email = %s;""", (str(input("Enter email address:")), ))
                print(cur.fetchall()[0][0])
            elif query == '2':
                cur.execute("""select client_id from phones where phone_number = %s;""", (str(input("Enter phone number:")), ))
                print(cur.fetchall()[0][0])
            conn.commit()
create_tables()
fill_client_data()
enter_client_number()
change_client_data()
delete_phone_number()
delete_client()
find_client()