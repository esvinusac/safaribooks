#!/usr/bin/env python3
# coding: utf-8
"""
Script unificado para descargar libros de O'Reilly (Safari Books Online) usando login tradicional o SSO (cookies).
Permite al usuario ingresar credenciales o una cadena de cookies, y descarga el libro especificado.
"""
import sys
import os
import argparse
import getpass
import safaribooks

# Reutiliza la función de sso_cookies.py para transformar la cadena de cookies
def transform_cookies(cookies_string):
    cookies = {}
    for cookie in cookies_string.split("; "):
        key, value = cookie.split("=", 1)
        cookies[key] = value
    with open(safaribooks.COOKIES_FILE, 'w') as f:
        import json
        json.dump(cookies, f)
    print("[+] Cookie Jar guardado en 'cookies.json'.")


def main():
    parser = argparse.ArgumentParser(
        prog="oreillybooks.py",
        description="Descarga y genera un EPUB de tus libros favoritos de O'Reilly/Safari Books Online usando login tradicional o SSO.",
        add_help=True
    )
    auth_group = parser.add_mutually_exclusive_group(required=True)
    auth_group.add_argument(
        "--cred", metavar="<EMAIL:PASS>",
        help="Credenciales para login tradicional. Ejemplo: --cred 'usuario@mail.com:password'"
    )
    auth_group.add_argument(
        "--sso", action="store_true",
        help="Usar Single Sign-On (SSO) copiando la cadena de cookies del navegador."
    )
    parser.add_argument(
        "bookid", metavar="<BOOK ID>",
        help="ID del libro a descargar (los dígitos que aparecen en la URL del libro)."
    )
    parser.add_argument(
        "--kindle", action="store_true", help="Añade reglas CSS para mejor compatibilidad con Kindle."
    )
    parser.add_argument(
        "--preserve-log", dest="log", action="store_true", help="No borra el archivo de log aunque no haya errores."
    )
    args = parser.parse_args()

    # Si es SSO, pedir la cadena de cookies y guardarla
    if args.sso:
        print("[*] Modo SSO seleccionado. Por favor, pega la cadena de cookies copiada de tu navegador:")
        cookies_string = input("Cookies: ").strip()
        if not cookies_string:
            print("[!] Error: No se ingresó ninguna cadena de cookies.")
            sys.exit(1)
        transform_cookies(cookies_string)
        cred = False
    else:
        # Login tradicional
        cred = safaribooks.SafariBooks.parse_cred(args.cred)
        if not cred:
            print("[!] Error: Formato de credenciales inválido. Debe ser 'email:password'.")
            sys.exit(1)

    # Construir argumentos para SafariBooks
    class Args:
        pass
    sb_args = Args()
    sb_args.cred = cred
    sb_args.no_cookies = False
    sb_args.kindle = args.kindle
    sb_args.log = args.log
    sb_args.bookid = args.bookid

    # Ejecutar descarga
    safaribooks.SafariBooks(sb_args)

if __name__ == "__main__":
    main()
