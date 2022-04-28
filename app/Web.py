import os
import logging
from flask import Flask, request, render_template, jsonify
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
    try:
        pred = Predict(MODEL_FILE, LABEL_FILE)
    except Exception as e:
        logger.info(f"Failed Predicting")
        return jsonify({
            'status': False,
            'message': 'failed',
            'status_code': 500,
        })
    if args:
        if args.get('mode').lower() == 'curl':
            logger.info(f"Predicting with mode {args}")
            result = pred.get_predicted_images(request.files['img'], mode='img')
            logger.info(f"Predicting Result: {result}")
            return result
        if args.get('mode').lower() == 'base64':
            logger.info(f"Predicting with mode {args}")
            result =  pred.get_predicted_images(request.json['base64-img'], mode='byte')
            logger.info(f"Predicting Result: {result}")
            return result
        if args.get('mode').lower() in ['image', 'imagefile', 'image_file', 'img', 'file']:
            logger.info(f"Predicting with mode {args}")
            result = pred.get_predicted_images(request.json['img'], mode='img')
            logger.info(f"Predicting Result: {result}")
            return result
    else:
        logger.info(f"Predicting with No Mode")
        result = pred.get_predicted_images(request.json)
        logger.info(f"Predicting Result: {result}")
        return result

@app.route('/label', methods=['GET', 'POST'])
def label():
    pred = Predict(MODEL_FILE, LABEL_FILE)
    print(f"Label: {pred.get_label()}")
    logger.info(f"Label: {pred.get_label()}")
