Source: https://no-sleep-pika.online/guide/es/keep-mac-awake/
Language: es

MAC GUIDE · 2026-10-02

# Cómo evitar que tu Mac se duerma: modo cerrado, caffeinate y pika

Compara la alimentación y el modo clamshell, los comandos de Terminal y pika. Aprende cuándo sirve cada método, qué ocurre al cerrar la tapa y cómo terminar la sesión.

## Elige según tu tarea

Apagar la pantalla, bloquearla y suspender el sistema son estados distintos. Un Mac bloqueado puede seguir trabajando. Para usar monitor externo, empieza por clamshell; para tareas temporales con tapa abierta, caffeinate; para trabajar cerrado sin monitor externo, considera pika con su servicio auxiliar.

## 1. Alimentación y modo clamshell

Con la tapa abierta, conecta alimentación, monitor compatible, teclado y ratón; comprueba su funcionamiento antes de cerrarla. Una pantalla que suministra energía puede sustituir al cargador según sus especificaciones. Conectar solamente el cargador no basta. El número y resolución de pantallas dependen del modelo; acepta los permisos de accesorios con la tapa abierta.

[Apple · External displays](https://support.apple.com/en-us/102501)

## Ajustes con la tapa abierta

En un portátil enchufado, busca en Ajustes del Sistema → Batería → Opciones la prevención de reposo automático cuando la pantalla está apagada. La ubicación varía según macOS y modelo. Puedes conservar la contraseña de bloqueo. No es una anulación universal del reposo al cerrar la tapa. Anota los ajustes originales.

[Apple · Sleep and wake settings](https://support.apple.com/guide/mac-help/mchle41a6ccd/mac)

## 2. Evitar reposo con caffeinate

Abre Terminal y ejecuta el comando siguiente. caffeinate viene con macOS y no necesita sudo. Evita el reposo por inactividad, aunque la pantalla puede apagarse. Mantén el proceso activo y pulsa Control+C en ese Terminal para terminar. Que no muestre mensajes es normal; la solicitud desaparece al finalizar el proceso.

```
caffeinate -i
```

## Duración, pantalla y comandos

El primer ejemplo dura 3.600 segundos, una hora; el segundo mantiene también la pantalla durante 1.800 segundos, media hora. Omite -d si no necesitas imagen. El tercero ejecuta realmente make y dura hasta que ese comando termina: úsalo solo en un proyecto que quieras compilar. Un lanzador que sale enseguida puede terminar antes que el trabajo real. Al ejecutar una utilidad, -t no se utiliza.

```
caffeinate -i -t 3600
```

```
caffeinate -di -t 1800
```

```
caffeinate -i make
```

## ¿Funciona con la tapa cerrada?

-i afecta al reposo del sistema por inactividad; -d al de la pantalla. Cerrar la tapa es otra condición: no son una garantía de funcionamiento cerrado sin monitor. -s solo es válido con alimentación de corriente; -u señala actividad y puede encender la pantalla. Selecciona las opciones por su función documentada.

## 3. Instalar pika

pika admite macOS 13 o posterior, Apple Silicon e Intel. Instala el PKG completo de la web oficial: contiene la app y el servicio auxiliar con privilegios. Completa personalmente la autenticación y aprobación necesarias en macOS. Abre /Applications/pika.app, confirma la conexión del servicio, activa Session, elige Monitor OFF si procede y cierra la tapa. La prevención se prepara antes; la política de pantalla se aplica después de cerrarla. Cambiar Monitor con la tapa abierta guarda la elección. Session OFF restaura el ajuste gestionado sin apagar inmediatamente la pantalla; cerrar la ventana no cierra la app.

[Descargar pika · 1.0.13](https://github.com/Ezcho/always-awake-mac/releases/download/v1.0.13/pika-1.0.13.pkg)

[Ayuda de instalación](https://no-sleep-pika.online/install/)

## Comprobar y finalizar

Prueba primero una tarea corta, registra la hora y revisa el progreso y los registros después. Es una prueba propuesta, no una certificación de todos los modelos. pmset -g assertions consulta solicitudes actuales sin modificarlas; no demuestra continuidad de red ni de funcionamiento cerrado. man caffeinate muestra el manual instalado.

```
pmset -g assertions
```

```
man caffeinate
```

## Bloqueo, red y temperatura

Bloqueo no significa necesariamente reposo. Wi-Fi, VPN, límites de API, permisos pendientes y errores pueden detener tareas: pika no continúa conversaciones ni reconecta la red. Mantén el Mac funcionando sobre una superficie firme y ventilada, no dentro de una bolsa. La protección térmica, la batería o un fallo del servicio pueden finalizar la sesión; no se garantiza evitar todo sobrecalentamiento o descarga.

## Fuentes y alcance

Comparación del creador de no-sleep-pika que incluye su propia app. Las fuentes son Apple, el manual caffeinate(8) de macOS y la documentación e implementación pública de pika 1.0.13. No implica recomendación de Apple ni de proveedores de IA. Mantén el equipo despierto solo durante el tiempo necesario.

- [Apple: If your external display is dark or low resolution](https://support.apple.com/en-us/102501)

- [Apple: Set sleep and wake settings for your Mac](https://support.apple.com/guide/mac-help/mchle41a6ccd/mac)

- [Apple: Allow USB and other accessories](https://support.apple.com/en-us/102282)

- `man caffeinate` · macOS System Manager’s Manual

Escrito por el creador de no-sleep-pika; incluye nuestra app.

[Descargar pika](https://github.com/Ezcho/always-awake-mac/releases/download/v1.0.13/pika-1.0.13.pkg)[Guía de MacBook cerrado →](https://no-sleep-pika.online/guide/es/macbook-lid-closed/)[Markdown](https://no-sleep-pika.online/guide/es/keep-mac-awake/index.md)
