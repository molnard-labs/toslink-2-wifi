# TOSLINK 2 Wi-Fi

An ESPHome-based Wi-Fi audio endpoint for a soundbar or amplifier with an optical S/PDIF input. Built for a JBL Bar 2.1 Deep Bass, which has no analog AUX input, using an ESP32-S3 and a CLIFF OTJ-5 optical transmitter.

**Status: working prototype.** Home Assistant announcements, Music Assistant audio, the onboard RGB LED, YouTube Music through Music Assistant, and Windows audio through VBAN were heard on the JBL. End-to-end video synchronization and automatic wake/input selection have **not** been measured or established.

```text
Music Assistant ── Home Assistant ── Wi-Fi ── ESP32-S3 ── OTJ-5 ── optical ── JBL
Windows / MPC-HC ── Voicemeeter VBAN ── Music Assistant ── same path ───────────┘
```

This is an ESPHome/Home Assistant media player, not a native Windows audio endpoint, Bluetooth receiver, Google Cast receiver, or DLNA renderer. YouTube Music is accessed through its Music Assistant provider; its own Cast button does not discover this device. Windows audio needs a sender such as Voicemeeter. Music Assistant's VBAN path is not designed for video synchronization; actual latency is unmeasured and may be noticeable. Audio from multiple sources is not simultaneous: select the required source in Music Assistant.

## Build and use

1. Gather the parts and wire the transmitter as described in [Hardware and assembly](docs/HARDWARE.md). Check the actual pin orientation against the linked manufacturer drawing **before applying power**.
2. Copy [`firmware/secrets.example.yaml`](firmware/secrets.example.yaml) to `firmware/secrets.yaml` and enter your own Wi-Fi, API encryption and OTA credentials. Never commit the filled-in file.
3. Use ESPHome Device Builder or ESPHome **2026.9.1** to validate, compile and initially flash [`firmware/jbl-wifi.yaml`](firmware/jbl-wifi.yaml). See [Software setup](docs/SOFTWARE.md) for installation and Home Assistant discovery.
4. Connect the optical cable from the OTJ-5 transmitter to the JBL's optical input, select **TV** on the JBL and start with moderate volume. In Music Assistant select the Home Assistant player **JBL WiFi** and play a track.
5. The RGB LED appears as **JBL RGB**; the configuration sets it off at every reboot. For Windows audio follow [Windows and VBAN](docs/WINDOWS.md).

The files in `firmware/` are the complete project-specific firmware configuration: there is no custom component to install. ESPHome itself generates the compiled firmware from this configuration and its upstream components. The working configuration uses GPIO4 for S/PDIF and GPIO48 for the board's WS2812-compatible RGB LED.

## Documentation

- [Hardware, bill of materials and wiring](docs/HARDWARE.md)
- [ESPHome, Home Assistant and Music Assistant setup](docs/SOFTWARE.md)
- [Windows/MPC-HC and VBAN](docs/WINDOWS.md)
- [Architecture, choices, verification and development](docs/DEVELOPMENT.md)
- [Enclosure and original model attribution](enclosure/README.md)

The original enclosure model is under a separate restrictive licence. The locally modified print file is **not redistributed** here; see the enclosure notes. Source code and original project documentation are available under the [MIT licence](LICENSE); third-party software and designs retain their own licences.
