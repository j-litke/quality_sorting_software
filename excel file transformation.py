import pandas as pd
import numpy as np

pd.set_option('display.max_columns', None)

def rename_columns(df,state):
# removes '_rework' and '_scrap' strings from column name after separating into two df
    df.columns = df.columns.str.replace(f'_{state}', '')
    return df

data_entry_file = 'data_entry.xlsx'
transformed_data_file = 'transformed_data.xlsx'
totals_file = 'total_checked.xlsx'
downtime_file = 'downtime.xlsx'

df = pd.read_excel(data_entry_file)

# set unique index
df['id'] = pd.Series(range(len(df))) 


# Turn boolean columns to single columns with strings
shift =         pd.Series(np.where(df.loc[:,["night","am","pm"]].any(axis=1),
                                   df.loc[:,["night","am","pm"]].idxmax(axis=1), np.nan), name="shift")
colour =        pd.Series(np.where(df.loc[:,["black","white"]].any(axis=1),
                                   df.loc[:,["black","white"]].idxmax(axis=1), np.nan), name="colour")
part =          pd.Series(np.where(df.loc[:,["front","rear"]].any(axis=1),
                                   df.loc[:,["front","rear"]].idxmax(axis=1), np.nan), name="part")
sort_type =     pd.Series(np.where(df.loc[:,["normal_sort","resorting"]].any(axis=1),
                                   df.loc[:,["normal_sort","resorting"]].idxmax(axis=1), np.nan), name="sort_type")
rack_type =     pd.Series(np.where(df.loc[:,["normal_rack","trial_corner_tape","trial_foam"]].any(axis=1),
                                   df.loc[:,["normal_rack","trial_corner_tape","trial_foam"]].idxmax(axis=1), np.nan), name="rack_type")

# take remaining colums from original df to place in final df

date = df[['date_checked']]
operator = df[['operator']]
operator_2 = df[['operator_2']]
id_sec = df[['id']]

# separate rework and scrap: from 1 to 2 rows
defect_rework = pd.DataFrame()
defect_rework = df.loc[:,df.columns.str.endswith('_rework', na=False)]
defect_scrap = pd.DataFrame()
defect_scrap = df.loc[:,df.columns.str.endswith('_scrap', na=False)]

# remove '_rework' and '_scrap' strings from column names
defect_rework = rename_columns(defect_rework,'rework')
defect_scrap = rename_columns(defect_scrap,'scrap')

# add 'rework' and 'scrap' to state column in each df
defect_rework.insert(loc=0, column='state', value='rework')
defect_scrap.insert(loc=0, column='state', value='scrap')

# append all other columns to rework and scrap df
df2 = pd.concat([id_sec,date,shift,colour,part,sort_type,rack_type,operator,operator_2],axis=1)
df2.rename(columns={'id': 'id_sec'}, inplace=True)
df_rework = pd.concat([df2,defect_rework],axis=1)
df_scrap = pd.concat([df2,defect_scrap],axis=1)

# merge both df to a single df
df3 = pd.concat([df_rework,df_scrap],ignore_index=True)

# set index for defect table
id_column = pd.Series(range(len(df3))) 
df3.insert(0, 'id', id_column)

# uoload data to excel
df3.to_excel(transformed_data_file,index=False)


# totals file
total_checked = df[['total_checked']]
df4 = pd.concat([id_sec,date,shift,colour,part,rack_type,total_checked],axis=1)
df4.to_excel(totals_file,index=False)      

#downtime_file
downtime = df[['downtime']]
df5 = pd.concat([id_sec,date,shift,part,downtime],axis=1)
df5.to_excel(downtime_file,index=False)     

# things to add
# - DONE ordenar columnas
# - DONE nuevo script para subir automaticamente a sql
# - DONE juntar todos los scripts
# - DONE agregar totales a nuevo archivo
# - DONE agregar dwntime a nuevo archivo
# - DONE agregar unique keys. a cada tabla. 
#   DONE    pero ademas, la de totals y downtime pueden it como secundaria en la de defectos. 
#   DONE    usar el index de la df de data_entry como index de totals y downtime.
#   DONE    resetear el index de nuevo una vez que hay dos filas por entry

# - change multiple excels to a single excel with multiple sheets
# - reporte automatico simil excel actual
#       - capacidad de agregar comentarios tipo "black rear scrap hig because of.."
# - poner todo en docker
# - columnas calculadas - directo en    metabase?