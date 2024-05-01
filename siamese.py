import os
import uuid
import time
from datetime import datetime

import matplotlib.pyplot as plt
import numpy as np
from keras import backend as K
from PIL import Image
import utils.file_name_compare
from nets.siamese import siamese
from utils.utils import (cvtColor, letterbox_image, preprocess_input,
                         show_config)


# ---------------------------------------------------#
#   使用自己训练好的模型预测需要修改model_path参数
# ---------------------------------------------------#
class Siamese(object):
    _defaults = {
        # -----------------------------------------------------#
        #   使用自己训练好的模型进行预测一定要修改model_path
        #   model_path指向logs文件夹下的权值文件
        # -----------------------------------------------------#
        "model_path": 'logs/#4_local_dataset_summary_224x224/best_epoch_weights.h5',
        # -----------------------------------------------------#
        #   输入图片的大小。
        # -----------------------------------------------------#
        "input_shape": [224, 224],
        # --------------------------------------------------------------------#
        #   该变量用于控制是否使用letterbox_image对输入图像进行不失真的resize
        #   否则对图像进行CenterCrop
        # --------------------------------------------------------------------#
        "letterbox_image": True,
    }

    @classmethod
    def get_defaults(cls, n):
        if n in cls._defaults:
            return cls._defaults[n]
        else:
            return "Unrecognized attribute name '" + n + "'"

    # ---------------------------------------------------#
    #   初始化Siamese
    # ---------------------------------------------------#
    def __init__(self, **kwargs):
        self.__dict__.update(self._defaults)
        for name, value in kwargs.items():
            setattr(self, name, value)

        self.sess = K.get_session()

        self.generate()

        show_config(**self._defaults)

    # ---------------------------------------------------#
    #   载入模型
    # ---------------------------------------------------#
    def generate(self):
        model_path = os.path.expanduser(self.model_path)
        assert model_path.endswith('.h5'), 'Keras model or weights must be a .h5 file.'
        # ---------------------------#
        #   载入模型与权值
        # ---------------------------#
        self.model = siamese([self.input_shape[0], self.input_shape[1], 3])
        self.model.load_weights(self.model_path)
        print('{} model loaded.'.format(model_path))

    # ---------------------------------------------------#
    #   检测图片
    # ---------------------------------------------------#
    def detect_image(self, image_1, image_2, image_1_name, test_type):
        # ---------------------------------------------------------#
        #   在这里将图像转换成RGB图像，防止灰度图在预测时报错。
        # ---------------------------------------------------------#
        image_1 = cvtColor(image_1)
        image_2 = cvtColor(image_2)

        # ---------------------------------------------------#
        #   对输入图像进行不失真的resize
        # ---------------------------------------------------#
        image_1 = letterbox_image(image_1, [self.input_shape[1], self.input_shape[0]], self.letterbox_image)
        image_2 = letterbox_image(image_2, [self.input_shape[1], self.input_shape[0]], self.letterbox_image)

        # ---------------------------------------------------------#
        #   归一化+添加上batch_size维度
        # ---------------------------------------------------------#
        photo1 = np.expand_dims(preprocess_input(np.array(image_1, np.float32)), 0)
        photo2 = np.expand_dims(preprocess_input(np.array(image_2, np.float32)), 0)

        # ---------------------------------------------------#
        #   获得预测结果，output输出为概率
        # ---------------------------------------------------#
        output = self.model.predict([photo1, photo2])[0]

        plt.subplot(1, 2, 1)
        plt.imshow(np.array(image_1))

        plt.subplot(1, 2, 2)
        plt.imshow(np.array(image_2))
        plt.text(-12, -12, 'Similarity:%.3f' % output, ha='center', va='bottom', fontsize=11)

        # 定义保存路径和文件名
        model_path = self.model_path[:-3]
        dir = test_type
        sub_dir = utils.file_name_compare.extract_letters(image_1_name[:-4])
        date = datetime.today().strftime('%Y%m%d')
        filename = f"match_{str(uuid.uuid4())}.png"
        path = os.path.join(model_path, dir, sub_dir, filename[:-4])

        # 创建目录（如果不存在）
        os.makedirs(os.path.dirname(path), exist_ok=True)

        # 保存文件
        plt.savefig(path)
        plt.close()

        return output

    def get_log_path(self):
        return self.model_path[:-3]

    def close_session(self):
        self.sess.close()
