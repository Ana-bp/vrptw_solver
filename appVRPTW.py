import streamlit as st 
import pandas as pd
from VRPTW_functions import read_file, coordinates_list, timetoseconds,convert_df,gantt
from VRPTW_main import VRPTWmain 
import plotly.figure_factory as ff
import plotly.express as px


df_address_aux = pd.DataFrame()

if 'flag' not in st.session_state:
    st.session_state["flag"]=0
if 'aux_coord_list' not in st.session_state:
    st.session_state['aux_coord_list']=[]
if 'original_df' not in st.session_state:
    st.session_state['original_df']=pd.DataFrame()
if 'copy_original_df' not in st.session_state:
    st.session_state['copy_original_df']=pd.DataFrame()
if 'teste_df' not in st.session_state:
    st.session_state['teste_df']=pd.DataFrame()
    


st.title("Vehicle Routing Website")

st.session_state["vehicles"] = st.number_input ("Quantity of available vehicles:",0,None, "min",1)
st.session_state["vehicles_capacity"] = st.number_input ("Vehicles capacity",0,None, "min",1)

"Upload your file"

address_file = st.file_uploader("Select a file", type=["csv"])

if address_file is not None:
    st.subheader("File content:")
    st.session_state['original_df'] = pd.read_csv(address_file,sep=';', encoding='ISO 8859-1')
    
    st.write("View CSV file:")
    st.write(st.session_state['original_df'])
    
    address_file.seek(0)

if st.button("Fill in coordinates"):
    st.session_state["df_address_aux"] = read_file(st.session_state['original_df'])
    #st.write(list( st.session_state["df_address_aux"].columns))
    updated_df, st.session_state["aux_coord_list"] = coordinates_list( st.session_state["df_address_aux"])
    st.session_state['copy_original_df']= st.session_state['original_df'].copy()
    st.session_state['copy_original_df']['lat']=updated_df['lat']
    st.session_state['copy_original_df']['long']=updated_df['long']
    st.write(st.session_state['copy_original_df'])
    st.session_state["flag"] = 1
    csv_coordinates = convert_df(st.session_state['copy_original_df'])
    st.download_button("Download file",csv_coordinates,"Address w/coordinates.csv","text/csv",key='download-csv')


if st.button("Generate routes"):
    #st.write(list( st.session_state["df_address_aux"].columns))
    if st.session_state["flag"]:
        routes,final_df = VRPTWmain(st.session_state["df_address_aux"], st.session_state["aux_coord_list"], st.session_state["vehicles"], st.session_state["vehicles_capacity"])
        st.session_state['copy_original_df']['Hora chegada']=final_df['Hora chegada']
        st.session_state['copy_original_df']['Inicio atendimento']=final_df['Inicio atendimento']
        st.session_state['copy_original_df']['Fim atendimento']=final_df['Fim atendimento']
        st.session_state['copy_original_df']['Rota']=final_df['Rota']
        st.session_state['copy_original_df']['ordem']=final_df['ordem']
        st.write(routes)
        st.session_state['teste_df']=st.session_state['copy_original_df'].sort_values(['Rota','ordem'])
        st.write(st.session_state['teste_df'])
        csv_VRPTW = convert_df(st.session_state['copy_original_df'])
        st.download_button("Download file",csv_VRPTW,"Routes plan.csv","text/csv",key='download-csv')
    else:
        st.session_state["df_address_aux"] = read_file(st.session_state['original_df'])
        if st.session_state["df_address_aux"]['long'].isnull().any():
            st.error('Please make sure that all the coordinates were provided')
        else:
            for i in range(len(st.session_state["df_address_aux"]['lat'])):
                st.session_state["aux_coord_list"].append(str(st.session_state["df_address_aux"]['long'][i])+','+str(st.session_state["df_address_aux"]['lat'][i]))
            routes,final_df = VRPTWmain(st.session_state["df_address_aux"], st.session_state["aux_coord_list"], st.session_state["vehicles"], st.session_state["vehicles_capacity"])
            #st.write(st.session_state["aux_coord_list"])
            st.session_state['original_df']['Hora chegada']=final_df['Hora chegada']
            st.session_state['original_df']['Inicio atendimento']=final_df['Inicio atendimento']
            st.session_state['original_df']['Fim atendimento']=final_df['Fim atendimento']
            st.session_state['original_df']['Rota']=final_df['Rota']
            st.session_state['original_df']['ordem']=final_df['ordem']
            st.write(routes)
            st.session_state['teste_df']=st.session_state['original_df'].sort_values(['Rota','ordem'])
            st.write(st.session_state['teste_df'])
            csv_VRPTW = convert_df(st.session_state['original_df'])
            st.download_button("Download file",csv_VRPTW,"Routes plan.csv","text/csv",key='download-csv')


if st.button("Gantt Chart"):
    df_copy = st.session_state['teste_df'].rename(columns ={'Rota': 'Task', 'Hora chegada':'Start','Fim atendimento':'Finish'})

    st.write(df_copy)
    #fig = ff.create_gantt(df_copy, index_col='Nome',show_colorbar=True, bar_width=0.5,showgrid_x=True, showgrid_y=True)
    #gantt_aux = gantt (st.session_state['teste_df'])
    fig = px.timeline(df_copy, x_start="Start", x_end="Finish", y="Task", color="Nome")
    fig.update_layout(xaxis=dict(title='Timestamp', tickformat = '%H:%M'))
    fig.update_yaxes(autorange="reversed")
    fig.show()
    st.plotly_chart(fig)

if st.button("Google Maps link"):
    link_maps="https://www.google.com/maps/dir/"
    for i in range (len(st.session_state['teste_df'])):
        if i==0:
            link_maps = link_maps + st.session_state['teste_df']["Endereco"][i]+"+"+str(st.session_state['teste_df']["Numero"][i])+"+"+st.session_state['teste_df']["Bairro"][i]+"+"+st.session_state['teste_df']["Cidade"][i]+"+"+st.session_state['teste_df']["Estado"][i]+"+"+st.session_state['teste_df']["Pais"][i]+"/"
        else:
           link_maps = link_maps +"+"+ st.session_state['teste_df']["Endereco"][i]+"+"+str(st.session_state['teste_df']["Numero"][i])+"+"+st.session_state['teste_df']["Bairro"][i]+"+"+st.session_state['teste_df']["Cidade"][i]+"+"+st.session_state['teste_df']["Estado"][i]+"+"+st.session_state['teste_df']["Pais"][i]+"/" 
    final_link = link_maps.replace(" ","+")
    st.write(final_link)
    #st.write(f'<iframe src="https://stackoverflow.com/questions/73247210/how-to-plot-a-gantt-chart-using-timesteps-and-not-dates-using-plotly"></iframe>',unsafe_allow_html=True)
        











       
