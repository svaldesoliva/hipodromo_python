import os
import time
import random
from termcolor import cprint


n = 5  # Número de caballos
dinero = 5000  # Dinero inicial


def animacion(n, cuser):
    posiciones = [0] * n  # Inicializar posiciones de los caballos
    distancia = 100  # Longitud de la carrera
    nombres = [f"Caballo {i+1}" for i in range(n)]
    caballo_emoji = "🐴"
    ganador = None

    while True:
        os.system("clear")  # Windows: os.system('cls') macOS/Linux : os.system('clear')
        cprint(f"Hipódromo v0.2\n", "light_blue")
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

    os.system("clear")  # Windows: os.system('cls') macOS/Linux : os.system('clear')
    cprint(f"Hipódromo v0.2\n", "light_blue")

    print("+" + "-" * (distancia + 15) + "+")
    for i in range(n):
        espacio = " " * posiciones[i]
        linea_meta = "|" if posiciones[i] >= distancia else ""
        ganador_texto = " Ganador!" if i == ganador - 1 else ""
        nombre = f">>{nombres[i]}<<" if i + 1 == cuser else nombres[i]
        print(f"| {nombre:<14} {espacio}{caballo_emoji}{linea_meta}{ganador_texto}")
    print("+" + "-" * (distancia + 15) + "+")
    print(f"El caballo {ganador} ganó la carrera!")
    return ganador


while True:
    cprint(f"Hipódromo v0.2\n", "light_blue")
    cuser = int(input(f"A cual le quieres apostar (1-{n}): "))
    apuesta = int(input(f"Tienes ${dinero}, cuánto quieres apostar?: "))

    if cuser > 0 and cuser <= n:
        if apuesta <= dinero and apuesta > 0:
            dinero -= apuesta
            ganador = animacion(n, cuser)
            if cuser == ganador:
                dinero += apuesta * 2
                cprint(
                    f"\nGanas ${apuesta * 2} pesos.\nTu dinero total es: ${dinero}",
                    "light_green",
                )
                input("Presiona enter para seguir jugando...")
            else:
                cprint(
                    f"Perdiste ${apuesta} pesos.\nTu dinero total es: ${dinero}.",
                    "light_red",
                )
                input("Ingresa enter para seguir jugando...")
        else:
            input("Error, ingresa un monto válido. Presiona enter para continuar...")
        if dinero == 0:
            input(
                "Te quedaste sin dinero, sal de mi hipódromo pobre de mierda. Presiona enter para salir..."
            )
            break
    else:
        input("Error, número mal ingresado. Presiona enter para continuar...")

    if os.name == "nt":
        os.system("cls")
    else:
        os.system("clear")
