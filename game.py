import time
import random
from termcolor import cprint

from utils import clear_screen


def animacion(num_caballos, caballo_usuario, t):
    posiciones = [0] * num_caballos
    distancia = 100
    nombres = [t("horse_name", idx=i + 1) for i in range(num_caballos)]
    caballo_emoji = "🐴"
    ganador = None

    while True:
        clear_screen()
        cprint(t("title"), "light_blue")
        print("+" + "-" * (distancia + 15) + "+")
        for i in range(num_caballos):
            espacio = " " * posiciones[i]
            linea_meta = "|" if posiciones[i] >= distancia else ""
            nombre = f">>{nombres[i]}<<" if i + 1 == caballo_usuario else nombres[i]
            print(f"| {nombre:<14} {espacio}{caballo_emoji}{linea_meta}")
        print("+" + "-" * (distancia + 15) + "+")

        if max(posiciones) >= distancia:
            ganador = posiciones.index(max(posiciones)) + 1
            break

        time.sleep(0.1)
        posiciones = [pos + random.randint(0, 2) for pos in posiciones]

    clear_screen()
    cprint(t("title"), "light_blue")

    print("+" + "-" * (distancia + 15) + "+")
    for i in range(num_caballos):
        espacio = " " * posiciones[i]
        linea_meta = "|" if posiciones[i] >= distancia else ""
        ganador_texto = t("winner_suffix") if i == ganador - 1 else ""
        nombre = f">>{nombres[i]}<<" if i + 1 == caballo_usuario else nombres[i]
        print(f"| {nombre:<14} {espacio}{caballo_emoji}{linea_meta}{ganador_texto}")
    print("+" + "-" * (distancia + 15) + "+")
    print(t("winner_announcement", winner=ganador))
    return ganador



