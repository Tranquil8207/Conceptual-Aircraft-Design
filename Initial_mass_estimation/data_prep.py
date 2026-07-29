import numpy as np 
from client import build_client,fetch_data

client = build_client()
data = fetch_data(client)

def reformat_data(data):
    data_list = []
    for i in range(0,len(data),1):
        get_key = data[i]['empty_mass_kg']
        data_list.append(get_key)
    return data_list

def empty_weight_array(data_list):
    array_e_weight = np.array(data_list)
    return array_e_weight

def clean_up(array):
    cleaned_values = []
    for i in range(0,len(array),1):
        if array[i] is not None:
            cleaned_values.append(array[i])
    return cleaned_values

data_list = reformat_data(data)
array = empty_weight_array(data_list)
clean = clean_up(array)
print(len(clean))