"""
publicar.py
Sincroniza las notas de Obsidian y publica el sitio en GitHub Pages.

Uso:
    python publicar.py
"""

import subprocess
import sys
import shutil
import os
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent
SITE_DIR   = SCRIPT_DIR / "site"
TMP_DIR    = SCRIPT_DIR / ".deploy-tmp"


def run(cmd, cwd=None, check=True):
    result = subprocess.run(cmd, shell=True, cwd=cwd or SCRIPT_DIR)
    if check and result.returncode != 0:
        print(f"[ERROR] {cmd}")
        sys.exit(1)
    return result


def main():
    print("=== 1/3 Sincronizando notas de Obsidian ===")
    run("python sync_to_docs.py")

    print("\n=== 2/3 Construyendo HTML ===")
    run("mkdocs build")

    print("\n=== 3/3 Publicando en GitHub Pages ===")

    # Clonar solo la rama gh-pages en una carpeta temporal
    if TMP_DIR.exists():
        shutil.rmtree(TMP_DIR)

    result = run(
        "git ls-remote --heads origin gh-pages",
        check=False
    )
    # Obtener la URL del remoto
    url_result = subprocess.run(
        "git remote get-url origin",
        shell=True, cwd=SCRIPT_DIR, capture_output=True, text=True
    )
    origin_url = url_result.stdout.strip()

    branch_exists = subprocess.run(
        "git ls-remote --heads origin gh-pages",
        shell=True, cwd=SCRIPT_DIR, capture_output=True, text=True
    ).stdout.strip()

    if branch_exists:
        run(f'git clone --branch gh-pages --single-branch "{origin_url}" "{TMP_DIR}"')
        # Limpiar contenido anterior (excepto .git)
        for item in TMP_DIR.iterdir():
            if item.name == ".git":
                continue
            if item.is_dir():
                shutil.rmtree(item)
            else:
                item.unlink()
    else:
        TMP_DIR.mkdir()
        run("git init", cwd=TMP_DIR)
        run("git checkout --orphan gh-pages", cwd=TMP_DIR)
        run(f'git remote add origin "{origin_url}"', cwd=TMP_DIR)

    # Copiar HTML generado al directorio temporal
    shutil.copytree(SITE_DIR, TMP_DIR, dirs_exist_ok=True)

    # Commit y push
    run("git add -A", cwd=TMP_DIR)
    run('git commit -m "Deploy"', cwd=TMP_DIR)
    run("git push origin HEAD:gh-pages --force", cwd=TMP_DIR)

    # Limpiar
    shutil.rmtree(TMP_DIR)

    print("\nPublicado. El sitio estara disponible en:")
    print("  https://AkkarinRothen.github.io/dnd5e-wiki/")


if __name__ == "__main__":
    main()
