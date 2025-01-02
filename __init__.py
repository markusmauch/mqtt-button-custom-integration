"""The MQTT Push Button integration."""

from __future__ import annotations

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import Platform
from homeassistant.core import HomeAssistant
from homeassistant.helpers import device_registry as dr

from .const import CONF_NAME, CONF_TOPIC, CONF_VALUE_TEMPLATE, DOMAIN

PLATFORMS: list[Platform] = [Platform.SENSOR]

type Data = dict[str, str, dr.DeviceEntry]
type MqttPushButtonConfigEntry = ConfigEntry[Data]


async def async_setup_entry(
    hass: HomeAssistant, entry: MqttPushButtonConfigEntry
) -> bool:
    """Set up MQTT Push Button from a config entry."""
    data: Data = {}
    hass.data.setdefault(DOMAIN, data)

    device_registry = dr.async_get(hass)
    device = device_registry.async_get_or_create(
        config_entry_id=entry.entry_id,
        identifiers={(DOMAIN, entry.unique_id)},
        name=entry.data[CONF_NAME],
    )
    hass.data[DOMAIN][entry.entry_id] = {
        "name": entry.data[CONF_NAME],
        "topic": entry.data[CONF_TOPIC],
        "value_template": entry.data[CONF_VALUE_TEMPLATE],
        "device": device,
    }

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    return True


# TODO Update entry annotation
async def async_unload_entry(
    hass: HomeAssistant, entry: MqttPushButtonConfigEntry
) -> bool:
    """Unload a config entry."""
    return await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
