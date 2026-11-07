# Developer notes and design decisions

## Problem and goals

Optical Audio Bridge adds Wi-Fi playback to a soundbar or amplifier with an optical input, with Home Assistant and Music Assistant control and an addressable LED. The original prototype used a JBL Bar 2.1 Deep Bass, which lacks AUX. Windows film audio was also heard on that prototype, without establishing low latency. The aim is a reproducible hobby build rather than a production-ready, certified appliance.

## Architecture

```text
Music Assistant / HA ── HTTP audio and native API ── ESPHome speaker media player
                                                     │
                     resamplers → mixer → I2S peripheral in S/PDIF mode
                                                     │ GPIO4
                                     CLIFF OTJ-5 → optical cable → soundbar

Windows → Voicemeeter B1 / VBAN → MA VBAN Receiver → HA/ESPHome path above
```

The selected ESP32-S3 N16R8 has 16 MB flash and 8 MB octal PSRAM. The tested configuration uses ESP-IDF and official ESPHome components only. The `speaker` media player has separate media and announcement pipelines, both resampled to a mixer and then a single S/PDIF output. FLAC, 48 kHz, two channels and 16-bit output are the configured integration format, not a claim that every source is lossless. The ESPHome APIs and components are described in the [speaker media player](https://esphome.io/components/media_player/speaker/) and [I2S audio speaker](https://esphome.io/components/speaker/i2s_audio/) documentation.

The CLIFF FCR684205T transmitter accepts the board's 3.3 V logic when supplied at 3.3 V and converts electrical S/PDIF to optical. This avoids a DAC and an analog conversion path. The GPIO48 RGB LED is exposed with the official RMT LED strip component and always starts off. Component choices, pin assignments and power limits are documented in [HARDWARE.md](HARDWARE.md).

The 500 ms speaker buffer and 1 MB media-player buffer favor stability over minimal latency; those configured sizes do **not** equal a measured end-to-end delay. Wi-Fi power saving is disabled to prioritize responsiveness. In the generic firmware the API is unencrypted and OTA has no password by default; the owner can configure these protections later. `reboot_timeout: 0s` avoids rebooting when Home Assistant is temporarily unavailable, which also means the API itself will not automatically reset a stalled connection.

## Why these choices

- **Optical instead of AUX:** the target soundbar has no AUX input; optical preserves a digital signal and isolates the electrical link.
- **ESPHome and Home Assistant:** use the existing home setup, native integration, OTA and maintained components; the same endpoint is usable from Music Assistant through its Home Assistant player provider.
- **S3 with PSRAM:** PSRAM is useful for buffered audio tasks and the board already has Wi-Fi and an addressable LED. The S3's Bluetooth is LE only; the firmware does not provide a classic Bluetooth A2DP receiver.
- **Music Assistant for services:** one controller and library, including the unofficial YouTube Music provider; a Google Cast receiver is not implemented. YouTube Music account cookies can expire and playback can fail independently of the ESP.
- **VBAN through Music Assistant for PC audio:** an existing provider and Windows sender gave a working proof of concept without adding a custom ESP component. It requires a sender on each Windows machine and can introduce significant buffering. It is not a direct, low-latency ESP32 VBAN receiver.
- **No automatic JBL controls:** no verified optical wake/source control or separate power-control interface is implemented. Select TV and power manually until behavior is tested.
- **Separate onboarding configuration:** new generic units use an ESPHome setup AP and captive portal without the builder's Wi-Fi credentials. The AP is deliberately open for ease of setup; anyone nearby can access the setup portal while it is active, including its firmware upload function. The default API is unencrypted and OTA has no password, so anyone who can reach the device on the network can control it and upload firmware. Owners can add API encryption and an OTA password later. The original JBL configuration remains available and is not migrated automatically.

## Verification record

Prototype testing on 2026-10-29: ESPHome 2026.9.1 firmware compiled and flashed; Wi-Fi and PSRAM were checked; the user confirmed red, green and blue LED colors, an optical test tone, Music Assistant's ocean-wave sample, YouTube Music audio after refreshing a cookie, and Windows/MPC-HC film audio via VBAN. YouTube Music initially returned HTTP 403. The VBAN receiver needed the source IP observed at the server rather than the sender's own configured LAN address.

Not verified: objective end-to-end latency, lip sync, long-term dropouts and stability, unattended recovery, JBL optical auto-wake/input selection, or reproducibility on other board revisions. Do not infer these from the successful audio test.

On 2026-11-07, an earlier generic configuration with API encryption and an OTA password passed ESPHome 2026.9.1 validation and compilation and was flashed and verified over USB on a separate ESP32-S3 with 16 MB flash and 8 MB PSRAM. The owner opened the setup portal over its open AP. After an intentionally incorrect Wi-Fi password, the setup network remained reachable; after entering the correct one, the bridge connected, Home Assistant discovered it, and its ESPHome integration was added temporarily: the media player, RGB light and diagnostics appeared. The test integration was removed afterward. The owner confirmed the LED showed red, green and blue. An OTA upload of the same firmware succeeded, and the device reconnected to Wi-Fi and the encrypted API afterward; it also reconnected after a USB power cycle. Before handover, the tested board's NVS partition was erased over USB to remove the builder's Wi-Fi credentials, and the owner confirmed that the open setup network and portal returned. The current configuration without API encryption and an OTA password requires its own physical verification. Wi-Fi outage behavior, simultaneous devices and physical sound output also still require verification on new hardware; the optical transmitter had not yet been wired to this board. The prototype's earlier results do not demonstrate these new behaviors.

The subsequent unauthenticated generic configuration passed ESPHome 2026.9.1 validation and compilation and was flashed to that same board with successful write verification. ESPHome's import function fetched the published full configuration and produced a valid per-device configuration with the MAC suffix preserved in the device name. The Device Builder user-interface adoption, its first OTA update, and runtime API/OTA access without credentials still require separate verification.

## Development workflow

The optional per-device configuration copies are kept in the ignored `firmware/private-devices/` directory; the original JBL configuration uses an ignored `firmware/secrets.yaml`. If adding credentials later, keep them out of the repository and share them privately with the owner. Build changes against the tested ESPHome version first; validate and compile, check ESPHome logs, and verify the physical output and LED after firmware changes. Back up the known-good configuration before OTA upgrades. Changes to the audio pipeline must be tested with announcements and music, restart/reconnect, and any Windows path they affect. Treat memory/buffer values as engineering tradeoffs and measure latency and packet loss before making performance claims.

For latency evaluation, use a known synchronized flash/click video and capture the screen and soundbar together with a camera or a shared measurement setup; report repetitions, direction of offset and method. A single anecdotal observation is not a measurement. Compare directly against the existing Bluetooth setup if relevant.

Possible future work: quantify latency, add documented wake/input control only after measurement, improve recovery, and investigate a direct low-latency receiver as a separate experimental component. None is part of the published working firmware. Local incomplete experiments are not included in this repository.
