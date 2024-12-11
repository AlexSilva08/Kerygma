import serial
import time
import os
import subprocess
import pandas as pd
import glob

baud = 9600

porta1 = "COM10" #Enviar dados para essa porta

ard1 = serial.Serial(porta1, baud, timeout=0.01, writeTimeout=3) #Enviar dados para essa porta

os.startfile("Project1\FileName.exe")  #Executa o programa de coleta de dados

time.sleep(1) #Espera 1 segundo para o programa abrir e se conectar

ard1.write(str.encode('#andre6')) # Nome do arquivo em que será salvo os dados (precisa ter o # antes)
time.sleep(1) # Espera 1 segundo para o arquivo ser criado
ard1.write(str.encode('I 0 0 0')) #Inicia a coleta



list_of_files = glob.glob('*.tsv') # * means all if need specific format then *.csv
latest_file = max(list_of_files, key=os.path.getctime)

start = time.time()
nDados = 0

time.sleep(1)

while (time.time() - start) < 2:

    valueSplit = valueRead.split(b",")

    valueRead = ard1.readline()



ard1.write(str.encode('F 0 0 0')) #Interrompe a coleta

time.sleep(1) #Espera 1 segundo para coletar todos os dados

if len(valueSplit) == 20:

        df = pd.read_csv(latest_file, sep='\t')
        NLinhas = len(df)
        Dado = df.iloc[(NLinhas - 2)].to_string(header=False,index=False)

print("ReadArquiv ", valueRead)


ard1.close() #Fecha a conexão com o Teensy
subprocess.call("taskkill /f /im WindowsTerminal.exe", shell=True) #Fecha programa de coleta