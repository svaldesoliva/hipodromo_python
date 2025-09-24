import os
import time
try:
    from termcolor import cprint
except Exception:
    import sys as _sys
    _sys.path.append(os.path.join(os.path.dirname(__file__), "termcolor", "src"))
    from termcolor.termcolor import cprint
from config import get_balance, set_balance, get_lang, set_lang
from i18n import TRANSLATIONS, translator
from utils import clear_screen, input_entero, fzf_available, fzf_select
from game import animacion


N_HORSES = 5


def cargar_idioma():
    try:
        lang = get_lang()
        if lang in TRANSLATIONS:
            return lang
    except Exception:
        pass
    # Ask the user if not set or invalid
    while True:
        try:
            if fzf_available():
                choice = fzf_select(["English", "Español"], "Language")
                if choice == "English":
                    lang = "en"
                elif choice == "Español":
                    lang = "es"
                else:
                    continue
            else:
                # Default to English prompt to be welcoming
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
            set_lang(lang)
            return lang
        except Exception:
            # On any unexpected error, default to Spanish to preserve original experience
            return "es"


LANG = cargar_idioma()
t = translator(LANG)


def cargar_dinero(valor_por_defecto=5000):
    try:
        valor = int(get_balance(valor_por_defecto))
        if valor < 0:
            raise ValueError("Balance negativo")
        return valor
    except Exception:
        pass
    guardar_dinero(valor_por_defecto)
    return valor_por_defecto


def guardar_dinero(valor):
    try:
        set_balance(valor)
    except Exception:
        pass


dinero = cargar_dinero()


def animar_carrera(n, cuser):
    return animacion(n, cuser, t)


def jugar():
    global dinero
    while True:
        cprint(t("title"), "light_blue")
        cuser = input_entero(
            t("bet_prompt", n=N_HORSES),
            0,
            N_HORSES,
            invalid_msg=t("invalid_int"),
            min_msg=t("enter_number_min", minimo=0),
            max_msg=t("enter_number_max", maximo=N_HORSES),
        )
        if cuser == 0:
            guardar_dinero(dinero)
            return
        apuesta = input_entero(
            t("how_much_to_bet", dinero=dinero),
            1,
            dinero,
            invalid_msg=t("invalid_int"),
            min_msg=t("enter_number_min", minimo=1),
            max_msg=t("enter_number_max", maximo=dinero),
        )

        dinero -= apuesta
        guardar_dinero(dinero)
        ganador = animar_carrera(N_HORSES, cuser)
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
        if fzf_available():
            choice = fzf_select(["English", "Español"], "Language")
            if choice == "English":
                LANG = "en"
            elif choice == "Español":
                LANG = "es"
            else:
                return
        else:
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
        set_lang(LANG)
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
        if fzf_available():
            menu_options = [
                t("menu_play"),
                t("menu_change_lang"),
                t("menu_show_balance"),
                t("menu_exit"),
            ]
            choice = fzf_select(menu_options, t("menu_header"))
            if choice is None:
                # Treat cancel as exit but persist
                cprint(t("thanks"), "light_blue")
                guardar_dinero(dinero)
                break
            if choice == t("menu_play"):
                opcion = 1
            elif choice == t("menu_change_lang"):
                opcion = 2
            elif choice == t("menu_show_balance"):
                opcion = 3
            elif choice == t("menu_exit"):
                opcion = 0
            else:
                opcion = 0
        else:
            print(t("menu_header"))
            print(t("menu_play"))
            print(t("menu_change_lang"))
            print(t("menu_show_balance"))
            print(t("menu_exit"))
            opcion = input_entero(t("menu_prompt"), 0, 3, invalid_msg=t("invalid_int"))
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
