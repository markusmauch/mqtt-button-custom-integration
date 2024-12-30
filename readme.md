# Maico Powerbox WS 75

![License](https://img.shields.io/badge/license-MIT-green)
![HACS Custom Integration](https://img.shields.io/badge/HACS-Custom-orange.svg)

A custom integration for Home Assistant to control and monitor the [Maico Powerbox WS 75](https://www.maico-ventilatoren.com/produkte/p/luftungsgerate-g61071/ws-75-powerbox-s-p124753) ventilation system. The device provides decentralized ventilation with heat and humidity recovery.

With this integration, you can monitor and manage key features of the Maico Powerbox WS 75, including operation mode and ventilation level switching, monitoring of temperature and air humidity values and controlling device parameters directly from Home Assistant.

## Prerequisites

The integration uses the device's ability to communication via modbus. You have to make sure that the powerbox is connected to your Network (either wired or WiFi) and modbus is activated. This requires to disable the AIR@home feature. You'll probably have to connect to the device via USB using the ['KWL-Inbetriebnahme-Software'](https://www.maico-ventilatoren.com/service/kwl-inbetriebnahme-software) in order to set things up.

## Features

- **Operation Mode Control**: Switch between the different operation modes.
- **Ventilation Level Control**: Switch between the different ventilation levels.
- **Control device parameter**: Change sleep function duration or reset error memory.
- **Temperature and Humidity Monitoring**: Real-time tracking of temperature valuess and air humidity.
- **Real time Energy Monitoring**: Real-time tracking of current power consumption.
- **Real time device parameter monitoring**: Real-time tracking of device parameters (air flow, internal states, etc.)
## Installation

1. **Download via HACS**:
   - Make sure [HACS](https://hacs.xyz/) is installed on your Home Assistant.
   - In HACS, go to **Integrations** > **+ Explore & Download Repositories**.
   - Add the custom repository https://github.com/markusmauch/powerbox-ws-75-custom-integration.
   - Click **Download** and follow the prompts to add the integration.

2. **Manual Installation**:
   - Clone or download this repository.
   - Copy the content of the repository folder to the `custom_components/powerbox` directory within your Home Assistant configuration.
   - Restart Home Assistant.

## Configuration

After installation, click the 'Add Integration' button in 'Settings', 'Devices and Services' and search for 'powerbox'. Then add the connection parameters to connect with your device:


name: "Maico Powerbox WS 75"
host: IP address of your Maico Powerbox device
port: Port (default is 80, change if necessary)
unit_id: # The modbus unit id (10 is default)


## Support
If you want to support my work feel free to
[!["Buy Me A Coffee"](https://www.buymeacoffee.com/assets/img/custom_images/orange_img.png)](https://www.buymeacoffee.com/markusmauch)