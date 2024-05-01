import visualkeras
from keras import layers
from nets.siamese import siamese
from PIL import ImageFont
from collections import defaultdict


color_map = defaultdict(dict)
color_map[layers.Conv2D]['fill'] = '#00f5d4'
color_map[layers.MaxPooling2D]['fill'] = '#8338ec'
color_map[layers.Dropout]['fill'] = '#03045e'
color_map[layers.Dense]['fill'] = '#fb5607'
color_map[layers.Flatten]['fill'] = '#ffbe0b'
font = ImageFont.truetype("arial.ttf", 20)
model = siamese([105, 105, 3])

visualkeras.layered_view(model, legend=True, font=font, color_map=color_map, to_file='siamese.png')

