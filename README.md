# Hipodromo de Caballos en Python 🐎

Código en Python que simula una carrera de caballos con apuestas.

## Instalación

- **Desde GitHub (recomendado, con pipx):**
```bash
pipx install git+https://github.com/svaldesoliva/hipodromo_python
```

- **Clonando el repo y usando el script:**
```bash
git clone https://github.com/svaldesoliva/hipodromo_python.git
cd hipodromo_python
./scripts/install.sh
```

- **Con pip (usuario actual):**
```bash
python3 -m pip install --user git+https://github.com/svaldesoliva/hipodromo_python
```

Después de instalar, el comando disponible es:
```bash
hipodromo
```

### Dependencias
`termcolor` se instala automáticamente como dependencia. Si no está disponible por alguna razón, el programa usa una copia vendorizada como respaldo.

## Uso
- Ejecuta el comando:
```bash
hipodromo
```
- El balance se guarda en `~/.hipodromo_balance`.

## Desarrollo local
- Instalación editable:
```bash
git clone https://github.com/svaldesoliva/hipodromo_python.git
cd hipodromo_python
./scripts/install.sh dev
```
- O manualmente con pipx:
```bash
pipx install --force --editable .
```

## Paquetes Homebrew / AUR
- Homebrew: edita `packaging/homebrew/hipodromo.rb`, reemplaza `sha256` con el del tarball y publícalo en tu tap (`brew tap <user>/tap` y `brew install --build-from-source <user>/tap/hipodromo`).
- AUR: edita `packaging/aur/PKGBUILD`, actualiza `pkgver` y sube al AUR. Usuarios pueden instalar con `yay -S hipodromo`.

Repositorio: https://github.com/svaldesoliva/hipodromo_python

## Licencia
MIT. Ver `LICENSE`.

