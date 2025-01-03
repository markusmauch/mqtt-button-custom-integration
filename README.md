![License](https://img.shields.io/badge/license-MIT-green)
![HACS Custom Integration](https://img.shields.io/badge/HACS-Custom-orange.svg)

# MQTT Push Button Custom Integration

This Home Assistant custom integration enables the use of modified [Xiaomi Aqara door and window contact sensors](https://www.aqara.com/eu/product/door-and-window-sensor/) as smart light push buttons. By leveraging [this tutorial](https://www.smarthomejetzt.de/xiaomi-aqara-tuer-und-fenstersensor-hack-fuer-die-nutzung-im-wandschalter-umbauen/), you can repurpose affordable Aqara contact sensors to smarten your light switches.

## Features

- Integrates modified Aqara contact sensors via Zigbee2MQTT.
- Allows configuration of MQTT topics, device names, and value templates.
- Detects **short push**, **long push**, and **double push** events.
- Enables automation based on the contact sensor's state.

## Installation

### Prerequisites

- Home Assistant
- [HACS (Home Assistant Community Store)](https://hacs.xyz/) installed
- [Zigbee2MQTT](https://www.zigbee2mqtt.io/guide/usage/integrations/home_assistant.html) setup with your modified Aqara contact sensor added

### Installation Steps

1. **Add Custom Repository to HACS**:

   - In Home Assistant, navigate to **HACS** in the sidebar.
   - Click on **Integrations**.
   - Click on the three dots (**⋮**) in the top right corner and select **Custom repositories**.
   - In the dialog that appears:
     - Paste the repository URL: `https://github.com/markusmauch/mqtt-push-button-custom-integration`
     - Select **Integration** as the category.
     - Click **Add**.

2. **Install the Integration**:

   - After adding the custom repository, search for "MQTT Push Button" in HACS.
   - Click on the integration and select **Download** to install it.

3. **Configure the Integration**:

   - Restart Home Assistant to load the new integration.
   - Go to **Settings** > **Devices & Services**.
   - Click **Add Integration** and search for "MQTT Push Button".
   - Follow the setup wizard:
     - **Name**: Enter the device name (e.g., `Lichtschalter Flur`).
     - **MQTT Topic**: Enter the Zigbee2MQTT topic where the contact state is published (e.g., `zigbee2mqtt/Lichtschalter Flur`).
     - **Value Template**: Enter the template to extract the contact state from the JSON payload (e.g., `{{ value_json.contact }}`).

## Usage

Once configured, the integration will create a sensor entity in Home Assistant that detects the following events:

- **Short Push**: A quick press and release.
- **Long Push**: A prolonged press.
- **Double Push**: Two quick presses in succession.

You can use these events in automations to trigger actions like toggling lights, activating scenes, or controlling other smart devices.

## Disclaimer

This integration involves hardware modification of the Aqara contact sensor. Please proceed with caution and understand that any modification may void warranties or cause unintended behavior. The author assumes no responsibility for any damage or issues arising from the use of this integration. Use at your own risk.

## Resources

- Tutorial for modifying the Aqara sensor: [Xiaomi Aqara Tür- und Fenstersensor hack für die Nutzung im Wandschalter umbauen](https://www.smarthomejetzt.de/xiaomi-aqara-tuer-und-fenstersensor-hack-fuer-die-nutzung-im-wandschalter-umbauen/)
- HACS Documentation: [https://hacs.xyz/](https://hacs.xyz/)
- Zigbee2MQTT Documentation: [https://www.zigbee2mqtt.io/](https://www.zigbee2mqtt.io/)

## Support
If you want to support my work feel free to

[!["Buy Me A Coffee"](https://www.buymeacoffee.com/assets/img/custom_images/orange_img.png)](https://www.buymeacoffee.com/markusmauch)