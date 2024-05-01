# 导入需要的模块
import os
import random
import shutil
from PIL import Image, ImageEnhance

import utils.file_name_compare


# 定义一个函数，接受一个目录路径和一个整数n作为参数
def make_support(dir_path, n):
    # 检查目录是否存在，如果不存在，抛出异常
    if not os.path.exists(dir_path):
        raise FileNotFoundError(f"{dir_path} does not exist.")
    # 检查目录是否是一个目录，如果不是，抛出异常
    if not os.path.isdir(dir_path):
        raise NotADirectoryError(f"{dir_path} is not a directory.")
    # 获取一级目录的父目录的路径
    parent_dir = os.path.dirname(dir_path)
    # 创建一个output文件夹在父目录下，如果已经存在，跳过
    output_dir = os.path.join(parent_dir, f"{os.path.basename(dir_path)}_support_set_{n}shot")
    if not os.path.exists(output_dir):
        os.mkdir(output_dir)
    # 遍历一级目录下的所有子目录
    for sub_dir in os.listdir(dir_path):
        # 获取子目录的完整路径
        sub_dir_path = os.path.join(dir_path, sub_dir)
        # 检查子目录是否是一个目录，如果不是，跳过
        if not os.path.isdir(sub_dir_path):
            continue
        # 获取子目录下的所有图片文件名，假设图片文件的扩展名是.jpg或.png
        image_files = [f for f in os.listdir(sub_dir_path) if f.endswith(".jpg") or f.endswith(".png")]
        # 检查子目录下是否有足够的图片文件，如果不够，抛出异常
        if len(image_files) < n:
            raise ValueError(f"{sub_dir_path} does not have enough images.")
        # 从图片文件中随机抽取n个文件名
        random_files = random.sample(image_files, n)
        # 在output文件夹中创建一个和子目录同名的文件夹，如果已经存在，跳过
        output_sub_dir = os.path.join(output_dir, sub_dir)
        if not os.path.exists(output_sub_dir):
            os.mkdir(output_sub_dir)
        # 遍历随机抽取的文件名
        for file in random_files:
            # 获取文件的完整路径
            file_path = os.path.join(sub_dir_path, file)
            # 将文件移动到test文件夹中
            shutil.move(file_path, output_sub_dir)

    print(f"Successfully made a support set of {n} shot.")


# 给定datasets的根目录，复制根目录下多shot的support set，返回少shot的support set
def copy_support(dir_path, n):
    # 检查目录是否存在，如果不存在，抛出异常
    # 获取一级目录的父目录的路径
    parent_dir = os.path.dirname(dir_path)
    five_shot_support_set = os.path.join(parent_dir, f"{os.path.basename(dir_path)}_support_set_5shot")
    if not os.path.exists(five_shot_support_set):
        raise FileNotFoundError(f"{five_shot_support_set} does not exist.")
    # 检查目录是否是一个目录，如果不是，抛出异常
    if not os.path.isdir(five_shot_support_set):
        raise NotADirectoryError(f"{five_shot_support_set} is not a directory.")
    # 创建一个output文件夹在父目录下，如果已经存在，跳过
    output_dir = os.path.join(parent_dir, f"{os.path.basename(dir_path)}_support_set_{n}shot")
    if not os.path.exists(output_dir):
        os.mkdir(output_dir)
    # 遍历一级目录下的所有子目录
    for sub_dir in os.listdir(five_shot_support_set):
        # 获取子目录的完整路径
        sub_dir_path = os.path.join(five_shot_support_set, sub_dir)
        # 检查子目录是否是一个目录，如果不是，跳过
        if not os.path.isdir(sub_dir_path):
            continue
        # 获取子目录下的所有图片文件名，假设图片文件的扩展名是.jpg或.png
        image_files = [f for f in os.listdir(sub_dir_path) if f.endswith(".jpg") or f.endswith(".png")]
        # 检查子目录下是否有足够的图片文件，如果不够，抛出异常
        if len(image_files) < n:
            raise ValueError(f"{sub_dir_path} does not have enough images.")
        # 从图片文件中随机抽取n个文件名
        random_files = random.sample(image_files, n)
        # 在output文件夹中创建一个和子目录同名的文件夹，如果已经存在，跳过
        output_sub_dir = os.path.join(output_dir, sub_dir)
        if not os.path.exists(output_sub_dir):
            os.mkdir(output_sub_dir)
        # 遍历随机抽取的文件名
        for file in random_files:
            # 获取文件的完整路径
            file_path = os.path.join(sub_dir_path, file)
            # 将文件移动到test文件夹中
            shutil.copy(file_path, output_sub_dir)

    print(f"Successfully made a support set of {n} shot from 5shot support set.")


def make_query(dir_path):
    # 检查目录是否存在，如果不存在，抛出异常
    if not os.path.exists(dir_path):
        raise FileNotFoundError(f"{dir_path} does not exist.")
    # 检查目录是否是一个目录，如果不是，抛出异常
    if not os.path.isdir(dir_path):
        raise NotADirectoryError(f"{dir_path} is not a directory.")
    # 获取一级目录的父目录的路径
    parent_dir = os.path.dirname(dir_path)
    # 创建一个output文件夹在父目录下，如果已经存在，跳过
    output_dir = os.path.join(parent_dir, f"{os.path.basename(dir_path)}_query_set")
    if not os.path.exists(output_dir):
        os.mkdir(output_dir)
    # 遍历一级目录下的所有子目录
    for sub_dir in os.listdir(dir_path):
        # 获取子目录的完整路径
        sub_dir_path = os.path.join(dir_path, sub_dir)
        # 检查子目录是否是一个目录，如果不是，跳过
        if not os.path.isdir(sub_dir_path):
            continue
        # 获取子目录下的所有图片文件名，假设图片文件的扩展名是.jpg或.png
        image_files = [f for f in os.listdir(sub_dir_path) if f.endswith(".jpg") or f.endswith(".png")]
        # 检查子目录下是否有足够的图片文件，如果不够，抛出异常
        if len(image_files) < 1:
            raise ValueError(f"{sub_dir_path} does not have enough images.")
        # 从图片文件中随机抽取n个文件名
        random_files = random.sample(image_files, 1)
        # 在output文件夹中创建一个和子目录同名的文件夹，如果已经存在，跳过
        output_sub_dir = os.path.join(output_dir, sub_dir)
        if not os.path.exists(output_sub_dir):
            os.mkdir(output_sub_dir)
        # 遍历随机抽取的文件名
        for file in random_files:
            # 获取文件的完整路径
            file_path = os.path.join(sub_dir_path, file)
            # 将文件复制到test文件夹中
            shutil.move(file_path, output_sub_dir)

    print(f"Successfully made a query set.")


def check_and_enhance(dir_path, n):
    # dir_path: the path of the given directory
    # n: the number of images to check
    # return: a string indicating the result

    # check if the directory exists
    if not os.path.isdir(dir_path):
        return "The directory does not exist."

    # get the list of subdirectories
    subdirs = [os.path.join(dir_path, name) for name in os.listdir(dir_path) if
               os.path.isdir(os.path.join(dir_path, name))]

    # loop through each subdirectory
    for subdir in subdirs:
        # get the list of image files
        image_files = [os.path.join(subdir, name) for name in os.listdir(subdir) if
                       name.endswith((".jpg", ".png", ".jpeg"))]

        # check the number of image files
        if len(image_files) == n:
            continue
        elif len(image_files) > n:
            # continue
            # 删除超出n张的部分，只留下n张图片
            while len(image_files) > n:
                # randomly choose an image file to delete
                image_file = random.choice(image_files)

                # delete the image file from the subdirectory
                os.remove(image_file)

                # remove the image file from the image files list
                image_files.remove(image_file)

        else:
            # loop until there are n image files
            while len(image_files) < n:
                # randomly choose an image file
                image_file = random.choice(image_files)

                # open the image with PIL
                image = Image.open(image_file)

                # # randomly choose an enhancement factor between 0.5 and 1.5
                # factor = random.uniform(0.5, 1.5)

                # randomly choose an enhancement type among color, contrast, brightness and sharpness
                enhancer_type = random.choice(["horizontal_flip", "vertical_flip"])

                # create an enhancer object according to the type
                if enhancer_type == "horizontal_flip":
                    enhanced_image = image.transpose(Image.FLIP_LEFT_RIGHT)

                else:
                    enhanced_image = image.transpose(Image.FLIP_TOP_BOTTOM)

                # get the file name and extension of the original image
                file_name, file_ext = os.path.splitext(image_file)

                # generate a new file name by adding "enhanced" and a random number to avoid duplication
                new_file_name = file_name + str(random.randint(1, 100)) + file_ext

                # save the enhanced image to the same subdirectory with the new file name
                enhanced_image.save(new_file_name)

                # add the new file name to the image files list
                image_files.append(new_file_name)

    print(f"Each subdirectory in dataset has exactly {n} pictures.")


# 输入一个二级目录的根目录，将二级目录下的所有图片的文件名改成二级目录的字母
def rename_images(root_dir):
    for subdir in os.listdir(root_dir):
        subdir_path = os.path.join(root_dir, subdir)
        if os.path.isdir(subdir_path):
            prefix = utils.file_name_compare.extract_letters(os.path.basename(subdir_path))
            count = 1
            for filename in os.listdir(subdir_path):
                if filename.endswith(".jpg") or filename.endswith(".JPG") or filename.endswith(".jpeg") or \
                        filename.endswith(".png"):
                    new_filename = prefix + '_' + str(count) + os.path.splitext(filename)[1]
                    print(new_filename)
                    old_filepath = os.path.join(subdir_path, filename)
                    new_filepath = os.path.join(subdir_path, new_filename)
                    os.rename(old_filepath, new_filepath)
                    count += 1


# rename_images('E:/College/3-2/MachineLearningProject/insects dataset/IP-FSL/Adult stage')
# 确认每个种类的文件夹里都至少有数量为n的图片
# check_and_enhance('E:/College/3-2/MachineLearningProject/insects dataset/summary/summary_test_set_original_6_pics', 6)

# 从每个种类文件里分割出n张图片，构建query set和support set
make_query('img/IP-FSL_test_16_way/IP-FSL_test')
make_support('img/IP-FSL_test_16_way/IP-FSL_test', 5)
copy_support('img/IP-FSL_test_16_way/IP-FSL_test', 4)
copy_support('img/IP-FSL_test_16_way/IP-FSL_test', 3)
copy_support('img/IP-FSL_test_16_way/IP-FSL_test', 2)
copy_support('img/IP-FSL_test_16_way/IP-FSL_test', 1)

