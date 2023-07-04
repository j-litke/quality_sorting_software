import mysql.connector
from mysql.connector import Error
import pandas as pd
import numpy as np

def add_column_sql(df,table_name):
    #aca meter el codigo que esta en import_to_sql que verifica si existe la columan yh la agrega, ya que tb lo voy a usar en la funcion verify keys
    # Get existing columns in the table 
    cursor.execute(f"SELECT * FROM {table_name} LIMIT 0")
    existing_columns = [desc[0] for desc in cursor.description]

    # Get new columns in the DataFrame
    new_columns = [col for col in df.columns if col not in existing_columns]

    # If there are new columns, alter the table to add them
    if new_columns:
        for column in new_columns:
            cursor.execute(f"ALTER TABLE {table_name} ADD COLUMN {column} int") 

def import_to_sql(df,table_name):
    #imports data to mysql
    
    #adds new columns if necesary
    add_column_sql(df,table_name)
    
    # Import data into the table
    for _, row in df.iterrows():
        # Create INSERT statement dynamically
        sql = f"INSERT INTO {table_name} ({', '.join(df.columns)}) VALUES ({', '.join(['%s'] * len(df.columns))})"
        values = tuple(row)
        cursor.execute(sql, values)  
        
    # Commit changes and close connection
    cnx.commit() 

def verify_unique_keys(df,table_name):
    #verifies that the rows don't already exist, using the unique keys
    
    #adds new columns if necesary
    add_column_sql(df,table_name)   
    
    # Specify primary key column
    primary_key_column = "id" 

    # Get existing primary keys in the table
    cursor.execute(f"SELECT {primary_key_column} FROM {table_name}")
    existing_primary_keys = set(row[0] for row in cursor.fetchall())

    # Filter out rows with existing primary keys from the DataFrame
    df = df[~df[primary_key_column].isin(existing_primary_keys)]

    return df

# create df from the three excel files
excel_files = ['transformed_data.xlsx','total_checked.xlsx','downtime.xlsx']
table_names = ['paint_defects','paint_totals','downtime']
df_index = [f'df_{i}' for i in enumerate(excel_files)]
df_list = [] # list of dataframes
for df,file in zip(df_index,excel_files):
    df = pd.read_excel(file)
    df.fillna(0,inplace=True)
    df_list.append(df)

# conection with mysql    
try:
    cnx = mysql.connector.connect(  host='localhost',
                                    database='fng',
                                    user='root',
                                    password='PassWord123')
    if cnx.is_connected():
        cursor = cnx.cursor(buffered=True)
        for df,table_name in zip(df_list,table_names):
            df = verify_unique_keys(df,table_name)
            import_to_sql(df,table_name)
            
except Error as e:
    print("Error while connecting to MySQL", e)
    
finally:
    if cnx.is_connected():
        cursor.close()
        cnx.close()
        print("MySQL connection is closed")

# DONE importar data de ultimo excel a mysql database. 
# DONE armar tablas en sql segun los excels generados aca (no en el script)
# DONE revisar si hay nuevos defectos -> agregar columna
# DONE subida de data para tablas de totales y downtime
# DONE antes de subir a sql, debe revisar que no exista ya esa data. 