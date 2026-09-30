Source: https://no-sleep-pika.online/guide/macbook-lid-closed/
Language: en

[← User guide](https://no-sleep-pika.online/guide/)

MACBOOK GUIDE

# How to keep a MacBook running with the lid closed

Close the screen and keep your work going. Choose the approach that fits an external-display desk or a background task without a monitor.

no-sleep-pika · October 1, 2026

For background work**Open pika → Session ON → Monitor OFF → close the lid**

Changing Session or Monitor with the lid open does not immediately blank your screen.

## Closing the lid: sleep or shutdown?

Closing a MacBook’s lid normally puts it to sleep rather than shutting it down. Finding your apps still open afterward does not mean a build, download or AI agent kept working throughout. [Apple’s sleep guide](https://support.apple.com/en-gb/guide/mac-help/mh10330/mac) lists closing a laptop display as a way to put the Mac to sleep.

The key distinction is between turning off a display and putting the system to sleep. A background task may need the Mac awake without needing a lit screen.

## Are you using an external monitor?

### Keep working on another screen

Check the Mac’s supported closed-display, or clamshell, setup with an external monitor, keyboard and mouse first. You may not need a separate sleep-prevention app for that workflow.

### Keep only a background task running

For a download, code build or AI agent without an external screen, follow the pika steps below. Start with a short test on your own Mac.

Before closing the lid, check that the external display and input devices work. On an Apple Silicon Mac, approve an accessory connection if requested. [Apple’s accessory guide](https://support.apple.com/en-us/102282) explains this for closed-lid use. Check your Mac model’s instructions for its power and supported display configuration.

## Use pika without an external monitor

- **Install and open pika.** Use the unified PKG from the homepage, then open pika in Applications. The helper must be connected. See [installation help](https://no-sleep-pika.online/install/) if setup is blocked.

- **Start your task and turn Session ON.** This does not immediately blank or lock the screen while the lid is open.

- **Leave Monitor OFF if you do not need a display.** Monitor is available while Session is ON. Its display policy applies after you close the lid.

- **Close the MacBook’s lid.** With Session ON, pika applies its closed-lid behavior. Use a ventilated desk.

- **Turn Session OFF when finished.** pika restores the sleep setting it managed. Monitor also shows OFF, without immediately turning the screen off.

The window’s × button only closes the controls. Leave pika running in the menu bar. If other status items hide its icon, open pika from Applications to bring the controls back.

## Check that your work actually continues

First try a task whose progress you can inspect, such as a build or AI agent job with timestamped logs.

- Note the progress or last log timestamp before closing the lid.

- Close the lid with Session ON and wait briefly.

- Reopen it and check for progress recorded during the closed-lid interval.

A lock screen alone does not mean the test failed. **Screen lock and system sleep are different.** Use your task’s progress as evidence. If an app is waiting for input or sign-in, pika cannot complete that interaction for you.

## Battery, heat and network conditions still matter

pika monitors battery level and macOS thermal state and may end a session when protection thresholds are reached. It uses more conservative limits with the lid closed and no external display. This does not make running a Mac inside a closed bag safe.

Preventing sleep does not guarantee Wi-Fi, VPN or remote API availability. A connection failure or service limit may stop an AI task. Use your tool’s supported retry and checkpoint features for long jobs.

The current download is not Developer ID signed or notarized, so macOS may block installation. Read the [security warning and installation guide](https://no-sleep-pika.online/install/) if needed. Verify behavior on your actual macOS version and hardware.

## Common questions

### Can I leave Session ON and Monitor OFF?

Yes. That is the setup for work without a lit display. Session manages keeping work running; Monitor controls display behavior after the lid closes.

### Will reopening the lid turn the screen off?

pika cancels its pending display-off work when the lid reopens. macOS’s own lock and display settings still apply.

### Can an AI agent control the session?

A local MCP client on the same Mac can query status and control Session and Monitor. See the [MCP setup steps and commands](https://no-sleep-pika.online/guide/#mcp).

For connection issues and missing menu bar icons, continue to the [full pika user guide](https://no-sleep-pika.online/guide/).

## Close your Mac. Keep work running.

pika is a macOS menu bar app with two switches: Session and Monitor. For macOS 13 or later on Apple Silicon and Intel.

[Download pika →](https://no-sleep-pika.online/)[Installation help](https://no-sleep-pika.online/install/)[Connect an AI agent with MCP](https://no-sleep-pika.online/guide/#mcp)
