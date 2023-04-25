# fall-detection-iot-solution

ver 0.0.1 (by Shiyu, Adam and Luohua)

All artifacts can be found from https://drive.google.com/drive/u/1/folders/1IZYhe6mn8hMXtcixAMq8bm1oOd1fXOrj

# Solution Diagram at a glance (WIP)

![IoT-based Fall Detection System for Home Safety ](doc/solution-diagram.jpeg)

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

# Using VS Code's Remote IDE

https://localhost:1441/#/
You need to run below command to generate console password daily

```
sudo /greengrass/v2/bin/greengrass-cli get-debug-password
```

# AWS IoT commands

Instead of using AWS's local Web Console, you can also use below command to list services

```
sudo /greengrass/v2/bin/greengrass-cli component list
```

To remove a component

```
sudo /greengrass/v2/bin/greengrass-cli deployment create --remove com.example.falldetect
```

To deploy a component

```
sudo /greengrass/v2/bin/greengrass-cli deployment create --recipeDir ~/fall-detection-iot-solution/rpi-aws-components/components/recipe/ --artifactDir ~/fall-detection-iot-solution/rpi-aws-components/components/artifacts/ --merge "com.example.falldetect=1.0.1"
```

The log is under (using root user to view or `sudo pcmanfm`)
```/greengrass/v2/logs```

# To check AWS IoT Greengrass logs

Run `sudo pcmanfm` and navigate to `/greengrass/v2/logs/`

# How to pair bangle watch and RPi

It tries to exposure BLE connection via JS from bangle watch, and then there is python script running on RPi to try to
connect to bangle watch via BLE by using device UUID.

# Humanizing the solution

We try to ship our products by enabling auto-pairing. For elder people, they just need to "Wear&GO"
The only step to onboard this product is, we will provide an admin portal to onboard the user. The admin portal requires
user (say, the caregiver) to provide device UUID and the mobile number for fall detection alert.

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

# Algo model update

We provide the caregiver a web page to report false fall detection.
Every night the RPi will upload the daily fall detection data in batch to AWS for model training.
Every night the RPi will download the latest model for fall detection.

# How to do a fall detection?

```
curl --location --request POST 'http://your-rpi-server-ip:5000/' \
--header 'Content-Type: application/json' \
--data-raw '{"Acc_X": 9.681701660156250000, "Acc_Y": 1.020812988281250000, "Acc_Z": 1.863098144531250000, "Mag_X": -0.815185546875000000, "Mag_Y": 0.412353515625000000, "Mag_Z": 0.079833984375000000}'
```

# How to notify caregiver when a fall is detected

The component `rpi-aws-components/components/artifacts/com.example.mqtt` will serve the fall detected msg and send msg
to AWS SNS service via MQTT. The AWS SNS then triggers a SMS to registered caregivers.

# When all else fails

This repo is a team effort, although it is under Luohua's git account. Contact luohua.huang@u.nus.edu and someone from
the team will help you out.

