from typing import Dict

TRANSLATIONS: Dict[str, Dict[str, str]] = {
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


def translator(lang: str):
    def t(key: str, **kwargs):
        text = TRANSLATIONS.get(lang, TRANSLATIONS["es"]).get(key, "")
        if kwargs:
            return text.format(**kwargs)
        return text
    return t
