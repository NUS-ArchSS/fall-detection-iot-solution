import time
import json

import json
import numpy as np
import joblib
import warnings

from flask import Flask, request

app = Flask(__name__)

warnings.filterwarnings('ignore', message='X does not have valid feature names')


def do_fall_detection(input_json):
    model_file = "/home/pi/fall-detection-iot-solution/algo-model/fall_detection_model.pkl"
    # load the saved model from disk
    rf_model = joblib.load(model_file)
    # convert the input JSON to a numpy array
    input_dict = json.loads(input_json)
    input_list = [input_dict[key] for key in input_dict.keys()]
    input_data = np.array(input_list).reshape(1, -1)
    # use the trained model to predict the fall value for the input record
    prediction = rf_model.predict(input_data)
    # print the predicted fall value
    if prediction[0]:
        print("The model predicts that the input record represents a fall.")
        return True
    else:
        print("The model predicts that the input record does not represent a fall.")
        return False


@app.route('/', methods=['POST'])
def post_request():
    data = request.get_json()
    Acc_X = data['acc_x']
    Acc_Y = data['acc_y']
    Acc_Z = data['acc_z']
    Mag_X = data['mag_x']
    Mag_Y = data['mag_y']
    Mag_Z = data['mag_z']
    # need to support heart rate

    input_json = '{{"Acc_X": {}, "Acc_Y": {}, "Acc_Z": {}, "Mag_X": {}, "Mag_Y": {}, "Mag_Z": {}}}'.format(Acc_X, Acc_Y,
                                                                                                           Acc_Z, Mag_X,
                                                                                                           Mag_Y, Mag_Z)
    print(input_json)
    if do_fall_detection(input_json):
        return 'yes'
    return 'no'


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
