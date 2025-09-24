import os


def clear_screen():
    if os.name == "nt":
        os.system("cls")
    else:
        os.system("clear")


def input_entero(prompt, minimo=None, maximo=None, invalid_msg="Entrada inválida.", min_msg=None, max_msg=None):
    while True:
        try:
            valor_str = input(prompt)
            valor = int(valor_str)
            if minimo is not None and valor < minimo:
                print(min_msg or f"Ingresa un número >= {minimo}.")
                continue
            if maximo is not None and valor > maximo:
                print(max_msg or f"Ingresa un número <= {maximo}.")
                continue
            return valor
        except ValueError:
            print(invalid_msg)


# Optional fzf integration
_def_checked = False
_has_fzf = False


def fzf_available():
    global _def_checked, _has_fzf
    if not _def_checked:
        _has_fzf = os.system("command -v fzf >/dev/null 2>&1") == 0
        _def_checked = True
    return _has_fzf


def fzf_select(options, header=None):
    if not fzf_available():
        return None
    try:
        import subprocess

        input_str = "\n".join(options)
        env = os.environ.copy()
        if header:
            env["FZF_DEFAULT_OPTS"] = (env.get("FZF_DEFAULT_OPTS", "") + f" --header='{header}'").strip()
        proc = subprocess.Popen(
            ["fzf", "--ansi"],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL,
            text=True,
            env=env,
        )
        out, _ = proc.communicate(input=input_str)
        out = out.strip()
        return out if out else None
    except Exception:
        return None
