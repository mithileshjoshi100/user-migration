import src.fetch_data as fetch
import src.insert_data as insert


if __name__ == '__main__':
    pass

# insert.insert_geidp_entitled_feature()



# fetch.fetch_contacts()
# fetch.fetch_users()
# fetch.fetch_psa()
# fetch.fetch_approllaccess()
# fetch.fetch_contact_additional_information()
# fetch.fetch_umr()
# fetch.fetch_geidp_entitled_feature()

# insert.insert_contact()
# insert.insert_users()
# insert.insert_psa()
# insert.insert_approllaccess()
# insert.insert_contact_additional_information()
# insert.insert_umr()
insert.insert_geidp_entitled_feature()





# import pandas as pd

# df = pd.read_csv('files/df_contact.csv')
# df2 = pd.read_csv('files/df_contact.csv')

# for index,row  in df.iterrows():
#     df.at[index,'Id'] = 'huhu'

# x = df2[df2['Email'] == 'testft2019+acpemea009m4@gmail.com' ]['Id']
# x = x[0]
# print(x)


####

import src.fetch_data as fetch
import src.insert_data as insert
import PySimpleGUI as sg


layout = [
    [sg.Text("Hello from IDM Team")], 
    [sg.Button("Fetch")],
    [sg.Button("Contact_Fetch"),sg.Button("User_Fetch")],
    [sg.Button("Insert")],
    [sg.Button("Contact_Insert"),sg.Button("User_Insert")],
    [sg.Button("Exit")],
]

# Create the window
window = sg.Window("Hey!!!", layout)

# Create an event loop
while True:
    event, values = window.read()
    # End program if user closes window or
    # presses the OK button

    if event == "Contact_Fetch":
        fetch.fetch_contacts()

    if event == "User_Fetch":
        fetch.fetch_users()
        
    if event == "Contact_Insert":
        insert.insert_contact()
        
    if event == "User_Insert":
        insert.insert_users()
        
    if event == "Exit" or event == sg.WIN_CLOSED:
        break

window.close()
