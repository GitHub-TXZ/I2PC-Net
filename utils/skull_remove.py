import numpy as np
import nibabel as nib

# 读取NIfTI文件
nifti_file = r'E:\biomedicine\imagesTr\SB_12811_1_0000.nii.gz'
img = nib.load(nifti_file)
data = img.get_fdata()

# 获取第15张切片
slice_15 = data[:, :, 15]

# 将大于50的像素值设为0
slice_15[slice_15 > 50] = 0

# 更新第15张切片至原数据
data[:, :, 15] = slice_15

# 创建修正后的NIfTI图像对象
output_img = nib.Nifti1Image(data, img.affine, img.header)

# 保存修正后的文件
output_file = r'E:\biomedicine\imagesTr\SB_12811_1_0000_aa.nii.gz'
nib.save(output_img, output_file)