import os
import nibabel as nib
import numpy as np
import matplotlib.pyplot as plt

# 病例id和感兴趣的切片编号
case_id = "SB_06403_1"
slice_num = 13

# 图像路径、标签路径和预测结果路径
image_path = "E:/biomedicine/imagesTr/"
label_path = "E:/biomedicine/labelsTr/"
prediction_path = "E:/biomedicine/prediction_example/"

# 读取图像
image_file = os.path.join(image_path, f"{case_id}_0000.nii.gz")
image_data = nib.load(image_file).get_fdata()

# 读取标签
label_file = os.path.join(label_path, f"{case_id}.nii.gz")
label_data = nib.load(label_file).get_fdata()

# 初始化 Dice 系数
dice_label1 = []
dice_label2 = []
dice_combined = []

# 遍历预测结果并计算 Dice 系数
num = 1
while True:
    # 构建预测结果文件路径
    prediction_file = os.path.join(prediction_path, f"{case_id}_{num}.nii.gz")
    
    # 检查预测结果文件是否存在
    if os.path.exists(prediction_file):
        # 读取预测结果
        prediction_data = nib.load(prediction_file).get_fdata()
        
        # 提取感兴趣的切片
        image_slice = image_data[:, :, slice_num]
        label_slice = label_data[:, :, slice_num]
        prediction_slice = prediction_data[:, :, slice_num]
        
        # 计算 Dice 系数
        intersection_label1 = np.sum(np.logical_and(label_slice == 1, prediction_slice == 1))
        union_label1 = np.sum(label_slice == 1) + np.sum(prediction_slice == 1)
        dice_label1.append(2 * intersection_label1 / union_label1)
        
        intersection_label2 = np.sum(np.logical_and(label_slice == 2, prediction_slice == 2))
        union_label2 = np.sum(label_slice == 2) + np.sum(prediction_slice == 2)
        dice_label2.append(2 * intersection_label2 / union_label2)
        
        intersection_combined = np.sum(np.logical_and(label_slice > 0, prediction_slice > 0))
        union_combined = np.sum(label_slice > 0) + np.sum(prediction_slice > 0)
        dice_combined.append(2 * intersection_combined / union_combined)
        
        # 显示图像叠加标签
        fig, axes = plt.subplots(1, 3, figsize=(10, 4))
        axes[0].imshow(image_slice, cmap="gray")
        axes[0].set_title("Image")
        axes[0].axis("off")
        
        axes[1].imshow(label_slice, cmap="jet")
        axes[1].set_title("Label")
        axes[1].axis("off")
        
        axes[2].imshow(prediction_slice, cmap="jet")
        axes[2].set_title("Prediction")
        axes[2].axis("off")
        
        plt.show()
        
        num += 1
    else:
        break

# 打印 Dice 系数结果
for i, (dice1, dice2, dice_combined) in enumerate(zip(dice_label1, dice_label2, dice_combined), start=1):
    print(f"Dice for prediction {i}:")
    print(f"Label 1: {dice1}")
    print(f"Label 2: {dice2}")
    print(f"Combined labels: {dice_combined}\n")