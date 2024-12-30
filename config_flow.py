from .const import DOMAIN, CONF_TOPIC
import voluptuous as vol
from homeassistant import config_entries
from homeassistant.core import callback
import homeassistant.helpers.config_validation as cv
from homeassistant.const import CONF_NAME

@config_entries.HANDLERS.register(DOMAIN)
class MqttButtonConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Config flow for Modbus Integration."""

    VERSION = 1
    CONNECTION_CLASS = config_entries.CONN_CLASS_LOCAL_PUSH

    def __init__(self):
        self.mqtt_prefix = None

    async def async_step_user(self, user_input=None):
        """Handle the initial step."""
        errors = {}
        if user_input is not None:
            # self.mqtt_prefix = user_input[CONF_PORT]
            # self.mqtt_prefix = user_input[CONF_HOST]
            # self.mqtt_prefix = user_input[CONF_USERNAME]
            # self.mqtt_prefix = user_input[CONF_PASSWORD]
            # self.mqtt_prefix = user_input[CONF_PREFIX]
            return await self.async_step_add_device()

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema({
                # vol.Required(CONF_HOST, default="mqtt.local", description="MQTT host name/address"): cv.string,
                # vol.Required(CONF_PORT, default=1883, description="MQTT TCP port"): int,
                # vol.Required(CONF_USERNAME, default="", description="MQTT username"): cv.string,
                # vol.Required(CONF_PASSWORD, default="", description="MQTT password"): cv.string,
                # vol.Required(CONF_PREFIX, default="mqtt_button",): cv.string,
            }),
        )

    async def async_step_add_device(self, user_input=None):
        """Handle adding a new device."""
        if user_input is not None:
            device_data = {
                CONF_NAME: user_input[CONF_NAME],
                CONF_TOPIC: user_input[CONF_TOPIC]
            }
            return self.async_create_entry(
                title=user_input[CONF_NAME],
                data=device_data
            )

        return self.async_show_form(
            step_id="add_device",
            data_schema = vol.Schema({
                vol.Required(CONF_NAME, default="My MQTT Button", description="Name of the button"): cv.string,
                vol.Required(CONF_TOPIC, default="", description="MQTT topic"): cv.string,
            })
        )
