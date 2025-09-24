import os
import shutil
import subprocess


def clear_screen():
    if os.name == "nt":
        os.system("cls")
    else:
        os.system("clear")


def input_entero(prompt, minimo=None, maximo=None, invalid_msg=None, min_msg=None, max_msg=None):
    while True:
        try:
            valor_str = input(prompt)
            valor = int(valor_str)
            if minimo is not None and valor < minimo:
                if min_msg:
                    print(min_msg)
                continue
            if maximo is not None and valor > maximo:
                if max_msg:
                    print(max_msg)
                continue
            return valor
        except ValueError:
            if invalid_msg:
                print(invalid_msg)


def fzf_available():
    return shutil.which("fzf") is not None


def fzf_select(options, prompt):
    """Return the selected option string via fzf, or None if canceled/error."""
    if not options:
        return None
    try:
        proc = subprocess.run(
            ["fzf", "--prompt", f"{prompt} "],
            input="\n".join(options),
            capture_output=True,
            text=True,
            check=False,
        )
        if proc.returncode == 0:
            return proc.stdout.strip()
    except Exception:
        return None
    return None


