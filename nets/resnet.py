from keras import Input
from keras.applications.resnet50 import ResNet50
from keras.layers import Flatten
from keras.models import Model

class myResNet50:
    def __init__(self):
        base_model = ResNet50(include_top=False,input_shape=(200,200,3)) # ensure input shape is correct
        x = base_model.output
        x = Flatten()(x)  # flatten the output tensor to 2D
        self.model = Model(inputs=base_model.input, outputs=x)

    def call(self, inputs):
        outputs = self.model(inputs)
        return outputs
