"""
Kleine CLI zum Speichern/Abrufen/Löschen von Zugangsdaten mit keyring.

Unterstützte Subcommands:
- set:    Passwort für (service, username) speichern
- get:    Passwort für (service, username) abrufen
- delete: Passwort für (service, username) löschen
- backend: Aktives Keyring-Backend anzeigen

Hinweise:
- Der Keyring ist OS- und nutzergebunden. Ein anderer Windows/macOS/Linux-User hat
  keinen Zugriff auf Deine Einträge und sieht sie nicht.
- Auf headless/Linux-Umgebungen kann ein Secret-Service/Keyring fehlen. Siehe README.
"""

from __future__ import annotations

import argparse
import sys
from getpass import getpass
from typing import Optional

import keyring
from keyring.errors import KeyringError, PasswordDeleteError


DEFAULT_SERVICE = "keyring-test"


def _prompt_password(confirm: bool = True) -> str:
    pw = getpass("Passwort: ")
    if confirm:
        pw2 = getpass("Passwort (Wiederholung): ")
        if pw != pw2:
            print("Fehler: Passwörter stimmen nicht überein.", file=sys.stderr)
            sys.exit(2)
    if not pw:
        print("Fehler: Leeres Passwort ist nicht erlaubt.", file=sys.stderr)
        sys.exit(2)
    return pw


def cmd_set(args: argparse.Namespace) -> int:
    service = args.service
    username = args.username
    password: Optional[str] = args.password
    if password is None:
        password = _prompt_password(confirm=not args.no_confirm)
    try:
        keyring.set_password(service, username, password)
        print(f"Gespeichert: service='{service}', username='{username}'")
        return 0
    except KeyringError as e:
        print(f"Keyring-Fehler beim Speichern: {e}", file=sys.stderr)
        return 1


def cmd_get(args: argparse.Namespace) -> int:
    service = args.service
    username = args.username
    try:
        pw = keyring.get_password(service, username)
        if pw is None:
            print("Kein Eintrag gefunden.", file=sys.stderr)
            return 3
        if args.quiet:
            # Nur das Passwort ausgeben (z.B. für Shell-Pipes)
            print(pw, end="")
        else:
            print(f"Passwort für '{username}' in service '{service}':\n{pw}")
        return 0
    except KeyringError as e:
        print(f"Keyring-Fehler beim Abrufen: {e}", file=sys.stderr)
        return 1


def cmd_delete(args: argparse.Namespace) -> int:
    service = args.service
    username = args.username
    try:
        keyring.delete_password(service, username)
        print(f"Gelöscht: service='{service}', username='{username}'")
        return 0
    except PasswordDeleteError:
        print("Kein Eintrag zum Löschen gefunden.", file=sys.stderr)
        return 3
    except KeyringError as e:
        print(f"Keyring-Fehler beim Löschen: {e}", file=sys.stderr)
        return 1


def cmd_backend(_: argparse.Namespace) -> int:
    kr = keyring.get_keyring()
    print(f"Aktives Backend: {kr.__class__.__module__}.{kr.__class__.__name__}")
    return 0


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        prog="keyring-test",
        description="CLI zum Speichern/Abrufen/Löschen von Credentials im OS-Keyring",
    )

    sub = p.add_subparsers(dest="cmd", required=True)

    # set
    p_set = sub.add_parser("set", help="Passwort speichern")
    p_set.add_argument("username", help="Benutzername")
    p_set.add_argument(
        "--service",
        default=DEFAULT_SERVICE,
        help=f"Service-Name (Default: {DEFAULT_SERVICE})",
    )
    p_set.add_argument(
        "--password",
        help="Passwort im Klartext übergeben (ansonsten sichere Eingabe-Prompt)",
    )
    p_set.add_argument(
        "--no-confirm",
        action="store_true",
        help="Keine Passwort-Bestätigung beim Prompt verlangen",
    )
    p_set.set_defaults(func=cmd_set)

    # get
    p_get = sub.add_parser("get", help="Passwort abrufen")
    p_get.add_argument("username", help="Benutzername")
    p_get.add_argument(
        "--service",
        default=DEFAULT_SERVICE,
        help=f"Service-Name (Default: {DEFAULT_SERVICE})",
    )
    p_get.add_argument(
        "-q",
        "--quiet",
        action="store_true",
        help="Nur das Passwort ohne Zusatztexte ausgeben",
    )
    p_get.set_defaults(func=cmd_get)

    # delete
    p_del = sub.add_parser("delete", help="Passwort löschen")
    p_del.add_argument("username", help="Benutzername")
    p_del.add_argument(
        "--service",
        default=DEFAULT_SERVICE,
        help=f"Service-Name (Default: {DEFAULT_SERVICE})",
    )
    p_del.set_defaults(func=cmd_delete)

    # backend
    p_be = sub.add_parser("backend", help="Aktives Keyring-Backend anzeigen")
    p_be.set_defaults(func=cmd_backend)

    return p


def main(argv: Optional[list[str]] = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
