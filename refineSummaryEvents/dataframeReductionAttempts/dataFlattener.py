import pandas as pd
import os
import json
import time


def main():
    start_time = time.time()
    file_paths = generate_file_list()
    dfs = traverse_all_jsons(file_paths)
    complete_time = time.time()
    print(f"Time: {complete_time -start_time} seconds")
    print(f"Number of dataframes: {len(dfs)}")
    print(f"Time per file, not accounting for : {(complete_time -start_time)/len(dfs)} seconds")



def generate_file_list():
    folder_path = '../data'

    file_paths = []

    # Walk through the folder and its subdirectories
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            chosen_path = os.path.join(root, file)
            chosen_path.replace('\\', '/')
            file_paths.append(chosen_path)

    return file_paths

def traverse_all_jsons(file_paths:list) -> list:
    dfs = []
    for json_file_path in file_paths:
        with open(json_file_path, 'r') as j:
            contents = json.loads(j.read())
        nested_df =pd.json_normalize(contents)
        dfs.append(nested_df)
    
    return dfs


if __name__ == '__main__':
    main()