import json

import pandas as pd

import re

import seaborn as sbn

def get_headers(data):
    headers = data['headers']
    names = []
    for name in headers:
        names.append(name['column'])

    return(names)

def get_df(file_path):
    
    # Assuming your JSON file is named data.json
    # file_path = "cas.json"

    # Open the JSON file and load its contents
    with open(file_path, "r") as json_file:
        data = json.load(json_file)

    # Now you can access the dictionary stored in the JSON file
    # print(data.keys())
    
    lines = data['rows']
    values = []
    for row in lines:
        values.append(row)

    main_data = pd.DataFrame(values, columns=get_headers(data))
    # main_data.to_csv(f"{saved_name}.csv", index = False)
    # main_data.to_excel(f"{saved_name}.xlsx")
    return(main_data)

def set_headers(dfs):
    
    df_hospi = dfs[0] ; df_consult = dfs[1]
    
    df_hospi["Event"] = "Hospitalisation"
    df_consult["Event"] = "Consultation"
    
    selected_head_cons = ['Event', 'Organisation unit name', 'Identification du Malade', 'Date de Saisie', 'Service',
        'Date de consultation','Diagnostic principal', 'Diagnostic secondaire 1', 
        'Diagnostic secondaire 2', 'Issue de la consultation', 'Tranche_d\'Age_Tracker', "Sexe"]
    selected_head_hosp = ['Event', 'Organisation unit name', 'Identification du Malade', 'Date Saisie', 'Service',
        'Date de sortie', 'Diagnostic principal', 'Diagnostic secondaire 1',
        'Diagnostic secondaire 2', 'Type de sortie', 'Tranche_d\'Age_Tracker', "Sexe"]
    
    new_cons = df_consult[selected_head_cons]
    new_hosp = df_hospi[selected_head_hosp]
    
    # new_hosp["Type de sortie"] = new_hosp["Type de sortie"].replace("Décès","Décédé")

    new_header = ['Programme', 'Unité d\'organisation','Identification du Malade', 'Date Saisie', 'Service',
        "Date d'entrée ou de consultation", 'Diagnostic principal', 'Diagnostic secondaire 1',
        'Diagnostic secondaire 2', 'Type de sortie', 'Tranche_d\'Age_Tracker', "Sexe"]
    
    new_hosp.columns = new_header;    new_cons.columns = new_header
    
    return([new_cons, new_hosp])

def database_from_excel(paths):
    
    dfs = [pd.read_excel(path) for path in paths]
    
    list_df = set_headers(dfs)
    
    all_cas = pd.concat(list_df)
    all_cas = all_cas.replace({"Tranche_d\'Age_Tracker": {"15 ans et plus" : "15-19 ans", "0-11 mois": "1-11 mois"},
                               "Type de sortie": {"Décès":"Décédé"}})
    
    
    all_cas.index = range(all_cas.shape[0])
    
    return(all_cas)

def database_from_json(paths):
    
    dfs = [get_df(path) for path in paths]
    
    list_df = set_headers(dfs)
    
    all_cas = pd.concat(list_df)
    all_cas = all_cas.replace({"Tranche_d\'Age_Tracker": {"15 ans et plus" : "15-19 ans", "0-11 mois": "1-11 mois"},
                               "Type de sortie": {"Décès":"Décédé"}})
    
    all_cas.index = range(all_cas.shape[0])
    
    return(all_cas)

corresp = pd.read_excel("./data/correspondance.xlsx", sheet_name="Sheet1",  index_col='Code_Diagnostic')

def split_code (text):
    try:
        for y in text.split(" "):
            if (y != ""):
                break
        return(y)
    except:
        return(text)          

# Get the correspondant affections using the code
def get_affect (code):
    try: 
        return(corresp["Affection_B5a"][corresp.index == code].iloc[0])
    except IndexError as ie:
        return(code) 



# Class DHIS2 creation --------------------------------------------------------------------------
class dhis2:
    
    def __init__(self, paths, file_type:str = "json"):
        if (file_type != "json"):
            data_frame = database_from_excel(paths)
        else :
            data_frame = database_from_json(paths)
            
        self.data_frame = data_frame
        df_shape = data_frame.shape
        self.nb_lignes = df_shape[0]
        self.nb_colonnes = df_shape[1]
        self.nb_de_cas = self.data_frame.Programme.value_counts()
        
    
    def diagramme_bar(self):
        sbn.countplot(x="Programme", data=self.data_frame)
        
    
    def get_data(self):
        return self.data_frame
    
    def display_head(self, n: int = 5):
        return self.data_frame.head(n)
    
    def export_into_excel(self, location: str = 'exported_dhis2_data.xlsx'):
        self.data_frame.to_excel(location, index=False)
        return print("Database exported succesfully on the location " + str(location) + " !!!!")
    
    def get_all_records(self, byhospi = False, separated = False, death = False):
        
        data = self.data_frame.copy()
        data = data.drop(data.index[data["Tranche_d\'Age_Tracker"] == ""])
        data = data.drop(data.index[data["Sexe"] == ""])
        
        programs = list(data["Programme"].unique())
        
        # Constants
        columnsOrder = ['Consultation Hôpital APH Gohomey - Sexe M - 0-1 mois',
       'Consultation Hôpital APH Gohomey - Sexe F - 0-1 mois',
       'Consultation Hôpital APH Gohomey - Sexe M - 1-11 mois',
       'Consultation Hôpital APH Gohomey - Sexe F - 1-11 mois',
       'Consultation Hôpital APH Gohomey - Sexe M - 1-4 ans',
       'Consultation Hôpital APH Gohomey - Sexe F - 1-4 ans',
       'Consultation Hôpital APH Gohomey - Sexe M - 5-9 ans',
       'Consultation Hôpital APH Gohomey - Sexe F - 5-9 ans',
       'Consultation Hôpital APH Gohomey - Sexe M - 10-14 ans',
       'Consultation Hôpital APH Gohomey - Sexe F - 10-14 ans',
       'Consultation Hôpital APH Gohomey - Sexe M - 15-19 ans',
       'Consultation Hôpital APH Gohomey - Sexe F - 15-19 ans',
       'Consultation Hôpital APH Gohomey - Sexe M - 20-24 ans',
       'Consultation Hôpital APH Gohomey - Sexe F - 20-24 ans',
       'Consultation Hôpital APH Gohomey - Sexe M - 25 ans et Plus',
       'Consultation Hôpital APH Gohomey - Sexe F - 25 ans et Plus',
       'Hospitalisation Hôpital APH Gohomey - Sexe M - 0-1 mois',
       'Hospitalisation Hôpital APH Gohomey - Sexe F - 0-1 mois',
       'Hospitalisation Hôpital APH Gohomey - Sexe M - 1-11 mois',
       'Hospitalisation Hôpital APH Gohomey - Sexe F - 1-11 mois',
       'Hospitalisation Hôpital APH Gohomey - Sexe M - 1-4 ans',
       'Hospitalisation Hôpital APH Gohomey - Sexe F - 1-4 ans',
       'Hospitalisation Hôpital APH Gohomey - Sexe M - 5-9 ans',
       'Hospitalisation Hôpital APH Gohomey - Sexe F - 5-9 ans',
       'Hospitalisation Hôpital APH Gohomey - Sexe M - 10-14 ans',
       'Hospitalisation Hôpital APH Gohomey - Sexe F - 10-14 ans',
       'Hospitalisation Hôpital APH Gohomey - Sexe M - 15-19 ans',
       'Hospitalisation Hôpital APH Gohomey - Sexe F - 15-19 ans',
       'Hospitalisation Hôpital APH Gohomey - Sexe M - 20-24 ans',
       'Hospitalisation Hôpital APH Gohomey - Sexe F - 20-24 ans',
       'Hospitalisation Hôpital APH Gohomey - Sexe M - 25 ans et Plus',
       'Hospitalisation Hôpital APH Gohomey - Sexe F - 25 ans et Plus',
       'Consultation H. St Camille Dogbo - Sexe M - 0-1 mois',
       'Consultation H. St Camille Dogbo - Sexe F - 0-1 mois',
       'Consultation H. St Camille Dogbo - Sexe M - 1-11 mois',
       'Consultation H. St Camille Dogbo - Sexe F - 1-11 mois',
       'Consultation H. St Camille Dogbo - Sexe M - 1-4 ans',
       'Consultation H. St Camille Dogbo - Sexe F - 1-4 ans',
       'Consultation H. St Camille Dogbo - Sexe M - 5-9 ans',
       'Consultation H. St Camille Dogbo - Sexe F - 5-9 ans',
       'Consultation H. St Camille Dogbo - Sexe M - 10-14 ans',
       'Consultation H. St Camille Dogbo - Sexe F - 10-14 ans',
       'Consultation H. St Camille Dogbo - Sexe M - 15-19 ans',
       'Consultation H. St Camille Dogbo - Sexe F - 15-19 ans',
       'Consultation H. St Camille Dogbo - Sexe M - 20-24 ans',
       'Consultation H. St Camille Dogbo - Sexe F - 20-24 ans',
       'Consultation H. St Camille Dogbo - Sexe M - 25 ans et Plus',
       'Consultation H. St Camille Dogbo - Sexe F - 25 ans et Plus',
       'Hospitalisation H. St Camille Dogbo - Sexe M - 0-1 mois',
       'Hospitalisation H. St Camille Dogbo - Sexe F - 0-1 mois',
       'Hospitalisation H. St Camille Dogbo - Sexe M - 1-11 mois',
       'Hospitalisation H. St Camille Dogbo - Sexe F - 1-11 mois',
       'Hospitalisation H. St Camille Dogbo - Sexe M - 1-4 ans',
       'Hospitalisation H. St Camille Dogbo - Sexe F - 1-4 ans',
       'Hospitalisation H. St Camille Dogbo - Sexe M - 5-9 ans',
       'Hospitalisation H. St Camille Dogbo - Sexe F - 5-9 ans',
       'Hospitalisation H. St Camille Dogbo - Sexe M - 10-14 ans',
       'Hospitalisation H. St Camille Dogbo - Sexe F - 10-14 ans',
       'Hospitalisation H. St Camille Dogbo - Sexe M - 15-19 ans',
       'Hospitalisation H. St Camille Dogbo - Sexe F - 15-19 ans',
       'Hospitalisation H. St Camille Dogbo - Sexe M - 20-24 ans',
       'Hospitalisation H. St Camille Dogbo - Sexe F - 20-24 ans',
       'Hospitalisation H. St Camille Dogbo - Sexe M - 25 ans et Plus',
       'Hospitalisation H. St Camille Dogbo - Sexe F - 25 ans et Plus',
       'Consultation HZ Aplahoue - Sexe M - 0-1 mois',
       'Consultation HZ Aplahoue - Sexe F - 0-1 mois',
       'Consultation HZ Aplahoue - Sexe M - 1-11 mois',
       'Consultation HZ Aplahoue - Sexe F - 1-11 mois',
       'Consultation HZ Aplahoue - Sexe M - 1-4 ans',
       'Consultation HZ Aplahoue - Sexe F - 1-4 ans',
       'Consultation HZ Aplahoue - Sexe M - 5-9 ans',
       'Consultation HZ Aplahoue - Sexe F - 5-9 ans',
       'Consultation HZ Aplahoue - Sexe M - 10-14 ans',
       'Consultation HZ Aplahoue - Sexe F - 10-14 ans',
       'Consultation HZ Aplahoue - Sexe M - 15-19 ans',
       'Consultation HZ Aplahoue - Sexe F - 15-19 ans',
       'Consultation HZ Aplahoue - Sexe M - 20-24 ans',
       'Consultation HZ Aplahoue - Sexe F - 20-24 ans',
       'Consultation HZ Aplahoue - Sexe M - 25 ans et Plus',
       'Consultation HZ Aplahoue - Sexe F - 25 ans et Plus',
       'Hospitalisation HZ Aplahoue - Sexe M - 0-1 mois',
       'Hospitalisation HZ Aplahoue - Sexe F - 0-1 mois',
       'Hospitalisation HZ Aplahoue - Sexe M - 1-11 mois',
       'Hospitalisation HZ Aplahoue - Sexe F - 1-11 mois',
       'Hospitalisation HZ Aplahoue - Sexe M - 1-4 ans',
       'Hospitalisation HZ Aplahoue - Sexe F - 1-4 ans',
       'Hospitalisation HZ Aplahoue - Sexe M - 5-9 ans',
       'Hospitalisation HZ Aplahoue - Sexe F - 5-9 ans',
       'Hospitalisation HZ Aplahoue - Sexe M - 10-14 ans',
       'Hospitalisation HZ Aplahoue - Sexe F - 10-14 ans',
       'Hospitalisation HZ Aplahoue - Sexe M - 15-19 ans',
       'Hospitalisation HZ Aplahoue - Sexe F - 15-19 ans',
       'Hospitalisation HZ Aplahoue - Sexe M - 20-24 ans',
       'Hospitalisation HZ Aplahoue - Sexe F - 20-24 ans',
       'Hospitalisation HZ Aplahoue - Sexe M - 25 ans et Plus',
       'Hospitalisation HZ Aplahoue - Sexe F - 25 ans et Plus',
       'Consultation HZ Klouekanme - Sexe M - 0-1 mois',
       'Consultation HZ Klouekanme - Sexe F - 0-1 mois',
       'Consultation HZ Klouekanme - Sexe M - 1-11 mois',
       'Consultation HZ Klouekanme - Sexe F - 1-11 mois',
       'Consultation HZ Klouekanme - Sexe M - 1-4 ans',
       'Consultation HZ Klouekanme - Sexe F - 1-4 ans',
       'Consultation HZ Klouekanme - Sexe M - 5-9 ans',
       'Consultation HZ Klouekanme - Sexe F - 5-9 ans',
       'Consultation HZ Klouekanme - Sexe M - 10-14 ans',
       'Consultation HZ Klouekanme - Sexe F - 10-14 ans',
       'Consultation HZ Klouekanme - Sexe M - 15-19 ans',
       'Consultation HZ Klouekanme - Sexe F - 15-19 ans',
       'Consultation HZ Klouekanme - Sexe M - 20-24 ans',
       'Consultation HZ Klouekanme - Sexe F - 20-24 ans',
       'Consultation HZ Klouekanme - Sexe M - 25 ans et Plus',
       'Consultation HZ Klouekanme - Sexe F - 25 ans et Plus',
       'Hospitalisation HZ Klouekanme - Sexe M - 0-1 mois',
       'Hospitalisation HZ Klouekanme - Sexe F - 0-1 mois',
       'Hospitalisation HZ Klouekanme - Sexe M - 1-11 mois',
       'Hospitalisation HZ Klouekanme - Sexe F - 1-11 mois',
       'Hospitalisation HZ Klouekanme - Sexe M - 1-4 ans',
       'Hospitalisation HZ Klouekanme - Sexe F - 1-4 ans',
       'Hospitalisation HZ Klouekanme - Sexe M - 5-9 ans',
       'Hospitalisation HZ Klouekanme - Sexe F - 5-9 ans',
       'Hospitalisation HZ Klouekanme - Sexe M - 10-14 ans',
       'Hospitalisation HZ Klouekanme - Sexe F - 10-14 ans',
       'Hospitalisation HZ Klouekanme - Sexe M - 15-19 ans',
       'Hospitalisation HZ Klouekanme - Sexe F - 15-19 ans',
       'Hospitalisation HZ Klouekanme - Sexe M - 20-24 ans',
       'Hospitalisation HZ Klouekanme - Sexe F - 20-24 ans',
       'Hospitalisation HZ Klouekanme - Sexe M - 25 ans et Plus',
       'Hospitalisation HZ Klouekanme - Sexe F - 25 ans et Plus']
        affectionB5a = list(corresp['Affection_B5a'].unique())
        # affectionB5a.append("Dracunculose")
        affectionB5a = sorted(affectionB5a)
        ages, cols = [], []
        organisations = sorted(data["Unité d'organisation"].unique())

        ages = ['0-1 mois', '1-11 mois', '1-4 ans', '5-9 ans', '10-14 ans', '15-19 ans', '20-24 ans', '25 ans et Plus']
        
        
        if (death):
            data = data.drop(data.index[(data["Type de sortie"] != "Décédé")])

        data['diag_princ_B5a'] = data["Diagnostic principal"].apply(split_code).apply(get_affect)
        data['Secon1_Aff_B5a'] = data["Diagnostic secondaire 1"].apply(split_code).apply(get_affect)
        data['Secon2_Aff_B5a'] = data["Diagnostic secondaire 2"].apply(split_code).apply(get_affect)
        
        # Save the missing affections within the diagnostics (principal, second 1 and 2)
        all_affB5a = sorted(data['diag_princ_B5a'].unique())+sorted(data['Secon1_Aff_B5a'].unique())+sorted(data['Secon2_Aff_B5a'].unique())
        missing_aff = []

        for aff in all_affB5a:
            if (aff not in affectionB5a and aff != ''):
                missing_aff.append(aff)
                
        missing_aff
        
        sexs = ["M", "F"]
        cols = []
        
        if (byhospi):
            for x in sorted(organisations):
                for y in ages:
                    for z in sexs:
                        cols.append(x + " - Sexe " + z + " - " + y)
                        
            def getAffectCount(data, countcol):
                # Function to get the number of occurences of each affections
                # data : the data base
                # countcol : the column name to counts occurences
                
                countsAffections = {}
                
                for unit in data["Unité d'organisation"].unique():
                    countsAffections[unit] = {}
                    
                    for age in ages:
                        countsAffections[unit][age] = {}
                        
                        for sex in sorted(data["Sexe"].unique(), reverse=True):
                        
                            values = data[countcol][(data["Unité d'organisation"] == unit) & 
                                                    (data["Tranche_d'Age_Tracker"] == age) &
                                                    (data["Sexe"] == sex)].value_counts().sort_index()
                            countsAffections[unit][age][sex] = values
                
                return(countsAffections)      


            def fillTable(organisations, ages, countsAffections):
                # To create and a database table
                table_affection = pd.DataFrame(0, columns = cols, index = affectionB5a)
                tabInd = table_affection.index
                for unit in organisations:
                    try:
                        for age in ages:
                            try:
                                for sex in ["M", "F"]:
                                    try:
                                        chgInd = countsAffections[unit][age][sex].index 
                                        
                                        for tInd in tabInd:
                                            try:
                                                if tInd in chgInd:
                                                    table_affection.loc[tInd,unit+" - Sexe "+sex+" - "+age] = countsAffections[unit][age][sex][tInd]
                                            
                                            except KeyError:
                                                continue
                                    except KeyError:
                                        continue
                            except KeyError:
                                continue
                    except KeyError:
                        continue           
                                
                return(table_affection)      
                        
        else:
            for y in ages:
                for z in sexs:
                    cols.append("Sexe " + z + " - " + y)
                    

            def getAffectCount(data, countcol):
                # Function to get the number of occurences of each affections
                # data : the data base
                # countcol : the column name to counts occurences

                countsAffections = {}

                for age in ages:
                    countsAffections[age] = {}
                        
                    for sex in sorted(data["Sexe"].unique(), reverse=True):
                    
                        values = data[countcol][(data["Tranche_d'Age_Tracker"] == age) &
                                                (data["Sexe"] == sex)].value_counts().sort_index()
                        countsAffections[age][sex] = values
                                
                return(countsAffections)

            def fillTable(ages, countsAffections):
                # To create and a database table
                table_affection = pd.DataFrame(0, columns = cols, index = affectionB5a)
                tabInd = table_affection.index
                for age in ages:
                    try:
                        for sex in ["M", "F"]:
                            try:
                                chgInd = countsAffections[age][sex].index 
                                
                                for tInd in tabInd:
                                    try:
                                        if tInd in chgInd:
                                            table_affection.loc[tInd,"Sexe "+sex+" - "+age] = countsAffections[age][sex][tInd]
                                    
                                    except KeyError:
                                        continue
                            except KeyError:
                                continue
                    except KeyError:
                        continue           
                return(table_affection)


        # Important functions 
        
        # Put all tables into one
        def getOneTable(tables):
            
            diagnostics = list(tables.keys())
            tablesDiag = tables[diagnostics[0]].copy()

            for tab in diagnostics[1:]:
                tablesDiag += tables[tab]
                
            return(tablesDiag)
        
        
        # To return processing
        def get_cons_hosp(data):
            alldata = {}
            
            if separated:
                for program in programs:
                    data_cons = data.copy().drop(data.index[(data["Programme"] != program)])
                    
                    tablesAll = {}
                    for aff in data_cons.columns[-3:]:
                        if byhospi:
                            tablesAll[aff] = fillTable(organisations, ages, getAffectCount(data=data_cons, countcol=aff))
                        else:
                            tablesAll[aff] = fillTable(ages, getAffectCount(data=data_cons, countcol=aff))
                            
                    cnsTable = getOneTable(tablesAll)
                    cnsTable.columns = program + " " + cnsTable.columns
                    
                    alldata[program] = cnsTable
                    
                alldata = pd.merge(alldata["Consultation"], alldata["Hospitalisation"],
                                left_index=True, right_index=True, how="inner")

            else:
                tablesAll = {}
                for aff in data.columns[-3:]:
                    if byhospi:
                        tablesAll[aff] = fillTable(organisations, ages, getAffectCount(data=data, countcol=aff))
                    else:
                        tablesAll[aff] = fillTable(ages, getAffectCount(data=data, countcol=aff))
                        
                    alldata = getOneTable(tablesAll)
                        
            return(alldata)

        cons_hosp_data = get_cons_hosp(data)
        
        # Print the missing affections
        if missing_aff != [] : print("Les affections manquantes sont: "+ str(missing_aff))
        
        try:
            return(cons_hosp_data.loc[:,columnsOrder])
        except:
            return(cons_hosp_data)
    
    
cs_corr = pd.read_excel("./data/CS_correspondance.xlsx", index_col="Affections")


# A reduire
def collapse(mylist):
    if (isinstance(mylist, str)):
        return mylist
    else:
        if (len(mylist)>=2):            
            collapsed = mylist[0]
            try:
                for arg in mylist[1:]:
                    collapsed += "|" + arg
                return collapsed        
            except:
                return collapsed
            
        else:
            print("La liste ne contient pas plusieurs valeurs")


def findMatch(regex, mytext):
    if (re.findall(regex+r".*", mytext)):
        return True
    else:
        return False
    
    
def hop_to_zs(Affection_df):
    
    # Constantes
    sexes = ["Sexe M", "Sexe F"]
    ages = ['0-1 mois','1-11 mois','1-4 ans','5-9 ans','10-14 ans','15-19 ans','20-24 ans','25 ans et Plus']
    zs = ["ZS ADD", "ZS KTL"]
    newcolumns = [z + " - "+ sex + " - " + age for z in zs for age in ages for sex in sexes ]
    newDataFrame = pd.DataFrame(0, columns=newcolumns, index=Affection_df.index)

    for age in ages:
        for sex in sexes:
            for z in zs:
                toCol = collapse(["Hôpital APH Gohomey","HZ Aplahoue","H. St Camille Dogbo"]) if z == "ZS ADD" else "HZ Klouekanme"
                for col in Affection_df.columns:
                    if (findMatch(regex=age,mytext=col) and findMatch(regex=sex,mytext=col) and findMatch(regex=toCol,mytext=col)):
                        newDataFrame[z + " - "+ sex + " - " + age] += Affection_df[col].copy()
    
    return newDataFrame
                    