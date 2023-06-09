import tkinter as tk
from tkinter import filedialog
import os
import re
import shutil
import glob
from PIL import Image


##Deklaracja 1 razowa
wz_path=filedialog.askdirectory( title = "Wybierz wzór tfile" )
BigImage_path=filedialog.askdirectory( title = "Wybierz Big image" )
##Deklaracja 1 razowa, ponizej petla zapisowa
print(BigImage_path)

while(True):
    # Otwórz okno dialogowe, aby wybrać plik SVG
    root = tk.Tk()
    root.withdraw()
    file_path = filedialog.askopenfilename(title="Wybierz plik SVG")
    ## Wyciety fragment wzoru
    splitter=wz_path.split( "/" )
    destination="/".join( splitter[:-1])
    txt_version=glob.glob( f'{wz_path}\*.txt') ##txt
    tflite_version=glob.glob( f'{wz_path}\*.tflite') ##tflie
    BigImage_version=glob.glob(f'{BigImage_path}\*.jpg') ##BigImageJpg

    ##ID
    spliters=file_path.split( "/" )
    nazwa=spliters[-1]
    nazwa_edit=nazwa.split( "_" )
    nazwa_końcowa=nazwa_edit[0]

    # Sprawdź, czy plik został wybrany
    if not file_path:
        print("Nie wybrano pliku")
        exit()

    # Wczytaj plik SVG
    with open(file_path, "r") as f:
        svg_data = f.read()

    #Plik wz
    # ROI BIERZE SIE Z GORNEGO ID
    match = re.findall(r'inkscape:label="(.+)"', svg_data) #ID
    name = match[0]
    #camera = re.findall(r'\s+style=.+\s+id="\D+(.+)"', svg_data) #id kamery
    #kamera = camera

    #width height x y label na liczbe i _ROI
    select_text = r'</g>([\S\s]*)</g>'
    texter = re.findall(select_text, svg_data)
    textester = " ".join(texter)
    textest = textester.replace(".", ",")
    #print(kamera)
    ###### Podpinanie elementów
    roi_regex = r'<rect'
    roi_matches = re.findall(roi_regex, textest)
    ##id
    roi_regex_id = nazwa_końcowa
    ##width
    roi_regex_width = r'width="(.+)"'
    roi_width = re.findall(roi_regex_width, textest)
    ##height
    roi_regex_height = r'height="(.+)"'
    roi_height=re.findall( roi_regex_height, textest)
    ##x
    roi_regex_x = r'\s[x]="(.+)"'
    roi_x=re.findall( roi_regex_x, textest )
    ##y
    roi_regex_y = r'\s[y]="(.+)"'
    roi_y=re.findall( roi_regex_y, textest )
    ##label
    roi_regex_label = r'"(.+_ROI)"'
    roi_label=re.findall( roi_regex_label, textest )
    print(roi_label)
    ##łączenie elementów
    elements = [roi_width, roi_height, roi_x, roi_y, roi_label]
    ##pętla robocza, przypisanie elementow + wycinanie zdjecia + generacja plikow
    print(elements)
    for item in range(len(roi_matches)):
        width = roi_width[item]
        height = roi_height[item]
        width = width.replace(',', '.')
        height = height.replace(',', '.')
        x = roi_x[item]
        y = roi_y[item]
        x=x.replace(',', '.')
        y=y.replace(',', '.')
        print(x, y)
        label = roi_label[item]
        #kameras = kamera[item]
        roi_data=f"({x}, {y}, {width}, {height})"
        print(roi_data)
        x_final = round(int(float(x)) + round(int(float(width))))
        y_final = round(int(float(y)) + round(int(float(height))))
        x_int = round(int(float(x)))
        y_int = round(int(float(y)))
        print(x_final, y_final, x_int, y_int)
        ##obraz
        i = 1
        for big in BigImage_version:
            print(big)
            Bigimage=Image.open( big )
            Big_Image_Crop=Bigimage.crop( (x_int, y_int, x_final, y_final))
            Big_Image_Crop=Big_Image_Crop.save(f"{big}_new_{label}.jpg")
            i+=1
        ##Folder
        roi_folder_path=os.path.join( os.path.dirname( file_path ), f"{name}_{label}" )
        os.makedirs( roi_folder_path, exist_ok = True )
        for file in ["1_OK", "2_NOK"]:
            for filex in txt_version:
                shutil.copy2(filex, f'{destination}/{name}_{label}.txt' )
            for file_tfile in tflite_version:
                shutil.copy2(file_tfile, f'{destination}/{name}_{label}.tflite' )
        ##Zapis
        for folder_name in ["1_OK", "2_NOK"]:
            folder_path = os.path.join(roi_folder_path, folder_name)
            os.makedirs(folder_path, exist_ok=True)
            # Zapisz plik tekstowy z parametrami ROI w katalogu głównym
            output_file_path=os.path.join( os.path.dirname( file_path ), f"{name}_{label}.txt" )
            with open( output_file_path, "w" ) as f :
                f.write( roi_data )

            print(
                f"Zapisano dane dla ROI {name} w pliku {output_file_path} oraz utworzono foldery dla ROI w katalogu {roi_folder_path}" )
input()
