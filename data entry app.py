import PySimpleGUI as sg
import pandas as pd
import pickle

def clear_input():
# clear all inputs except date and return all spin counters to zero
    for key in values:
        if key != 'date':
            window[key]('')
    for key in defect_and_state:
        window[key].update(value=0)
    for key in defect_and_state_new:
        window[key].update(value=0)
    return None

def add_state(defects):
# takes defect list and returns two lists, one for rework and one for scrap. also creates spins
    defect_state = ['rework','scrap']
    defect_and_state = [defect+'_'+state for state in defect_state for defect in defects]
   
    half = int(len(defect_and_state)/2)
    
    defect_layout_col1 =[]
    for defects in defect_and_state[0:half]:
        defect_layout_col1 += [[sg.Text(defects),sg.Spin([x for x in range(0,100)],0,key=defects,expand_x=1)]]

    defect_layout_col2 =[]
    for defects in defect_and_state[half:]:
        defect_layout_col2 += [[sg.Text(defects),sg.Spin([x for x in range(0,100)],0,key=defects,expand_x=1)]]

    return defect_layout_col1,defect_layout_col2,defect_and_state

def create_new_defect_row(defect):
    # name of the new defect taken from text box
    known_defects.append(defect)
    defect_list = [defect]
    defect_layout_col1_new,defect_layout_col2_new,defect_and_state_new = add_state(defect_list)
    layout_new_defect = [[sg.Column(defect_layout_col1_new,key='new_defect_row_1'),sg.Column(defect_layout_col2_new,key='new_defect_row_2')]]
   
    return layout_new_defect,defect_and_state_new

sg.theme('Dark Blue 3')

# excel_file = 'data_entry_test.xlsx'
# df = pd.read_excel(excel_file)

csv_file = 'data_entry.csv'
# df = pd.DataFrame(list())             # usar para reinicialiazr el csv
# df.to_csv('data_entry.csv')           
df = pd.read_csv(csv_file,header=None)

# list of already known defects
# known_defects = ['inclusions', 'paint_sags','scratches','transit_damage','missing_paint','missing_paint_corners']
known_defects = pickle.load(open('C:/Users/Vincent/Desktop/FnG Project/added_defects.p', "rb"))

# create rework and scrap columns from defects to place in window layout
defect_layout_col1,defect_layout_col2,defect_and_state = add_state(known_defects)
defect_and_state_new =[]

# main layout
layout_main_1 = [
   [sg.Text('Date'), sg.InputText(key='date',size=(10,1),expand_x=1),
    sg.CalendarButton("Select Date",close_when_date_chosen=True, target='date', format='%Y-%m-%d',size=(10,1))]
   ,[sg.Text('Shift'), sg.Radio('night','shift_group',key='night',default=True)
                     , sg.Radio('am','shift_group',key='am')
                     , sg.Radio('pm','shift_group',key='pm')]
   ,[sg.Text('Colour'), sg.Radio('Black','colour_group',key='black',default=True)
                     , sg.Radio('White','colour_group',key='white')]
   ,[sg.Text('Part'), sg.Radio('Front','part_group',key='front',default=True)
                     , sg.Radio('Rear','part_group',key='rear')]
   ,[sg.Frame('Sort Type',([[sg.Text('Sort Type'), sg.Radio('Normal Sorting','sort_type_group',key='normal_sort',default=True)
                     , sg.Radio('Resorting','sort_type_group',key='resorting')]]))]
   ,[sg.Frame('Rack Type',[
                    [sg.Radio('     Normal Rack','rack_type_group',key='normal_rack',default=True)]
                    ,[sg.Radio('     Trial rack - Corner Tape','rack_type_group',key='trial_corner_tape')]   
                    ,[sg.Radio('     Trial rack - Foam','rack_type_group',key='trial_foam')]])]
   ,[sg.Text('Operator'), sg.InputText(key='operator',size=(10,1),expand_x=1)]
   ,[sg.Text('Operator 2'), sg.InputText(key='operator_2',size=(10,1),expand_x=1)]
   ,[sg.Text('New Defect'), sg.InputText(key='new_defect',size=(10,1),expand_x=1), sg.Button('Add')]

]

layout_main_2 = [
    [sg.Column(defect_layout_col1),sg.Column(defect_layout_col2)]
   ,[sg.Frame('New Defects',[[]], key='-FRAME-')]
   ,[sg.Frame('Total Checked',[[sg.Spin([x for x in range(0,500)],0,key='total_checked',expand_x=1)]],key='-FRAME 2-')]
   ,[sg.Submit(disabled=False), sg.Button('Clear'), sg.Exit()]
]

window = sg.Window('Data Entry',[[sg.Column(layout_main_1),sg.Column(layout_main_2)]])

while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED or event == 'Exit':
        break
    
    if event == 'Add': 
        layout_new_defects,defect_and_state_new = create_new_defect_row(values['new_defect'])
        window.extend_layout(window['-FRAME-'], layout_new_defects)
        # known_defects = [] - activate line to reset known defects, make corrections if added wrong defect
        pickle.dump(known_defects, open('C:/Users/Vincent/Desktop/FnG Project/added_defects.p',"wb"))
        df2 = pd.DataFrame(known_defects)
        df2.to_csv('defect_list.csv') # saves defects in csv for easy editing of list 
    if event == 'Clear':
        clear_input()
        
    if event == 'Submit':
        new_record = pd.DataFrame(values, index=[0])
        df = pd.concat([df, new_record],ignore_index=True)
        df.to_csv(csv_file,index=False)
        sg.popup('Data Saved')
        clear_input()

window.close()

# things to add
# - disabled 'Submit' until date is entered
# - DONE dont clear date, it will be used again in next submit
# - DONE resetear spins a 0 luego de cada submit 
# - DONE manera facil de agregar nuevos defectos/ - ver comentarios en codigo
# una vez agregado el defecto nuevodebe concatenarse a la lista ppal. grabar csv con lista de defectos al cerrar, y volver a leerla al abrir, para no perder los defectos agregados
# - agregar nuevos nuevos trials 
# - add way to modify defect list
# - cambiar excels a csv
# - add total checked and downtime
