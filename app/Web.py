import os
import logging
from flask import Flask, request, render_template
from models import Predict
from config import MODEL_FILE, LABEL_FILE

logging.basicConfig(level=logging.DEBUG,
                    format='[%(asctime)s]: {} %(levelname)s %(message)s'.format(os.getpid()),
                    datefmt='%Y-%m-%d %H:%M:%S',
                    handlers=[logging.StreamHandler()])

logger = logging.getLogger()

app = Flask(__name__)

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    args = request.args
    pred = Predict(MODEL_FILE, LABEL_FILE)
    if args:
        if args.get('mode').lower() == 'curl':
            logger.info(f"Predicting with mode {args}")
            result = pred.get_predicted_images(request.files['img'], mode='img')
            return logger.info(f"Predicting Result: {result}")
        if args.get('mode').lower() == 'base64':
            logger.info(f"Predicting with mode {args}")
            result =  pred.get_predicted_images(request.json['base64-img'], mode='byte')
            return logger.info(f"Predicting Result: {result}")
        if args.get('mode').lower() in ['image', 'imagefile', 'image_file', 'img', 'file']:
            logger.info(f"Predicting with mode {args}")
            result = pred.get_predicted_images(request.json['img'], mode='img')
            return logger.info(f"Predicting Result: {result}")
    else:
        logger.info(f"Predicting with No Mode")
        result = pred.get_predicted_images(request.json)
        return logger.info(f"Predicting Result: {result}")

@app.route('/label', methods=['GET', 'POST'])
def label():
    pred = Predict(MODEL_FILE, LABEL_FILE)
    print(f"Label: {pred.get_label()}")
    logger.info(f"Label: {pred.get_label()}")
