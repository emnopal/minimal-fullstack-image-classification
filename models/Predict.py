import re
import base64
import numpy as np
import tensorflow as tf

from io import BytesIO
from pathlib import Path
from PIL import Image
from flask import jsonify


class Predict:

    def __init__(self, model_file='model.h5', label_file='labels.txt'):
        self.PARENT_PATH = str(Path(__file__).parent.parent)
        self.MODEL_PATH = self.PARENT_PATH + '/models'
        self.MODEL = self.MODEL_PATH + "/" + model_file
        self.MODEL_TFLITE = self.MODEL_PATH + "/" + model_file.strip('.')[0] + ".tflite"
        self.LABELS = self.PARENT_PATH + '/models' + "/" +label_file

    def __model(self):
        return tf.keras.models.load_model(self.MODEL)

    def __label(self):
        with open(self.LABELS, 'r') as label:
            labels = list(map(lambda x:x.strip(), label.readlines()))
        return labels

    def __predict(self, image, mode='base64'):
        model = self.__model()
        if mode.lower() == 'base64':
            img = self.base64_to_pil(image)
        if mode.lower() == 'img':
            img = Image.open(image)
        if mode.lower() == 'byte':
            img = Image.open(BytesIO(base64.b64decode(image)))
        img = img.convert('RGB')
        img = img.resize((150, 150))
        img = np.array(img)
        img = img.astype(np.float32) / 255
        img = np.expand_dims(img, axis=0)
        pred = model.predict(img)
        return pred

    # Convert base64 image data to PIL image
    def base64_to_pil(self, img_base64):
        image_data = re.sub('^data:image/.+;base64,', '', img_base64)
        pil_image = Image.open(BytesIO(base64.b64decode(image_data)))
        return pil_image

    # Convert numpy image (RGB) to base64 string
    def np_to_base64(self, img_np):
        img = Image.fromarray(img_np.astype('uint8'), 'RGB')
        buffered = BytesIO()
        img.save(buffered, format="PNG")
        return u"data:image/png;base64," + base64.b64encode(buffered.getvalue()).decode("ascii") # noqa

    def get_predicted_images(self, image, mode='base64'):
        predicted = self.__predict(image, mode)
        label = self.__label()
        probability_prediction = f"{(np.max(predicted))*100:.2f}%"
        class_prediction = label[np.argmax(predicted)]
        return jsonify({
            'status': True,
            'message': 'success',
            'status_code': 200,
            'data': {
                'result': class_prediction,
                'probability': probability_prediction
            }
        })

    def h5_to_tflite(self, optimizer=tf.lite.Optimize.OPTIMIZE_FOR_SIZE):
        model = self.__model()
        converter = tf.lite.TFLiteConverter.from_keras_model(model)
        converter.optimizations = [optimizer]
        tflite_model = converter.convert()
        open(self.MODEL_TFLITE, "wb").write(tflite_model)
        print(f"Model Exported from h5 ({self.MODEL}) to tflite ({self.MODEL_TFLITE})")

    def get_label(self):
        return self.__label()

    def get_model(self):
        return self.__model()
