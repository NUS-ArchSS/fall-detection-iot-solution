# Fall Detection using Bangle.js 2 Smart watch

## How it works

- [x] Get real-time Accelerometer, Magnetometer, and Heart Rate data from the bangle watch

- [x] Auto connect with [Bangle.js](https://www.espruino.com/Bangle.js2) smart watch on Raspberry Pi and get real-time data through Web Bluetooth

- [x] Analysis of the collected data to detect the occurrence of falls
- [x] Sent notification to AWS by MQTT on RPi
- [x] Store data in local db on Raspberry Pi
- [ ] Send data in RPi local db to AWS S3
- [ ] Schedual a cron job to send db data to AWS S3 for future fall prediction
