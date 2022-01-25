from os import write
import pyodbc
import pandas as pd


db_instance = ""
db_user = ""
db_password = ""
db_name = ""


dbjoin = '''
    SELECT * 
    FROM [AXxess].[dbo].[AxPerson] 
    INNER JOIN [AXxess].[dbo].[Badges] ON [AXxess].[dbo].[AxPerson].Id=[AXxess].dbo.Badges.CardholderId
    WHERE [AXxess].[dbo].AxPerson.Allowed = 1 AND [AXxess].[dbo].[Badges].Status = 1 AND LEN([AXxess].[dbo].[Badges].Number) = 6
    '''
db_levels = '''
    SELECT * 
    FROM [AXxess].[dbo].[CardholderAccessLevels]
    '''

conn = pyodbc.connect('''
    Driver={{SQL Server}};
    Server={0};
    Database={1};
    UID={2};
    PWD={3};
    '''.format(db_instance,db_name,db_user,db_password))

query = pd.read_sql_query(
    dbjoin,
    conn)

level_query = pd.read_sql_query(
    db_levels,
    conn
)

def map_levels(id):
    out = ""
    for index, level in levels_frame.loc[levels_frame["Id"] == id].iterrows():
        out += (level["Access Level"] + " ")
    return out

frame = pd.DataFrame(query)
levels_frame = pd.DataFrame(level_query)

with open('output.csv', 'w') as file:
    file.write("First_Name,Last_Name,User_Code,Card_Name,Card_Format,Card_Number,Card_Hex_Number,Access_Level_Id\n")
    for index, row in frame.iterrows():
        out = "{0},{1},{2},{3},{4},{5},{6},{7}\n".format(
            row["First"],
            row["Last"],
            (lambda: row["Pin"][0] if row["Pin"][0] != None else "")(),
            "",
            "",
            row["Number"],
            "",
            map_levels(row["Id"][0])
        )
        print(out)
        file.write(out)

