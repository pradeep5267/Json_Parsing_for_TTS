#%%
import pandas as pd 
import numpy as np 
import json
import jsonschema
import os
#%%
os.chdir('/home/pradeep/Desktop/ambrapali_electrotech')
os.getcwd()
# %%
def read_json_file(filepath):
    with open(filepath,'r') as fhandle:
        json_data = json.load(fhandle)
    return json_data
#%%
def pass_1(json_data):
    '''
    pass_1 to get
    start-end time and speaker relation
    '''
    time_speaker_dict = {}
    pass_1 = json_data['speaker_labels']
    for idx, data in enumerate(pass_1):
        time_speaker_dict[idx] = [data['from'], data['to'], data['speaker']]
    return time_speaker_dict

#%%
########### pass_2 to get words and start-end timestamps ############
# timestamp_list[0][0] since its a list of list
def pass_2(json_data):
    '''
    pass_2 to get  
    start-end time and word relation
    '''
    time_word_dict = {}
    for results in json_data['results']:
        for timestamps in results['alternatives']:
            if ('timestamps' in timestamps.keys()):
                for idx,data in enumerate(timestamps['timestamps']):
                    time_word_dict[idx] = (data[1], data[2], data[0])

    return time_word_dict

#%%
def create_dataframe_from_dict(data_dict, columns):
    df = pd.DataFrame.from_dict(data=data_dict, orient='index', columns=columns)
    return df
#%%
def merge_dataframes(df1, df2, on_columns):
    df3 = pd.merge(df1, df2, on= on_columns)
    return df3
#%%
def create_sentence_list(df, target_speaker):
    speaker_sent_list = []
    speaker_sent_list = df[df.speaker ==  target_speaker].word.tolist()
    return speaker_sent_list
#%%
def merge_list_of_strings_to_string(sent_list):
    s = ' '.join(sent_list)
    return s

#%%
filepath = 'dataset/speechToText.json'

time_speaker_dict = {}

df1_columns = ['from','to','speaker']
df2_columns = ['from', 'to', 'word']
merge_columns = ['from', 'to']
#%%
json_data = read_json_file(filepath)
time_speaker_dict = pass_1(json_data)
time_word_dict = pass_2(json_data)
#%%
df1 = create_dataframe_from_dict(time_speaker_dict, df1_columns)
df2 = create_dataframe_from_dict(time_word_dict, df2_columns)
#%%
df_processed = merge_dataframes(df1, df2, merge_columns)
#%%
df_processed.head()
#%%
speaker_sent_1_list = create_sentence_list(df_processed, 0)
speaker_sent_2_list = create_sentence_list(df_processed, 1)
#%%
s1_sent = merge_list_of_strings_to_string(speaker_sent_1_list)
s2_sent = merge_list_of_strings_to_string(speaker_sent_2_list)
#%%
df_final = pd.DataFrame(columns=['speaker_1_sentence', 'speaker_2_sentence'])
df_final['speaker_1_sentence'] = [s1_sent]
df_final['speaker_2_sentence'] = [s2_sent]
df_final.head()
df_final.to_csv('./speaker_sentence.csv')

df_processed.to_csv('./speaker_timestamp_words.csv')
