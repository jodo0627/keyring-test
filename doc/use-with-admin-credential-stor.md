# Mit Admin Credentials nutzen

Um den **Windows Credential Manager** mit dem Python-Paket **`keyring`** für einen **Admin-Account** zu verwenden, gibt es ein paar wichtige Punkte zu beachten. Hier ist eine Schritt-für-Schritt-Anleitung:

---

## 🔧 Voraussetzungen

1. **Python installiert**
2. **`keyring`-Modul installiert**

   ```sh
   pip install keyring
   ```

3. **Python-Skript wird mit Admin-Rechten ausgeführt**, wenn du auf den Admin-Credential Store zugreifen willst.

---

## 🧠 Grundlegende Verwendung von `keyring`

```python
import keyring

# Speichern eines Passworts
keyring.set_password("System", "admin_username", "admin_password")

# Abrufen des Passworts
password = keyring.get_password("System", "admin_username")
print(password)
```

---

## 🛡️ Zugriff auf Admin-Credentials

Windows speichert Credentials pro Benutzer. Wenn du also mit einem normalen Benutzerkonto arbeitest, kannst du **nicht direkt auf die Admin-Credentials** zugreifen, es sei denn:

- Du führst das Skript **als Administrator** aus.
- Du verwendest ein Tool wie `runas` oder startest Python über eine **elevated PowerShell oder CMD**.

Beispiel:

```sh
runas /user:Administrator "python script.py"
```

---

## 🧰 Alternative: Verwenden eines benutzerdefinierten Backends

Falls du mehr Kontrolle brauchst, kannst du ein eigenes Backend definieren oder z. B. das `WindowsCredential`-Backend direkt verwenden:

```python
import keyring.backends.Windows

keyring.set_keyring(keyring.backends.Windows.WinVaultKeyring())
```
