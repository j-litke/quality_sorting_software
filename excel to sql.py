# DONE importar data de ultimo excel a mysql database. 
# DONE armar tablas en sql segun los excels generados aca (no en el script)
# DONE revisar si hay nuevos defectos -> agregar columna
# DONE subida de data para tablas de totales y downtime
# antes de subir a sql, debe revisar que no exista ya esa data. para eso, hay que agregar primary keys al hacer la transformacion

import mysql.connector
from mysql.connector import Error
import pandas as pd
import numpy as np


# defect_csv = 'defect_list.csv'
# df = pd.read_csv(defect_csv)
# defect_list = df.iloc[:,1].tolist()

# create df from the three excel files
excel_files = ['transformed_data.xlsx','total_checked.xlsx','downtime.xlsx']
table_names = ['paint_defects','paint_totals','downtime']
df_index = [f'df_{i}' for i in enumerate(excel_files)]
dfs = [] # list of dataframes
for df,file in zip(df_index,excel_files):
    df = pd.read_excel(file)
    df.fillna(0,inplace=True)
    dfs.append(df)

print(dfs)
print(dfs[0])

def import_to_sql(df,table_name):
    #checks for new columns in df, adds to database, and imports data to mysql
    
    # Get existing columns in the table 
    cursor.execute(f"SELECT * FROM {table_name} LIMIT 0")
    existing_columns = [desc[0] for desc in cursor.description]

    # Get new columns in the DataFrame
    new_columns = [col for col in df.columns if col not in existing_columns]

    # If there are new columns, alter the table to add them
    if new_columns:
        for column in new_columns:
            cursor.execute(f"ALTER TABLE {table_name} ADD COLUMN {column} int") 
    
    # Import data into the table
    for _, row in df.iterrows():
        # Create INSERT statement dynamically
        sql = f"INSERT INTO {table_name} ({', '.join(df.columns)}) VALUES ({', '.join(['%s'] * len(df.columns))})"
        values = tuple(row)
        cursor.execute(sql, values)  
        
    # Commit changes and close connection
    cnx.commit() 

try:
    cnx = mysql.connector.connect(  host='localhost',
                                    database='fng',
                                    user='root',
                                    password='PassWord123')
    if cnx.is_connected():
        cursor = cnx.cursor(buffered=True)
        for df,table_name in zip(dfs,table_names):
            import_to_sql(df,table_name)
            
except Error as e:
    print("Error while connecting to MySQL", e)
finally:
    if cnx.is_connected():
        cursor.close()
        cnx.close()
        print("MySQL connection is closed")
        
        
        
        
