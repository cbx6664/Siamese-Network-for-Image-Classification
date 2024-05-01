## 修改后的使用方法
### 训练
#### 1.使用前先用make_dataset.py处理一下数据集（路径参数要求像这样:folder/sub folder/pic1.png ....），将query set和support set从训练集中分割出来
#### 2.在train.py的model_path指定主干网络的预训练权值，若训练自己的数据集则将train_own_data设置为True
### 测试
#### 1.在siamese.py的model_path指定训练好的模型文件
#### 2.使用test.py进行测试
