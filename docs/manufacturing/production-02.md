# Production 02 firmware record

The second unit is a previously tested ESP32-S3 board with 16 MB flash and 8 MB PSRAM. On 2026-11-07 the exact factory image from the first production build and the published [v1.0.0 release](https://github.com/molnard-labs/toslink-2-wifi/releases/tag/v1.0.0) was written over USB; the flashing tool verified the written data. First-boot and device-specific tests for this build are pending.

- Manufacturing firmware source: [`1f2ccfa`](https://github.com/molnard-labs/toslink-2-wifi/commit/1f2ccfa5a4c5ec82aa2dd2caf05ad0c6fb6c6f81), tag `manufacturing-2026-11-07-01`.
- Factory binary SHA-256: `74519098ed238cd871fc39b37398dd6632e024b0438ba120d831baf5eba2e1f3`.
- USB flashing and write verification: `esptool` `5.3.1` using the board's USB-to-serial interface.
- The flash operation wrote the factory image but did not erase the NVS settings partition. An earlier reset of this board had returned it to setup mode; the settings present at the time of this flash were not independently checked.

See [Production 01](production-01.md) for the build toolchain, component lock and OTA binary hash. The first unit's tests do not by themselves prove the second unit's optical output or network behavior.
