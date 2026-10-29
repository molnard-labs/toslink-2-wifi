# Software setup

## Firmware and first flash

The verified build used ESPHome **2026.9.1**, ESP-IDF, 16 MB flash and 8 MB octal PSRAM. Music Assistant **2.10.8** was used for the integration test. Other versions may work but should be validated separately. The file sets `min_version`; it does not pin an installed ESPHome version.

1. Install the tested ESPHome version or use an ESPHome Device Builder installation of that version. Copy this repository's `firmware/jbl-wifi.yaml` and `firmware/secrets.example.yaml` to the same configuration directory.
2. Copy `secrets.example.yaml` to `secrets.yaml`. Set your 2.4 GHz Wi-Fi credentials, a unique ESPHome API encryption key, and a unique OTA password. Generate a 32-byte base64 key with ESPHome's key generator; do not copy a real key into the repository. Back up the secrets securely.
3. Validate: `esphome config firmware/jbl-wifi.yaml`. Compile and flash: `esphome run firmware/jbl-wifi.yaml`. In Device Builder, install using its USB/serial flow instead. If multiple serial devices are connected, identify the board by disconnecting and reconnecting it before flashing.
4. Check startup logs for Wi-Fi and PSRAM. Subsequent firmware changes may be installed over OTA using the configured OTA password. Removing power during a flash can require USB recovery.

The ESPHome API uses encryption. API reboot timeout is disabled and Wi-Fi power saving is disabled in this prototype. The player uses 48 kHz, 16-bit stereo S/PDIF and FLAC media/announcement pipelines, with mixer and resampler tasks in PSRAM. Player volume starts at 25%. GPIO48 LED starts off on each boot. Actual ESPHome entity names depend on the device and friendly names.

## Home Assistant and Music Assistant

1. Add the device through the Home Assistant ESPHome integration; enter the API encryption key when prompted. Check the media player, RGB light and diagnostic entities.
2. In Music Assistant, enable the Home Assistant player provider and select **JBL WiFi**. Names may differ if you changed the configuration. YouTube Music requires configuring its provider separately; follow the [Music Assistant instructions](https://www.music-assistant.io/music-providers/youtube-music/).
3. Select the JBL **TV** source and test a quiet announcement or known audio track. Increase volume gradually.

The YouTube Music provider is unofficial and requires a supported paid account, a login cookie and a PO-token service. Cookies may expire or rotate. One initial attempt returned HTTP 403; replacing the expired cookie restored playback during testing, although subsequent errors are possible. Never publish cookies or authentication data.

For Windows audio see [WINDOWS.md](WINDOWS.md). Source-specific integrations are configured in Music Assistant; no Google Cast receiver is included in the firmware.

## Troubleshooting

- **Device unavailable:** check 2.4 GHz Wi-Fi, USB power, API encryption key, IP/mDNS reachability and ESPHome logs.
- **No sound:** verify GPIO4, transmitter VCC/GND/VIN and decoupling, optical cable and JBL TV input; try a Music Assistant test source before diagnosing a streaming provider.
- **Wrong RGB colors or no light:** check the board's LED/jumper, GPIO48 and GRB order.
- **YouTube Music searches but does not play:** inspect Music Assistant logs for auth or stream errors, follow the provider's current setup guidance, and do not expose the cookie in logs or screenshots.
- **JBL does not wake:** select TV and power it on manually. Automatic power/input control is not implemented or verified.
