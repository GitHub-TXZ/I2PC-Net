#%%
import os
import pandas as pd

#%% 将目录下的文件存放为列表，并去掉后缀
directory = r'E:\DWI_FLAIR_MISMATCH_database_toWU\NCCT'  # 替换成你的目录

file_list = []
for filename in os.listdir(directory):
    if filename.endswith(".nii.gz"):
        file_list.append(filename[:-7])  # 删除".nii.gz"后缀，假设文件名都是以.nii.gz结尾的

print(file_list)


excel_path = r"C:\Users\31590\Documents\WeChat Files\wxid_f0nlwzc0i6q612\FileStorage\File\2024-01\Baseline characteristics.xlsx"

dataframe = pd.read_excel(excel_path)

print(dataframe)

file_list = [i.replace('_','-') for i in file_list]

#%%    删选一遍，看看哪些文件在 excel 中，输出过滤之后的表格，对181个文件计算统计指标
filtered_dataframe = dataframe[dataframe['Uni_num'].isin(file_list)]
total_male = filtered_dataframe['male'].sum()
male_rate = (total_male+8)/len(file_list)
print(male_rate, len(file_list))



import numpy as np

median = filtered_dataframe['age'].median()
q1 = filtered_dataframe['age'].quantile(0.25)
q3 = filtered_dataframe['age'].quantile(0.75)

print("age：Median (Q1, Q3): {:.2f} ({:.2f}, {:.2f})".format(median, q1, q3))




import pandas as pd

# 转换时间列为 datetime 类型
filtered_dataframe['arrival'] = pd.to_datetime(filtered_dataframe['arrival'])
filtered_dataframe['FAT'] = pd.to_datetime(filtered_dataframe['FAT'])

# 计算时间差并转换为分钟
filtered_dataframe['time_difference'] = (filtered_dataframe['arrival'] - filtered_dataframe['FAT']).dt.total_seconds() / 60

# 输出 Median（Q1，Q3）
median = filtered_dataframe['time_difference'].median()
q1 = filtered_dataframe['time_difference'].quantile(0.25)
q3 = filtered_dataframe['time_difference'].quantile(0.75)

print("time-to-ct:Median (Q1, Q3): {:.2f} ({:.2f}, {:.2f})".format(median, q1, q3))





median = filtered_dataframe['ini_nih'].median()
q1 = filtered_dataframe['ini_nih'].quantile(0.25)
q3 = filtered_dataframe['ini_nih'].quantile(0.75)

print("NIHSS：Median (Q1, Q3): {:.2f} ({:.2f}, {:.2f})".format(median, q1, q3))





ischemia_unique_values = filtered_dataframe['ischemia'].unique()
ischemia_unique_count = len(ischemia_unique_values)

tx_throm_unique_values = filtered_dataframe['tx_throm'].unique()
tx_throm_unique_count = len(tx_throm_unique_values)

is_start_unique_values = filtered_dataframe['ia_start'].unique()
is_start_unique_count = len(is_start_unique_values)

print("ischemia unique values and their counts:")
for value in ischemia_unique_values:
    count = filtered_dataframe[filtered_dataframe['ischemia'] == value].shape[0]
    print(value, ":", count)

print("\ntx_throm unique values and their counts:")
for value in tx_throm_unique_values:
    count = filtered_dataframe[filtered_dataframe['tx_throm'] == value].shape[0]
    print(value, ":", count)

print("\nia_start unique values and their counts:")
for value in is_start_unique_values:
    count = filtered_dataframe[filtered_dataframe['ia_start'] == value].shape[0]
    print(value, ":", count)



row = filtered_dataframe.loc[filtered_dataframe['ischemia'] == 2]
print(row)




########计算EVT时间相关信息
import pandas as pd

# 删除 "ia_start" 列中的空值
filtered_dataframe = filtered_dataframe.dropna(subset=['ia_start'])

# 将 "ia_start" 和 "arrival" 列转换为 datetime 类型
filtered_dataframe['ia_start'] = pd.to_datetime(filtered_dataframe['ia_start'])
filtered_dataframe['arrival'] = pd.to_datetime(filtered_dataframe['arrival'])

# 计算时间差，并转换为分钟
filtered_dataframe['time_diff'] = (filtered_dataframe['ia_start'] - filtered_dataframe['arrival']).dt.total_seconds() / 60

# 输出 Median（Q1，Q3）
median = filtered_dataframe['time_diff'].median()
q1 = filtered_dataframe['time_diff'].quantile(0.25)
q3 = filtered_dataframe['time_diff'].quantile(0.75)

print("Median: ", median)
print("Q1: ", q1)
print("Q3: ", q3)


















# print(filtered_dataframe)
# %%    用于检查哪些文件没有在 excel 中
import pandas as pd

# 原始的 DataFrame
dataframe = pd.read_excel(r"C:\Users\31590\Documents\WeChat Files\wxid_f0nlwzc0i6q612\FileStorage\File\2024-01\Baseline characteristics.xlsx")

# 过滤不在 dataframe['Uni_num'] 中的值
missing_records = [num for num in file_list if num not in dataframe['Uni_num'].values]

print(missing_records)
#


# %%
