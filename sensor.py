from .const import DOMAIN, CONF_HOST, CONF_PORT, CONF_TOPIC, CONF_PREFIX, CONF_NAME, CONF_PASSWORD, CONF_USERNAME
from homeassistant.components.mqtt import async_subscribe
from .detector import ButtonEventsDetector, SHORT_PRESS, DOUBLE_PRESS, LONG_PRESS
from homeassistant.components.sensor import ConfigType, SensorEntity, SensorDeviceClass
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers.entity import DeviceInfo, EntityCategory
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from homeassistant.helpers import device_registry as dr
from homeassistant.const import TEMP_CELSIUS, PERCENTAGE, DEVICE_CLASS_HUMIDITY, VOLUME_FLOW_RATE_CUBIC_METERS_PER_HOUR
from homeassistant.const import UnitOfTime, UnitOfPower

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry, async_add_entities) -> None:
    device: dr.DeviceEntry = hass.data[DOMAIN][entry.entry_id].get("device")
    name: str = hass.data[DOMAIN][entry.entry_id].get("name")
    topic: str = hass.data[DOMAIN][entry.entry_id].get("topic")
    sensors = [
        ButtonEvent(device, name, topic),
    ]
    async_add_entities(sensors, update_before_add=False)


class ButtonEvent(SensorEntity):
    def __init__(self, device: dr.DeviceEntry, name: str, topic: str):
        super().__init__()
        @callback
        def short_press_handler():
            self._event = SHORT_PRESS
            self.async_write_ha_state()
        @callback
        def long_press_handler():
            self._event = LONG_PRESS
            self.async_write_ha_state()
        @callback
        def double_press_handler():
            self._event = DOUBLE_PRESS
            self.async_write_ha_state()
        self._event = None
        self._device = device
        self._name = name
        self._topic = topic
        self._detector = ButtonEventsDetector()
        self._detector.on(SHORT_PRESS, short_press_handler)
        self._detector.on(LONG_PRESS, long_press_handler)
        self._detector.on(DOUBLE_PRESS, double_press_handler)


    async def async_added_to_hass(self):
        """Run when entity is about to be added to Home Assistant."""
        @callback
        def message_received(self, msg):
            self._detector.process_event(msg.payload.decode("utf-8"))
        await async_subscribe(self.hass, self._topic, message_received)


    @property
    def device_info(self) -> DeviceInfo:
        return {
            "name": self._device.name,
            "manufacturer": self._device.manufacturer,
            "model": self._device.model,
            "identifiers": self._device.identifiers,
            "connections": self._device.connections,
            "sw_version": self._device.sw_version,
            "hw_version": self._device.hw_version,
        }

    @property
    def state(self):
        return self._event

    @property
    def id(self):
        return f"{self._device.id}_{self._name}"

    @property
    def name(self):
        return self._name