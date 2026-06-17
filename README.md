# Deployment einer Todo-Listen-Verwaltung auf Raspberry Pi OS

## Ziel

Ziel dieser Aufgabe ist die Bereitstellung einer Todo-Listen-Verwaltung als Docker-Container auf einem Raspberry Pi mit Raspberry Pi OS.

Die Anwendung wurde in Python mit Flask entwickelt. Die API-Spezifikation befindet sich in der Datei `openapi.yml`.

---

# 1. System aktualisieren

Nach der Installation von Raspberry Pi OS werden zunächst die Paketquellen aktualisiert.

```bash
sudo apt update
sudo apt upgrade -y
```

---

# 2. Statische IP-Adresse konfigurieren

Für den Server wird eine feste IP-Adresse benötigt.

Die Konfiguration erfolgt mit NetworkManager:

```bash
sudo nmtui
```

Menü:

1. Edit a connection
2. Ethernet-Verbindung auswählen
3. IPv4 Configuration → Manual

Folgende Werte eintragen:

| Einstellung | Wert                    |
| ----------- | ----------------------- |
| IP-Adresse  | 192.168.24.111/24       |
| Gateway     | 192.168.24.254          |
| DNS         | 8.8.8.8, 192.168.24.254 |

Verbindung speichern und aktivieren.

Überprüfung:

```bash
nmcli connection show netplan-eth0
```

Die Ausgabe sollte folgende Werte enthalten:

```text
ipv4.method: manual
ipv4.addresses: 192.168.24.111/24
ipv4.gateway: 192.168.24.254
```

---

# 3. Benutzer anlegen

Benutzer ohne Administratorrechte erstellen:

```bash
sudo adduser willi
```

Benutzer für den Fernzugriff erstellen:

```bash
sudo adduser fernzugriff
```

Benutzer zur sudo-Gruppe hinzufügen:

```bash
sudo usermod -aG sudo fernzugriff
```

Überprüfung:

```bash
groups fernzugriff
```

Die Ausgabe muss die Gruppe `sudo` enthalten.

---

# 4. SSH installieren und aktivieren

OpenSSH Server installieren:

```bash
sudo apt install openssh-server -y
```

Dienst aktivieren:

```bash
sudo systemctl enable ssh
sudo systemctl start ssh
```

Status prüfen:

```bash
sudo systemctl status ssh
```

Der Dienst muss den Status `active (running)` besitzen.

---

# 5. Git installieren

```bash
sudo apt install git -y
```

---

# 6. Docker installieren

Docker installieren:

```bash
sudo apt install docker.io -y
```

Docker-Dienst aktivieren:

```bash
sudo systemctl enable docker
sudo systemctl start docker
```

Installation prüfen:

```bash
docker run hello-world
```

---

# 7. Repository herunterladen

Repository klonen:

```bash
git clone https://github.com/8lackSt33L/todo-api.git
```

Projektverzeichnis öffnen:

```bash
cd todo-api
```

---

# 8. Anwendung starten

Die Anwendung wird mit Docker Compose gestartet.

Container erstellen und starten:

```bash
docker compose up -d
```

Laufende Container anzeigen:

```bash
docker compose ps
```

Container stoppen:

```bash
docker compose down
```

Durch die Einstellung

```yaml
restart: unless-stopped
```

im `docker-compose.yml` wird der Container nach einem Neustart automatisch wieder gestartet.

---

# 9. Funktion prüfen

API lokal testen:

```bash
curl http://localhost:5000/todo-lists
```

API über das Netzwerk testen:

```text
http://192.168.24.111:5000/todo-lists
```

Bei erfolgreicher Installation liefert die Anwendung eine JSON-Antwort.

---

# Projektdateien

| Datei              | Beschreibung                               |
| ------------------ | ------------------------------------------ |
| main.py            | Python-Implementierung der REST-API        |
| openapi.yml        | OpenAPI-Spezifikation                      |
| Dockerfile         | Definition des Docker-Images               |
| docker-compose.yml | Container-Konfiguration                    |
| README.md          | Installations- und Konfigurationsanleitung |

---

# Verwendete Software

* Raspberry Pi OS
* Python 3.11
* Flask
* Docker
* Docker Compose
* OpenSSH Server
