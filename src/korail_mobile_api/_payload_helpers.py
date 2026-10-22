"""Common protocol fields for existing imports."""


def _device_version_key(config, *, include_key=True):
    fields = {"Device": config.device, "Version": config.version}
    if config.app_version is not None:
        fields["AppVersion"] = config.app_version
    if include_key:
        fields["Key"] = config.key
    if config.lang is not None:
        fields["lang"] = config.lang
    return fields
