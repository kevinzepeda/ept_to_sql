import sqlite3
import pandas as pd
#from sqlalchemy import create_engine
conn = sqlite3.connect('db-ericsson.db')
#conn = create_engine('postgresql://postgres:root@localhost:5432/db')
sheet_names = ['EPT_3G_LTE_OUTDOOR','EPT_3G_LTE_INDOOR','PLAN_OUTDOOR','PLAN_INDOOR']
data = pd.read_excel('EPT_ATT_UMTS_LTE_2021-02-17.xlsx', sheet_name=sheet_names, usecols = "G,CQ,B,L,N,AU,BU,D")
for sheet in data:
    df = data[sheet]
    df['tab'] = sheet
    df['cvegeo'] = df['ID_state'].astype(str).str.zfill(2).astype(str) + df['ID_Country'].astype(str).str.zfill(3).astype(str)
    df.rename(columns={
    'Node_B_U2000':'node1', 
    'Node B U2000_Anterior':'node2',
    'AT&T_Node_Name':'node3',
    'RNC':'rnc', 
    'Vendor':'vendor',
    'AT&T_Tech':'tecnologia'
    }, inplace=True)
    df = df.drop_duplicates(subset=['node1', 'node2','node3','tecnologia'])
    df = df[['node1', 'node2', 'node3', 'cvegeo','rnc', 'vendor','tecnologia','tab']]
    df.to_sql(name='ept', con=conn, if_exists='append', index=False)