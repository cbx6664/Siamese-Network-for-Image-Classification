import tensorflow as tf
import keras.backend as K
from keras import Input, Model
from keras.layers import Conv2D, Flatten, MaxPooling2D

from nets.siamese import siamese


def get_flops(model):
    run_meta = tf.RunMetadata()
    opts = tf.profiler.ProfileOptionBuilder.float_operation()

    # We use the Keras session graph in the call to the profiler.
    flops = tf.profiler.profile(graph=K.get_session().graph,
                                run_meta=run_meta, cmd='op', options=opts)

    return flops.total_float_ops  # Prints the "flops" of the model.


def main():
    # # 第一个卷积部分
    # # 105, 105, 3 -> 105, 105, 64 -> 52, 52, 64
    # block1_conv1 = Conv2D(64, (3, 3), activation='relu', padding='same', name='block1_conv1')
    # block1_conv2 = Conv2D(64, (3, 3), activation='relu', padding='same', name='block1_conv2')
    # block1_pool = MaxPooling2D((2, 2), strides=(2, 2), name='block1_pool')
    #
    # # 第二个卷积部分
    # # 52, 52, 64 -> 52, 52, 128 -> 26, 26, 128
    # block2_conv1 = Conv2D(128, (3, 3), activation='relu', padding='same', name='block2_conv1')
    # block2_conv2 = Conv2D(128, (3, 3), activation='relu', padding='same', name='block2_conv2')
    # block2_pool = MaxPooling2D((2, 2), strides=(2, 2), name='block2_pool')
    #
    # # 第三个卷积部分
    # # 26, 26, 128-> 26, 26, 256 -> 13, 13, 256
    # block3_conv1 = Conv2D(256, (3, 3), activation='relu', padding='same', name='block3_conv1')
    # block3_conv2 = Conv2D(256, (3, 3), activation='relu', padding='same', name='block3_conv2')
    # block3_conv3 = Conv2D(256, (3, 3), activation='relu', padding='same', name='block3_conv3')
    # block3_pool = MaxPooling2D((2, 2), strides=(2, 2), name='block3_pool')
    #
    # # 第四个卷积部分
    # # 13, 13, 256-> 13, 13, 512 -> 6, 6, 512
    # block4_conv1 = Conv2D(512, (3, 3), activation='relu', padding='same', name='block4_conv1')
    # block4_conv2 = Conv2D(512, (3, 3), activation='relu', padding='same', name='block4_conv2')
    # block4_conv3 = Conv2D(512, (3, 3), activation='relu', padding='same', name='block4_conv3')
    # block4_pool = MaxPooling2D((2, 2), strides=(2, 2), name='block4_pool')
    #
    # # 第五个卷积部分
    # # 6, 6, 512-> 6, 6, 512 -> 3, 3, 512
    # block5_conv1 = Conv2D(512, (3, 3), activation='relu', padding='same', name='block5_conv1')
    # block5_conv2 = Conv2D(512, (3, 3), activation='relu', padding='same', name='block5_conv2')
    # block5_conv3 = Conv2D(512, (3, 3), activation='relu', padding='same', name='block5_conv3')
    # block5_pool = MaxPooling2D((2, 2), strides=(2, 2), name='block5_pool')
    #
    # # 3*3*512 = 4500 + 90 + 18 = 4608
    # flatten = Flatten(name='flatten')
    #
    # inp = Input(shape=(105, 105, 3))
    # x = block1_conv1(inp)
    # x = block1_conv2(x)
    # x = block1_pool(x)
    #
    # x = block2_conv1(x)
    # x = block2_conv2(x)
    # x = block2_pool(x)
    #
    # x = block3_conv1(x)
    # x = block3_conv2(x)
    # x = block3_conv3(x)
    # x = block3_pool(x)
    #
    # x = block4_conv1(x)
    # x = block4_conv2(x)
    # x = block4_conv3(x)
    # x = block4_pool(x)
    #
    # x = block5_conv1(x)
    # x = block5_conv2(x)
    # x = block5_conv3(x)
    # x = block5_pool(x)
    #
    # out = flatten(x)

    inp = (105, 105, 3)
    model = siamese(inp)
    model.summary()
    print(get_flops(model))


if __name__ == "__main__":
    main()
