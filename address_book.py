from pprint import pprint
import csv
import re
import pandas as pd
import os

with open("phonebook_raw.csv", encoding='utf8') as f:
    rows = csv.reader(f, delimiter=",")
    contacts_list = list(rows)

output_list = []

for element_list in contacts_list:
    # Task 1
    name_pattern = re.compile(
        r"\[\'*(\w{4,})\'*\s*\,*\s*\s*\'*(\w{4,})\'*\,*\s*\'*(\w{7,})*\'*")
    res_text_1 = name_pattern.findall(str(element_list))
    res_text = list(res_text_1[0])
    res_text.append(element_list[3])
    res_text.append(element_list[4])

    # Task 2
    phone_pattern = re.compile(r"(\+7|8)\s*\(*(\d{3})\)*\-*\s*(\d{3})\-*\s*"
                               r"(\d{2})\-*\s*(\d+)\s*\(*(\w{3}\.)*\s*(\d{4})*\)*")
    res_text_2 = phone_pattern.sub(r'+7(\2)\3-\4-\5 \6\7', element_list[-2])
    res_text.append(res_text_2)
    res_text.append(element_list[-1])

    output_list.append(res_text)

with open("tmp.csv", "w", encoding='utf8') as f:
    datawriter = csv.writer(f, delimiter=',')
    datawriter.writerows(output_list)

# Task 3
df = pd.read_csv("tmp.csv", delimiter=",")
df_2 = df.groupby(['lastname']).agg({'firstname': 'first', 'surname': 'first', 'organization': 'first',
                                     'position': 'first', 'phone': 'first',
                                     'email': 'first'}).reset_index().reindex(columns=df.columns)


df_2.to_csv("phonebook.csv")
pprint(df_2)
os.remove('tmp.csv')
