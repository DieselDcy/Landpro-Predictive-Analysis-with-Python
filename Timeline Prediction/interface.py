#!/usr/bin/env python
# coding: utf-8

import streamlit as st
import pandas as pd
import numpy as np
import pickle
import matplotlib.pyplot as plt
import datetime
from sklearn.metrics import precision_score
import matplotlib.pyplot as plt
#import plotly.figure_factory as ff

# =======================================================
# display data
st.header('1. Explore the dataset')
data = pd.read_csv('streamlitdata.csv')
data = data.iloc[:,1:]

rows = st.number_input("",min_value = 0,value = 5)
if rows>0:
    st.dataframe(data.head(rows))
    
# Draw the line plot
st.write('Bar chart of Historical Timeline:')
#fig = ff.create_distplot([data['time']], group_labels = ['time difference between creation date and sales date'], bin_size=2500)
#st.plotly_chart(fig, use_container_width=True)
#fig, ax = plt.subplots()
#ax.hist(data['time'], bins=20)
#st.bar_chart(data=data['time'], width=0, height=0, use_container_width=True)

fig, ax = plt.subplots()
ax.hist(data['time'], bins=15)
st.pyplot(fig)

#fig,ax = plt.subplots()
#ax.boxplot(np.array(data[['EquipmentAmount','NetCost','time']]))
#st.pyplot(fig)

st.write('')
st.write('')
st.header('2. Timeline prediction model')
# Select the input values of the features.
st.sidebar.subheader("Input values: ")
st.sidebar.write('1.Equipment Amount')
EquipmentAmount = st.sidebar.number_input("Select the value of Equipment Amount:", min_value = 0, value = 9257)
st.sidebar.write('2.Net Cost')
NetCost = st.sidebar.number_input("Select the value of Net Cost:", min_value = 0, value = 15233)
st.sidebar.write('3.Dealer State')
DealerState_OH = st.sidebar.selectbox('Select 1 if the Dealer State is OH:',options = np.array([0,1])).astype(int)
DealerState_PA = st.sidebar.selectbox('Select 1 if the Dealer State is PA:',options = np.array([0,1])).astype(int)
Sum_DealerState = DealerState_OH + DealerState_PA

if Sum_DealerState==0 | Sum_DealerState == 1:
    st.sidebar.write('')
else:
    st.sidebar.write('Please select the correct Dealer State.')
 
st.sidebar.write('4.Equipment Type')
EquipmentType_Configurator_NewEquipmentConfiguration = st.sidebar.selectbox('Select 1 if the Equipment Type is Configurator - New Equipment Configuration:',options = np.array([0,1])).astype(int)
EquipmentType_DealerCollateral_NewInventory = st.sidebar.selectbox('Select 1 if the Equipment Type is Dealer Collateral - New Inventory:',options = np.array([0,1])).astype(int)
EquipmentType_DealerBusinessSystem = st.sidebar.selectbox('Select 1 if the Equipment Type is Dealer business system:',options = np.array([0,1])).astype(int)
EquipmentType_FreeformEntry_NotFromAnyExternalSources = st.sidebar.selectbox('Select 1 if the Equipment Type is Freeform Entry - Not from any External Sources:',options = np.array([0,1])).astype(int)
EquipmentType_JDSC_Equipment = st.sidebar.selectbox('Select 1 if the Equipment Type is JDSC Equipment:',options = np.array([0,1])).astype(int)
EquipmentType_UsedEquipment_UsedInventory = st.sidebar.selectbox('Select 1 if the Equipment Type is Used Inventory - Used Inventory:',options = np.array([0,1])).astype(int)
EquipmentType_e_Valuator = st.sidebar.selectbox('Select 1 if the Equipment Type is e-Valuator:',options = np.array([0,1])).astype(int)

Sum_EquipmentType = EquipmentType_Configurator_NewEquipmentConfiguration+EquipmentType_DealerCollateral_NewInventory+EquipmentType_DealerBusinessSystem+EquipmentType_FreeformEntry_NotFromAnyExternalSources+EquipmentType_JDSC_Equipment+EquipmentType_UsedEquipment_UsedInventory+EquipmentType_e_Valuator

if Sum_EquipmentType==0 | Sum_EquipmentType == 1:
    st.sidebar.write('')
else:
    st.sidebar.write('Please input the correct equipment type.')

st.sidebar.write('5. Base Model or Implement Model')
BaseImplement_Implement = st.sidebar.selectbox('Select 1 if the machine is an Implement model, and select 0 if the machine is a Base model.',options = np.array([0,1])).astype(int)

# # Load the model.
filename = 'finalized_model.sav'
with open(filename, 'rb') as f:
    loaded_model = pickle.load(f)
    
x = pd.DataFrame([[EquipmentAmount,NetCost,DealerState_OH,DealerState_PA,EquipmentType_Configurator_NewEquipmentConfiguration,EquipmentType_DealerCollateral_NewInventory,EquipmentType_DealerBusinessSystem,EquipmentType_FreeformEntry_NotFromAnyExternalSources,EquipmentType_JDSC_Equipment,EquipmentType_UsedEquipment_UsedInventory,EquipmentType_e_Valuator,BaseImplement_Implement]])

y = loaded_model.predict(x)



st.write('* Time difference refers to the difference between sales date and creation date. Our prediction accuracy based on the historical model is 40%.')

st.write('* The timeline variable is correlated with 5 core features: Equipment Amount, Net Cost, Dealer State, Equipment Type, and whether the equipment is a base model or implement model.')

st.write('* The details are shown in the sidebar, and you could input values of a specific quote to attain the predictive outcome as followed.')

#st.write('Based on the quote information you inputed, the predicted time difference between sales date and creation date is',y)

#a = st.date_input(value=(datetime(2020, 1, 1), datetime(2030, 1, 1)))
#st.sidebar.date_input('Quote Creation date', datetime.date(2011,1,1))
#CreationDate = st.date_input('Quote Creation date', datetime.date(2011,1,1))
#st.write('With the quote creation date of',CreationDate,'We predict that the sales date for this quote would be',y,'days after the creation date',CreationDate,'.')
st.header('3. Prediction Outcome')
st.caption('For example, if the creation date for the quote is 2021-09-01 and the sales date for the quote is 2021-09-05, then we indicate that there are 5 days of time difference.')
st.write('Based on the quote information you inputted and the timeline predictive model, we estimate that the sales date for this quote would be',y,'days after the creation date.')

if Sum_DealerState==0 | Sum_DealerState == 1:
    st.write('')
else:
    st.write('* **Warning**: The Dealer State is not inputted correctly. The prediction result of the timeline model could result in biased value. Please follow the instruction on the sidebar to input the specific **_Dealer State_**!')
               
if Sum_EquipmentType==0 | Sum_EquipmentType == 1:
    st.write('')
else:
    st.write('* **Warning**: The Equipment Type is not inputted correctly. The prediction result of the timeline model could result in biased value.Please follow the instruction on the sidebar to input the specific **_Equipment Type_**!')

