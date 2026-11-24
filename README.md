# Wireless Modulation Interface (WMI)

An experimental hardware and software platform for electronic musical performance devices.

## Purpose

The Wireless Modulation Interface project explores how physical gestures, environmental observations, tactile interactions and computational processes can be transformed into musically useful modulation signals.

The platform separates signal acquisition, communication, interpretation, transformation and output generation, allowing different performance devices to share a common technical foundation.

## Design principles

- Source independence
- Communication protocol independence
- Instrument independence within defined electrical limits
- Standalone performance operation
- Expressive and configurable signal transformation
- Predictable timing and responsiveness
- Electrical safety and defined failure behaviour
- Modular hardware and software
- Reproducible construction and verification

## Platform architecture

```text
Performance devices
        |
Communication adapters
        |
Common signal representation
        |
Modulation processing and routing
        |
Output interfaces
        |
Musical instruments
```

## Communication interfaces

Planned interfaces include Bluetooth Low Energy (BLE), Wi-Fi, Open Sound Control (OSC), ESP-NOW, BLE MIDI and USB MIDI. Individual implementations may support a subset of these interfaces.

## Reference implementations

### WMI-01

A standalone, battery-powered wireless modulation interface based on the ESP32-S3.

Initial design objectives:

- Two independent analog control voltage outputs
- Four logical DAC channels
- BLE gesture controller support
- Wi-Fi configuration
- Physical modulation depth controls
- Hardware output muting
- Power supervision and watchdog protection
- Modular internal construction

The initial target instrument is the ASM Hydrasynth Desktop.

### Nano 33 BLE Gesture Controller

An existing handheld motion-sensing controller based on the Arduino Nano 33 BLE Rev2. This device is the first intended performance signal source for WMI-01.

## Repository organization

| Directory | Purpose |
|---|---|
| `docs/` | Architecture and engineering decisions |
| `hardware/common/` | Reusable hardware subsystems |
| `hardware/WMI-01/` | First reference implementation |
| `firmware/common/` | Reusable embedded software |
| `firmware/WMI-01/` | WMI-01 firmware |
| `protocols/` | Communication and signal specifications |
| `devices/` | Performance signal source implementations |
| `tools/` | Development and diagnostic utilities |
| `tests/` | Automated tests |
| `examples/` | Example configurations and applications |

## Development environment

Python 3.12, Conda, PlatformIO, KiCad and Git.

```bash
conda env create -f environment.yml
conda activate wmi
python -m pip check
```

KiCad is installed separately.

## Development status

Experimental engineering project. Hardware designs are under development and have not yet completed electrical verification or instrument integration testing. Draft circuits are not released for construction or connection to musical instruments.

## Licensing

Licensing has not yet been selected. No open-source or open-hardware license is granted by this draft repository.
