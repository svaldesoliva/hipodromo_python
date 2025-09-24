# Hippodrome (Horse Racing) in Python 🐎

Simple terminal horse racing betting game with color output and a language selector (English/Español). Balance and language are persisted under `~/.config/hipodromo`.

<details>
<summary><strong>English</strong></summary>

#### Installation
- Via pipx (recommended) — see `pipx` docs: [pipx documentation](https://pypa.github.io/pipx/)
```bash
pipx install git+https://github.com/svaldesoliva/hipodromo_python
```
- From source — repo: [github.com/svaldesoliva/hipodromo_python](https://github.com/svaldesoliva/hipodromo_python)
```bash
git clone https://github.com/svaldesoliva/hipodromo_python.git
cd hipodromo_python
./scripts/install.sh
```
- Using pip — docs: [pip user installs](https://pip.pypa.io/en/stable/user_guide/#user-installs)
```bash
python3 -m pip install --user git+https://github.com/svaldesoliva/hipodromo_python
```
 

After installation, run:
```bash
hipodromo
```

#### Usage
- You will see a main menu to play, change language, or show your balance.
- Balance file: `~/.config/hipodromo/balance`
- Language file: `~/.config/hipodromo/lang`

#### Development
- Editable install script:
```bash
git clone https://github.com/svaldesoliva/hipodromo_python.git
cd hipodromo_python
./scripts/install.sh dev
```
- Or with pipx editable — see [pipx docs](https://pypa.github.io/pipx/docs/):
```bash
pipx install --force --editable .
```

Repository: [github.com/svaldesoliva/hipodromo_python](https://github.com/svaldesoliva/hipodromo_python)

</details>

<details>
<summary><strong>Español</strong></summary>

#### Instalación
- Con pipx (recomendado) — documentación: [pipx documentation](https://pypa.github.io/pipx/)
```bash
pipx install git+https://github.com/svaldesoliva/hipodromo_python
```
- Desde el código fuente — repositorio: [github.com/svaldesoliva/hipodromo_python](https://github.com/svaldesoliva/hipodromo_python)
```bash
git clone https://github.com/svaldesoliva/hipodromo_python.git
cd hipodromo_python
./scripts/install.sh
```
- Con pip — docs: [pip user installs](https://pip.pypa.io/en/stable/user_guide/#user-installs)
```bash
python3 -m pip install --user git+https://github.com/svaldesoliva/hipodromo_python
```
 

Después de instalar, ejecuta:
```bash
hipodromo
```

#### Uso
- Verás un menú principal para jugar, cambiar el idioma o mostrar tu saldo.
- Archivo de saldo: `~/.config/hipodromo/balance`
- Archivo de idioma: `~/.config/hipodromo/lang`

#### Desarrollo
- Instalación editable:
```bash
git clone https://github.com/svaldesoliva/hipodromo_python.git
cd hipodromo_python
./scripts/install.sh dev
```
- O con pipx editable — [documentación pipx](https://pypa.github.io/pipx/docs/):
```bash
pipx install --force --editable .
```

 </details>

## License / Licencia
MIT — see `LICENSE`.

