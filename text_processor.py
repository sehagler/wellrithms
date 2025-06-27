# -*- coding: utf-8 -*-
"""
Created on Mon Jun 23 10:14:10 2025

@author: sehag
"""

from fuzzywuzzy import process
import os
import numpy as np
import pandas as pd

#
class Text_processor_object(object):
    
    #
    def __init__(self):
        self.df = None
        self.groups_df = None
    
    #
    def _get_unique_arr(self, column_name):
        unique_arr = self.df[column_name].unique()
        idxs = np.where(unique_arr == '')
        unique_arr = np.delete(unique_arr, idxs)
        unique_arr = np.sort(unique_arr)
        return unique_arr
    
    #
    def _replace_with_shortest_name_match_in_list(self, x, args):
        idxs = [i for i, char in enumerate(x) if char == ' ']
        if len(idxs) > 0:
            y_list = self._get_unique_arr(args)
            matching_startswith = [y for y in y_list if x.startswith(y)]
            matching_endswith = [y for y in y_list if x.endswith(y)]
            matching_items = matching_startswith + matching_endswith
            matching_items.append(x)
            matching_items = list(set(matching_items))
            shortest_match = min(matching_items, key=len)
        else:
            shortest_match = x
        return shortest_match
    
    #
    def _replace_with_single_name_match_in_list(self, x, args):
        idxs = [i for i, char in enumerate(x) if char == ' ']
        if len(idxs) > 0:
            unique_arr = self._get_unique_arr(args)
            y_list = []
            for y in unique_arr:
                idxs = [i for i, char in enumerate(y) if char == ' ']
                if len(idxs) == 0:
                    y_list.append(y)
            matching_items = [y for y in y_list if y in x]
            matching_items = list(set(matching_items))
            if len(matching_items) > 1:
                longest_match = max(matching_items, key=len)
            else:
                longest_match = x
        else:
            longest_match = x
        return longest_match
    
    #
    def _replace_with_longest_common_startswith(self, x, args):
        idxs = [i for i, char in enumerate(x) if char == ' ']
        if len(idxs) > 0:
            unique_arr = self._get_unique_arr(args)
            unique_arr_tmp = unique_arr.copy()
            idxs = np.where(unique_arr_tmp == x)
            unique_arr_tmp = np.delete(unique_arr_tmp, idxs)
            y_list = []
            for y in unique_arr_tmp:
                idxs = [i for i, char in enumerate(y) if char == ' ']
                if len(idxs) > 0:
                    idxs.append(len(y))
                    idxs = sorted(idxs)
                    for i in range(len(idxs)):
                        y_list.append(y[:idxs[i]])
            y_list = list(set(y_list))   
            matching_items = [y for y in y_list if y in x]
            matching_items = list(set(matching_items))
            if len(matching_items) > 0:
                longest_match = max(matching_items, key=len)
            else:
                longest_match = x
        else:
            longest_match = x
        return longest_match
    
    #
    def assign_to_group(self, column_name_0, column_name_1, column_name_2):
        group_arr = self._get_unique_arr(column_name_0)
        group_list = group_arr.tolist()
        assigned_groups = []
        assigned_scores = []
        for idx, row in self.df.iterrows():
            item_text = row[1]
            assigned_group = process.extractOne(item_text, group_list)
            assigned_groups.append(assigned_group[0])
            assigned_scores.append(assigned_group[1])
        self.df[column_name_1] = assigned_groups
        self.df[column_name_2] = assigned_scores
                
    #
    def cleanup_white_space(self, column_name):
        self.df[column_name] = \
            self.df[column_name].str.replace(r' +', ' ', regex=True)
        self.df[column_name] = \
            self.df[column_name].str.replace(r'^ +', '', regex=True)
        self.df[column_name] = \
            self.df[column_name].str.replace(r' +$', '', regex=True)
        
    #
    def display_data_frame(self):
        print(self.df)
        
    #
    def display_unique(self, column_name):
        unique_arr = self._get_unique_arr(column_name)
        print(unique_arr)
        print(len(unique_arr))
        
    #
    def generate_groups_data_frame(self, column_name):
        group_arr = self._get_unique_arr(column_name)
        assign_arr = self.df['assigned_group']
        num_assigned = []
        group_list = list(group_arr)
        assign_list = list(assign_arr)
        for i in range(len(group_list)):
            num_assigned.append(str(assign_list.count(group_list[i])))
        self.group_df = pd.DataFrame(group_arr)
        self.group_df.columns = ['extracted_groups']
        self.group_df['num_assigned'] = num_assigned
        
    #
    def read_data_from_xls(self, column_name, path, filename):
        self.df = pd.read_excel(os.path.join(path, filename), header=None)
        self.df.columns = [column_name]
        
    #
    def reduce_to_shortest_name_matches(self, column_name_0, column_name_1):
        self.df[column_name_1] = \
            self.df[column_name_0].apply(self._replace_with_shortest_name_match_in_list,
                                         args = ([column_name_0]))
        
    #
    def reduce_to_single_name_matches(self, column_name_0, column_name_1):
        self.df[column_name_1] = \
            self.df[column_name_0].apply(self._replace_with_single_name_match_in_list,
                                         args = ([column_name_0]))
            
    #
    def reduce_to_longest_common_startswith(self, column_name_0, column_name_1):
        self.df[column_name_1] = \
            self.df[column_name_0].apply(self._replace_with_longest_common_startswith,
                                         args = ([column_name_0]))
        
    #
    def trim_tails(self, column_name_0, column_name_1):
        self.df[column_name_1] = \
            self.df[column_name_0].str.replace(r'(?<=\s)[A-Z\-]*[0-9].*$', '',
                                            regex=True)
            
    #
    def write_to_excel(self, path, filename):
        with pd.ExcelWriter(os.path.join(path, filename)) as writer:
            self.df.to_excel(writer, index=False,
                             sheet_name='group_assignments') 
            self.group_df.to_excel(writer, index=False, sheet_name='groups') 