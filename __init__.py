from .const import DOMAIN, CONF_TOPIC
from .sensor import ButtonEvent
from homeassistant.components.mqtt import async_subscribe
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers import device_registry as dr
from homeassistant.const import CONF_NAME


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry):
    """Set up MQTT Button integration from a config entry."""
    # Forward the setup to the sensor platform
    try:
        hass.data.setdefault(DOMAIN, {})

        device_registry = dr.async_get(hass)
        device = device_registry.async_get_or_create(
            config_entry_id=entry.entry_id,
            identifiers={(DOMAIN, entry.unique_id)},
            name=entry.data[CONF_NAME],
        )
        hass.data[DOMAIN][entry.entry_id] = {
            "name": entry.data[CONF_NAME],
            "topic": entry.data[CONF_TOPIC],
            "device": device
        }
        await hass.config_entries.async_forward_entry_setup(entry, "sensor")
        return True
    except:
        return False

async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry):
    """Unload a config entry."""
    # Unload the sensor platform
    unload_ok = await hass.config_entries.async_forward_entry_unload(entry, "sensor")

    # Clean up any global references if necessary
    if unload_ok and entry.entry_id in hass.data.get(DOMAIN, {}):
        hass.data[DOMAIN].pop(entry.entry_id)

    return unload_ok