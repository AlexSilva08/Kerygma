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

Dados_CopX = [0]
Dados_CopY = [0]
Dados_Tempo = [0]


start = time.time()

while (time.time() - start) < 2:

    valueRead = ard1.readline()

    valueSplit = valueRead.split(b",")

    print(valueRead)

    if len(valueSplit) == 20:

        P0 = float(valueSplit[12])
        P1 = float(valueSplit[13])
        P2 = float(valueSplit[14])
        P3 = float(valueSplit[15])

        P4 = float(valueSplit[16])
        P5 = float(valueSplit[17])
        P6 = float(valueSplit[18])
        P7 = float(valueSplit[19])

        X = float(valueSplit[1])
        Y = float(valueSplit[2])

        T = time.time() - start

        DxP0= 16.8
        DyP0= 16
        DxP1= 3.4
        DyP1= 16.5
        DxP2= 3.4
        DyP2= 16
        DxP3= 17
        DyP3= 16

        DxP4= 3.5
        DyP4= 16
        DxP5= 17
        DyP5= 15.5
        DxP6= 17
        DyP6= 16
        DxP7= 3.8
        DyP7= 16

        if (P0+P1+P2+P3+P4+P5+P6+P7) > 0:
            CopX = (P4*DxP4 + P5*DxP5 + P6*DxP6 + P7*DxP7 - P0*DxP0 - P1*DxP1 - P2*DxP2 - P3*DxP3)/(P0+P1+P2+P3+P4+P5+P6+P7)
        else:
            CopX = 0

        if (P0+P2+P4+P6) > 0:
            CopY = (P0*DyP0 + P1*DyP1 + P4*DyP4 + P5*DyP5 - P2*DyP2 - P3*DyP3 - P6*DyP6 - P7*DyP7)/(P0+P1+P2+P3+P4+P5+P6+P7)
        else:
            CopY = 0

        Dados_CopX.append(CopX)
        Dados_CopY.append(CopY)
        Dados_Tempo.append(T)


ard1.write(str.encode('F 0 0 0')) #Interrompe a coleta


time.sleep(1) #Espera 1 segundo para coletar todos os dados

ard1.close() #Fecha a conexão com o Teensy
subprocess.call("taskkill /f /im WindowsTerminal.exe", shell=True) #Fecha programa de coleta

print(str(Dados_CopX) + " " + str(Dados_CopY) + " " + str(Dados_Tempo))

