# -*- coding: utf-8 -*-
"""
Created on Mon Jun 23 10:43:53 2025

@author: sehag
"""

import cv2
from doctr.models import ocr_predictor
from doctr.io import DocumentFile
import fitz
import numpy as np
import os
import pandas as pd

#
class Image_processor_object(object):
    
    #
    def __init__(self):
        self.thresh = 200
        self.img_dict = {}
        
    #
    def create_np_arrays(self):
        for key in self.img_dict.keys():
            np_arr = np.frombuffer(self.img_dict[key]['raw_img_bytes'],
                                   np.uint8)
            img_np = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)
            self.img_dict[key]['raw_img_np'] = img_np
            self.img_dict[key]['processed_img_np'] = img_np.copy()
        
    #
    def display_images(self):
        for key in self.img_dict.keys():
            if 'raw_img_np' in self.img_dict[key].keys():
                cv2.imshow('Raw Image ' + key,
                           self.img_dict[key]['raw_img_np'])
            if 'processed_img_np' in self.img_dict[key].keys():
                cv2.imshow('Processed Image ' + key,
                           self.img_dict[key]['processed_img_np'])
            if 'extracted_text' in self.img_dict[key].keys():
                print(self.img_dict[key]['extracted_text'])
            cv2.waitKey(0)
        cv2.destroyAllWindows()
        
    #
    def generate_data_frames(self):
        for key in self.img_dict.keys():
            img_df = pd.DataFrame(self.img_dict[key]['processed_img_np'])
            self.img_dict[key]['processed_img_df'] = img_df
            
    #
    def make_images_black_and_white(self):
        for key in self.img_dict.keys():
            self.img_dict[key]['processed_img_np'] = \
                cv2.cvtColor(self.img_dict[key]['processed_img_np'],
                             cv2.COLOR_BGR2GRAY)
            self.img_dict[key]['processed_img_np'] = \
                cv2.threshold(self.img_dict[key]['processed_img_np'], 
                              self.thresh, 255, cv2.THRESH_BINARY)[1]
                
    #
    def ocr_images(self):
        img_file_tmp = 'image_tmp.png'
        model = \
            ocr_predictor(det_arch='db_resnet50', reco_arch='crnn_vgg16_bn',
                          pretrained=True)
        for key in self.img_dict.keys():
            cv2.imwrite(img_file_tmp, self.img_dict[key]['processed_img_np'])
            doc = DocumentFile.from_images(img_file_tmp)
            result = model(doc)
            self.img_dict[key]['extracted_text'] = result.export()
        
    #
    def read_data_from_pdf(self, path, filename):
        doc = fitz.open(os.path.join(path, filename))
        img_idx = 0
        for i in range(len(doc)):
            if i != 0:
                page = doc[i]
                img_list = page.get_images(full=True)
                for img_index, img in enumerate(img_list):
                    base_img = doc.extract_image(img[0])
                    self.img_dict[str(img_idx)] = {}
                    self.img_dict[str(img_idx)]['raw_img_bytes'] = \
                        base_img['image']
                    self.img_dict[str(img_idx)]['raw_img_ext'] = base_img['ext']
                    img_idx += 1
        doc.close()
        
    #
    def remove_horizontal_lines_from_images(self):
        horizontal_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (40,1))
        for key in self.img_dict.keys():
            thresh = cv2.threshold(self.img_dict[key]['processed_img_np'], 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]
            remove_horizontal = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, horizontal_kernel, iterations=2)
            cnts = cv2.findContours(remove_horizontal, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            cnts = cnts[0] if len(cnts) == 2 else cnts[1]
            for c in cnts:
                cv2.drawContours(self.img_dict[key]['processed_img_np'], [c], -1, (255,255,255), 5)
                
    #
    def remove_vertical_lines_from_images(self):
        vertical_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (1,40))
        for key in self.img_dict.keys():
            thresh = cv2.threshold(self.img_dict[key]['processed_img_np'], 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]
            remove_vertical = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, vertical_kernel, iterations=2)
            cnts = cv2.findContours(remove_vertical, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            cnts = cnts[0] if len(cnts) == 2 else cnts[1]
            for c in cnts:
                cv2.drawContours(self.img_dict[key]['processed_img_np'], [c], -1, (255,255,255), 5)
                
    #
    def save_cleaned_images(self, path):
        for key in self.img_dict.keys():
            filename = 'image_' + key + '.png'
            cv2.imwrite(os.path.join(path, filename),
                        self.img_dict[key]['processed_img_np'])