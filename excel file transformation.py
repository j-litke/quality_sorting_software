import pandas as pd
import numpy as np

pd.set_option('display.max_columns', None)

def rename_columns(df,state):
# removes '_rework' and '_scrap' strings from column name after separating into two df
    df.columns = df.columns.str.replace(f'_{state}', '')
    return df

excel_file = 'data_entry_test.xlsx'
excel_file_2 = 'data_para_analysis.xlsx'
df = pd.read_excel(excel_file)

# csv_file = 'data_entry.csv'
# csv_file_2 = 'transformed_data.csv'
# df = pd.read_csv(csv_file)

# Turn boolean columns to single columns with strings
shift = pd.Series(np.where(df.loc[:,["night","am","pm"]].any(axis=1), df.loc[:,["night","am","pm"]].idxmax(axis=1), np.nan), name="shift")
colour = pd.Series(np.where(df.loc[:,["black","white"]].any(axis=1), df.loc[:,["black","white"]].idxmax(axis=1), np.nan), name="colour")
part = pd.Series(np.where(df.loc[:,["front","rear"]].any(axis=1), df.loc[:,["front","rear"]].idxmax(axis=1), np.nan), name="part")
sort_type = pd.Series(np.where(df.loc[:,["normal_sort","resorting"]].any(axis=1),
                               df.loc[:,["normal_sort","resorting"]].idxmax(axis=1), np.nan), name="sort_type")
rack_type = pd.Series(np.where(df.loc[:,["normal_rack","trial_corner_tape","trial_foam"]].any(axis=1),
                               df.loc[:,["normal_rack","trial_corner_tape","trial_foam"]].idxmax(axis=1), np.nan), name="rack_type")

# take remaining colums from original df to place in final df
date = df[['date']]
operator = df[['operator']]
operator_2 = df[['operator_2']]

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
df2 = pd.concat([date,shift,colour,part,sort_type,rack_type,operator,operator_2],axis=1)
df_rework = pd.concat([df2,defect_rework],axis=1)
df_scrap = pd.concat([df2,defect_scrap],axis=1)

# merge both df to a single df
df3 = pd.concat([df_rework,df_scrap])
df3.to_excel(excel_file_2,index=False)
# df3.to_csv(csv_file_2,index=False)


# things to add
# - ordenar columnas

# luego
# - nuevo script para subir automaticamente a sql
# - juntar todos los scripts

# - reporte automatico simil excel actual
#       - capacidad de agregar comentarios tipo "black rear scrap hig because of.."
# - poner todo en docker
# - columnas calculadas
# - agregar totales a nuevo archivo
# - agregar dwntime a nuevo archivo