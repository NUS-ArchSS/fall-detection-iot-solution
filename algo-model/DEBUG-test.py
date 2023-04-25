import json
import numpy as np
import joblib
import warnings

from flask import Flask, request

app = Flask(__name__)

warnings.filterwarnings('ignore', message='X does not have valid feature names')


# create a sample input record in JSON format
# fall = false
# input_json = '{"Acc_X": 9.352111816406250000, "Acc_Y": -2.879333496093750000, "Acc_Z": 1.144409179687500000, "Mag_X": -0.623779296875000000, "Mag_Y": 0.662597656250000000, "Mag_Z": -0.643066406250000000}'
# fall = true
# input_json = '{"Acc_X": 9.681701660156250000, "Acc_Y": 1.020812988281250000, "Acc_Z": 1.863098144531250000, "Mag_X": -0.815185546875000000, "Mag_Y": 0.412353515625000000, "Mag_Z": 0.079833984375000000}'


def do_fall_detection(input_json):
    model_file = "/Users/huanglh/Downloads/fall_detection_model.pkl"
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
    else:
        print("The model predicts that the input record does not represent a fall.")


@app.route('/', methods=['POST'])
def post_request():
    data = request.get_json()
    Acc_X = data['Acc_X']
    Acc_Y = data['Acc_Y']
    Acc_Z = data['Acc_Z']
    Mag_X = data['Mag_X']
    Mag_Y = data['Mag_Y']
    Mag_Z = data['Mag_Z']

    input_json = '{{"Acc_X": {}, "Acc_Y": {}, "Acc_Z": {}, "Mag_X": {}, "Mag_Y": {}, "Mag_Z": {}}}'.format(Acc_X, Acc_Y,
                                                                                                           Acc_Z, Mag_X,
                                                                                                           Mag_Y, Mag_Z)
    print(input_json)
    do_fall_detection(input_json)
    return 'ok'


if __name__ == '__main__':
    app.run()

