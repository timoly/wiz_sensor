"""Support for WiZ sensors."""
from __future__ import annotations

from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorEntity,
    SensorEntityDescription,
    SensorStateClass,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import SIGNAL_STRENGTH_DECIBELS_MILLIWATT
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers.entity import EntityCategory
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from homeassistant.const import (
    CONF_DEVICE,
    ENERGY_KILO_WATT_HOUR,
    POWER_WATT,
    VOLUME_CUBIC_METERS,
)

from .const import DOMAIN
from .entity import WizEntity
from .models import WizData

SENSORS: tuple[SensorEntityDescription, ...] = (
    SensorEntityDescription(
        key="rssi",
        name="Signal Strength",
        entity_registry_enabled_default=False,
        state_class=SensorStateClass.MEASUREMENT,
        device_class=SensorDeviceClass.SIGNAL_STRENGTH,
        entity_category=EntityCategory.DIAGNOSTIC,
        native_unit_of_measurement=SIGNAL_STRENGTH_DECIBELS_MILLIWATT,
    ),
)

POWER_SENSORS: tuple[SensorEntityDescription, ...] = (
    SensorEntityDescription(
        key="power",
        name="power",
        entity_registry_enabled_default=True,
        state_class=SensorStateClass.MEASUREMENT,
        device_class=SensorDeviceClass.POWER,
        native_unit_of_measurement=POWER_WATT,
    ),
)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the wiz sensor."""
    wiz_data: WizData = hass.data[DOMAIN][entry.entry_id]
    # async_add_entities(
    #     WizSensor(wiz_data, entry.title, description) for description in SENSORS
    # )
    async_add_entities(
        WizPowerSensor(wiz_data, entry.title, description) for description in POWER_SENSORS
    )


class WizSensor(WizEntity, SensorEntity):
    """Defines a WiZ sensor."""

    entity_description: SensorEntityDescription

    def __init__(
        self, wiz_data: WizData, name: str, description: SensorEntityDescription
    ) -> None:
        """Initialize an WiZ sensor."""
        super().__init__(wiz_data, name)
        self.entity_description = description
        self._attr_unique_id = f"{self._device.mac}_{description.key}"
        self._attr_name = f"{name} {description.name}"
        self._async_update_attrs()

    @callback
    def _async_update_attrs(self) -> None:
        """Handle updating _attr values."""
        self._attr_native_value = self._device.state.pilotResult.get(
            self.entity_description.key
        )

class WizPowerSensor(WizEntity, SensorEntity):
    """Defines a WiZ sensor."""

    entity_description: SensorEntityDescription

    def __init__(
        self, wiz_data: WizData, name: str, description: SensorEntityDescription
    ) -> None:
        """Initialize an WiZ sensor."""
        super().__init__(wiz_data, name)
        self.entity_description = description
        self._attr_unique_id = f"{self._device.mac}_{description.key}"
        self._attr_name = f"{name} {description.name}"
        self._async_update_attrs()

    @callback
    def _async_update_attrs(self) -> None:
        """Handle updating _attr values."""
        self._attr_native_value = self._device.state.get_power()
