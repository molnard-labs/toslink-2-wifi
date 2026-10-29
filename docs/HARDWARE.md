# Hardware and assembly

## Bill of materials

| Qty | Part | Notes |
| --- | --- | --- |
| 1 | [ESP32-S3-DEV-N16R8-US development board](https://www.hestore.eu/en/prod_10048120.html) | 16 MB flash, 8 MB octal PSRAM; the tested board has a GPIO48 addressable RGB LED. Verify the pinout and LED jumper on your particular board. |
| 1 | CLIFF FCR684205T / OTJ-5 | Optical **transmitter**, not the similarly named receiver. [Manufacturer data sheet, revision 2.1](https://www.cliffuk.co.uk/products/optical/FCR684205T.pdf). |
| 1 | 100 nF ceramic capacitor | Across the transmitter's supply and ground; mount within 7 mm of its lead frame, as specified by CLIFF. |
| 1 | TOSLINK optical cable | From transmitter output to the soundbar optical input. |
| 1 | Regulated 5 V USB power supply and USB cable | Supply the ESP32 board via USB; use a data-capable cable for initial flashing. |
| As needed | Insulated wire, mounting hardware and enclosure | Provide strain relief and insulation. A small piece of prototyping board is optional. |

## Wiring

The OTJ-5 has three electrical pins. Pin numbers below are **manufacturer pin numbers**, not the left-to-right positions on an arbitrary view. Check the drawing on page 3 of the [CLIFF data sheet](https://www.cliffuk.co.uk/products/optical/FCR684205T.pdf) against your actual part before soldering.

| OTJ-5 pin | Function | Connect to ESP32-S3 board |
| --- | --- | --- |
| 1 | GND | GND |
| 2 | VCC | **3V3**, not the 5 V USB rail |
| 3 | VIN | **GPIO4**, ESPHome S/PDIF output |

```text
ESP32-S3 3V3 ───────────┬───── OTJ-5 pin 2 (VCC)
                        │
                      100 nF
                        │
ESP32-S3 GND ───────────┴───── OTJ-5 pin 1 (GND)
ESP32-S3 GPIO4 ─────────────── OTJ-5 pin 3 (VIN)
                                  │ optical cable
                                  └──────────► JBL OPTICAL IN
```

The capacitor is connected **between VCC and GND**, not between VCC and itself. Check its two ends against the pin table. The transmitter has its own drive circuitry; the GPIO supplies a logic-level S/PDIF signal rather than driving the LED directly. The specified operating supply is 2.7–5.5 V and the input high threshold is 2.0 V; powering it from the board's 3.3 V rail makes the 3.3 V ESP32 logic interface appropriate. These limits apply to the specified OTJ-5, not arbitrary optical modules. Observe the data sheet's ESD and soldering guidance.

Power off before wiring; confirm 3V3/GND/VIN and check for shorts with a meter. Connect USB power to the development board, not to the OTJ signal pin. Do not look directly into the optical transmitter. Keep the cable mechanically supported.

## RGB LED

The tested board has one WS2812-compatible addressable LED on GPIO48, configured for GRB order. Board variants may differ. If the LED does not respond, check the board's RGB solder bridge/jumper and its documentation before changing the GPIO or color order. The tested board displayed red, green and blue correctly.

## Soundbar

Use the JBL **TV** source for optical input. This build has no HDMI connection to a TV, so HDMI ARC source priority was not tested. Optical auto-wake, standby behavior, source selection on wake and loss of the beginning of a track remain unverified; the firmware does not control JBL power or its input. A Home Assistant player state describes the ESP, not the physical JBL state.

See [Enclosure](../enclosure/README.md) for the local printable adaptation and redistribution restrictions. No PCB or fabrication Gerbers are supplied; this prototype is point-to-point wiring, so the pin table and data sheet are the assembly reference.
