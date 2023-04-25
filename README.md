# fall-detection-iot-solution

ver 0.0.1 (by Adam, ChatGPT, Luohua, Shiyu)

All artifacts can be found from https://drive.google.com/drive/u/1/folders/1IZYhe6mn8hMXtcixAMq8bm1oOd1fXOrj

# Solution Diagram at a glance

![IoT-based Fall Detection System for Home Safety](doc/solution-diagram.jpg)

# Data Flow

![Data Flow](doc/data-flow.jpg)

# Data from bangle watch

![sc-bangle](https://p.ipic.vip/o7maa9.png)

Once the app is launched by user, the following data will be send out through Web Bluetooth

- Time - Current time (milliseconds since 1970)

- [Accelerometer data](http://www.espruino.com/ReferenceBANGLEJS2#l_Bangle_accel)

    - `x` is X axis (left-right) in `g`
    - `y` is Y axis (up-down) in `g`
    - `z` is Z axis (in-out) in `g`

- [Magnetometer readings](http://www.espruino.com/ReferenceBANGLEJS2#l_Bangle_mag)

    - `x/y/z` raw x,y,z magnetometer readings

# Fall Detection Algo Design Process

We follow the Design Process for Human-Centric Systems to design our fall detection algo.
See [Design Process](doc/fall-detection-design-process.pdf)

# The fall detection Algo

The data we reply on to do fall detections, are from

* 3 Axis Accelerometer (Kionix KX023)
* 3 Axis Magnetometer
  and the model is trained with data set
  from https://archive.ics.uci.edu/ml/datasets/Simulated+Falls+and+Daily+Living+Activities+Data+Set#

The classifier accuracy comparison:

| Classifier                               | Training Accuracy |
| ---------------------------------------  | ----------------- |
| Random_Forest_classifier.py              | 0.999             |
| knn_classifier.py                        | 0.979             |
| Artificial_Neural_Networks_classifier.py | 0.934             |
| LSM_classifier.py                        | 0.635             |
| bayesian_decision_making_classifier.py   | 0.646             |

We decided to use Random Forest Classifier to do fall detection.

# When all else fails

This repo is a team effort, although it is under Luohua's git account. Contact luohua.huang@u.nus.edu and someone from
the team will help you out.

