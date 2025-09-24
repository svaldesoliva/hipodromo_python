import time
import random
from typing import Optional
from termcolor import cprint

from utils import clear_screen


def _generate_weights(num_horses: int, seed: Optional[int] = None):
    """Return a list of positive weights for each horse.

    Heavier weight => higher chance to advance on each tick.
    """
    rng = random.Random(seed)
    # Sample from a simple bounded distribution to avoid extreme odds
    return [rng.uniform(0.6, 1.4) for _ in range(num_horses)]


def compute_decimal_odds(weights):
    """Compute house-edge-adjusted decimal odds from probability.

    probability_i = w_i / sum(weights)
    fair_odds = 1.0 / probability_i
    Apply a 10% house edge by multiplying fair payout by 0.9.
    Minimum odds clamped at 1.5x to keep wins exciting for favorites.
    """
    total = sum(weights) if weights else 1.0
    odds = []
    for w in weights:
        p = max(1e-6, w / total)
        fair = 1.0 / p
        house = fair * 0.9
        odds.append(round(max(1.5, house), 2))
    return odds


def build_race(num_horses: int, seed: Optional[int] = None):
    """Create a race profile with weights and precomputed odds."""
    weights = _generate_weights(num_horses, seed)
    odds = compute_decimal_odds(weights)
    return {
        "weights": weights,
        "odds": odds,
        "distance": 100,
        "emoji": "🐴",
    }


def animacion(num_caballos, caballo_usuario, t, race_profile=None, fast=False):
    posiciones = [0] * num_caballos
    if race_profile is None:
        race_profile = build_race(num_caballos)
    pesos = race_profile.get("weights", [1.0] * num_caballos)
    distancia = race_profile.get("distance", 100)
    caballo_emoji = race_profile.get("emoji", "🐴")
    nombres = [t("horse_name", idx=i + 1) for i in range(num_caballos)]
    ganador = None

    # Normalize weights to probabilities for a small bonus step chance
    total_peso = sum(pesos) if pesos else 1.0
    bonus_probs = [max(0.0, min(0.6, w / total_peso)) for w in pesos]

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

        if not fast:
            time.sleep(0.08)

        # Advance positions with a small bias from weights
        nuevas = []
        for i, pos in enumerate(posiciones):
            paso = random.randint(0, 2)
            if random.random() < bonus_probs[i] * 0.5:
                paso += 1
            nuevas.append(pos + paso)
        posiciones = nuevas

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


