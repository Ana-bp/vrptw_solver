import requests
import pandas as pd
import json
import csv
import codecs
from datetime import timedelta, datetime, time
import time
import plotly.figure_factory as ff

beggining=0

def read_file(df):
    
    df_address = df.drop(['Endereco','Numero','Bairro','Cidade','Estado','Pais'], axis=1)
    df_address.insert(1,'Endereco',df['Endereco'] + ', ' + df['Numero'].astype(str) + ', ' + df['Bairro'] + ', ' + df['Cidade'] + ', ' + df['Estado'] + ', ' + df['Pais'])

    return df_address



def timetoseconds(address_list):
    s_time = []
    e_time=[]
    print (list(address_list.columns))
    for i in range(len(address_list['Janela de tempo inicial'])):
        time_aux = address_list['Janela de tempo inicial'][i].split(':')
        h= int(time_aux[0])
        m= int(time_aux[1])
        hour_to_seconds = timedelta(hours=h,minutes=m)
        if i == 0:
            global beggining
            beggining= hour_to_seconds.seconds
        #print(hour_to_seconds)
        s_time.append((hour_to_seconds.seconds-beggining))

    for j in range(len(address_list['Janela de tempo final'])):
        time_aux = address_list['Janela de tempo final'][j].split(':')
        h= int(time_aux[0])
        m= int(time_aux[1])
        hour_to_seconds = timedelta(hours=h,minutes=m)
        e_time.append((hour_to_seconds.seconds-beggining))


    new_address_list = address_list.drop(['Janela de tempo inicial','Janela de tempo final'], axis=1)
    new_address_list.insert(4,'Inicio Janela',s_time)
    new_address_list.insert(5,'Fim Janela',e_time)

    return new_address_list

def secondstotime(seconds):
    now=datetime.now()
    date_time = now.strftime("%m/%d/%Y")
    #return (date_time + " " + time.strftime("%H:%M", time.gmtime(beggining+seconds))) 
    return ("1970-01-01" + " " + time.strftime("%H:%M", time.gmtime(beggining+seconds)))


def convert_df(df):
   return df.to_csv(index=False,sep=";").encode('utf-8')

def coordinates_list(df_address):
    
    url_path_addr = 'https://nominatim.openstreetmap.org/search?q='
    
            
    #criar uma função para os request na api (pra cada api), e condições para o user escolher qual api ele quer usar (so opensource, so google, ambos)
    #api_type = input ('Which API would you like to use?\n1- Open source\n2- Google\n3- Both')

    """if api_type == '2':
        ad_coordinates = google_api(df_address)
    else:"""
    ad_coordinates = opensource_api(df_address)

    return ad_coordinates


def opensource_api (df_address_1):

    url_path_addr = 'https://nominatim.openstreetmap.org/search?q='
    coordinates = []
    address_notfound = []
    df_address = df_address_1.copy()
    for h in range(len(df_address['Endereco'])):
        url_path_addr1 = url_path_addr + df_address['Endereco'][h] + '&format=jsonv2'
        json_coord = requests.get (url_path_addr1)
        if json_coord.json() != []:
            list_coord = json_coord.json()[0]
            coordinates.append(list_coord['lon'] + ',' + list_coord['lat'])
            df_address['lat'][h] = list_coord['lat']
            df_address['long'][h] = list_coord['lon']
        else:
            address_notfound.append(df_address['Endereco'][h])
            """if indicator ==  '1':
                address_notfound.append(df_address['Endereco'][h])
            if indicator == '3':
                google_coordinates = google_api(df_address['Endereco'][h])
                coordinates.append(google_coordinates)
            continue"""
        
        url_path_addr1 = ""    
    
    return df_address, coordinates
    


def get_timematrix(coordinates):

    list_distancies = []
    url_path_coord = 'http://router.project-osrm.org/table/v1/driving/'

    for i in range(len(coordinates)):
        if i == len(coordinates)-1:
            url_path_coord = url_path_coord + coordinates[i]
        else:
            url_path_coord = url_path_coord + coordinates[i] + ';'

    for j in range(len(coordinates)):
        url_path_coord1 = url_path_coord + '?sources=' + str(j)
        json_distancias = requests.get (url_path_coord1)
        list_distancies.append(json_distancias.json()['durations'][0])
        url_path_coord1 = ""

    df_distancies = pd.DataFrame(list_distancies)
    return df_distancies


def VRPTW (vehicles, capacity, new_address_list, timematrix):    
    arrival_time=0
    route_index=0
    all_routes = []
    all_visited = [0]
    df_final = new_address_list.copy()
    df_final[['Rota','Hora chegada','Inicio atendimento','Fim atendimento','ordem']]= ""
    

    #print(closest)
    while len(all_visited) < len(timematrix):
        route_index= route_index + 1
        sort_aux=0
        visited = [0]
        end_time=0
        start_time=0
        arrival_time=0
        client = 0
        demand = 0 

        for i in visited:
            closest = new_address_list['Fim Janela'][0]
            for j in range(len(timematrix)):
                    if new_address_list['Fim Janela'][j] != 0 and j not in all_visited :
                        if new_address_list['Fim Janela'][j] <= closest and (demand+new_address_list['Demanda'][j]<=capacity): #and ((end_time + distmatrix[i][j]) >= int(content_txt[j][3]) and (end_time + distmatrix[i][j]) <= int(content_txt[j][4])):
                            closest = new_address_list['Fim Janela'][j]
                            client = j
                            
            if client not in all_visited:
                visited.append(client) #lista de clientes visitados
                demand = demand + new_address_list['Demanda'][client]
                all_visited.append(client)
                arrival_time = end_time + timematrix[i][client]

                if arrival_time >= new_address_list['Inicio Janela'][client]:
                    start_time = arrival_time
                else:
                    start_time = new_address_list['Inicio Janela'][client]

                end_time = start_time + (new_address_list['Tempo de servico'][client])#*60 momento q o veiculo termina a entrega no cliente
                df_final['Hora chegada'][client]=secondstotime(arrival_time)
                df_final['Inicio atendimento'][client]=secondstotime(start_time)
                df_final['Fim atendimento'][client]=secondstotime(end_time)
                df_final['Rota'][client]=route_index
                sort_aux=sort_aux+1
                df_final['ordem'][client]=sort_aux

            else:
                break

            
        #if client == '':
        #   break

        all_routes.append(visited)

    df_final['Rota'][0]=0
   
    return all_routes,df_final

def gantt (df):
    df_copy = df.rename(columns ={'Rota': 'Task', 'Hora chegada':'Start','Fim atendmento':'Finish'})
    print (df_copy.columns)

    fig = ff.create_gantt(df_copy, index_col='Nome')

    
    return fig

