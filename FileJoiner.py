import os
import glob

path = 'C:/Users/ALF/Documents/Copia Scrape Incompleto'
extension = 'csv'
os.chdir(path)
result = glob.glob('*.{}'.format(extension))
print(result)

f = open("unificado.csv","w",encoding="utf-8")
f.write("NAME;ROOMS;AREA;FLOOR;LOCATION;ELEVATOR;PRICE;GARAGE;GARAGE_PRICE;OLD_PRICE;CHANGE_IN_PRICE\n")

for filename in result:
    with open(path+"/"+filename,"r", encoding="utf-8") as t:
        t.readline()
        for line in t:
            f.write(line)
    t.close()
f.close()

