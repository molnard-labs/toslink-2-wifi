# Production 01 firmware build record

This is the first production-unit build record, not a GitHub Release. On 2026-11-07 the factory image below was written over USB and verified on an ESP32-S3 with 16 MB flash and 8 MB PSRAM. The assembled unit opened its setup portal, joined the test Wi-Fi, appeared in Home Assistant and ESPHome Device Builder, and displayed red, green and blue on its LED. The user heard a Google Translate text-to-speech announcement and a Music Assistant sample through the optical output. An OTA upload of the archived OTA binary succeeded and the unit reconnected afterward. The temporary Home Assistant and Music Assistant entries were removed after testing. The unit's verified NVS partition was erased over USB to remove test Wi-Fi settings, and the user confirmed that the open setup network and portal returned. Device Builder adoption and the first update after adoption were not tested.

- Source commit: `1f2ccfa5a4c5ec82aa2dd2caf05ad0c6fb6c6f81`.
- Manufacturing tag / Device Builder import ref: `manufacturing-2026-11-07-01` (points to the source commit above).
- Project version in ESPHome: `1.0.0`.
- Toolchain used: ESPHome `2026.9.1`, ESP-IDF `5.5.5`, Xtensa GCC `14.2.0`; component versions and hashes: [dependencies.lock](production-01-dependencies.lock).
- USB flashing and write verification: `esptool` `5.3.1`, native ESP32-S3 USB serial/JTAG.
- Build time recorded in binary: `2026-11-07 11:14:59 +0100`.
- Committed YAML SHA-256: `5b00ef4366361e3eb4dad33f2f32de8dc7e19aa2e9482eab6b2a1aa78b96a432`.
- Build-copy YAML SHA-256: `d46c875623ab0fbb8236e0cdf4a21dddf748d51db7d54fbe504dacfbba21e962` (the copy has Windows CRLF endings; its contents match the committed YAML after normalizing line endings).
- Factory binary SHA-256: `74519098ed238cd871fc39b37398dd6632e024b0438ba120d831baf5eba2e1f3`.
- OTA binary SHA-256: `c4a485e884f09dc533902aca1bc88d2077c4542ccac5b80e47adc7ba384ab4e7`.

The two binaries and their build metadata are archived locally under the ignored `firmware/private-devices/production-01-20261107/archive/` directory for a potential later release. They do not include a configured station Wi-Fi network, API key or OTA password. A build timestamp and environmental differences mean that rebuilding the same source may not yield byte-identical artifacts; verify the hashes when distributing these exact binaries.

The setup access point and captive portal are open, and the default network API and OTA have no authentication. See [Software setup](../SOFTWARE.md) for the implications and optional protection.
