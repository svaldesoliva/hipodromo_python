import os
import time
import argparse
try:
    from termcolor import cprint
except Exception:
    import sys as _sys
    _sys.path.append(os.path.join(os.path.dirname(__file__), "termcolor", "src"))
    from termcolor.termcolor import cprint
from config import (
    get_balance,
    set_balance,
    get_lang,
    set_lang,
    get_fast,
    set_fast,
    get_horses,
    set_horses,
    get_seed,
    set_seed,
)
from i18n import TRANSLATIONS, translator
from utils import clear_screen, input_entero, fzf_available, fzf_select
from game import animacion, build_race, compute_decimal_odds


N_HORSES = get_horses(5)


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
FAST_MODE = get_fast(False)
SEED = get_seed(None)


def animar_carrera(n, cuser):
    race = build_race(n, SEED)
    return animacion(n, cuser, t, race_profile=race, fast=FAST_MODE)


def jugar():
    global dinero
    global N_HORSES
    # Build race upfront to show odds
    race = build_race(N_HORSES, SEED)
    odds = compute_decimal_odds(race["weights"]) if "weights" in race else []
    while True:
        cprint(t("title"), "light_blue")
        try:
            # Show odds
            print(t("odds_header"))
            for i in range(N_HORSES):
                name = t("horse_name", idx=i + 1)
                odd = odds[i] if i < len(odds) else 2.0
                print(t("odds_line", idx=i + 1, name=name, odds=odd))
            print()
        except Exception:
            pass
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
        # Use the prepared race for consistency with shown odds
        ganador = animacion(N_HORSES, cuser, t, race_profile=race, fast=FAST_MODE)
        if cuser == ganador:
            # Decimal odds payout: stake * (odds - 1) + stake = stake * odds
            odd = odds[cuser - 1] if cuser - 1 < len(odds) else 2.0
            ganancia = int(round(apuesta * odd))
            dinero += ganancia
            guardar_dinero(dinero)
            cprint(
                t("you_win", ganancia=ganancia, dinero=dinero),
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


def toggle_fast():
    global FAST_MODE
    FAST_MODE = not FAST_MODE
    set_fast(FAST_MODE)
    cprint(t("fast_on") if FAST_MODE else t("fast_off"), "light_blue")
    input(t("press_enter_continue"))


def mostrar_saldo():
    cprint(t("current_balance", dinero=dinero), "light_blue")
    input(t("press_enter_continue"))


def main():
    global dinero
    global N_HORSES
    global FAST_MODE
    global SEED

    # CLI flags
    try:
        parser = argparse.ArgumentParser(add_help=False)
        parser.add_argument("--fast", action="store_true")
        parser.add_argument("--no-fast", action="store_true")
        parser.add_argument("--horses", type=int)
        parser.add_argument("--seed")
        args, _ = parser.parse_known_args()

        if args.fast and not args.no_fast:
            FAST_MODE = True
        if args.no_fast:
            FAST_MODE = False
        if args.horses and args.horses >= 2:
            N_HORSES = args.horses
            set_horses(N_HORSES)
        if args.seed is not None:
            # Accept int or any string; keep as provided
            try:
                SEED = int(args.seed)
            except Exception:
                SEED = str(args.seed)
            set_seed(SEED)
        # Persist fast preference on startup change
        set_fast(FAST_MODE)
    except Exception:
        pass
    while True:
        clear_screen()
        cprint(t("title"), "light_blue")
        if fzf_available():
            menu_options = [
                t("menu_play"),
                t("menu_change_lang"),
                t("menu_show_balance"),
                t("menu_toggle_fast"),
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
            elif choice == t("menu_toggle_fast"):
                opcion = 4
            elif choice == t("menu_exit"):
                opcion = 0
            else:
                opcion = 0
        else:
            print(t("menu_header"))
            print(t("menu_play"))
            print(t("menu_change_lang"))
            print(t("menu_show_balance"))
            print(t("menu_toggle_fast"))
            print(t("menu_exit"))
            opcion = input_entero(t("menu_prompt"), 0, 4, invalid_msg=t("invalid_int"))
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
        elif opcion == 4:
            toggle_fast()
        else:
            print(t("invalid_option"))
            time.sleep(1)


if __name__ == "__main__":
    main()
