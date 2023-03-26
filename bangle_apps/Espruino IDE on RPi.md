

## [Using the Espruino IDE Via a Raspberry Pi](http://www.espruino.com/Quick+Start+BLE#via-a-raspberry-pi)

There are two ways of using the Raspberry Pi to control Espruino devices.

1. You can use the Espruino Hub software (which provides an MQTT bridge) and the Node-RED UI - see the [Node RED Tutorial](http://www.espruino.com/Puck.js+Node-RED)

2. ~~Or you can [use the Raspberry Pi to host a web-based version of the Web IDE](http://www.espruino.com/Raspberry+Pi+Web+IDE).~~  <- not working

### Use the Espruino Hub software

1.  Follow the instructions [on the EspruinoHub GitHub page](https://github.com/espruino/EspruinoHub)
   - Can ignore the "Get Raspbian running on your Raspberry Pi" part
   - Can choose between "Installation of everything (EspruinoHub, Node-RED, Web IDE)" or "Installation of EspruinoHub and Web IDE"

### Enable Web Bluetooth on Chromium

Follow the instruction on http://www.espruino.com/Quick+Start+BLE#with-web-bluetooth

> #### Linux
>
> Linux is not officially supported in Chrome and is not enabled by default, but it does work.
>
> To enable it:
>
> - Type `chrome://flags` in the address bar
> - You need to enable `Experimental Web Platform Features` (`chrome://flags/#enable-experimental-web-platform-features`).
> - Also enable `Use the new permissions backend for Web Bluetooth` (`chrome://flags/#enable-web-bluetooth-new-permissions-backend`) if it exists
> - Restart your browser

### Open [Espruino Web IDE](https://www.espruino.com/Web+IDE#espruino-web-ide)

1. Open the Web IDE [straight from the Web Browser](https://www.espruino.com/ide)

2. Install the IDE from the [Chrome Web Store](https://chrome.google.com/webstore/detail/espruino-web-ide/bleoifhkdalbjfbobjackfdifdneehpo)



**Now shoud be able to connect the Bangle.js 2 Watch to Raspberry Pi**



### Other Resource

- [Bluetooth LE and Node-RED with MQTT](https://www.espruino.com/BLE%20Node-RED)

- [Node-RED Running on Raspberry Pi](https://nodered.org/docs/getting-started/raspberrypi)
