import sqlite3
from sqlite3 import Error
import pandas as pd
import numpy as np
from pandastable import Table
import customtkinter
from pathlib import Path

class App(customtkinter.CTk):
    """
    Description: Main App Window Class
    """
    def __init__(self):
        super().__init__()
        df = load_df_objects(1)
        self.title(f"Collectio version {APP_VERSION}")
        self.geometry("1800x800")
        self.resizable(False,False)
        self.iconbitmap(APP_ICO)
        #self.table = Table(self.frame, dataframe=df,showtoolbar=False,showstatusbar=True)
        #self.table.show()

def init_db():
    """
    Description: Sqlite DB initialisation
    """
    conn = None
    try:
        with open(APP_INIT_SQL,'r') as sql_file:
            sql = sql_file.read()
        conn = sqlite3.connect(APP_DATABASE)
        cur = conn.cursor()
        cur.executescript(sql)
        conn.commit()
    except Error as e:
        print(f"> {CRED}Error init_db - {e}{CEND}")
    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()

def get_categories():
    """
    Description: Get Objects Categories (ex: Video Games, Books, ...)
    """
    conn = None
    try:
        conn = sqlite3.connect(APP_DATABASE)
        cur = conn.cursor()
        cur.execute("""SELECT id, label FROM categories;""")
        records = cur.fetchall()
        list_categories_name = []
        list_categories = []
        for row in records:
            list_categories.append(row[0])
            list_categories_name.append(row[1])
    except Error as e:
        print(f"> {CRED}Error get_categories - {e}{CEND}")
    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()    
        return dict(zip(list_categories,list_categories_name))
    
def get_category_properties(category: int):
    """
    Description: Get Objects Categories (ex: Video Games, Books, ...)
    Arguments:
        - category (integer)
    """
    conn = None
    try:
        conn = sqlite3.connect(APP_DATABASE)
        cur = conn.cursor()
        cur.execute(f"""SELECT properties_template FROM categories WHERE id={category};""")
        records = cur.fetchall()
        for row in records:
            list_properties = row[0].split(',')
    except Error as e:
        print(f"> {CRED}Error get_category_properties - {e}{CEND}")
    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()    
        return list_properties

def add_obj(category: int, properties: list):
    """
    Description: Add Object
    Arguments:
        - category (integer)
        - properties (list with field names)
    """
    conn = None
    try:
        conn = sqlite3.connect(APP_DATABASE)
        cur = conn.cursor()
        cur.execute(f"""INSERT INTO objects ( category_id, properties) VALUES ({category},"{str(properties)[1:-1]}");""")
        conn.commit()
    except Error as e:
        print(f"> {CRED}Error add_obj - {e}{CEND}")
    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()

def get_obj(obj_id: int):
    """
    Description: Get Object
    Arguments:
        - category (integer)
    """
    conn = None
    try:
        conn = sqlite3.connect(APP_DATABASE)
        cur = conn.cursor()
        cur.execute(f"""SELECT * FROM objects WHERE id={obj_id};""")
        records = cur.fetchall()
        for row in records:
            properties_var = row[2]
        return eval("[" + properties_var + "]")
    except Error as e:
        print(f"> {CRED}Error get_obj - {e}{CEND}")
    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()

def import_csv(category: int, filename: str):
    """
    Description: Import CSV File in Objects table
    Arguments:
        - category (integer)
        - filename (string)
    """
    conn = None
    try:
        conn = sqlite3.connect(APP_DATABASE)
        cur = conn.cursor()
        with open(filename,  encoding="utf8", errors='ignore') as file:
            linenb=0
            for line in file:
                linenb=linenb+1
                if linenb>1:
                    cur.execute(f"""INSERT INTO objects (category_id, properties) VALUES ({category},"{line.strip()}");""")
                    conn.commit()
    except Error as e:
        print(f"> {CRED}Error import_csv - {e}{CEND}")
    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()
    return linenb

def load_df_objects(category: int):
    """
    Description: Load all objects in dataframe (filter with category id)
    Arguments:
        - category (integer)
    """
    conn = None
    try:
        #get properties's names
        fields_list = get_category_properties(category)
        #get objects
        conn = sqlite3.connect(APP_DATABASE)
        df = pd.read_sql_query(f"""SELECT * FROM objects WHERE category_id={category};""", conn)
        #transform properties to fields
        df[fields_list] = df["properties"].str.split(",", expand = True)
        #remove properties column
        df.drop(["properties"],axis=1,inplace=True)
    except Error as e:
        print(f"> {CRED}Error load_df_objects - {e}{CEND}")
    finally:
        if conn:
            conn.close()    
        return df

if __name__ == "__main__":
    """
    Description: Main routine
    """
    APP_PATH=Path(__file__).parent
    APP_VERSION="alpha 0.1"
    APP_DATABASE=APP_PATH / "data/db/data.db"
    APP_INIT_SQL=APP_PATH / "data/sql/init_db.sql"
    APP_ICO=APP_PATH / "data/assets/collectio.ico"
    CRED = "\033[91m"
    CGREEN = "\033[92m"
    CBLUE = "\033[94m"
    CYELLOW = "\033[93m"
    CEND = "\033[0m"
    print(f"> {CGREEN}run{CEND} collectio version {CYELLOW}{APP_VERSION}{CEND}")
    print(f"> {CGREEN}init database{CEND} ({APP_DATABASE})")
    init_db()
    #print(f"> {CGREEN}Import {import_csv(1,"C:\\Users\\Raging\\python.vscode\\inventaire.csv")} objects from inventaire.csv file{CEND}")
    print(f"> {CGREEN}launch main windows{CEND}")
    app = App()
    app.mainloop()
    print(f"> {CGREEN}exit main windows{CEND}")
