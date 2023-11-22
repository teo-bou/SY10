import csv
import glob
from unidecode import unidecode
import shutil
def correct(mot):
    return unidecode(mot).strip().lower()
def write(file):
    with open(file) as file_obj:

        reader_obj = csv.reader(file_obj, delimiter=';')
        corrected_file = []
        for row in reader_obj:
            row = [correct(mot) for mot in row]
            corrected_file.append(row)
    with open(file[:-4]+"_corrected"+".csv", 'w', newline='') as f:
        csvwriter = csv.writer(f, delimiter=",")
        for col in corrected_file:
            csvwriter.writerow(col)




def move(file):
    if not "_corrected" in file:
        shutil.move(file, 'old'+file)
    else:
        shutil.move(file, file.replace("_corrected", ""))

for file in glob.glob('./*.csv'):
    #write(file)
    #move(file)



