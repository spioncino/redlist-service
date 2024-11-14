import re
import pandas as pd
import numpy as np
import os

# ������� ��� ������ � ���������� ������ �� ����������� ���������
def find_re(pattern, text):
    match = re.search(pattern, text)
    return match.group(1).strip() if match else None

# ������� ��� �������� ���������� � ������ ���� �� ������
def parse_animal(text):
    animal_data = {}

    # ���������� ��������� ��� ��������� �����
    regex_patterns = {
        "�������� �� �������": r'\s([�-ߨ\s\/-/,]{5,})',
        "�������": r'�������\s([\w\s/,�/-]+)\s�',
        "���������": r'���������\s([\w\s/,�/-]+)\s�',
        "������": r'������\.\s(.+?)\x1f',
        "���������������": r'���������������\.\s(.+?)\x1f',
        "�����������": r'�����������\.\s(.+?)\x1f',
        "����������� ��������": r'����������� ��������\.\s(.+?)\x1f',
        "������������ �������": r'������������ �������\.\s(.+?)\x1f',
        "�������� ���� ������": r'�������� ���� ������\.\s(.+?)\x1f',
        "��������� ��������� ����": r'��������[��] ��������� ����\.\s(.+?)\x1f',
        "����������� ����������� �� ���������� ����": r'����������� ����������� �� ���������� ����\.\s(.+?)\x1f',
        "��������� ����������": r'��������� ����������\.\s(.+?)\x1f'
    }
    
    # ����� ���������� �� ������� ����������� ���������
    for key, pattern in regex_patterns.items():
        animal_data[key] = find_re(pattern, text)

    return animal_data

# ������� ��� ��������� ���������� ����� � ���������� ��� � Excel
def parse_text_file_to_excel(file_path, output_excel_path):
    with open('PythonParserAnimals\\' + file_path, "r", encoding="utf-8") as file:
        text = file.read()

    # ������� ������ �� ������ �������� � ����������
    text = text.replace("- ", "")
    stop_words = ['��������', '�������������', '����', '�����', '�������������� � �����������', '��������������', 
                  '���������� ��������', '�������� � �����', '����������', '���������', '���������', '�����']
    for word in stop_words:
        text = re.sub(r'\n' + re.escape(word) + r'\n', '\n', text)

    text = re.sub(r'\n\d+\n{1,3}', '\n', text)
    text = re.sub(r'����:\s.+\n', '\n', text)

    # ���������� ������ �� ����� ��� ������� ���������
    animals = re.split(r'�����[�]?\:\s.+?\n', text)[:-1]
    animal_list = [parse_animal(animal.replace("\n", " ")) for animal in animals]

    # �������������� ������ � DataFrame � ���������� � Excel
    df = pd.DataFrame(animal_list)
    df = df.replace("", None)
    df.to_excel(output_excel_path, index=False)

# ������ ��������� ������ ��� �������� � �� ��������������� �������� Excel-������
text_files = [
    ('Animal.txt', 'animals_table.xlsx', '�������������'),
    ('Bird1.txt', 'bird1_table.xlsx', '�����'),
    ('Bird2.txt', 'bird2_table.xlsx', '�����'),
    ('Amphibians.txt', 'amphibians_table.xlsx', '�������������� � �����������'),
    ('Fish.txt', 'fish_table.xlsx', '����'),
    ('Invertebrates1.txt', 'invertebrates1_table.xlsx', '��������������'),
    ('Invertebrates2.txt', 'invertebrates2_table.xlsx', '��������������'),
    ('Invertebrates3.txt', 'invertebrates3_table.xlsx', '��������������'),
    ('Invertebrates4.txt', 'invertebrates4_table.xlsx', '��������������'),
    ('Invertebrates5.txt', 'invertebrates5_table.xlsx', '��������������'),
    ('Vascular_plants1.txt', 'vascular_plants1_table.xlsx', '���������� ��������'),
    ('Vascular_plants2.txt', 'vascular_plants2_table.xlsx', '���������� ��������'),
    ('Mossy.txt', 'mossy_table.xlsx', '����������'),
    ('Seaweed.txt', 'seaweed_table.xlsx', '���������'),
    ('Lichens.txt', 'lichens_table.xlsx', '���������'),
    ('Mushrooms.txt', 'mushrooms_table.xlsx', '�����')
]

# ������� ��������� ������ � �������� ������������� Excel-������
for text_file, output_excel, section_name in text_files:
    parse_text_file_to_excel(text_file, output_excel)
    print(f'Parsed {text_file} and saved to {output_excel}')

# ������� ��� ���������� �������� ������������� � ����������� ������
def prepare_table(file_path, section_name, extra_cols):
    df = pd.read_excel(file_path)
    df.insert(1, '������', section_name)
    for col_name, col_value in extra_cols:
        df[col_name] = col_value
    return df

# ���������� � ������ � ��������������� ������
files_info = [
    ('animals_table.xlsx', '�������������', [('�������', np.nan), ('�����', np.nan)]),
    ('bird1_table.xlsx', '�����', [('�������', np.nan), ('�����', np.nan)]),
    ('bird2_table.xlsx', '�����', [('�������', np.nan), ('�����', np.nan)]),
    ('amphibians_table.xlsx', '�������������� � �����������', [('�������', np.nan), ('�����', np.nan)]),
    ('fish_table.xlsx', '����', [('�������', np.nan), ('�����', np.nan)]),
    ('invertebrates1_table.xlsx', '��������������', [('�������', np.nan), ('�����', np.nan)]),
    ('invertebrates2_table.xlsx', '��������������', [('�������', np.nan), ('�����', np.nan)]),
    ('invertebrates3_table.xlsx', '��������������', [('�������', np.nan), ('�����', np.nan)]),
    ('invertebrates4_table.xlsx', '��������������', [('�������', np.nan), ('�����', np.nan)]),
    ('invertebrates5_table.xlsx', '��������������', [('�������', np.nan), ('�����', np.nan)]),
    ('vascular_plants1_table.xlsx', '���������� ��������', [('�����', np.nan), ('�����', np.nan)]),
    ('vascular_plants2_table.xlsx', '���������� ��������', [('�����', np.nan), ('�����', np.nan)]),
    ('mossy_table.xlsx', '����������', [('�����', np.nan), ('�����', np.nan)]),
    ('seaweed_table.xlsx', '���������', [('�����', np.nan), ('�������', np.nan)]),
    ('lichens_table.xlsx', '���������', [('�����', np.nan), ('�����', np.nan)]),
    ('mushrooms_table.xlsx', '�����', [('�����', np.nan), ('�����', np.nan)])
]

# ����������� ���� ������ � ���� �������
combined_df = pd.DataFrame()
for file_path, section_name, extra_cols in files_info:
    df = prepare_table(file_path, section_name, extra_cols)
    combined_df = pd.concat([combined_df, df], ignore_index=True)

# ���������� ����������� ������� � Excel
combined_df.to_excel('Concat_table.xlsx', index=False)
print("All files combined and saved to Full_table.xlsx")