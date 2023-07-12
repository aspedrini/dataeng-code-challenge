import pandas as pd
from datetime import datetime
import os
from sqlalchemy import create_engine
import glob

directory_paths = {
    "csv": r".\data\csv",
    "postgres": r".\data\postgres"}

db = {"database": "db",
      "host": "localhost",
      "port": 3306,
      "user": "augusto",
      "password": "123456",
      }


class SendFilesToMySQL:

    target_date = None

    def __init__(self):
        if SendFilesToMySQL.target_date is None:
            SendFilesToMySQL.target_date = self.date_func()

    @staticmethod
    def date_func():
        """
        Determines if user wants to use today's date or a custom date.
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
            print("Incorrect values. Please try again")


    def folder_check_postgres(self, postgres_path):
        """
        Checks if exists folders in local storage named as the input date for all PSQL extracted tables
        """
        results_postgres = []
        for folder in os.listdir(postgres_path):
            if os.path.isdir(os.path.join(postgres_path, folder)):
                if self.target_date in os.listdir(os.path.join(postgres_path, folder)):
                    results_postgres.append(True)
                else:
                    results_postgres.append(False)
        return results_postgres


    def folder_check_csv(self, csv_path):
        """
        Checks if exists folders in local storage as the input date for the order_details table
        """
        results_ord_details = []
        if self.target_date in os.listdir(csv_path):
            results_ord_details.append(True)
        else:
            results_ord_details.append(False)
        return results_ord_details


    def folder_check_date(self):
        """
        Checks if exists target folder name in the two locations. If one of them is False, the proccess will be aborted so the DB won't have incomplete data uploaded.
        """
        results_postgre = self.folder_check_postgres(postgres_path=directory_paths["postgres"])
        results_ord_details = self.folder_check_csv(csv_path=directory_paths["csv"])
        if all(results_postgre) and all(results_ord_details):
            return True
        else:
            return False


    def get_files_in_folders(self, path):
        """
        Extracts the full path to all files so they can served as a parameter to pandas open the files.
        """
        date_check = self.folder_check_date()
        files = []
        if date_check is True:
            matching_paths = glob.glob(os.path.join(path, '**', self.target_date), recursive=True)
            for value in matching_paths:
                sub_paths = glob.glob(os.path.join(value, '*.csv'))
                files.extend(sub_paths)
            return files
        else:
            raise ValueError("No files found for that date")


    def send_to_mysql(self, path):
        """
        Send the tables from local storage to a target database.
        """
        files_from_csv = self.get_files_in_folders(directory_paths["csv"])
        files_from_postgres = self.get_files_in_folders(directory_paths["postgres"])
        full_path_list = files_from_csv + files_from_postgres
        try:
            for value in full_path_list:
                filenames = os.path.basename(value).split('.', 1)[0]
                df = pd.read_csv(value)
                df["extracted_at"] = self.target_date
                with engine.connect() as conn:
                    df.to_sql(name=filenames, con=conn, if_exists="append", index=False, method="multi", chunksize=1000)
            return "Upload successfully"
        except:
            return "Error uploading files" 


if __name__ == "__main__":

    engine = create_engine(f"mysql+mysqlconnector://{db['user']}:{db['password']}@{db['host']}/{db['database']}")
    instance = SendFilesToMySQL()
    run = instance.send_to_mysql(directory_paths)
    print(run)
    engine.dispose()
