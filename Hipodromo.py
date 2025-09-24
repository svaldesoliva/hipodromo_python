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


# Store balance in the user's home directory to ensure write permissions when installed
BALANCE_FILE = os.path.expanduser("~/.hipodromo_balance")


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
                print(f"Ingresa un número >= {minimo}.")
                continue
            if maximo is not None and valor > maximo:
                print(f"Ingresa un número <= {maximo}.")
                continue
            return valor
        except ValueError:
            print("Entrada inválida. Ingresa un número entero.")


def animacion(n, cuser):
    posiciones = [0] * n  # Inicializar posiciones de los caballos
    distancia = 100  # Longitud de la carrera
    nombres = [f"Caballo {i+1}" for i in range(n)]
    caballo_emoji = "🐴"
    ganador = None

    while True:
        clear_screen()
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

    clear_screen()
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


def main():
    while True:
        cprint(f"Hipódromo v0.2\n", "light_blue")
        cuser = input_entero(f"A cual le quieres apostar (1-{n}, 0 para salir): ", 0, n)
        if cuser == 0:
            cprint("Gracias por jugar!", "light_blue")
            guardar_dinero(dinero)
            break
        apuesta = input_entero(f"Tienes ${dinero}, cuánto quieres apostar?: ", 1, dinero)

        dinero_local = apuesta  # placeholder to satisfy linter in nested scopes (not used)
        # Actual balance updates use the outer-scope variable 'dinero'
        global dinero
        dinero -= apuesta
        guardar_dinero(dinero)
        ganador = animacion(n, cuser)
        if cuser == ganador:
            dinero += apuesta * 2
            guardar_dinero(dinero)
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

        if dinero == 0:
            input(
                "Te quedaste sin dinero, sal de mi hipódromo pobre de mierda. Presiona enter para salir..."
            )
            guardar_dinero(dinero)
            break

        clear_screen()


if __name__ == "__main__":
    main()
