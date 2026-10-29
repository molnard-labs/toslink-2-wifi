# Developer notes and design decisions

## Problem and goals

The JBL Bar 2.1 Deep Bass accepts digital optical input but lacks AUX. The project adds Wi-Fi playback, Home Assistant and Music Assistant control, and an addressable status/ambient LED. The prototype was also tested with Windows film audio, without claiming low latency. The aim is a reproducible hobby build rather than a production-ready, certified appliance.

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

The 500 ms speaker buffer and 1 MB media-player buffer favor stability over minimal latency; those configured sizes do **not** equal a measured end-to-end delay. Wi-Fi power saving is disabled to prioritize responsiveness. API encryption and OTA credentials are user-provided secrets. `reboot_timeout: 0s` avoids rebooting when Home Assistant is temporarily unavailable, which also means the API itself will not automatically reset a stalled connection.

## Why these choices

- **Optical instead of AUX:** the target soundbar has no AUX input; optical preserves a digital signal and isolates the electrical link.
- **ESPHome and Home Assistant:** use the existing home setup, native integration, OTA and maintained components; the same endpoint is usable from Music Assistant through its Home Assistant player provider.
- **S3 with PSRAM:** PSRAM is useful for buffered audio tasks and the board already has Wi-Fi and an addressable LED. The S3's Bluetooth is LE only; the firmware does not provide a classic Bluetooth A2DP receiver.
- **Music Assistant for services:** one controller and library, including the unofficial YouTube Music provider; a Google Cast receiver is not implemented. YouTube Music account cookies can expire and playback can fail independently of the ESP.
- **VBAN through Music Assistant for PC audio:** an existing provider and Windows sender gave a working proof of concept without adding a custom ESP component. It requires a sender on each Windows machine and can introduce significant buffering. It is not a direct, low-latency ESP32 VBAN receiver.
- **No automatic JBL controls:** no verified optical wake/source control or separate power-control interface is implemented. Select TV and power manually until behavior is tested.

## Verification record

Prototype testing on 2026-10-29: ESPHome 2026.9.1 firmware compiled and flashed; Wi-Fi and PSRAM were checked; the user confirmed red, green and blue LED colors, an optical test tone, Music Assistant's ocean-wave sample, YouTube Music audio after refreshing a cookie, and Windows/MPC-HC film audio via VBAN. YouTube Music initially returned HTTP 403. The VBAN receiver needed the source IP observed at the server rather than the sender's own configured LAN address.

Not verified: objective end-to-end latency, lip sync, long-term dropouts and stability, unattended recovery, JBL optical auto-wake/input selection, or reproducibility on other board revisions. Do not infer these from the successful audio test.

## Development workflow

Keep credentials in an ignored `firmware/secrets.yaml`. Build changes against the tested ESPHome version first; validate and compile, check generated ESPHome logs, and verify the physical output and LED after firmware changes. Back up the known-good configuration before OTA upgrades. Changes to the audio pipeline must be tested with announcements and music, restart/reconnect, and any Windows path they affect. Treat memory/buffer values as engineering tradeoffs and measure latency and packet loss before making performance claims.

For latency evaluation, use a known synchronized flash/click video and capture the screen and soundbar together with a camera or a shared measurement setup; report repetitions, direction of offset and method. A single anecdotal observation is not a measurement. Compare directly against the existing Bluetooth setup if relevant.

Possible future work: quantify latency, add documented wake/input control only after measurement, improve recovery, and investigate a direct low-latency receiver as a separate experimental component. None is part of the published working firmware. Local incomplete experiments are not included in this repository.
