#  Siamese Network在图像分类上的应用

 本仓库基于[bubbliiiing/Siamese-keras: 这是一个孪生神经网络（Siamese network）的库，可进行图片的相似性比较。 (github.com)](https://github.com/bubbliiiing/Siamese-keras)改造而成。

在原来的基础上，本仓库新增了以下功能：

1. backbone新增了ResNet50，nets/resnet.py（原仓库仅有VGG16）

2. 新增了数据集处理函数make_dataset.py，使用时确保二级目录“class1”、“class2”... 内包含各自类别的图像，且二级目录名已改为对应类别的名字

   ```plaintext
   dataset/
   ├── class1/
   │   ├── img1.jpg
   │   ├── img2.jpg
   │   ├── img3.jpg
   ├── class2/
   │   ├── img1.jpg
   │   ├── img2.jpg
   │   ├── img3.jpg
   └── class3/
   |    ├── img1.jpg
   |    ├── img2.jpg
   |    ├── img3.jpg
   ...
   ```

3. 新增了计算分类准确度的函数test.py，原理是通过对比图像的相似度，相似度最高视为同类

4. 新增了文件名对比函数utils/file_name_compare.py，我们以图像的文件名为类别标识（所以图像文件的命名很重要，在make_dataset.py中会自动重命名图像文件为其父目录的名字）

5. 新增了可视化backbone的函数viz_xx.py

6. 新增了可视化训练过程loss的函数draw_loss.py，training和validation的loss curve呈现在一张图上

7. 新增了可视化训练过程中图像增强的函数，在utils/dataloader.py中

8. 新增了模型复杂度的计算utils/model_complexity.py，计算模型的flops

## 使用方法

### 训练
1. 使用前先用make_dataset.py处理一下数据集，分割出query set和support set
2. 在train.py中设置超参数，训练自己的数据集需将 train_own_data 设置为 True

### 测试
1. siamese.py中的input_shape需要与train.py中的input_shape对应上
2. siamese.py中的model_path修改为logs目录下训练好的.h5权值文件
3. 使用test.py进行测试
