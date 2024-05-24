import os

import matplotlib.pyplot as plt

def load_loss_data(file_path):
    """从给定路径中加载loss数据，并跳过无效行"""
    loss_data = []
    with open(file_path, 'r') as file:
        for line in file:
            try:
                # 尝试将每行转换为浮点数，并去除空白字符
                loss = float(line.strip())
                loss_data.append(loss)
            except ValueError:
                # 如果转换失败（比如空行或非数字字符），则跳过该行
                print(f"Warning: Line '{line.strip()}' could not be converted to float and was skipped.")
    return loss_data

# 替换下面的路径为您的实际文件路径
vgg16_train_loss_path = 'logs/vgg16_d0/epoch_loss.txt'
vgg16_val_loss_path = 'logs/vgg16_d0/epoch_val_loss.txt'
resnet50_train_loss_path = 'logs/resnet50_d0_complete/epoch_loss.txt'
resnet50_val_loss_path = 'logs/resnet50_d0_complete/epoch_val_loss.txt'

# 加载数据
vgg16_train_loss = load_loss_data(vgg16_train_loss_path)
vgg16_val_loss = load_loss_data(vgg16_val_loss_path)
resnet50_train_loss = load_loss_data(resnet50_train_loss_path)
resnet50_val_loss = load_loss_data(resnet50_val_loss_path)

# 设置绘图样式
plt.style.use('seaborn-darkgrid')

# 绘制曲线
plt.plot(vgg16_train_loss, label='VGG16 Train Loss', color='red')
plt.plot(vgg16_val_loss, label='VGG16 Validation Loss', linestyle=':', color='red')
plt.plot(resnet50_train_loss, label='ResNet50 Train Loss', color='orange')
plt.plot(resnet50_val_loss, label='ResNet50 Validation Loss', linestyle=':', color='orange')

# 添加图例
plt.legend()

# 添加标题和轴标签
plt.title('Training and Validation Loss for VGG16 and ResNet50 in D0')
plt.xlabel('Epochs')
plt.ylabel('Loss')

# 保存图表到文件
plt.savefig(os.path.join('pics','vgg16_resnet50_d0.svg'))