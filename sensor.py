"""Detect the button events and provde them via sensor platform."""

import asyncio

from homeassistant.components.mqtt import ReceiveMessage, async_subscribe
from homeassistant.components.sensor import SensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers import device_registry as dr, json
from homeassistant.helpers.entity import DeviceInfo
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.template import Template
from homeassistant.util.json import json_loads

from .const import CONF_NAME, CONF_TOPIC, CONF_VALUE_TEMPLATE, DOMAIN
from .detector import (
    DOUBLE_PRESS,
    DOWN,
    LONG_PRESS,
    SHORT_PRESS,
    UP,
    ButtonEventsDetector,
    EventType,
)


async def async_setup_entry(
    hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback
) -> None:
    """."""
    device: dr.DeviceEntry = hass.data[DOMAIN][entry.entry_id].get("device")
    name: str = hass.data[DOMAIN][entry.entry_id].get(CONF_NAME)
    topic: str = hass.data[DOMAIN][entry.entry_id].get(CONF_TOPIC)
    value_template: str = hass.data[DOMAIN][entry.entry_id].get(CONF_VALUE_TEMPLATE)
    sensor = ButtonEvent(device, name, topic, value_template)
    async_add_entities([sensor], update_before_add=False)


class ButtonEvent(SensorEntity):
    """Integrates the push button events detector."""

    def __init__(
        self, device: dr.DeviceEntry, name: str, topic: str, value_template=None
    ) -> None:
        """Register the sensor with the MQTT and initiating the button events detector."""
        super().__init__()

        @callback
        def handler(event_type: EventType):
            self._attr_state = event_type
            self.schedule_update_ha_state()
            asyncio.run(self.reset())

        self._device = device
        self._name = name
        self._topic = topic
        self._value_template = value_template
        self._unsubscribe = None
        self._detector = ButtonEventsDetector()
        self._detector.on(SHORT_PRESS, handler)
        self._detector.on(LONG_PRESS, handler)
        self._detector.on(DOUBLE_PRESS, handler)

        self._attr_name = name
        self._attr_unique_id = f"{self._device.name}_{self.name}"
        self._attr_device_info = DeviceInfo(
            identifiers=self._device.identifiers,
            name=self._device.name,
            manufacturer=self._device.manufacturer,
            model=self._device.model,
        )

    async def async_added_to_hass(self) -> None:
        """Subscribe to MQTT topic when entity is added to Home Assistant."""
        self._unsubscribe = await async_subscribe(
            self.hass, self._topic, self.message_received
        )

    async def async_remove(self):
        """Unsubscribe from MQTT topic when entity is removed."""
        if self._unsubscribe:
            self._unsubscribe()  # Unsubscribe when the entity is removed
        await super().async_remove()

    def message_received(self, msg: ReceiveMessage):
        """Send the payload to the events detector."""
        val = msg.payload
        if self._value_template is not None:
            val = self.apply_jinja_template(self._value_template, val)
        self._detector.process_event(DOWN if val else UP)

    def apply_jinja_template(self, template_string, json_string):
        """Apply a Jinja2 template to a string with given variables."""
        try:
            json_data = json_loads(json_string)
        except json.JSONDecodeError as e:
            return f"Error parsing JSON string: {e}"
        template = Template(template_string, self.hass)
        try:
            return template.async_render(json_data)
        except Exception as e:
            return f"Error rendering template: {e}"

    async def reset(self):
        """Reset the sensor after 1 second."""
        await asyncio.sleep(1)
        self._attr_state = None
        self.schedule_update_ha_state()

    @property
    def state(self) -> str:
        """."""
        return self._attr_state
