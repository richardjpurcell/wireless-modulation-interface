# WMI-01 | revision 2.4 | 2026-11-24

**REVIEW ONLY — not released for construction or connection to an instrument.**

This package provides five editable KiCad legacy-format schematic review sheets, a common pin/net register and an installed-component BOM. KiCad is not installed in the generation environment; opening, conversion to modern .kicad_sch, ERC and physical validation have not been performed. The drawings use pin-labelled block symbols rather than conventional graphical device symbols; all pins are passive in the draft library. They are independent sheets, not a hierarchical electrical project. Same-named nets across sheets are joined in the CSV design intent, not automatically in KiCad. Module and switch/relay pin IDs are logical, not footprint numbers. Do not fabricate a PCB from these files.

## Files and workflow

Open each `WMI-*.sch` in KiCad's schematic editor with its adjacent `-cache.lib` present. Save a copy in the current KiCad format; resolve any legacy library import warning using the included cache. Build a hierarchical root with global nets or explicit sheet ports, replace draft symbols with verified device symbols and assign footprints. Run ERC after changing pin electrical types. The CSV is the cross-sheet reference and should be reconciled against the resulting KiCad netlist. `bom.csv` lists installed design positions (not purchasing quantities or live distributor stock). HOLD means unresolved, not approved to install. NC denotes a deliberately unconnected terminal, not a shared net.

## Sheet notes

- PWR: protected cell -> BQ24074 -> fuse -> load-rated SPST -> 5 V boost. Charger USB independent. Feather BAT unused. The charger remains connected with power off. Set charger to 0.5 A only after checking cell charge rating. Verify discharge limit, thermal behavior, inrush, fuse and actual regulator current at low voltage. The 2000 mAh cell's standard discharge is listed as 0.5 A; this is not proof of 1 A capability. Target 500 mA at 5 V requires about 0.98 A at 3 V / 85% efficiency. Use current-limited bench power first.
- CORE: D5/D6 depth, D9 READY, D10 mode, D11 mute, D12/D13 LEDs, A4 heartbeat, A3 FAULT_N input, A5 optional battery measurement. 3.3 V DAC, direct I2C. DAC reference internal 2.048 V gain 1; initialize all channels, check address 0x60 or 0x64. No physical CV3/4. J4 represents removable boundary, not actual connector pinout or a second electrical path. No USB connection in RUN. Switch OFF, unplug **all** core harness connections (including expansion and any external signals), remove core from enclosure or otherwise enforce access, then connect Feather USB for SERVICE. Disconnect USB before reattaching. No simultaneous USB MIDI in this revision. This replaces unselected RUN/OFF/SERVICE rotary switch. The connector arrangement is on HOLD.
- SAFE: TPS3808 monitors 5 V via 107k/10k divider (nominal 4.7385 V), open drain reset to TPS3823 MR with 10k pullup. CT open for nominal 20 ms. TPS3823 reset output drives AND and GPIO input, not Feather reset (avoid contention with reset circuitry). READY and FAULT_N must both be high for ENABLE. Watchdog has nominal 1.6 s timeout, not a latched fault; firmware must drop READY on fault and explicitly rearm, but firmware lockup may defeat that action. A timed watchdog reset pulse alone does not guarantee persistent isolation; add independent latched inhibit or verified open-drain reset interface before release. Do not claim fail-safe behavior. Heartbeat only on successful processing loop; test stuck high, stuck low and floating. 10k WDI pulldown. Manual mute directly interrupts coil even if ENABLE remains high. Flyback diode directly across coil after switch; relay release is not instantaneous. Measure release delay. Manual unmute must occur only with READY low, then rearm; current circuit does not enforce this in hardware.
- CV2: two DAC input switches and two output switches in one ADG4612, all controlled by ENABLE. 100k input bias resistors establish reference when disconnected. MCP6002 gain 2.2, nominal no-load amplifier maximum 4.505 V, 1k/1uF filter ~159 Hz unloaded. Relay NO from filter, NC via 10k to ground, COM to output switch. 330R series and permanent 100k jack pulldown. Powered-off jack is weakly grounded, not a hard zero. The ADG4612 must be tested for operating signal range, logic levels, fault conditions and power sequencing. Do not assume negative fault protection from negative signal capability. TVS positions D2/D3 are DNP/HOLD: a ground-referenced clamp at the jack has no source-side current limit. Resolve polarity, leakage, ESD and sustained-fault envelope before release. Do not connect an external CV output to these jacks. Relay and jack terminal IDs logical until checked. Initial 0–4 V operating target is load-dependent; at 10k load the nominal model gives about 3.93 V full scale. No precision pitch specification.
- UI: two 10k linear pots, RC ADC filters, mode button, DPDT maintained mute, two LEDs. Battery divider is DNP/HOLD until actual switched battery measurement circuit exists. Do not attach BAT_SENSE_SW directly to battery; off-state backfeeding must be resolved. A3 repurposed to fault input; battery sense enable removed. Battery warning and dedicated mute LED remain deferred, not silently implemented. No additional I2C pullups specified until actual breakout pullups are measured. Do not assume ADC full-rail linearity.

## Release gates (all open)

1. Check exact battery ratings, charging, fuse, boost regulation and thermal performance; measure low-voltage and Wi-Fi peak loads.
2. Confirm Feather supply input and harness physical isolation; test USB and RUN separately without analog load.
3. Verify exact relay bottom-view drawing, contact continuity, coil polarity, switch terminals and all adapter mapping.
4. Close watchdog latching/reset and manual rearm logic; prove no uncontrolled re-enable after fault.
5. Complete battery measurement and hardware CV ESD/overvoltage network; document bounded positive/negative external fault test conditions.
6. Convert to native KiCad project, assign verified symbols, ERC, check against CSV. Bench-test with current-limited supply, DMM and oscilloscope before battery or synthesizer connection.
7. Test both channels with dummy loads 10k, 47k, 100k and measure startup/shutdown, mute, reset, stale data, recovery, ripple and latency. Confirm actual Hydrasynth input range/impedance from manual or measurement before connection.

## Manufacturer references

- https://www.adafruit.com/product/4755 and https://learn.adafruit.com/adafruit-bq24074-universal-usb-dc-solar-charger-breakout/pinouts
- https://www.adafruit.com/product/2011
- https://www.pololu.com/product/2565
- https://learn.adafruit.com/adafruit-esp32-s3-feather/pinouts
- https://www.adafruit.com/product/4470 and https://learn.adafruit.com/adafruit-mcp4728-i2c-quad-dac/pinouts
- https://www.ti.com/lit/ds/symlink/tps3823.pdf (DBV pinout)
- https://www.ti.com/lit/ds/symlink/tps3808.pdf (DBV pinout, not DRV)
- https://www.ti.com/product/SN74LVC1G08
- https://www.analog.com/media/en/technical-documentation/data-sheets/adg4612_4613.pdf (TSSOP pinout)

## Revision notes

2.4: replaces rotary service selector with removable core harness, keeps 5 V boost provisionally, assigns fault input instead of driving Feather RST directly, adds amplifier input bias, explicitly holds unverified TVS and battery sensing, exposes watchdog re-enable and manual mute rearm as unresolved requirements. The package records design intent rather than a final production design. Procurement list revision 2.3 remains provisional and must be reconciled after closure.
