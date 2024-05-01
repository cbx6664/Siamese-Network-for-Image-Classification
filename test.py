import datetime
import fnmatch
import utils.file_name_compare
import numpy as np
import os
from PIL import Image

from siamese import Siamese

if __name__ == "__main__":
    model = Siamese()


    def get_all_image_files(folder_path):
        image_files = []
        for root, dirs, files in os.walk(folder_path):
            for name in files:
                if name.endswith(('.png', '.jpg', '.jpeg')):
                    image_files.append(os.path.join(root, name))
        return image_files


    def process_images_in_folder(folder):

        # 获取指定文件夹中所有文件的文件名
        global max_probability, max_image_name

        files = os.listdir(folder)
        probability_dict = {}

        # 循环遍历每support set一个文件名，读取并处理图片
        for file in files:
            try:
                # 拼接文件路径
                file_path = os.path.join(folder, file)

                # 如果是文件夹，则递归调用process_images_in_folder函数
                if os.path.isdir(file_path):
                    process_images_in_folder(file_path)
                # 如果是图片文件，则处理该图片
                elif file.lower().endswith(('.png', '.jpg', '.jpeg')):
                    # 使用Pillow库打开图片
                    image_2 = Image.open(file_path)
                    images_2_name = os.path.basename(file_path)

                    # 获取图片所在的上级目录
                    parent_folder = os.path.abspath(os.path.join(folder, '.'))

                    probability = model.detect_image(image_1, image_2, image_1_name,
                                                     os.path.basename(support_set_folder))
                    print(f"Similarity of {image_1_name} and {images_2_name}: {probability}")

                    # 将图片的相似度值存储到 probability_dict 中
                    if parent_folder in probability_dict:
                        probability_dict[parent_folder].append(probability)
                    else:
                        probability_dict[parent_folder] = [probability]

                    # # 如果匹配度比已有的最大值大，则更新最大值和对应的图片文件名
                    # if probability > max_probability:
                    #     max_probability = probability
                    #     max_image_name = images_2_name

            except:
                print(f"{file_path} Error opening, skipping...")

        # 计算每个上级目录的平均相似度值
        avg_probability_dict = {}
        for parent_folder in probability_dict:
            probabilities = probability_dict[parent_folder]
            avg_probability = sum(probabilities) / len(probabilities)
            avg_probability_dict[parent_folder] = avg_probability

        # 取最大平均相似度的图片文件名
        for parent_folder in sorted(avg_probability_dict, key=avg_probability_dict.get,
                                    reverse=True):
            avg_probability = avg_probability_dict[parent_folder]
            if avg_probability > max_probability:
                folder_files = os.listdir(parent_folder)
                for file in sorted(folder_files):
                    if file.lower().endswith(('.png', '.jpg', '.jpeg')):
                        max_image_name = file
                        break
                max_probability = avg_probability

        print("-" * 66)
        for key, value in avg_probability_dict.items():
            print(f'The average similarity between {image_1_name} and {os.path.basename(os.path.normpath(key))}in the '
                  f'support set is:{value}')
        print("-" * 66)

        # 调用递归函数，处理support set中的所有图片


    query_set_folder = input("Please specify the query set folder path:")
    # 检查support set图片文件夹是否存在
    if not os.path.exists(query_set_folder):
        print(f"{query_set_folder} The folder does not exist!")
    else:
        # 获取指定文件夹中所有文件的文件名
        image_files = get_all_image_files(query_set_folder)

        success_count = 0
        success_file = []
        total_count = 0
        total_file = []

        # 提示用户输入support set图像文件夹路径
        support_set_folder = input("Please specify the support set folder path:")

        # 循环遍历每一个query set文件名，读取并处理图片
        for image_file in image_files:
            try:
                # 使用Pillow库打开图片
                image_1 = Image.open(os.path.join(image_file))
                image_1_name = os.path.basename(image_file)

                # 检查support set图片文件夹是否存在
                if not os.path.exists(support_set_folder):
                    print(f"{support_set_folder} The folder does not exist!")
                else:

                    max_probability = -1  # 初始化最大匹配度为-1
                    max_image_name = None  # 初始化最大匹配度对应的support set图片文件名为None
                    total_file.append(utils.file_name_compare.extract_letters(image_1_name[:-4]))
                    process_images_in_folder(support_set_folder)
                    print("*" * 100)
                    print(image_1_name + " " + "is most similar to:" + " " + max_image_name)
                    print("*" * 100)

                    # 如果query文件名在支持集最大匹配度对应的文件名中出现，则认为匹配成功
                    if utils.file_name_compare.compare_filenames(image_1_name[:-4].lower(),
                                                                 max_image_name[:-4].lower()):
                        success_count += 1
                        success_file.append(utils.file_name_compare.extract_letters(image_1_name[:-4]))

                    total_count += 1
            except:
                print(f"{image_file} Error opening, skipping...")

        # 创建未能识别的昆虫列表，用来输出没能识别的昆虫种类
        unidentified_list = list(set(total_file) - set(success_file))

        # 打印准确率和成功识别的昆虫类别
        print(f"accuracy:{success_count / total_count}\nSuccessfully identified insects:\n")
        for val in success_file:
            print(str(val) + ',')

        # 打印未能识别的昆虫类别
        print(f"\nUnidentified insects:\n")
        for val in unidentified_list:
            print(str(val) + ',')

        file_name = f"{os.path.basename(support_set_folder)} accuracy is {success_count / total_count:.2f}.txt"
        log_path = model.get_log_path()
        file_path = f"{log_path}/{os.path.basename(support_set_folder)}/{file_name}"
        # 打开文件以写入模式
        file = open(file_path, 'w')

        # 写入内容
        file.write(
            f"Date:{datetime.datetime.now()}\n\nModel Weights:{model.get_defaults('model_path')}\n\nAccuracy:{success_count / total_count}\n\nSuccessfully identified {len(success_file)} out of "
            f"{total_count} insects:\n")
        for val in success_file:
            file.write(str(val) + ',' + '\n')

        file.write(f"\nUnidentified Insects:\n")
        for val in unidentified_list:
            file.write(str(val) + ',' + '\n')

        # 关闭文件
        file.close()
