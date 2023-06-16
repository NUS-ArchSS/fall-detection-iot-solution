sudo /greengrass/v2/bin/greengrass-cli deployment create --recipeDir ~/Desktop/fall-detection-iot-solution/rpi-aws-components/components/recipe/ --artifactDir ~/Desktop/fall-detection-iot-solution/rpi-aws-components/components/artifacts/ --merge "com.example.mqtt=1.0.2"

sudo /greengrass/v2/bin/greengrass-cli deployment create --recipeDir ~/Desktop/fall-detection-iot-solution/rpi-aws-components/components/recipe/ --artifactDir ~/Desktop/fall-detection-iot-solution/rpi-aws-components/components/artifacts/ --merge "com.example.falldetect=1.0.3"

sudo /greengrass/v2/bin/greengrass-cli deployment create --recipeDir ~/Desktop/fall-detection-iot-solution/rpi-aws-components/components/recipe/ --artifactDir ~/Desktop/fall-detection-iot-solution/rpi-aws-components/components/artifacts/ --merge "com.example.datacollector=1.0.2"

sudo /greengrass/v2/bin/greengrass-cli deployment create --recipeDir ~/Desktop/fall-detection-iot-solution/rpi-aws-components/components/recipe/ --artifactDir ~/Desktop/fall-detection-iot-solution/rpi-aws-components/components/artifacts/ --merge "com.example.bangledatareceiver=1.0.2"