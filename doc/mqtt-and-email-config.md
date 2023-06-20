# Setup MQTT Broker and email

## Set up an MQTT broker, using the Mosquitto broker

1. Download and install Mosquitto
   - Go to the Mosquitto website: https://mosquitto.org/download/ and follow the instruction.
   
4. Verify the Mosquitto broker installation:
   - Open a command prompt.
   - Execute the following command to check the version of the Mosquitto broker:
     ```shell
     mosquitto -h
     ```

   If the installation was successful, you should see the version and other information about the Mosquitto broker.
   
4. Start the Mosquitto broker:
   
   - After the installation is complete, the Mosquitto broker should start automatically as a service.

## Setup email configuration

1. Copy the `.env.example` file to the root directory and rename to `.env` 
2. Add configuration accordingly

### Use Gmail as the sender email

1. Follow the [instruction from Google](https://support.google.com/mail/answer/7104828) to set up SMTP server
2. Go to https://myaccount.google.com/ -> In Security Settings
   1. Enable 2-Step Verification
   2. Create an App password for this application
   3. Fill the password in your `.env` files

