# Diaper Detective Device

This repository contains the code for the Diaper Detective device. It is written using MicroPython for the PyCom WiPy 3.0 board.

## Hardware Setup

Visit the [WiPy hardware setup documentation](https://docs.pycom.io/gettingstarted/connection/wipy/), and follow the instructions for your particular connection method.

## Software Setup

Visit the [WiPy software setup documentation](https://docs.pycom.io/gettingstarted/installation/), and follow the instructions.

## IDE Setup
### Installation
* Install [Atom](https://atom.io/) (if you don't have it already)
* Go to packages > settings view > install packages, and install the "pymakr" package.  This adds a panel with a custom built-in serial terminal.
* You may also want to install the "language-python" and "linter-pylint" plugins. They help with code-completion, and help enforce python best practices.

### Connecting
* If you're using the Expansion board, you should be good to go.  Just try to connect your device.
* If you're using a USB-serial or USB-UART adapter, make sure that you've added your device's manufacturer to the "autoconnect_comport_manufacturers" setting in "global settings".
* If you're still having connection issues, visit [PyCom getting started forum](https://forum.pycom.io/category/24/getting-started)

## IDE Usage
Once your device is connected, and communicating with the IDE plugin, we should be ready to run code.

* To run code (over the serial port, without writing it to the device's flash memory), just click "Run" in the IDE plugin.
* To upload code to the device (write it to the device's flash memory so it remains on the board), just click "Upload".

## More Resources
* Learn more about [MicroPython](https://docs.pycom.io/gettingstarted/programming/micropython/)
* Learn more about the [Pymakr plugin](https://atom.io/packages/pymakr)
* Learn more about the [WiPy 3.0](https://pycom.io/product/wipy-3-0/)
* Learn more about the [DHT22 Humidity/Temp sensor](https://www.adafruit.com/product/385)
* Learn more about the [PyCom Bluetooth APIs](https://docs.pycom.io/firmwareapi/pycom/network/bluetooth/)
