# -*- coding: utf-8 -*-
"""
Created on Mon Jun 23 10:36:53 2025

@author: sehag
"""

from image_processor import Image_processor_object
from text_processor import Text_processor_object

data_path = 'data'
output_filename = 'output.xlsx'
pdf_filename = 'WellRithms MLE Take Home Assessment.pdf'
xlsx_filename = 'WellRithms_Text_MLE.xlsx'

'''
Task 1
1. You have been provided with the text in the Excel file.
2. We need to process and clean the data and identify specific groups which we can
group items together.
3. How many items are in the Excel file? How many groups have you identified?
4. Please return a table with the items, their corresponding groups and score of how
likely items fit into that group.
'''

if False:
    text_processor = Text_processor_object()
    text_processor.read_data_from_xls('raw_text', data_path, xlsx_filename)
    text_processor.trim_tails('raw_text', 'trimmed_text')
    text_processor.cleanup_white_space('trimmed_text')
    text_processor.reduce_to_shortest_name_matches('trimmed_text', 'extracted_group')
    text_processor.cleanup_white_space('extracted_group')
    text_processor.reduce_to_single_name_matches('extracted_group', 'extracted_group')
    text_processor.cleanup_white_space('extracted_group')
    text_processor.reduce_to_longest_common_startswith('extracted_group', 'extracted_group')
    text_processor.cleanup_white_space('extracted_group')
    text_processor.reduce_to_shortest_name_matches('extracted_group', 'extracted_group')
    text_processor.cleanup_white_space('extracted_group')
    text_processor.reduce_to_single_name_matches('extracted_group', 'extracted_group')
    text_processor.cleanup_white_space('extracted_group')
    text_processor.assign_to_group('extracted_group', 'assigned_group', 'assignment_score')
    text_processor.generate_groups_data_frame('extracted_group')
    text_processor.write_to_excel(data_path, output_filename)

'''
Task 2:
1. You have been provided with 3 images.
2. We need to process each image using Python. For each image, we need to return a
table in pandas for a further analysis.
3. Once the table is returned, how will you further process and clean the data? Please
return the cleaned data.
'''

if True:
    image_processor = Image_processor_object()
    image_processor.read_data_from_pdf(data_path, pdf_filename)
    image_processor.create_np_arrays()
    image_processor.make_images_black_and_white()
    image_processor.remove_vertical_lines_from_images()
    image_processor.remove_horizontal_lines_from_images()
    image_processor.ocr_images()
    image_processor.display_images()
    image_processor.save_cleaned_images(data_path)