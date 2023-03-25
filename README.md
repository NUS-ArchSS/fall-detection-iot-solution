fall-detection-iot-solution

# Using VS Code's Remote IDE
https://localhost:1441/#/
You need to run below command to geneate console password daily
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

# The fall detection Algo
It is using Random Forest Classifer, the data we reply on to do fall detections, are from 
* 3 Axis Accelerometer (Kionix KX023)
* 3 Axis Magnetometer

and the model is trained with data set from https://archive.ics.uci.edu/ml/datasets/Simulated+Falls+and+Daily+Living+Activities+Data+Set#

# How to do a fall detection? 
```
curl --location --request POST 'http://your-rpi-server-ip:5000/' \
--header 'Content-Type: application/json' \
--data-raw '{"Acc_X": 9.681701660156250000, "Acc_Y": 1.020812988281250000, "Acc_Z": 1.863098144531250000, "Mag_X": -0.815185546875000000, "Mag_Y": 0.412353515625000000, "Mag_Z": 0.079833984375000000}'
```

# How to notify caregiver when a fall is detected
The component `rpi-aws-components/components/artifacts/com.example.mqtt` will serve the fall detected msg and send msg to AWS SNS service via MQTT. The AWS SNS then triggers a SMS to registered caregivers.

# When all else fails
WIP so relik. Or just check with ChatGPT.
