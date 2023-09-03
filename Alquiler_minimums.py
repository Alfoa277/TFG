import pandas as pd
import patsy as patsy
import statistics as statistics

import Levenshtein

def find_population(provincia,town, poblacion_dataset):
    pob = poblacion_dataset[poblacion_dataset['PROVINCIA']==provincia]
    string_list = pob['NOMBRE'].tolist()
    string_list = [string.lower() for string in string_list]
    similarity_scores = []
    for s in string_list:
        variations = s.split('/')
        scores = []
        for variation in variations:
            scores.append(Levenshtein.distance(town, variation))
        similarity_scores.append((s, min(scores)))
    most_similar = sorted(similarity_scores, key=lambda x: x[1])[0][0]
    return pob[pob['NOMBRE']==most_similar]['POB22'].iloc[0]

rent = pd.read_csv('DataRent.csv')
sold = pd.read_csv('DataSold.csv')
sold = sold.drop(['CHANGE_IN_PRICE', 'OLD_PRICE'],axis=1)
rent = rent.drop(['CHANGE_IN_PRICE', 'OLD_PRICE'],axis=1)

provinces = sold['PROVINCE'].unique()
selected_provinces = {}
for p in provinces:
    subset = sold[sold['PROVINCE']==p]
    towns = subset['TOWN'].tolist()
    town_counter = {}
    for town in towns:
        if town not in town_counter:
            town_counter[town] = 0
        town_counter[town] += 1
    highest_keys = sorted(town_counter, key=town_counter.get, reverse=True)[:]
    selected_provinces[p] = highest_keys

selected_towns = []
for i in selected_provinces:
    selected_towns+=selected_provinces[i]

selected_sold = sold[sold['TOWN'].isin(selected_towns)]

for min_houses in [5,10,25,50,100,200]:
    print("starting "+str(min_houses))
    rent_towns = rent['TOWN'].unique()
    cannot_use = []
    for i in selected_towns:
        if i not in rent_towns:
            cannot_use.append(i)
        elif len(rent[rent['TOWN']==i])<min_houses:
            #Remove towns with less than 10 rental homes
            cannot_use.append(i)

    selected_sold = selected_sold[~selected_sold['TOWN'].isin(cannot_use)]
    selected_towns = [x for x in selected_towns if x not in cannot_use]
    selected_rent = rent[rent['TOWN'].isin(selected_towns)]

    sold = selected_sold.copy(deep=True)
    rent = selected_rent.copy(deep=True)

    num_houses = []
    for town in rent['TOWN'].drop_duplicates(keep='first'):
        temp = rent[rent['TOWN']==town]
        num_houses+= [len(temp)]*len(temp)
    rent['NUM_HOUSES']=num_houses

    num_houses = []
    for town in sold['TOWN'].drop_duplicates(keep='first'):
        temp = sold[sold['TOWN']==town]
        num_houses+= [len(temp)]*len(temp)
    sold['NUM_HOUSES']=num_houses

    poblacion = pd.read_csv('poblacion.csv', encoding='ISO-8859-1')
    poblacion = poblacion.drop(["CPRO","CMUN","HOMBRES","MUJERES"],axis=1)

    poblacion['PROVINCIA'].unique().tolist() # Manually change error

    for i in range(len(poblacion)):
        name = poblacion.iloc[i,0]
        name_ = name.split('/')
        if len(name_)>1:
            if name_[0] == 'Alicante':
                poblacion.iloc[i,0] = name_[0]
            elif name_[0] == 'Araba':
                poblacion.iloc[i,0] = name_[1]
            elif name_[0] == 'Castellón':
                poblacion.iloc[i,0] = name_[0]
            elif name_[0] == "Valencia":
                poblacion.iloc[i,0] = name_[0]
        else:
            name_2 = name.split(',')
            if len(name_2) > 1:
                if name_2[0] == "Balears":
                    poblacion.iloc[i,0] = "Balears (Illes)"
                elif name_2[0] == "Coruña":
                    poblacion.iloc[i,0] = "A Coruña"
                elif name_2[0] == "Palmas":
                    poblacion.iloc[i,0] = "Las Palmas"
                elif name_2[0] == "Rioja":
                    poblacion.iloc[i,0] = "La Rioja"

    for i in range(len(poblacion)):
        name = poblacion.iloc[i,1]
        name_ = name.split(',')
        if len(name_)>1:
            s = ''
            name_.reverse()
            for word in name_:
                s+=word+" "
            s=s[:-1]
            poblacion.iloc[i,1] = s

    poblacion['NOMBRE'] = [string.lower() for string in poblacion['NOMBRE'].tolist()]
    allowed_provinces = poblacion['PROVINCIA'].unique().tolist()



    t = rent[rent['FLOOR']!="UNK"]
    unk = rent[rent['FLOOR']=="UNK"]
    t = t[t['FLOOR']!="-"]
    t['FLOOR']=t['FLOOR'].astype(int)
    t = t[t['FLOOR']<15].astype(str)
    data_rent = pd.concat([t, unk], ignore_index=True)
    data_rent = data_rent[data_rent['PROVINCE'].isin(allowed_provinces)]

    t = sold[sold['FLOOR']!="UNK"]
    unk = sold[sold['FLOOR']=="UNK"]
    t = t[t['FLOOR']!="-"]
    t['FLOOR']=t['FLOOR'].astype(int)
    t = t[t['FLOOR']<15].astype(str)
    data_sold = pd.concat([t, unk], ignore_index=True)
    data_sold = data_sold[data_sold['PROVINCE'].isin(allowed_provinces)]

    habitantes = []
    for town in data_rent['TOWN'].drop_duplicates(keep='first'):
        subset = data_rent[data_rent['TOWN']==town]
        province = subset['PROVINCE'].tolist()[0]
        habit = find_population(province,town,poblacion)
        habitantes+=len(subset)*[habit]
    data_rent['POPULATION'] = habitantes

    data_sold = data_sold[data_sold['PROVINCE']!="Andorra"]
    data_sold=data_sold.replace({'Guipúzcoa':'Gipuzkoa'},regex=True)
    data_sold=data_sold.replace({'València':'Valencia'},regex=True)
    data_sold=data_sold.replace({'Vizcaya':'Bizkaia'},regex=True)

    habitantes = []
    for town in data_sold['TOWN'].drop_duplicates(keep='first'):
        subset = data_sold[data_sold['TOWN']==town]
        province = subset['PROVINCE'].tolist()[0]
        habit = find_population(province,town,poblacion)
        habitantes+=len(subset)*[habit]
    data_sold['POPULATION'] = habitantes

    data_rent['GARAGE'] = data_rent['GARAGE'].astype(bool)
    #data_rent['GARAGE_PRICE'] = data_rent['GARAGE_PRICE'].astype(int)
    data_rent = data_rent.drop(['GARAGE_PRICE'],axis=1)
    data_rent['AREA'] = data_rent['AREA'].astype(float)
    data_rent['ROOMS'] = data_rent['ROOMS'].astype(int)
    data_rent['NUM_HOUSES'] = data_rent['NUM_HOUSES'].astype(int)
    data_rent['PRICE'] = data_rent['PRICE'].astype(int)
    data_rent = data_rent[data_rent['ROOMS']<11]

    nan_rows = data_rent[data_rent.isna().any(axis=1)]
    data_rent = data_rent.dropna()

    data_sold['GARAGE'] = data_sold['GARAGE'].astype(bool)
    #data_sold['GARAGE_PRICE'] = data_sold['GARAGE_PRICE'].astype(float)
    data_sold = data_sold.drop(['GARAGE_PRICE'],axis=1)
    data_sold['AREA'] = data_sold['AREA'].astype(float)
    data_sold['ROOMS'] = data_sold['ROOMS'].astype(int)
    data_sold['NUM_HOUSES'] = data_sold['NUM_HOUSES'].astype(int)
    data_sold['PRICE'] = data_sold['PRICE'].astype(float)
    data_sold = data_sold[data_sold['ROOMS']<11]

    nan_rows = data_sold[data_sold.isna().any(axis=1)]
    data_sold = data_sold.dropna()

    data_rent.to_csv("Variants/selectedRent"+str(min_houses)+".csv",sep=";",index=False)
    data_sold.to_csv("Variants/selectedForSale"+str(min_houses)+".csv",sep=";",index=False)
    print("Done with "+str(min_houses))