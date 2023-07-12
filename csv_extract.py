import pandas as pd
import os
from datetime import datetime

directory_paths = {
    "csv": r".\data\csv",
    "postgres": r".\data\postgres"}

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


class CsvHandler:
    def __init__(self, tb_name):
        self.tb_name = tb_name
        self.base_path = directory_paths["csv"]
        self.date_str = date_func()

    def csv_path_creator(self):
        """
        Create path for extracted order_details.csv based on input date.
        """
        create_path = os.path.join(self.base_path, self.date_str)
        try:
            if not os.path.exists(create_path):
                os.makedirs(create_path, exist_ok=True)
            return create_path
        except:
            return "Impossible to create path"
    

    def csv_extraction(self):
        """
        Reads order_details.csv from the source csv.
        """
        csv_path = os.path.join(self.base_path, self.tb_name)
        try:
            base_csv = pd.read_csv(filepath_or_buffer=csv_path)
            return base_csv
        except:
            return f"Could not read {self.tb_name} from source folder"
    

    def store_csv(self):
        """
        Save extracted csv to local storage.
        """
        base_csv = self.csv_extraction()
        folder_creation = self.csv_path_creator()
        try:
            base_csv.to_csv(path_or_buf=os.path.join(folder_creation, self.tb_name), index=False)
            return "CSV saved successfully to local storage"
        except:
            return "Could not save .csv file"


if __name__ == "__main__":

    handler = CsvHandler(tb_name="order_details.csv")
    extract = handler.store_csv()
    print(extract)