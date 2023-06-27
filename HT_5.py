import psycopg2

def create_tables(cur):
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
        
def fill_client_data(cur):
        cur.execute(f"""INSERT INTO clients(first_name, last_name, email) VALUES ('{str(input("Enter first name:"))}', '{str(input("Enter last name:"))}', '{str(input("Enter the email:"))}') on conflict do nothing;""", )
        conn.commit()

def enter_client_number(cur):
        cur.execute(f"""INSERT INTO phones(phone_number, client_id) VALUES ('{str(input("Enter phone number:"))}', '{str(input("Enter client id:"))}') on conflict do nothing;""")
        conn.commit()

def change_client_data(cur):
    client_id = input("Enter client id:")
    update_query = 'UPDATE clients SET'
    first_name = input("Enter new first name (leave blank to keep existing): ")
    if first_name:
        update_query += f" first_name='{first_name}',"
    last_name = input("Enter new last name (leave blank to keep existing): ")
    if last_name:
        update_query += f" last_name='{last_name}',"
    email = input("Enter new email (leave blank to keep existing): ")
    if email:
        update_query += f" email='{email}',"
    if update_query[-1] == ',':
        update_query = update_query[:-1]
    update_query += f' WHERE id={client_id};'
    cur.execute(update_query)
    conn.commit()

def delete_phone_number(cur):
        cur.execute("""DELETE FROM phones WHERE id=%s;""", (str(input("Enter phone id:")),))
        conn.commit()

def delete_client(cur):
        new_client_id = str(input("Enter client id:"))
        cur.execute("""DELETE FROM phones WHERE client_id=%s;""", (new_client_id,))
        cur.execute("""DELETE FROM clients WHERE id=%s;""", (new_client_id,))
        conn.commit()

def find_client(cur):
        update_query = 'SELECT clients.id FROM clients '
        phone = input("Enter phone (leave blank to keep existing): ")
        if phone:
            update_query += f"JOIN phones ON phones.client_id = clients.id WHERE phone_number='{phone}' and"
        else:
            update_query += 'WHERE'
        first_name = input("Enter first name (leave blank to keep existing): ")
        if first_name:
            update_query += f" first_name='{first_name}' and"
        last_name = input("Enter last name (leave blank to keep existing): ")
        if last_name:
            update_query += f" last_name='{last_name}' and"
        email = input("Enter email (leave blank to keep existing): ")
        if email:
            update_query += f" email='{email}' and"
        if update_query[-3:] == 'and':
            update_query = update_query[:-3]
        cur.execute(update_query)
        print(cur.fetchall())
        conn.commit()
    
conn = psycopg2.connect(database='SQL_5', user='appadmin', password='jdfh8jhtghnjkfrvhyu')
with conn.cursor() as cur:
    # create_tables(cur)
    # fill_client_data(cur)
    # enter_client_number(cur)
    change_client_data(cur)
    # delete_phone_number(cur)
    # delete_client(cur)
    # find_client(cur)
conn.close()