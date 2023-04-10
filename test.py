import tkinter as tk
from tkinter import filedialog
from pathlib import Path
import shutil
import os
import glob

root = tk.Tk()
root.withdraw()
file_path = filedialog.askdirectory()

splitter=file_path.split( "/" )
destination="/".join( splitter[:-1])
print(destination)

files = glob.glob(f'{file_path}\*.txt')
file2 = glob.glob(f'{file_path}\*.tflite')

for item in files:
    shutil.copy2(item, destination)

for item in file2:
    shutil.copy2(item, f'{destination}/retard')