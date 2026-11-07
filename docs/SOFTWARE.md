# Software setup

The original JBL prototype was tested with ESPHome **2026.9.1**, ESP-IDF, 16 MB flash, 8 MB octal PSRAM and Music Assistant **2.10.8**. The new generic firmware and its onboarding flow require separate hardware verification. Other software versions may work but should be validated separately; `min_version` does not pin ESPHome.

## Prepare each new device

1. Install Python and ESPHome 2026.9.1, or use an ESPHome Device Builder installation of that version. From the repository root, run `python firmware/prepare_device.py friend1`, choosing a different label for each device. The script creates `firmware/private-devices/friend1/` with a separate copy of the configuration and refuses to overwrite an existing device directory. No API encryption key or OTA password is generated for the generic default.
2. From the repository root run `esphome config firmware/private-devices/friend1/optical-audio-bridge.yaml` and `esphome compile firmware/private-devices/friend1/optical-audio-bridge.yaml`. For initial USB flashing, use `esphome run firmware/private-devices/friend1/optical-audio-bridge.yaml`. Identify the correct serial device by disconnecting and reconnecting the board before flashing. Check the startup logs for PSRAM and the setup access point.
3. Label the enclosure so the owner can match it to its setup network. The device name has a MAC-derived suffix to distinguish units on the same network. The generic configuration does not include the builder's home Wi-Fi credentials.

The generic firmware has an **open setup access point**, no baked-in station SSID, an unencrypted API and no OTA password. While the AP is active, anyone nearby can connect and access the captive portal, which also offers firmware upload. On the normal Wi-Fi network, anyone with network access to the device can use its API and upload firmware over OTA. Use a trusted network and keep this behavior in mind if the configured Wi-Fi becomes unavailable.

## Connect to the owner's Wi-Fi

1. Power the bridge via a regulated USB supply and wait for its setup Wi-Fi network to appear. Connect a phone to the open `optical-audio-bridge` network; the device-specific name includes a suffix. The phone may report that the network has no internet.
2. Open the setup page presented by the phone. If it does not appear, open `http://192.168.4.1/` in the browser. Select the owner's **2.4 GHz** Wi-Fi network, enter its password and submit. Do not send that password to the builder.
3. After the device connects, reconnect the phone to the normal home network. If the Wi-Fi details are wrong or the network later becomes unavailable, wait for the open setup AP to return, reconnect to it and correct the credentials. The exact recovery timing and reboot behavior require testing on the new build.

The portal stores credentials on the device. ESPHome notes that flashing firmware by serial can overwrite Wi-Fi settings; test credential persistence after OTA or USB updates rather than assuming it. See the [official captive portal documentation](https://esphome.io/components/captive_portal/).

If you temporarily provision a friend's device on your own network for testing, remove those credentials before handover. An ordinary firmware upload is not a reliable factory reset. On the tested ESP32-S3 build, the Wi-Fi settings are in the NVS partition: a targeted NVS erase over USB resets all saved preferences but leaves the firmware intact. Identify the correct board and read and decode its actual partition table before erasing; offsets can differ across builds. Afterward, confirm that the open setup AP and portal return.

## Adopt and secure the device

After connecting the bridge to the owner's Wi-Fi, look for the discovered device in ESPHome Device Builder and choose **Adopt**. The firmware advertises the project's full configuration for import so the owner can edit the imported copy locally. This specific adoption and the first update after adoption have not yet been tested on the new device; a same-configuration OTA update preserved provisioned Wi-Fi during the earlier prototype test.

The owner can later add [API encryption](https://esphome.io/components/api/) and an [ESPHome OTA password](https://esphome.io/components/ota/esphome/) in that configuration and install the updated firmware. Keep those secrets private; the Home Assistant integration may need reconfiguration with the new API key when encryption is enabled. These protections do not add a password to the separate captive portal upload path.

## Home Assistant and Music Assistant

1. In Home Assistant, add the discovered ESPHome device, or add it by its IP address if discovery fails. The generic default does not require an API encryption key. Check its media player, RGB light and diagnostic entities; rename or assign it to a room in Home Assistant as needed.
2. In Music Assistant, enable the Home Assistant player provider and select the bridge's media player. YouTube Music requires configuring its provider separately; follow the [Music Assistant instructions](https://www.music-assistant.io/music-providers/youtube-music/).
3. Connect the TOSLINK cable to the soundbar or amplifier's optical input, select that input, and test a quiet Home Assistant announcement or known Music Assistant track. Increase volume gradually. On the tested JBL Bar 2.1 Deep Bass the optical input is labelled **TV**.

The original `jbl-wifi.yaml` remains available for the existing device, along with its original `JBL WiFi` and `JBL RGB` entity naming; do not replace its installed firmware as part of setting up a new bridge. Its original Wi-Fi and credential setup remains in `secrets.example.yaml`.

The YouTube Music provider is unofficial and requires separate setup. Cookies may expire or rotate; consult current provider guidance and do not publish authentication data. For Windows audio see [WINDOWS.md](WINDOWS.md). Neither the setup AP nor this firmware makes the bridge a Google Cast receiver or a native Windows sound output.

## Troubleshooting

- **No setup page:** ensure the phone is connected to the bridge's setup network and open `http://192.168.4.1/` directly. Some phones may automatically switch back to a network with internet access.
- **Device unavailable:** check 2.4 GHz Wi-Fi, USB power, IP/mDNS reachability and ESPHome logs. If API encryption was enabled later, check its key in Home Assistant as well.
- **No sound:** verify GPIO4, transmitter VCC/GND/VIN and decoupling, optical cable and the receiver's selected optical input; try a Music Assistant test source before diagnosing a streaming provider.
- **Wrong RGB colors or no light:** check the board's LED/jumper, GPIO48 and GRB order.
- **Soundbar does not wake:** select the optical input and power it on manually. Automatic power/input control is not implemented or verified.
