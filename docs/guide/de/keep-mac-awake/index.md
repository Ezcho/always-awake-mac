Source: https://no-sleep-pika.online/guide/de/keep-mac-awake/
Language: de

MAC GUIDE · 2026-10-02

# Mac wach halten: Clamshell-Modus, caffeinate und pika im Vergleich

Netzteil und geschlossener Bildschirm, Terminal-Befehle oder pika: Voraussetzungen, Grenzen und das sichere Beenden einer Sitzung verständlich erklärt.

## Die passende Methode wählen

Ein dunkles Display, eine Bildschirmsperre und Systemruhezustand sind unterschiedliche Zustände. Ein gesperrter Mac kann weiterarbeiten. Für externe Bildschirme eignet sich Clamshell, für kurze Aufgaben mit offenem Deckel caffeinate und für Arbeit ohne externen Bildschirm bei geschlossenem Deckel pika mit Hilfsdienst.

## 1. Stromversorgung und Clamshell-Modus

Verbinde bei offenem Deckel Strom, einen unterstützten Monitor, Tastatur und Maus. Prüfe alles vor dem Zuklappen. Ein stromliefernder Monitor kann je nach Spezifikation das Netzteil ersetzen. Ein Ladegerät allein ergibt diese Konfiguration nicht. Monitoranzahl und Auflösung hängen vom Mac ab. Zubehörfreigaben bei offenem Deckel bestätigen.

[Apple · External displays](https://support.apple.com/en-us/102501)

## Einstellungen bei geöffnetem Deckel

Suche am angeschlossenen Notebook unter Systemeinstellungen → Batterie → Optionen nach der Verhinderung automatischen Ruhezustands bei ausgeschaltetem Display. Namen und Orte unterscheiden sich je nach macOS und Modell. Das Sperrpasswort kann aktiv bleiben. Diese Option ist keine allgemeine Umgehung des Ruhezustands beim Zuklappen. Notiere den ursprünglichen Wert.

[Apple · Sleep and wake settings](https://support.apple.com/guide/mac-help/mchle41a6ccd/mac)

## 2. Mit caffeinate vorübergehend wach bleiben

Öffne Terminal und starte den folgenden Befehl. caffeinate gehört zu macOS und benötigt kein sudo. Er verhindert inaktivitätsbedingten Systemruhezustand, während das Display ausgehen darf. Lass den Prozess laufen und beende ihn dort mit Control+C. Eine wartende Eingabe ohne Ausgabe ist normal. Die Anforderung endet mit dem Prozess.

```
caffeinate -i
```

## Zeitlimit, Display und einzelne Befehle

Der erste Befehl gilt 3.600 Sekunden, also eine Stunde. Der zweite hält auch das Display für 1.800 Sekunden, also 30 Minuten wach; ohne Bedarf -d weglassen. Der dritte führt make tatsächlich aus und begleitet diesen Prozess. Nur im gewünschten Build-Projekt starten. Ein sofort endender Starter kann die Anforderung vor der eigentlichen Hintergrundarbeit verlieren. Mit einem ausgeführten Programm wird -t nicht verwendet.

```
caffeinate -i -t 3600
```

```
caffeinate -di -t 1800
```

```
caffeinate -i make
```

## Was passiert beim Zuklappen?

-i betrifft Systemleerlauf, -d das Display. Deckelschließen ist eine andere Bedingung, deshalb garantieren diese Optionen keinen Betrieb ohne externen Monitor. -s gilt nur bei Netzstrom; -u meldet Benutzeraktivität und kann das Display einschalten. Flags nach ihrem dokumentierten Zweck auswählen.

## 3. pika installieren

pika unterstützt macOS 13 oder neuer, Apple Silicon und Intel. Das vollständige offizielle PKG installiert App und Administrator-Hilfsdienst. macOS-Authentifizierung und erforderliche Freigaben selbst abschließen. /Applications/pika.app öffnen, Dienstverbindung prüfen, Session einschalten, bei Bedarf Monitor OFF wählen und Deckel schließen. Schlafverhinderung wird vorher vorbereitet, Displaysteuerung danach angewendet. Bei offenem Deckel speichert Monitor nur die Wahl. Session OFF stellt die verwaltete Einstellung wieder her, ohne sofort das Display auszuschalten. Das Schließen des Fensters beendet die App nicht.

[pika herunterladen · 1.0.13](https://github.com/Ezcho/always-awake-mac/releases/download/v1.0.13/pika-1.0.13.pkg)

[Installationshilfe](https://no-sleep-pika.online/install/)

## Fortschritt prüfen und beenden

Notiere bei einem kurzen Test Startzeit und Fortschritt, und kontrolliere danach das Aufgabenprotokoll. Dies ist ein Prüfverfahren, keine Aussage über Tests aller Modelle. pmset -g assertions liest aktuelle Anforderungen, beweist aber weder Netzwerk- noch Deckelkontinuität. man caffeinate zeigt die lokal installierte Anleitung.

```
pmset -g assertions
```

```
man caffeinate
```

## Sperre, Netzwerk und Wärme

Eine Sperre ist nicht zwingend Schlaf. WLAN, VPN, API-Limits, wartende Freigaben oder App-Fehler können Arbeit unterbrechen. pika führt KI-Gespräche nicht weiter und repariert keine Verbindung. Ein laufender Mac gehört auf eine feste, belüftete Fläche, nicht in eine Tasche. Akku- oder Wärmeschutz sowie Dienstfehler können die Sitzung beenden; vollständiger Schutz vor Überhitzung oder Entladung wird nicht garantiert.

## Quellen und Geltungsbereich

Vergleich vom Entwickler von no-sleep-pika mit eigener App. Grundlage sind Apple-Dokumente, das macOS-Handbuch caffeinate(8) und pika 1.0.13. Keine Empfehlung durch Apple oder KI-Anbieter. Nur so lange wach halten, wie die Aufgabe es benötigt.

- [Apple: If your external display is dark or low resolution](https://support.apple.com/en-us/102501)

- [Apple: Set sleep and wake settings for your Mac](https://support.apple.com/guide/mac-help/mchle41a6ccd/mac)

- [Apple: Allow USB and other accessories](https://support.apple.com/en-us/102282)

- `man caffeinate` · macOS System Manager’s Manual

Vom no-sleep-pika-Entwickler verfasst; enthält unsere eigene App.

[pika herunterladen](https://github.com/Ezcho/always-awake-mac/releases/download/v1.0.13/pika-1.0.13.pkg)[MacBook mit geschlossenem Deckel →](https://no-sleep-pika.online/guide/de/macbook-lid-closed/)[Markdown](https://no-sleep-pika.online/guide/de/keep-mac-awake/index.md)
