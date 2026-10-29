# Windows / MPC-HC audio via VBAN

The tested path is `MPC-HC → Voicemeeter Input → Voicemeeter B1 → VBAN → Music Assistant VBAN Receiver → Home Assistant player → ESP32 → TOSLINK`. The PC must be able to reach the Music Assistant server over the network. The ESPHome player is not directly discoverable as a Windows audio device.

## Configure the sender

1. Install [Voicemeeter Banana](https://vb-audio.com/Voicemeeter/banana.htm) following the vendor instructions. Restart Windows if requested by the installer.
2. Start Voicemeeter. Choose a working **A1 hardware output** as required by Voicemeeter. In the **Voicemeeter Input** virtual input strip, enable **B1**. Disable A1 on that strip if you do not want local monitoring or echo.
3. Open **VBAN**, enable VBAN, and configure an outgoing stream: source **BUS B1**, stream name `JBLPC`, destination = **your Music Assistant server's reachable LAN IP**, UDP port **6980**, 48 kHz, 2 channels, PCM 16-bit. Enable the outgoing stream. Never use an example address as a substitute for finding your own server address.
4. In MPC-HC, set **View → Options → Playback → Output → Audio Renderer** to `DirectSound: Voicemeeter Input (VB-Audio Voicemeeter VAIO)`. Reopen the movie for the renderer change to take effect. This changes MPC-HC's renderer; it does not require changing the Windows default output. To restore the original behavior, choose **System Default** and reopen the movie.

To send other applications, choose Voicemeeter Input for them in the Windows volume mixer, or make it the system default if desired. Consider whether local notification sounds should also be routed.

## Configure Music Assistant

1. Add the **VBAN Receiver** plugin. Set UDP port `6980`, stream name `JBLPC`, signed 16-bit little-endian PCM, 48000 Hz, 2 channels, and the sender IP **as observed by the Music Assistant host**.
2. In Music Assistant, select **JBL WiFi** as the player and choose **Browse → VBAN Receiver: JBLPC**. A sender must be actively transmitting. See the [official plugin documentation](https://www.music-assistant.io/plugins/vban-receiver/).
3. If packets do not arrive, check the sender's ON state, B1 routing, server address, port, local firewall and receiver settings. On the tested network, the packets arrived with a different source IP than the PC's LAN address, so the receiver had to be configured with the observed source address. This may depend on routing or NAT; do not assume the same address in another installation.

For a second laptop, install/configure a VBAN sender on that laptop and update the receiver's sender IP. Alternatively create another receiver instance with its own UDP port and matching sender settings, if supported by the sender. The tested Voicemeeter version used port 6980; check your sender's actual port configuration before relying on multiple instances.

## Film playback limitation

During the prototype test the user confirmed hearing film audio on the JBL. Video-to-audio synchronization was **not measured**, so this result does not establish that the setup is suitable for lip sync. Music Assistant explicitly says its VBAN path is not intended for sound that must line up with picture. Measure with a synchronized visual flash/audio click, repeat during playback, and consider buffering and drift before adjusting a player delay. Avoid assuming that an audio-delay control can compensate for audio that already arrives late: such controls generally delay audio rather than video, and behavior depends on the player.
