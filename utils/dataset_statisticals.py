import os
import nibabel as nib

# 定义目标目录路径
directory = 'E:\\biomedicine\\imagesTr'

# 初始化最小值和最大值变量
min_slices = [float('inf'), float('inf'), float('inf')] # 分别对应轴向、冠状、矢状
max_slices = [0, 0, 0] # 同上

# 遍历目录下的所有.nii.gz文件
for filename in os.listdir(directory):
    if filename.endswith('.nii.gz'):
        file_path = os.path.join(directory, filename)
        
        # 使用nibabel读取文件
        img = nib.load(file_path)
        
        # 获取图像数据的维度（假设是3D图像）
        dims = img.shape
        
        # 更新最小值和最大值
        for i in range(3):
            min_slices[i] = min(min_slices[i], dims[i])
            max_slices[i] = max(max_slices[i], dims[i])

# 打印结果
views = ['Axial', 'Coronal', 'Sagittal']
for i in range(3):
    print(f"{views[i]} view: ({min_slices[i]}-{max_slices[i]}) slices")
