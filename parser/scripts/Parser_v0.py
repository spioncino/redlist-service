import re
import pandas as pd

# ������� ��� ������ � ���������� ������ �� ����������� ���������
def find_re(pattern, text):
    """
    ���� ����� �� ��������� ����������� ��������� � ���������� ������ ��������� ������.
    ���� ���������� �� �������, ���������� None.
    """
    match = re.search(pattern, text)
    return match.group(1).strip() if match else None

# �������� ������� ��� �������� ���������� � ������ ���� ���������
def parse_animal(text):
    """
    ��������� ���������� � �������� �� ���������� �����.
    ���������� ������� � ������� � ����, ������� ��������, ���������, ������ � ������ ����.
    """
    animal_data = {}

    # �������� �� ������� �����
    regex_name_rus = r'\s([�-ߨ\s\/-/,]{5,})'
    animal_data["�������� �� �������"] = find_re(regex_name_rus, text)

    # ������� (��������������� ���������)
    regex_order = r'�������\s([\w\s/,�/-]+)\s�'
    animal_data["�������"] = find_re(regex_order, text)

    # ��������� (��������������� ���������)
    regex_family = r'���������\s([\w\s/,�/-]+)\s�'
    animal_data["���������"] = find_re(regex_family, text)

    # ������ (��������� ��������)
    regex_status = r'������\.\s(.+?)\x1f'
    animal_data["������"] = find_re(regex_status, text)

    # ��������������� (��� ������� ���)
    regex_distribution = r'���������������\.\s(.+?)\x1f'
    animal_data["���������������"] = find_re(regex_distribution, text)

    # ����������� (���������� � ���������)
    regex_population = r'�����������\.\s(.+?)\x1f'
    animal_data["�����������"] = find_re(regex_population, text)

    # ����������� �������� (����� �������� � ���������)
    regex_habitat = r'����������� ��������\.\s(.+?)\x1f'
    animal_data["����������� ��������"] = find_re(regex_habitat, text)

    # ������������ ������� (�������������� �������)
    regex_limiting_factors = r'������������ �������\.\s(.+?)\x1f'
    animal_data["������������ �������"] = find_re(regex_limiting_factors, text)

    # �������� ���� ������
    regex_conservation_measures = r'�������� ���� ������\.\s(.+?)\x1f'
    animal_data["�������� ���� ������"] = find_re(regex_conservation_measures, text)

    # ��������� ��������� ����
    regex_state_changes = r'��������[��] ��������� ����\.\s(.+?)\x1f'
    animal_data["��������� ��������� ����"] = find_re(regex_state_changes, text)

    # ����������� ����������� �� ���������� ����
    regex_conservation_needs = r'����������� ����������� �� ���������� ����\.\s(.+?)\x1f'
    animal_data["����������� ����������� �� ���������� ����"] = find_re(regex_conservation_needs, text)

    # ��������� ����������
    regex_sources = r'��������� ����������\.\s(.+?)\x1f'
    animal_data["��������� ����������"] = find_re(regex_sources, text)

    return animal_data

# �������� � ������ ���������� ����� � ������� �� PDF
file_path = "Mushrooms.txt"
with open(file_path, "r", encoding="utf-8") as file:
    text = file.read()

# ������� ��������, ����� �������� ������ ��� ������
text = text.replace("- ", "")

# �������� �������� ���������� ��������
stop_words = ['��������', '�������������', '����', '�����', '�������������� � �����������', '��������������', 
              '���������� ��������', '�������� � �����', '����������', '���������', '���������', '�����']
for word in stop_words:
    text = re.sub(r'\n' + re.escape(word) + r'\n', '\n', text)

# ������� ������ � �������� ������� � ������� ���������� ����������
text = re.sub(r'\n\d+\n{1,3}', '\n', text)
text = re.sub(r'����:\s.+\n', '\n', text)

# ���������� ������ �� ����� ��� ������� ��������� �� ��������� ����� "�����"
animals = re.split(r'�����[�]?\:\s.+?\n', text)[:-1]

# ������� ������ ��� ������� ���������
animal_list = [parse_animal(animal.replace("\n", " ")) for animal in animals]

# �������������� ������ � DataFrame ��� �������� ������ � ��������
df = pd.DataFrame(animal_list)

# ������ ������ ����� �� None
df = df.replace("", None)

# ���������� �������� ������� � Excel ����
df.to_excel("mushrooms_table.xlsx", index=False)

# ��������, ������� ����� � ������ �������� � ������ �������
print(df.shape[0])
print(df.isna().sum())
