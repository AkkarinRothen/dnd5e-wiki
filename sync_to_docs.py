"""
sync_to_docs.py
Copia las notas de Obsidian a la carpeta docs/ de MkDocs,
convirtiendo la sintaxis de Obsidian a Markdown estándar.

Uso:
    python sync_to_docs.py

Luego:
    mkdocs serve       <- previsualización local
    mkdocs build       <- genera HTML en /site
    mkdocs gh-deploy   <- publica en GitHub Pages
"""

import re
import shutil
from pathlib import Path

# Rutas relativas al directorio de este script
SCRIPT_DIR = Path(__file__).parent
SOURCE_DIR = SCRIPT_DIR          # Notas de Obsidian (raíz del wiki)
DOCS_DIR   = SCRIPT_DIR / "docs"

# Mapeo de archivos fuente → destino en docs/
FILES = {
    "00 - Índice.md":                    "docs/index.md",
    "Reglas/Condiciones.md":             "docs/reglas/condiciones.md",
    "Reglas/Economía de Acción.md":      "docs/reglas/economia-de-accion.md",
    "Reglas/Combate.md":                 "docs/reglas/combate.md",
    "Reglas/Concentración.md":           "docs/reglas/concentracion.md",
    "Reglas/Descansos.md":               "docs/reglas/descansos.md",
    "Reglas/Maestría de Armas.md":       "docs/reglas/maestria-de-armas.md",
    "Clases/Bardo.md":                   "docs/clases/bardo.md",
    "Clases/Clérigo.md":                 "docs/clases/clerigo.md",
    "Clases/Guerrero.md":                "docs/clases/guerrero.md",
    "Clases/Hechicero.md":              "docs/clases/hechicero.md",
    "Clases/Mago.md":                    "docs/clases/mago.md",
}


def convert_obsidian_to_mkdocs(content: str) -> str:
    """Convierte sintaxis de Obsidian a Markdown estándar para MkDocs."""

    # 1. Eliminar YAML frontmatter (MkDocs lo ignora, pero limpia el output)
    content = re.sub(r"^---\n.*?\n---\n", "", content, flags=re.DOTALL)

    # 2. Convertir wikilinks [[Nota]] → texto plano (sin link, para simplicidad)
    #    Si quieres links reales, necesitarías mapear cada nota a su URL
    content = re.sub(r"\[\[([^\]|]+)\|([^\]]+)\]\]", r"\2", content)  # [[Nota|Texto]] → Texto
    content = re.sub(r"\[\[([^\]]+)\]\]", r"\1", content)              # [[Nota]] → Nota

    # 3. Convertir callouts de Obsidian a admonitions de MkDocs Material
    #    Obsidian: > [!info] Título
    #    MkDocs:   !!! info "Título"
    def replace_callout(match):
        indent   = match.group(1)
        tipo     = match.group(2).lower()
        titulo   = match.group(3).strip()
        cuerpo   = match.group(4)

        # Mapeo de tipos Obsidian → MkDocs
        tipo_map = {
            "info": "info", "tip": "tip", "warning": "warning",
            "danger": "danger", "example": "example", "note": "note",
            "quote": "quote", "success": "success", "question": "question",
        }
        tipo_mkdocs = tipo_map.get(tipo, "note")

        # Limpiar el cuerpo (quitar el > de cada línea)
        lineas = []
        for linea in cuerpo.split("\n"):
            linea = re.sub(r"^> ?", "", linea)
            lineas.append("    " + linea)  # 4 espacios de indentación para MkDocs

        titulo_fmt = f' "{titulo}"' if titulo else ""
        return f'!!! {tipo_mkdocs}{titulo_fmt}\n' + "\n".join(lineas)

    content = re.sub(
        r"([ \t]*)> \[!(\w+)\] ?(.*?)\n((?:[ \t]*>.*\n)*)",
        replace_callout,
        content,
        flags=re.MULTILINE
    )

    # 4. Eliminar links a notas privadas (rutas que apuntan fuera de docs/)
    content = re.sub(r"\s*\|\s*\[Nota completa\]\([^)]+\)", "", content)
    content = re.sub(r"^\[Nota completa\]\([^)]+\)\n?", "", content, flags=re.MULTILINE)

    # 5. Limpiar líneas vacías duplicadas (máximo 2 seguidas)
    content = re.sub(r"\n{3,}", "\n\n", content)

    return content.strip() + "\n"


def sync():
    """Copia y convierte todos los archivos."""
    DOCS_DIR.mkdir(exist_ok=True)
    (DOCS_DIR / "reglas").mkdir(exist_ok=True)
    (DOCS_DIR / "clases").mkdir(exist_ok=True)

    for src_rel, dst_rel in FILES.items():
        src = SCRIPT_DIR / src_rel
        dst = SCRIPT_DIR / dst_rel

        if not src.exists():
            print(f"  [SKIP] No encontrado: {src_rel}")
            continue

        content = src.read_text(encoding="utf-8")
        converted = convert_obsidian_to_mkdocs(content)
        dst.write_text(converted, encoding="utf-8")
        print(f"  [OK]   {src_rel} -> {dst_rel}")

    print(f"\nSync completo. {len(FILES)} archivos procesados.")
    print("\nPróximos pasos:")
    print("  mkdocs serve       # Previsualizar en http://127.0.0.1:8000")
    print("  mkdocs gh-deploy   # Publicar en GitHub Pages")


if __name__ == "__main__":
    sync()
