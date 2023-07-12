import pandas as pd
import psycopg2
from sqlalchemy import create_engine, text
from datetime import datetime
import os

directory_paths = {
    "csv": r".\data\csv",
    "postgres": r".\data\postgres"}

db = {"database": "northwind",
      "host": "localhost",
      "port": 5432,
      "user": "northwind_user",
      "password": "thewindisblowing",
      }

def date_func():
    """
    Determines target date for database extraction based on user input.
    """
    print("Select an option: 1 - current date OR 2 - type target date.")
    option = input("1 / 2: ")
    if int(option) == 1:
        date_str = str(datetime.now().year) + "-" + str(datetime.now().month).zfill(2) + "-" + str(datetime.now().day).zfill(2)
        return date_str

    elif int(option) == 2:
        input_date = input("Type in your date (YYYY-MM-DD): ")
        try:
            date_str = datetime.strptime(input_date, "%Y-%m-%d").strftime("%Y-%m-%d")
            return date_str
        except ValueError:
            print("Incorrect values to format as date. Please try again.")
    
    else:
        print("Incorret values. Please try again")


def list_all_tables():
    db_tables = []

    query_all_tables = """
            SELECT table_name FROM information_schema.tables
            WHERE table_schema = 'public' AND table_type = 'BASE TABLE'
            """
    
    with engine.connect() as connection:
            try:
                    exec = connection.execute(text(query_all_tables))
                    for result in exec:
                            db_tables.append(result[0])
                    return db_tables
            except:
                    return "Query step failed"      


def path_creator(base_path, table, date_str):
    """ 
    Creates the folders to store .csv files separated by table and date

    Args:
    base_path (dict): The base path located in dict "path"
    table (str): Str representing the target table
    date_str (str): Str representing the date of extraction
    """
    create_path = os.path.join(base_path, table, date_str)
    try:
        if not os.path.exists(create_path):
            os.makedirs(create_path, exist_ok=True)
        return create_path
    except:
        return "Impossible to create path"
    

def extract_sql_csv():
    """ 
    Extracts respectives .csv files from the first SQL database to folders separated by table and date  
    """
    selected_date = date_func()

    with engine.connect() as connection:
        
        table_list = list_all_tables()
        try:
            for table in table_list:
                folder_creation = path_creator(base_path=directory_paths["postgres"], table=table, date_str=selected_date)
                query = f"select * from {table}"
                df = pd.read_sql_query(query, connection)
                df.to_csv(path_or_buf = folder_creation + f"/{table}.csv", index=False)
            return "Tables from PSQL saved successfully to local storage."
        except:
             return "Could not save tables to local storage."  

if __name__ == "__main__":
    
    engine = create_engine(f"postgresql+psycopg2://{db['user']}:{db['password']}@{db['host']}:{db['port']}/{db['database']}")
    extract = extract_sql_csv()
    print(extract)
    engine.dispose()
