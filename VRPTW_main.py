import requests
import pandas as pd
import json
import csv
from datetime import timedelta, datetime, time
from VRPTW_functions import timetoseconds, get_timematrix, VRPTW

def VRPTWmain(address_list,coordinates, vehicles, vehicles_capacity):
    #address_filename = ['D:\Arquivos Usuário\Desktop\TCC - VRP\Atividade 4\MuitosClientes.csv','D:\Arquivos Usuário\Desktop\TCC - VRP\VRPTW - Solomon\25\C107.txt']
    #filename = 'D:\Arquivos Usuário\Desktop\TCC - VRP\Atividade 4\MuitosClientesteste.csv'
    


    #df_txt = read_txt(address_filename[1])
    #lista_endereços = le_dados_interface()
    #address_list = read_file(filename) 
    new_address_list= timetoseconds(address_list)
    #coordinates = coordinates_list(new_address_list)
    timematrix = get_timematrix(coordinates)
    VRPTW_opt,VRPTW_df = VRPTW(vehicles,vehicles_capacity,new_address_list,timematrix)

    return VRPTW_opt, VRPTW_df

            

    #http://router.project-osmr.org/route/v1/driving/13.388860,52.517037;13.397634,52.529407;13.428555,52.523219?overview=false
    #https://nominatim.openstreetmap.org/search?q= &format=jsonv2
