# Hippodrome (Horse Racing) in Python 🐎

Simple terminal horse racing betting game with color output and a language selector (English/Español). Settings now use a single config file at `~/.config/hipodromo/config.json`.

New in v0.3:
- Odds per horse with fair-ish payouts (house edge ~10%).
- Fast mode toggle and CLI flags.
- Seeded runs and configurable number of horses.

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
- You will see a main menu to play, change language, toggle fast mode, or show your balance.
- Config file: `~/.config/hipodromo/config.json`
- Example contents:
```json
{
  "balance": 7500,
  "lang": "en",
  "fast": false,
  "horses": 5,
  "seed": null
}
```
  - On first run, the app migrates legacy files if present: `~/.hipodromo_balance`, `~/.hipodromo_lang`, `~/.config/hipodromo/balance`, `~/.config/hipodromo/lang`.

CLI options (optional):
```bash
# Enable fast mode for this run
hipodromo --fast

# Disable fast mode (overrides config)
hipodromo --no-fast

# Set number of horses (>=2) and an initial seed
hipodromo --horses 7 --seed 12345
```

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
- Verás un menú principal para jugar, cambiar el idioma, alternar modo rápido o mostrar tu saldo.
- Archivo de configuración: `~/.config/hipodromo/config.json`
- Ejemplo de contenido:
```json
{
  "balance": 7500,
  "lang": "es",
  "fast": false,
  "horses": 5,
  "seed": null
}
```
  - En la primera ejecución, la app migra archivos antiguos si existen: `~/.hipodromo_balance`, `~/.hipodromo_lang`, `~/.config/hipodromo/balance`, `~/.config/hipodromo/lang`.

Opciones CLI (opcionales):
```bash
# Activar modo rápido para esta sesión
hipodromo --fast

# Desactivar modo rápido (sobre-escribe la config)
hipodromo --no-fast

# Establecer número de caballos (>=2) y una semilla inicial
hipodromo --horses 7 --seed 12345
```

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

