# Making an App

## Open Espruino Web IDE 

### 1. Update app code: `fd.app.js`

Click the down-arrow below the Upload button, then choose `Storage`, then `New File`, and then type `fd.app.js` and click `Ok`.

Now, click the `Upload` button. The app will be uploaded to the watch and then executed from the file. With this set, you can easily continue to develop your app as it is on the watch.

### 2. Upload an icon image: `fd.img`

1. Click the `Storage` icon
1. Choose `Upload a File`
1. Select the image file `fd.png`
1. The IDE will detect it is an image and offer you some options for conversion
1. Name the icon `fd.img`
1. Ensure `Convert for Espruino` and `Transparency` are checked
1. Choose `4 bit Mac Palette` and check the Preview. If the colours aren't good enough, try `8 bit Web Palette` instead.
1. Now click `Ok` to upload

### 3. App Info: `fd.app.info`

Copy and paste the following into the **left-hand side** of the IDE.

It'll write the relevant info to the file `fd.info`

```javascript
require("Storage").write("timer.info",{
  "id":"fd",
  "name":"FallDetect",
  "src":"fd.app.js",
  "icon":"fd.img"
});
```

Now can see the app on bangle watch:

![sc-bangle](https://p.ipic.vip/o7maa9.png)

Once the app is launched by user, the following data will be send out through Web Bluetooth

- Time - Current time (milliseconds since 1970)

- [Accelerometer data](http://www.espruino.com/ReferenceBANGLEJS2#l_Bangle_accel)

  - `x` is X axis (left-right) in `g`
  - `y` is Y axis (up-down) in `g`
  - `z` is Z axis (in-out) in `g`

- [Magnetometer readings](http://www.espruino.com/ReferenceBANGLEJS2#l_Bangle_mag)

  - `x/y/z` raw x,y,z magnetometer readings

- [HRM](http://www.espruino.com/ReferenceBANGLEJS2#l_Bangle_HRM)

  Heat rate data, as an object. Contains:

  ```json
  { "bpm": number,             // Beats per minute
    "confidence": number,      // 0-100 percentage confidence in the heart rate
    "raw": Uint8Array,         // raw samples from heart rate monitor
  }
  ```

- [HRM-raw](http://www.espruino.com/ReferenceBANGLEJS2#l_Bangle_HRM-raw)

  Contains:

  - HRM_r - `e.raw` from the `Bangle.on("HRM-raw")` event. This is the value that gets passed to the HRM algorithm.
  - HRM_f - `e.filt` from the `Bangle.on("HRM-raw")` event. This is the filtered value that comes from the Bangle's HRM algorithm and which is used for peak detection
  - PPG_r - `e.vcPPG` from the `Bangle.on("HRM-raw")` event. This is the PPG value direct from the sensor
  - PPG_o - `e.vcPPGoffs` from the `Bangle.on("HRM-raw")` event. This is the PPG offset used to map `e.vcPPG` to `e.raw` so there are no glitches when the exposure values in the sensor change.
