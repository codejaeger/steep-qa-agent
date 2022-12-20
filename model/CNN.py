import os
import tensorflow as tf
import numpy as np
import cv2
from PIL import Image
from utils import label_map_util
import time


class CNN(object):
    """
    This class acts as the intermediate "API" to the actual game. Double quotes API because we are not touching the
    game's actual code. It interacts with the game simply using screen-grab (input) and keypress simulation (output)
    using some clever python libraries.
    """
    # What model to download.
    MODEL_NAME = 'steep'

    # Path to frozen detection graph. This is the actual model that is used for the object detection.
    PATH_TO_CKPT = MODEL_NAME + '/frozen_inference_graph.pb'

    # Path to frozen detection graph. This is the actual model that is used for the object detection.
    PATH_TO_LABELS = os.path.join('data', 'some.pbtxt')

    NUM_CLASSES = 3

    detection_graph = tf.Graph()

    def __init__(self):
        with self.detection_graph.as_default():
            od_graph_def = tf.GraphDef()
            with tf.gfile.GFile(self.PATH_TO_CKPT, 'rb') as fid:
                serialized_graph = fid.read()
                od_graph_def.ParseFromString(serialized_graph)
                tf.import_graph_def(od_graph_def, name='')

        label_map = label_map_util.load_labelmap(self.PATH_TO_LABELS)
        categories = label_map_util.convert_label_map_to_categories(label_map, max_num_classes=self.NUM_CLASSES,
                                                                    use_display_name=True)
        category_index = label_map_util.create_category_index(categories)

    def get_image_feature_map(self, image):
        start = time.time()
        with self.detection_graph.as_default():
            with tf.Session(graph=self.detection_graph) as sess:
            	# Definite input and output Tensors for detection_graph
                image_tensor = self.detection_graph.get_tensor_by_name('image_tensor:0')
                feature_vector = self.detection_graph.get_tensor_by_name(
                    "FeatureExtractor/MobilenetV1/Conv2d_13_pointwise_2_Conv2d_5_3x3_s2_128/Relu6:0")

                # image_np = cv2.resize(image, (490, ))
                image_np_expanded = np.expand_dims(image, axis=0)
                rep = sess.run([feature_vector], feed_dict={image_tensor: image_np_expanded})
                return np.array(rep).reshape(-1, 128)
# image = cv2.imread("iimma.jpg")
# # image_np = cv2.resize(image, (900, 400))
# im = Image.fromarray(image_np)
# im.show()
# Cnn = CNN()
# print(Cnn.get_image_feature_map(image)[1],Cnn.get_image_feature_map(image)[0])