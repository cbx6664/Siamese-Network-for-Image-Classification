import datetime
import os
from PIL import Image
from siamese import Siamese
from utils import file_name_compare


def get_all_image_files(folder_path):
    # 获取文件夹中所有图像文件的完整路径
    image_files = []
    for root, dirs, files in os.walk(folder_path):
        for name in files:
            if name.lower().endswith(('.png', '.jpg', '.jpeg')):
                image_files.append(os.path.join(root, name))
    return image_files


def process_images(query_set_folder, query_image, query_image_name, support_set_folder, model):

    max_avg_probability = -1
    max_avg_image_name = None

    for root, dirs, files in os.walk(support_set_folder):
        probability_list = list()
        classified_image_name_list = list()
        avg_probability = 0
        avg_image_name = None

        for support_image_name in files:
            if support_image_name.lower().endswith(('.png', '.jpg', '.jpeg')):
                support_image_path = os.path.join(root, support_image_name)
                try:
                    support_image = Image.open(support_image_path)
                    probability = model.detect_image(query_set_folder, support_set_folder, query_image, support_image, query_image_name, support_image_name)
                    print(f"Similarity of {query_image_name} and {support_image_name}: {probability}")

                    probability_list.append(probability)
                    classified_image_name_list.append(support_image_name)

                except IOError:
                    print(f"Error opening {support_image_path}, skipping...")

        if files.__len__() == 0:
            continue
        else:
            avg_probability = sum(probability_list) / len(probability_list)
            avg_image_name = classified_image_name_list[0]
            print(f"avg_similarity of {query_image_name} and the class of {support_image_name}: {avg_probability}")
            print()

            if avg_probability > max_avg_probability:
                max_avg_probability = avg_probability
                max_avg_image_name = avg_image_name


    return max_avg_image_name, max_avg_probability


def evaluate_images(query_set_folder, support_set_folder, model):
    query_image_files = get_all_image_files(query_set_folder)
    success_count = 0
    total_count = 0
    success_file = []
    total_file = []

    for query_image_path in query_image_files:
        query_image_name = os.path.basename(query_image_path)
        try:
            image = Image.open(query_image_path)
            max_avg_image_name, max_avg_probability = process_images(query_set_folder, image, query_image_name, support_set_folder, model)
            print(f"{query_image_name} is classified as: {max_avg_image_name}")
            print("-"*99)
            print()


            total_count += 1
            total_file.append(file_name_compare.extract_letters(query_image_name[:-4]))
            if file_name_compare.compare_filenames(query_image_name[:-4].lower(), max_avg_image_name[:-4].lower()):
                success_count += 1
                success_file.append(file_name_compare.extract_letters(query_image_name[:-4]))

        except IOError:
            print(f"Error opening {query_image_path}, skipping...")

    return success_count, total_count, success_file, total_file


def write_results(query_set_folder, support_set_folder, success_count, total_count, success_file, unidentified_list, model):
    sup_dir = model.get_log_path()+"_"+os.path.basename(query_set_folder)+"_"+os.path.basename(support_set_folder)[-2:]
    accuracy = success_count / total_count if total_count > 0 else 0
    file_name = f"{os.path.basename(support_set_folder)}_accuracy_{accuracy:.2f}.txt"
    # log_path = os.path.join(model.get_log_path(query_set_folder, support_set_folder))
    full_file_path = os.path.join(sup_dir, file_name)

    with open(full_file_path, 'w', encoding='utf-8') as file:
        file.write(f"Date:{datetime.datetime.now()}\n")
        file.write(f"Accuracy:{accuracy}\n")
        file.write(f"\n")
        file.write(f"Identified {len(success_file)} out of {total_count} insects:\n")
        file.write(f"\n")
        file.writelines(f"{insect},\n" for insect in success_file)
        file.write("\nUnidentified Insects:\n")
        file.write(f"\n")
        file.writelines(f"{insect},\n" for insect in unidentified_list)


def main():
    query_set_folder = input("Please specify the query set folder path:")
    if not os.path.exists(query_set_folder):
        print(f"The folder {query_set_folder} does not exist!")
        return

    support_set_folder = input("Please specify the support set folder path:")
    if not os.path.exists(support_set_folder):
        print(f"The folder {support_set_folder} does not exist!")
        return

    model = Siamese()
    success_count, total_count, success_file, total_file = evaluate_images(query_set_folder, support_set_folder, model)
    unidentified_list = list(set(total_file) - set(success_file))
    write_results(query_set_folder, support_set_folder, success_count, total_count, success_file, unidentified_list, model)
    print(f"Accuracy: {success_count / total_count:.2f}")
    print(f"successfully classified:{success_count}")
    print(f"totally classified:{total_count}")
    print("Successfully identified insects:")
    print(*success_file, sep=', ')
    print("\nUnidentified insects:")
    print(*unidentified_list, sep=', ')


if __name__ == "__main__":
    main()
