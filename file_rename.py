# -*- coding: utf-8 -*-
"""
Created on Sat Jun 22 21:24:18 2024

@author: amitc
"""

import os
import glob

Dir_path = 'C:/Users/amitc/Downloads/Malaria-Priyanka Roy/NIH-NLM-ThickBloodSmearsPV/NIH-NLM-ThickBloodSmearsPV/'
Dir_name = 'All_PvTk/'

full_path = glob.glob(os.path.join(Dir_path, Dir_name, '*/*'))

for path in full_path:
    base_name = os.path.basename(path)
    if "_" in base_name:
        new_base_name = base_name.replace("_", "")
        new_path = os.path.join(os.path.dirname(path), new_base_name)
        os.rename(path, new_path)
        #print(f"Renamed {base_name} to {new_base_name}")
