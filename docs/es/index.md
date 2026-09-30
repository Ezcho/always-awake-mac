Source: https://no-sleep-pika.online/es/
Language: es

# Cierra tu Mac y mantén tus tareas en marcha.

[Descargar para Mac](https://github.com/Ezcho/always-awake-mac/releases/download/v1.0.13/pika-1.0.13.pkg) 

36 Descargas

Versión pública 1.0.13 · macOS 13+ · Apple Silicon e Intel

## Conectar MCP

STDIO

Instala y abre pika; conecta con el comando de abajo. [Ver código fuente ↗](https://github.com/Ezcho/always-awake-mac#mcp)

`/Applications/pika.app/Contents/MacOS/pika-mcp`

## Connect your agent to pika

Set up once on the same Mac. Your agent can then read status and control Session / Monitor.

### 1Prepare pika

Install the pika PKG, which includes the app and helper. Open pika from Applications and keep it running in the menu bar. [Installation help ↗](https://no-sleep-pika.online/install/)

### 2Add the MCP server

If Codex CLI is installed, paste this into Terminal once. The MCP client starts the server when it connects.

`codex mcp add pika -- /Applications/pika.app/Contents/MacOS/pika-mcp`

No Codex CLI? Use a configuration file

For Codex, add this section to ~/.codex/config.toml. If pika already exists, update it instead of adding a duplicate. Keep your other settings.

```
[mcp_servers.pika]
command = "/Applications/pika.app/Contents/MacOS/pika-mcp"
```

Other local MCP clients

Add a server named pika using STDIO. Set Command to the path below. Leave arguments and environment variables empty. No server URL or API key is required.

`/Applications/pika.app/Contents/MacOS/pika-mcp`

This is a local STDIO connection. The website address is not an MCP endpoint, and a cloud-only URL connector cannot run this Mac executable.

[Codex official documentation ↗](https://learn.chatgpt.com/docs/extend/mcp?surface=cli) 

### 3Check the connection

Save, restart your MCP client, and open a new chat. Ask your agent:

`Call pika_status and show the current state. Do not change Session or Monitor.`

A successful pika_status tool result confirms the connection to the app. Session OFF is normal; helper registration alone does not confirm helper connectivity.

### What you can ask next

`pika_set_session` — Session ON / OFF
`pika_set_monitor` — Monitor ON / OFF · requires Session ON

Session ON prepares pika. Display policy applies only after the lid closes. With the lid open, Monitor changes only save your preference.

Closing the agent does not end a pika session. Turn Session OFF in pika or ask your agent to do so.

Connection not working?

No tools: confirm the command path and restart the client. App connection error: open pika on the same Mac and user account. Helper error: quit pika, reinstall the latest full PKG, and reopen pika. If Terminal says codex was not found, use the configuration-file option above.
