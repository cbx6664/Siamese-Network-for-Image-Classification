import visualkeras
from keras import layers
from keras.models import Sequential
from keras.layers import Input, Conv2D, Dense, Flatten, Dropout
from keras.layers import GlobalMaxPooling2D, MaxPooling2D
from PIL import ImageFont
from PIL import ImageFont
from collections import defaultdict

color_map = defaultdict(dict)
color_map[layers.Conv2D]['fill'] = '#00f5d4'
color_map[layers.MaxPooling2D]['fill'] = '#8338ec'
color_map[layers.Dropout]['fill'] = '#03045e'
color_map[layers.Dense]['fill'] = '#fb5607'
color_map[layers.Flatten]['fill'] = '#ffbe0b'
font = ImageFont.truetype("arial.ttf", 20)

model = Sequential()

# 第一个卷积部分
# 105, 105, 3 -> 105, 105, 64 -> 52, 52, 64
model.add(Conv2D(64, (3, 3), input_shape=(105, 105, 3), activation='relu', padding='same', name='block1_conv1'))
model.add(Conv2D(64, (3, 3), activation='relu', padding='same', name='block1_conv2'))
model.add(MaxPooling2D((2, 2), strides=(2, 2), name='block1_pool'))

# 第二个卷积部分
# 52, 52, 64 -> 52, 52, 128 -> 26, 26, 128
model.add(Conv2D(128, (3, 3), activation='relu', padding='same', name='block2_conv1'))
model.add(Conv2D(128, (3, 3), activation='relu', padding='same', name='block2_conv2'))
model.add(MaxPooling2D((2, 2), strides=(2, 2), name='block2_pool'))

# 第三个卷积部分
# 26, 26, 128-> 26, 26, 256 -> 13, 13, 256
model.add(Conv2D(256, (3, 3), activation='relu', padding='same', name='block3_conv1'))
model.add(Conv2D(256, (3, 3), activation='relu', padding='same', name='block3_conv2'))
model.add(Conv2D(256, (3, 3), activation='relu', padding='same', name='block3_conv3'))
model.add(MaxPooling2D((2, 2), strides=(2, 2), name='block3_pool'))

# 第四个卷积部分
# 13, 13, 256-> 13, 13, 512 -> 6, 6, 512
model.add(Conv2D(512, (3, 3), activation='relu', padding='same', name='block4_conv1'))
model.add(Conv2D(512, (3, 3), activation='relu', padding='same', name='block4_conv2'))
model.add(Conv2D(512, (3, 3), activation='relu', padding='same', name='block4_conv3'))
model.add(MaxPooling2D((2, 2), strides=(2, 2), name='block4_pool'))

# 第五个卷积部分
# 6, 6, 512-> 6, 6, 512 -> 3, 3, 512
model.add(Conv2D(512, (3, 3), activation='relu', padding='same', name='block5_conv1'))
model.add(Conv2D(512, (3, 3), activation='relu', padding='same', name='block5_conv2'))
model.add(Conv2D(512, (3, 3), activation='relu', padding='same', name='block5_conv3'))
model.add(MaxPooling2D((2, 2), strides=(2, 2), name='block5_pool'))

# 3*3*512 = 4500 + 90 + 18 = 4608
model.add(Flatten(name='flatten'))

visualkeras.layered_view(model, legend=True, font=font, color_map=color_map, to_file='vgg.png')
