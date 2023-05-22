# Set up Raspberry Pi as a Greengrass core device

## AWS setup

Sign in AWS Console - Navigate to `AWS Greengrass`

or click the url: https://ap-southeast-1.console.aws.amazon.com/iot/home?region=ap-southeast-1#/greengrass/v2/cores/create

Note: remember to change to your region

Follow the instructions to set up one greengrass core device

![image-20230401150749815](https://p.ipic.vip/mapf6c.png)

- Key in the core device name and thing group name respectively

## [Install Java on Raspberry Pi](https://pimylifeup.com/raspberry-pi-java/)

## Configure AWS credentials

Navigate to `IAM` - `Users`: Add users

Config as follow:

![image-20230415143039686](https://p.ipic.vip/gn1doy.png)

![image-20230523003330329](https://p.ipic.vip/xz55ex.png)

- Attach policies to the user
- Under `Security credentials` tab, create Access keys, after creation, download the `.csv` file containg the `ACCESS_KEY_ID` and `ACCESS_KEY`

- Open Terminal on Raspberry Pi, excute the command:


```
export AWS_ACCESS_KEY_ID=<AWS_ACCESS_KEY_ID>
export AWS_SECRET_ACCESS_KEY=<AWS_SECRET_ACCESS_KEY>
```

Continue with the instruction:

![image-20230523004144840](https://p.ipic.vip/f9l3mo.png)

## Greengrass deployment

### View all component list

```
sudo /greengrass/v2/bin/greengrass-cli component list
```

### Create a deployment

```
sudo /greengrass/v2/bin/greengrass-cli deployment create --recipeDir ./components/recipe --artifactDir ./components/artifacts --merge "com.example.mqtt=1.0.0"
```

### To remove a component:

```
sudo /greengrass/v2/bin/greengrass-cli deployment create --remove "com.example.mqtt"
```

The AWS Greengrass debug console is running on ports **1441** and **1442**, so we can forward Ports **1441** and **1442**, and change the port protocol to **HTTPS**

Then open https://localhost:1441/

Get debug password:

```
sudo /greengrass/v2/bin/greengrass-cli get-debug-password
```

Open up an explorer with privileges 

```
sudo pcmanfm
```

open `/greengrass/v2/logs` folder, and look at the logs

![image-20230401163615112](https://p.ipic.vip/679r3y.png)

