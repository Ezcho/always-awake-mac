Source: https://no-sleep-pika.online/guide/
Language: en

[← Home](https://no-sleep-pika.online/)

# Keep a MacBook awake with the lid closed: pika guide

Use Session to keep work running, and Monitor to choose the display behavior after you close the lid.

Updated October 1, 2026

[How to keep a MacBook running with the lid closed →](https://no-sleep-pika.online/guide/macbook-lid-closed/)

## Start a closed-lid session

Install the full pika PKG and open /Applications/pika.app. Wait for the helper connection, turn Session ON, choose Monitor, then close your MacBook’s lid. Keep the Mac ventilated.

Turning Session ON does not immediately blank or lock the screen. While the lid is open, changing Monitor saves your choice; pika applies its display policy after the lid closes. Reopening the lid cancels pending display-off work.

When you finish, turn Session OFF. This restores the sleep setting managed by pika and shows Monitor as OFF. It does not immediately turn off the screen. Closing the control window keeps pika running in the menu bar.

## Monitor OFF, screen locked: is the Mac asleep?

A locked screen and system sleep are different states. Monitor OFF requests display sleep after the lid closes; macOS may then require your password according to your Lock Screen settings. You do not need to disable that password requirement for pika.

While the Session and helper remain active, pika requests that the Mac stay awake. A lock screen alone does not prove that background work has stopped. An individual app may still pause when locked or need user input; check your actual agent or job log.

pika can end a session when battery or thermal protection triggers, the helper connection is lost, or the app stops responding. Session ON is not a promise that a job will run indefinitely.

## Can Wi-Fi or an AI agent disconnect?

Yes. Preventing system sleep does not guarantee a network connection. Wi-Fi signal, router or ISP outages, VPN policies, and a remote API’s timeout or service limits can still interrupt a job. pika does not reconnect Wi-Fi or retry your agent’s failed requests.

For a first run, try a short job with the lid closed, reopen the Mac, and check timestamps and errors in the job’s own log. If work stopped, check both pika’s session status and the network. A local process can continue while a remote API request fails.

For Wi-Fi problems, Option-click the Wi-Fi menu and open Wireless Diagnostics. For long remote jobs, use the agent’s supported retry and checkpoint features when available.

## Update without downloading another installer

If an older version cannot check for updates or macOS blocks pika-updater, install pika 1.0.13 or later once using the full PKG. After that, choose Check for Updates in the menu bar or the update button in the control window. Automatic checks only notify through the menu; installation starts when you choose it.

Keep the lid open and finish your work before updating. pika stops the Session, verifies the download, and opens the standard macOS Installer. Complete its authorization and installation steps, then reopen pika from Applications. The PKG updates the app and helper together. Session stays OFF. If installation is cancelled, reopen pika and try again. Restart MCP client connections after updating.

## The menu bar icon is missing

Open pika from Applications to bring its controls to the foreground. Closing that window leaves the app running. If many status items crowd the menu bar, reduce other menu bar items or switch to an app with fewer menus, then check again.

Check Activity Monitor for pika / AlwaysAwake before opening more copies. To quit fully, use pika’s Quit action rather than the window’s × button.

## Connect pika to a local MCP client

Keep pika running on the same Mac and user account as your MCP client. The server uses local STDIO; the website address is not an MCP endpoint.

With Codex CLI installed, run once in Terminal:

```
codex mcp add pika -- /Applications/pika.app/Contents/MacOS/pika-mcp
```

Or add this to ~/.codex/config.toml. Update an existing pika entry instead of duplicating it:

```
[mcp_servers.pika]
command = "/Applications/pika.app/Contents/MacOS/pika-mcp"
```

Restart the MCP client and open a new chat. Ask: “Call pika_status and show the state without changing Session or Monitor.” A successful tool response confirms the app connection. Inspect sessionOn, recoveryRequired and lastError before requesting changes.

pika_set_session controls Session. pika_set_monitor controls Monitor and requires Session ON. For another local MCP client, use STDIO with the executable path below, no arguments, and no API key:

```
/Applications/pika.app/Contents/MacOS/pika-mcp
```

Closing the agent does not end the pika session. Turn Session OFF in the app or ask the agent to do it.

## Installation or helper connection failed?

The installation guide covers the unified PKG, macOS security warnings, and reinstalling after quitting pika. The download is not Developer ID signed or notarized; behavior depends on macOS security settings.

[Install pika →](https://no-sleep-pika.online/install/)
