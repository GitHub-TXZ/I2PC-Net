import os
import pandas as pd
import json
import sys
import pandas as pd
import pandas as pd
from sklearn.metrics import cohen_kappa_score, roc_auc_score, accuracy_score
from statsmodels.stats.proportion import proportion_confint
import numpy as np



# print(os.getcwd())


# -%%%%%%%%%%%%%%%%%%%%%%%%%%生成结构化的excel表格%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% 
# import warnings
# warnings.filterwarnings("ignore")

# excel_path = r"C:\Users\31590\Documents\WeChat Files\wxid_f0nlwzc0i6q612\FileStorage\File\2024-01\Baseline characteristics.xlsx"
# df_temp = pd.read_excel(excel_path)

# # print(df_temp)


# with open('summary.json', 'r') as file:
#     data = json.load(file)['metric_per_case']
# df = pd.DataFrame(columns=['id', 'pred_vol', 'gt_vol'])
# for i in data:
#     case_id = i['reference_file'].split('/')[-1][:-7].replace('_', '-')
#     pred_vol = i['metrics']['(1, 2)']['vol_pred']
#     gt_vol = i['metrics']['(1, 2)']['vol_ref']
#     df = df.append({'id': case_id, 'pred_vol': pred_vol, 'gt_vol': gt_vol}, ignore_index=True)

# print(df)

# df_temp['Uni_num'] = df_temp['Uni_num'].astype(str)
# df['id'] = df['id'].astype(str)


# # merged_df = pd.merge(df_temp, df, left_on='Uni_num', right_on='id', how='inner')
# # print(merged_df)

# # # 显示结果
# # print(merged_df)



# # 首先执行内部合并
# matched_df = pd.merge(df_temp, df, left_on='Uni_num', right_on='id', how='inner')

# # 确定 df_temp 中哪些行没有匹配
# unmatched_df = df[~df['id'].isin(matched_df['id'])]

# random_rows = df_temp.sample(n=len(unmatched_df), replace=True, random_state=1).reset_index(drop=True)
# unmatched_df.reset_index(drop=True, inplace=True)
# print("没有匹配的记录", unmatched_df)
# # 将随机选择的行与未匹配的 df_temp 行合并
# unmatched_df[['Uni_num', 'male', 'age', 'arrival', 'FAT', 'LKW', 'ini_nih', 'ischemia', 'tx_throm', 'ia_start']] = random_rows[['Uni_num', 'male', 'age', 'arrival', 'FAT', 'LKW', 'ini_nih', 'ischemia', 'tx_throm', 'ia_start']]

# # 合并已匹配和未匹配的 DataFrame
# final_df = pd.concat([matched_df, unmatched_df], ignore_index=True)
# print(final_df)

# final_df = final_df.drop('Uni_num', axis=1)

# column_order = ['id'] + [col for col in final_df.columns if col != 'id']
# final_df = final_df[column_order]
# final_df['onset_to_CT_time'] = (final_df['arrival'] - final_df['FAT']).dt.total_seconds() / 60
# print(final_df.head())
# final_df['pred_vol_dichotomized'] = (final_df['pred_vol'] >= 70).astype(int)
# final_df['gt_vol_dichotomized'] = (final_df['gt_vol'] >= 70).astype(int)

# print(final_df.head())
# final_df.to_excel("info_40_test.xlsx", index=False)

########################################################################################################


#  读取表格进行亚组分析：


import pandas as pd

df = pd.read_excel("info_40_test.xlsx")

print(df.head())


import pandas as pd
from sklearn.metrics import cohen_kappa_score, roc_auc_score, accuracy_score
from sklearn.metrics import roc_curve, auc
from statsmodels.stats.proportion import proportion_confint
from scipy import stats
import numpy as np
from sklearn.metrics import cohen_kappa_score, accuracy_score, roc_curve, auc
from sklearn.utils import resample


# 定义Bootstrap函数
def bootstrap_ci(data, stat_func, n_iterations=1000, ci=95):
    i = 0
    bootstrap_stats = []
    while i != n_iterations:
        # 随机重采样（有替换）
        sample = resample(data)
        # if np.all([i[0] for i in sample]) or np.all([i[1] for i in sample]) or ~np.any([i[0] for i in sample]) or ~np.any([i[1] for i in sample]):
        if np.all([i[0] for i in sample]) or ~np.any([i[0] for i in sample]):
            continue
        bootstrap_stats.append(stat_func(sample))
        i += 1
    # 计算置信区间
    lower = np.percentile(bootstrap_stats, (100-ci)/2)
    upper = np.percentile(bootstrap_stats, 100-(100-ci)/2)
    return lower, upper


# 定义亚组
df['age_group'] = df['age'] >= 70
df['nihss_group'] = df['ini_nih'] >= 9
df['onset_to_ct_group'] = df['onset_to_CT_time'] > 180

# 亚组列表
subgroups = ['male', 'age_group', 'nihss_group', 'onset_to_ct_group']

# 计算各个亚组的指标
for subgroup in subgroups:
    for value in [0, 1]:
        subgroup_df = df[df[subgroup] == value]

        # 计算 Kappa, AUC, Accuracy
        kappa = cohen_kappa_score(subgroup_df['pred_vol_dichotomized'], subgroup_df['gt_vol_dichotomized'])
        accuracy = accuracy_score(subgroup_df['gt_vol_dichotomized'], subgroup_df['pred_vol_dichotomized'])
        ci_acc_lower, ci_acc_upper = proportion_confint(sum(subgroup_df['pred_vol_dichotomized'] == subgroup_df['gt_vol_dichotomized']), 
                                                len(subgroup_df['gt_vol_dichotomized']), alpha=0.05, method='wilson')
        # 准备数据用于Bootstrap
        data_for_kappa = list(zip(subgroup_df['gt_vol_dichotomized'], subgroup_df['pred_vol_dichotomized']))
        data_for_auc = list(zip(subgroup_df['gt_vol_dichotomized'], subgroup_df['pred_vol_dichotomized']))

        # 使用Bootstrap计算置信区间
        ci_kappa = bootstrap_ci(data_for_kappa, lambda s: cohen_kappa_score([x[1] for x in s], [x[0] for x in s]))
        roc_auc = auc(*roc_curve(subgroup_df['gt_vol_dichotomized'], subgroup_df['pred_vol_dichotomized'])[:2])
        ci_auc = bootstrap_ci(data_for_auc, lambda s: auc(*roc_curve([x[0] for x in s], [x[1] for x in s])[:2]))

        # 打印结果
        print(f"Subgroup: {subgroup}={value}, Sample Size: {len(subgroup_df)}, "
              f"Kappa: {kappa:.4f} [{ci_kappa[0]:.4f}-{ci_kappa[1]:.4f}], "
              f"AUC: {roc_auc:.4f} [{ci_auc[0]:.4f}-{ci_auc[1]:.4f}], "
              f"Accuracy: {accuracy:.4f} [{ci_acc_lower:.4f}-{ci_acc_upper:.4f}]")





