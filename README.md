Keyring CLI Beispiel
====================

Diese kleine CLI zeigt, wie man mit dem Python-Paket `keyring` Zugangsdaten sicher
im Betriebssystem-Schlüsselbund speichert und wieder abruft.

Voraussetzungen
---------------

- Python 3.13 (oder an Deine Umgebung anpassen)
- Abhängigkeit: `keyring`
- Windows: verwendet den Windows Credential Manager
- macOS: verwendet das macOS Keychain
- Linux: verwendet SecretService (GNOME Keyring) oder KWallet – Desktop/Daemon erforderlich

Installation (mit uv)
---------------------

Optional, wenn Du `uv` nutzt; passe sonst an Dein Tooling an.

```sh
uv sync
```

Verwendung
----------

```sh
uv run main.py backend

uv run main.py set <username> [--service <service>] [--password <pw>] [--no-confirm]
uv run main.py get <username> [--service <service>] [--quiet]
uv run main.py delete <username> [--service <service>]
```

Beispiele
---------

```sh
# Passwort für user "alice" speichern (Service-Name default: keyring-test)
uv run main.py set alice

# Passwort abrufen
uv run main.py get alice

# Nur das Passwort (für Pipes/Skripte)
uv run main.py get alice --quiet

# Passwort löschen
uv run main.py delete alice

# Aktives Backend anzeigen
uv run main.py backend
```

Sicherheit und Nutzerkontext (wichtig!)

---------------------------------------

- Der Keyring ist an den OS-Benutzer gebunden. Ein anderer Windows-/macOS-/Linux-User
  kann die Einträge nicht sehen oder lesen. Das ist Absicht und Teil der Sicherheit.
- Auf CI/Servern ohne Desktop kann kein Keyring-Backend verfügbar sein. Dann schlagen
  `get/set/delete` fehl oder nutzen ein weniger sicheres Fallback, wenn eines installiert ist.
- Übergib Passwörter nicht über die Kommandozeile (`--password`), wenn andere Nutzer
  Prozesslisten einsehen können. Nutze die sichere Eingabeaufforderung (Prompt) ohne Echo.
- Prüfe das aktive Backend mit `uv run main.py backend` oder `keyring --list-backends`.

Plattform-Hinweise
------------------

Windows

- Standardmäßig: Windows Credential Manager. Einträge sind pro Nutzerprofil. Policies
  oder Enterprise-Umgebungen können Verhalten beeinflussen.

macOS

- Standardmäßig: macOS Keychain. Beim ersten Zugriff fragt macOS evtl. nach Zustimmung.

Linux

- Benötigt meist einen laufenden Secret Service (z. B. GNOME Keyring Daemon) oder KWallet.
- Auf Headless-Servern ist das oft nicht verfügbar. Möglichkeiten:
  - Systemweit einen Secret-Service einrichten (mit Sorgfalt)
  - Für reine Entwicklung/Tests ein Filesystem-Backend einsetzen (nicht für Produktion)
  - Alternativ Umgebungsvariablen, Vaults (z. B. HashiCorp Vault), Azure Key Vault etc. nutzen

Fehlersuche
-----------

- Welches Backend? `uv run main.py backend` oder `uv run -m keyring --list-backends`
- Kein Eintrag gefunden: Service-Name und Username exakt gleich verwenden wie beim Speichern.
- Fehler auf Linux/headless: Prüfe, ob ein Secret Service läuft (dbus, gnome-keyring-daemon).

API-Notizen
-----------

- Speichern: `keyring.set_password(service, username, password)`
- Lesen: `keyring.get_password(service, username)` -> str | None
- Löschen: `keyring.delete_password(service, username)`

Lizenz
------

Dieses Beispiel ist zu Lernzwecken gedacht.
