# Setup MQTT Broker and email configuration

## Set up an MQTT broker on Windows, using the Mosquitto broker

1. Download Mosquitto:
   - Go to the Mosquitto website: https://mosquitto.org/download/
   - Under the Windows section, click on the "Mosquitto Installer" link to download the installer for Windows.

2. Run the Mosquitto Installer:
   - Double-click the downloaded installer file (.msi) to run the Mosquitto Installer.
   - Follow the on-screen instructions to install Mosquitto. You can choose the default settings unless you have specific preferences.

3. Start the Mosquitto broker:
   - After the installation is complete, the Mosquitto broker should start automatically as a Windows service.
   - To verify if the service is running, open the Services Manager:
     - Press the Windows key + R to open the Run dialog box.
     - Type `services.msc` and press Enter.
   - In the Services Manager, look for a service named "Mosquitto Broker" or similar. The Status column should indicate that it is "Running".

4. Verify the Mosquitto broker installation:
   - Open a command prompt.
   - Execute the following command to check the version of the Mosquitto broker:
     ```shell
     mosquitto -h
     ```

   If the installation was successful, you should see the version and other information about the Mosquitto broker.

## Setup email configuration

1. Copy the `.env.example` file to the root directory and rename to `.env` 
2. Add configuration accordingly

### Use Gmail as the sender email

1. Follow the [instruction from Google](https://support.google.com/mail/answer/7104828) to set up SMTP server
2. Go to https://myaccount.google.com/ -> In Security Settings
   1. Enable 2-Step Verification
   2. Create an App password for this application
   3. Fill the password in your `.env` files

