# fall-detection-iot-solution

ver 0.0.1 (by Shiyu, Adam and Luohua)

# Solution Diagram at a glance (WIP)
[IoT-based Fall Detection System for Home Safety ](./course-report/solution-diagram.jpeg)

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
We follow the Design Process for Human-Centric Systems to design our fall detection algo. See ![Design Process](./course-report/fall-detection-design-process.pdf)

# The fall detection Algo

It is using Random Forest Classifier, the data we reply on to do fall detections, are from

* 3 Axis Accelerometer (Kionix KX023)
* 3 Axis Magnetometer

and the model is trained with data set
from https://archive.ics.uci.edu/ml/datasets/Simulated+Falls+and+Daily+Living+Activities+Data+Set#

To make the fall detection more precise, we also try to introduce the heart-rate data to calibrate the detection result.

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

WIP so relik. Or just check with ChatGPT. This repo is a team effort, although it is under Luohua's git account.
