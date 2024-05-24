import os
import random

root_dir = r'E:\CBX\UnderGraduate\4-2\CapstoneProject\Siamese-keras\img\test_d0_dataset\test_data_d0_dataset_10_class'  # 根目录路径

for class_dir in os.listdir(root_dir):
    count = 1  # 开始的顺序数字
    class_dir_path = os.path.join(root_dir, class_dir)
    if os.path.isdir(class_dir_path):
        for file in os.listdir(class_dir_path):
            if file.lower().endswith(('.png', '.jpg', '.jpeg', '.tiff', '.bmp', 'gif')):  # 更改所有图片类型文件的名字
                new_file_name = class_dir + str(count) + '.jpg'  # 新的文件名
                # new_file_name =  str(random.randint(1,1021331211300)) + '.jpg'  # 新的文件名

                new_file_name = new_file_name.replace(' ', '')  # 删除空格
                src = os.path.join(class_dir_path, file)  # 原文件路径
                dst = os.path.join(class_dir_path, new_file_name)  # 新文件路径
                os.rename(src, dst)
                count += 1