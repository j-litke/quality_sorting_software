import PySimpleGUI as sg
import pandas as pd

sg.theme('Dark Blue 3')

excel_file = 'data_entry_test.xlsx'
df = pd.read_excel(excel_file)

defects = ['inclusions', 'paint_sags','scratches','transit_damage','missing_paint','missing_paint_corners']
defect_state = ['rework','scrap']
defect_and_state = [defect+'_'+state for state in defect_state for defect in defects]

defect_layout_col1 =[]
half = int(len(defect_and_state)/2)

for defect in defect_and_state[0:half]:
    defect_layout_col1 += [[sg.Text(defect),sg.Spin([x for x in range(0,100)],0,key=defect,expand_x=1)]]

defect_layout_col2 =[]
for defect in defect_and_state[half:]:
    defect_layout_col2 += [[sg.Text(defect),sg.Spin([x for x in range(0,100)],0,key=defect,expand_x=1)]]



layout = (
    [sg.Text('Fill the following fields')]
    # ,[sg.Text('Name',size=(15,1)),sg.InputText(key='Name')]
   ,[sg.Text('Date'), sg.InputText(key='date',size=(10,1),expand_x=1),
    sg.CalendarButton("Select Date",close_when_date_chosen=True, target="date", format='%Y-%m-%d',size=(10,1))]
   ,[sg.Text('Shift'), sg.Radio('night','shift_group',key='night',default=True)
                     , sg.Radio('am','shift_group',key='am')
                     , sg.Radio('pm','shift_group',key='pm')]
   ,[sg.Text('Colour'), sg.Radio('Black','colour_group',key='black',default=True)
                     , sg.Radio('White','colour_group',key='white')]
   ,[sg.Text('Part'), sg.Radio('Front','part_group',key='front',default=True)
                     , sg.Radio('Rear','part_group',key='rear')]
   ,[sg.Text('Sort Type'), sg.Radio('Normal Sorting','sort_type_group',key='normal_sort',default=True)
                     , sg.Radio('Resorting','sort_type_group',key='resorting')]
   ,[sg.Text('Rack Type'), sg.Radio('Normal Rack','rack_type_group',key='normal_rack',default=True)
                     , sg.Radio('Trial rack - Corner Tape','rack_type_group',key='trial_corner_tape')   
                     , sg.Radio('Trial rack - Foam','rack_type_group',key='trial_foam')]   
   #,[sg.Text('State'), sg.Radio('Rework','state_group',key='rework',default=True)
   #                  , sg.Radio('Scrap','state_group',key='scrap')]
    ,[sg.Text('Operator'), sg.InputText(key='operator',size=(10,1),expand_x=1)]
    ,[sg.Text('Operator 2'), sg.InputText(key='operator_2',size=(10,1),expand_x=1)]
    ,[sg.Column(defect_layout_col1),sg.Column(defect_layout_col2)]
    ,[sg.Submit(), sg.Button('Clear'), sg.Exit()]
)

window = sg.Window('Data Entry',layout)

def clear_input():
# clear all inputs except date
    for key in values:
        if key != 'date':
            window[key]('')
    for key in defect_and_state:
        window[key].update(value=0)
    return None

while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED or event == 'Exit':
        break
    if event == 'Clear':
        clear_input()
    if event == 'Submit':
        new_record = pd.DataFrame(values, index=[0])
        df = pd.concat([df, new_record],ignore_index=True)
        df.to_excel(excel_file,index=False)
        sg.popup('Data Saved')
        clear_input()

window.close()

# things to add
# - disabled element until all necesary data is updated
# - dont clear date, it will be used again in next submit
# - DONE resetear spins a 0 luego de cada submit 
# - manera facil de agregar nuevos defectos/ y menos importante nuevos trials