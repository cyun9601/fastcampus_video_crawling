from modules.tree import *
import urllib.request
import os 
import multiprocessing
import pandas as pd
from modules.utils import load_config
import numpy as np 
from multiprocessing import Pool
from tqdm.auto import tqdm
import threading 

def download_videos(df, save_dir, func, n_thread = None):
    df['save_dir'] = save_dir
    df_split = np.array_split(df, n_thread)
    
    thread_list = []
    for i in range(n_thread):
        thread_list.append(threading.Thread(target=func, args=(df_split[i],)))
    for i in range(n_thread):
        thread_list[i].start()
    
    return pd.concat(df_split)
    
def download_video(data):
    data['download_TF'] = False
    for index, row in tqdm(data.iterrows(), total = len(data)):
        row = row.fillna('')
        save_dir = os.path.join(row['save_dir'], row['parent.parent.title'], row['parent.title'])
        os.makedirs(save_dir, exist_ok=True)
        
        ## 영상 다운          
        # print('download : ', row.url, 'to', save_dir, '...')
        urllib.request.urlretrieve(row.url, os.path.join(save_dir, row['title'] + '.mp4'))
        data.loc[index, 'download_TF'] = True
    
if __name__ == '__main__':

    PRJ_DIR = os.path.dirname(os.path.realpath(__file__))
    os.chdir(PRJ_DIR)

    # config 
    CONFIG_PATH = os.path.join(PRJ_DIR, 'config/download.yaml')
    args = load_config(CONFIG_PATH)
    
    if args.n_thread == None:
        args.n_thread = multiprocessing.cpu_count()
    
    df = pd.read_excel(os.path.join(PRJ_DIR, 'result.xlsx'))
    
    df = download_videos(df, args.save_dir, download_video, args.n_thread)