import os
import time
import random
try:
    from termcolor import cprint
except Exception:
    # Fallback to vendored termcolor if not installed
    import sys as _sys
    _sys.path.append(os.path.join(os.path.dirname(__file__), "termcolor", "src"))
    from termcolor.termcolor import cprint


n = 5  # Número de caballos


# Config directory under XDG-like path
CONFIG_DIR = os.path.expanduser("~/.config/hipodromo")
OLD_BALANCE_FILE = os.path.expanduser("~/.hipodromo_balance")
OLD_LANG_FILE = os.path.expanduser("~/.hipodromo_lang")
BALANCE_FILE = os.path.join(CONFIG_DIR, "balance")
LANG_FILE = os.path.join(CONFIG_DIR, "lang")

# Ensure config directory exists and migrate old files if present
def _ensure_and_migrate_config():
    try:
        os.makedirs(CONFIG_DIR, exist_ok=True)
        # Migrate balance
        if os.path.exists(OLD_BALANCE_FILE) and not os.path.exists(BALANCE_FILE):
            try:
                with open(OLD_BALANCE_FILE, "r", encoding="utf-8") as f:
                    content = f.read()
                with open(BALANCE_FILE, "w", encoding="utf-8") as f:
                    f.write(content)
                # Best effort: remove old file
                try:
                    os.remove(OLD_BALANCE_FILE)
                except Exception:
                    pass
            except Exception:
                pass
        # Migrate language
        if os.path.exists(OLD_LANG_FILE) and not os.path.exists(LANG_FILE):
            try:
                with open(OLD_LANG_FILE, "r", encoding="utf-8") as f:
                    content = f.read()
                with open(LANG_FILE, "w", encoding="utf-8") as f:
                    f.write(content)
                try:
                    os.remove(OLD_LANG_FILE)
                except Exception:
                    pass
            except Exception:
                pass
    except Exception:
        # Silent: do not break the game on config errors
        pass

_ensure_and_migrate_config()

# Translations
TRANSLATIONS = {
    "es": {
        "title": "Hipódromo v0.2\n",
        "menu_header": "Menú principal",
        "menu_play": "1) Jugar",
        "menu_change_lang": "2) Cambiar idioma",
        "menu_show_balance": "3) Mostrar saldo",
        "menu_exit": "0) Salir",
        "menu_prompt": "Selecciona una opción: ",
        "invalid_option": "Opción inválida.",
        "current_balance": "Tu dinero total es: ${dinero}",
        "language_changed_es": "Idioma actualizado a Español.",
        "language_changed_en": "Idioma actualizado a English.",
        "enter_number_min": "Ingresa un número >= {minimo}.",
        "enter_number_max": "Ingresa un número <= {maximo}.",
        "invalid_int": "Entrada inválida. Ingresa un número entero.",
        "horse_name": "Caballo {idx}",
        "winner_suffix": " Ganador!",
        "winner_announcement": "El caballo {winner} ganó la carrera!",
        "bet_prompt": "A cual le quieres apostar (1-{n}, 0 para salir): ",
        "thanks": "Gracias por jugar!",
        "how_much_to_bet": "Tienes ${dinero}, cuánto quieres apostar?: ",
        "you_win": "\nGanas ${ganancia} pesos.\nTu dinero total es: ${dinero}",
        "press_enter_continue": "Presiona enter para seguir jugando...",
        "you_lose": "Perdiste ${apuesta} pesos.\nTu dinero total es: ${dinero}.",
        "press_enter_continue_alt": "Ingresa enter para seguir jugando...",
        "out_of_money": "Te quedaste sin dinero, sal de mi hipódromo pobre de mi*rda. Presiona enter para salir...",
        "language_prompt": "Selecciona idioma / Select language: 1) Español  2) English: ",
    },
    "en": {
        "title": "Hippodrome v0.2\n",
        "menu_header": "Main menu",
        "menu_play": "1) Play",
        "menu_change_lang": "2) Change language",
        "menu_show_balance": "3) Show balance",
        "menu_exit": "0) Exit",
        "menu_prompt": "Select an option: ",
        "invalid_option": "Invalid option.",
        "current_balance": "Your total money is: ${dinero}",
        "language_changed_es": "Language changed to Español.",
        "language_changed_en": "Language changed to English.",
        "enter_number_min": "Enter a number >= {minimo}.",
        "enter_number_max": "Enter a number <= {maximo}.",
        "invalid_int": "Invalid input. Enter an integer.",
        "horse_name": "Horse {idx}",
        "winner_suffix": " Winner!",
        "winner_announcement": "Horse {winner} won the race!",
        "bet_prompt": "Which one do you want to bet on (1-{n}, 0 to exit): ",
        "thanks": "Thanks for playing!",
        "how_much_to_bet": "You have ${dinero}, how much do you want to bet?: ",
        "you_win": "\nYou win ${ganancia}.\nYour total money is: ${dinero}",
        "press_enter_continue": "Press enter to keep playing...",
        "you_lose": "You lost ${apuesta}.\nYour total money is: ${dinero}.",
        "press_enter_continue_alt": "Press enter to keep playing...",
        "out_of_money": "You ran out of money you f*cking loser. Press enter to exit...",
        "language_prompt": "Select language / Selecciona idioma: 1) English  2) Español: ",
    },
}


def cargar_idioma():
    try:
        if os.path.exists(LANG_FILE):
            with open(LANG_FILE, "r", encoding="utf-8") as f:
                lang = f.read().strip()
                if lang in TRANSLATIONS:
                    return lang
    except Exception:
        pass
    # Ask the user if not set or invalid
    while True:
        try:
            # Default to English prompt to be welcoming, also understandable in ES
            sel = input(TRANSLATIONS["en"]["language_prompt"]).strip()
            if sel == "1":
                lang = "en"
            elif sel == "2":
                lang = "es"
            else:
                # Try inverse mapping for Spanish-first prompt
                if sel in ("es", "ES", "2"):
                    lang = "es"
                elif sel in ("en", "EN", "1"):
                    lang = "en"
                else:
                    continue
            with open(LANG_FILE, "w", encoding="utf-8") as f:
                f.write(lang)
            return lang
        except Exception:
            # On any unexpected error, default to Spanish to preserve original experience
            return "es"


LANG = cargar_idioma()


def t(key, **kwargs):
    text = TRANSLATIONS.get(LANG, TRANSLATIONS["es"]).get(key, "")
    if kwargs:
        return text.format(**kwargs)
    return text


def cargar_dinero(valor_por_defecto=5000):
    try:
        if os.path.exists(BALANCE_FILE):
            with open(BALANCE_FILE, "r", encoding="utf-8") as f:
                contenido = f.read().strip()
                valor = int(contenido)
                if valor < 0:
                    raise ValueError("Balance negativo")
                return valor
    except Exception:
        # Si el archivo está corrupto o no es válido, reestablecer al valor por defecto
        pass
    guardar_dinero(valor_por_defecto)
    return valor_por_defecto


def guardar_dinero(valor):
    try:
        with open(BALANCE_FILE, "w", encoding="utf-8") as f:
            f.write(str(int(valor)))
    except Exception:
        # Silenciar fallos de escritura para no romper el juego
        pass


dinero = cargar_dinero()  # Dinero inicial (persistente)


def clear_screen():
    if os.name == "nt":
        os.system("cls")
    else:
        os.system("clear")


def input_entero(prompt, minimo=None, maximo=None):
    while True:
        try:
            valor_str = input(prompt)
            valor = int(valor_str)
            if minimo is not None and valor < minimo:
                print(t("enter_number_min", minimo=minimo))
                continue
            if maximo is not None and valor > maximo:
                print(t("enter_number_max", maximo=maximo))
                continue
            return valor
        except ValueError:
            print(t("invalid_int"))


def animacion(n, cuser):
    posiciones = [0] * n  # Inicializar posiciones de los caballos
    distancia = 100  # Longitud de la carrera
    nombres = [t("horse_name", idx=i + 1) for i in range(n)]
    caballo_emoji = "🐴"
    ganador = None

    while True:
        clear_screen()
        cprint(t("title"), "light_blue")
        print("+" + "-" * (distancia + 15) + "+")
        for i in range(n):
            espacio = " " * posiciones[i]
            linea_meta = "|" if posiciones[i] >= distancia else ""
            nombre = f">>{nombres[i]}<<" if i + 1 == cuser else nombres[i]
            print(f"| {nombre:<14} {espacio}{caballo_emoji}{linea_meta}")
        print("+" + "-" * (distancia + 15) + "+")

        if max(posiciones) >= distancia:
            ganador = posiciones.index(max(posiciones)) + 1
            break

        time.sleep(0.1)  # "Velocidad"
        posiciones = [pos + random.randint(0, 2) for pos in posiciones]

    clear_screen()
    cprint(t("title"), "light_blue")

    print("+" + "-" * (distancia + 15) + "+")
    for i in range(n):
        espacio = " " * posiciones[i]
        linea_meta = "|" if posiciones[i] >= distancia else ""
        ganador_texto = t("winner_suffix") if i == ganador - 1 else ""
        nombre = f">>{nombres[i]}<<" if i + 1 == cuser else nombres[i]
        print(f"| {nombre:<14} {espacio}{caballo_emoji}{linea_meta}{ganador_texto}")
    print("+" + "-" * (distancia + 15) + "+")
    print(t("winner_announcement", winner=ganador))
    return ganador


def jugar():
    global dinero
    while True:
        cprint(t("title"), "light_blue")
        cuser = input_entero(t("bet_prompt", n=n), 0, n)
        if cuser == 0:
            guardar_dinero(dinero)
            return
        apuesta = input_entero(t("how_much_to_bet", dinero=dinero), 1, dinero)

        dinero -= apuesta
        guardar_dinero(dinero)
        ganador = animacion(n, cuser)
        if cuser == ganador:
            dinero += apuesta * 2
            guardar_dinero(dinero)
            cprint(
                t("you_win", ganancia=apuesta * 2, dinero=dinero),
                "light_green",
            )
            input(t("press_enter_continue"))
        else:
            cprint(
                t("you_lose", apuesta=apuesta, dinero=dinero),
                "light_red",
            )
            input(t("press_enter_continue_alt"))

        if dinero == 0:
            input(t("out_of_money"))
            guardar_dinero(dinero)
            return

        clear_screen()


def cambiar_idioma():
    global LANG
    try:
        sel = input(TRANSLATIONS["en"]["language_prompt"]).strip()
        if sel == "1":
            LANG = "en"
        elif sel == "2":
            LANG = "es"
        else:
            if sel in ("es", "ES", "2"):
                LANG = "es"
            elif sel in ("en", "EN", "1"):
                LANG = "en"
            else:
                return
        with open(LANG_FILE, "w", encoding="utf-8") as f:
            f.write(LANG)
        # Confirm change in the chosen language
        msg_key = "language_changed_en" if LANG == "en" else "language_changed_es"
        cprint(t(msg_key), "light_blue")
        input(t("press_enter_continue"))
    except Exception:
        pass


def mostrar_saldo():
    cprint(t("current_balance", dinero=dinero), "light_blue")
    input(t("press_enter_continue"))


def main():
    global dinero
    while True:
        clear_screen()
        cprint(t("title"), "light_blue")
        print(t("menu_header"))
        print(t("menu_play"))
        print(t("menu_change_lang"))
        print(t("menu_show_balance"))
        print(t("menu_exit"))
        opcion = input_entero(t("menu_prompt"), 0, 3)
        if opcion == 0:
            cprint(t("thanks"), "light_blue")
            guardar_dinero(dinero)
            break
        elif opcion == 1:
            jugar()
        elif opcion == 2:
            cambiar_idioma()
        elif opcion == 3:
            mostrar_saldo()
        else:
            print(t("invalid_option"))
            time.sleep(1)


if __name__ == "__main__":
    main()
