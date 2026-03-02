# Instrucciones — Publicar Wiki en GitHub Pages

## 1. Instalar dependencias (una sola vez)

```bash
pip install mkdocs-material
```

---

## 2. Sincronizar notas de Obsidian → docs/

Cada vez que edites las notas en Obsidian, ejecuta:

```bash
cd "TTRPG/DND 5E 2024/Wiki Jugadores"
python sync_to_docs.py
```

Esto copia y convierte los archivos de Obsidian a la carpeta `docs/` con sintaxis compatible con MkDocs.

---

## 3. Previsualizar localmente

```bash
mkdocs serve
```

Abre http://127.0.0.1:8000 en el navegador.

---

## 4. Publicar en GitHub Pages (primera vez)

### 4a. Crear repositorio en GitHub
1. Ve a github.com → New repository
2. Nombre sugerido: `dnd5e-wiki` (o el que quieras)
3. Pon el repositorio en **Público** (GitHub Pages gratuito requiere repo público)
4. No añadas README (lo haremos desde aquí)

### 4b. Inicializar Git en esta carpeta

```bash
cd "TTRPG/DND 5E 2024/Wiki Jugadores"
git init
git remote add origin https://github.com/TU_USUARIO/dnd5e-wiki.git
```

### 4c. Crear .gitignore

```bash
echo "site/" > .gitignore
echo "__pycache__/" >> .gitignore
echo "*.pyc" >> .gitignore
```

### 4d. Publicar

```bash
git add .
git commit -m "Wiki inicial D&D 5e 2024"
git push -u origin main
mkdocs gh-deploy
```

La URL de tu wiki será: `https://TU_USUARIO.github.io/dnd5e-wiki/`

---

## 5. Actualizaciones futuras

```bash
# 1. Edita las notas en Obsidian
# 2. Sincroniza
python sync_to_docs.py

# 3. Publica
mkdocs gh-deploy
```

---

## Estructura de archivos

```
Wiki Jugadores/
├── 00 - Índice.md          ← notas Obsidian (edita aquí)
├── Reglas/
│   ├── Condiciones.md
│   ├── Economía de Acción.md
│   ├── Combate.md
│   ├── Concentración.md
│   ├── Descansos.md
│   └── Maestría de Armas.md
├── Clases/
│   ├── Bardo.md
│   ├── Clérigo.md
│   ├── Guerrero.md
│   ├── Hechicero.md
│   └── Mago.md
├── docs/                   ← generado por sync_to_docs.py (NO editar aquí)
├── site/                   ← HTML generado por mkdocs build (ignorado en git)
├── mkdocs.yml              ← configuración del sitio
├── sync_to_docs.py         ← script de sincronización
└── INSTRUCCIONES.md        ← este archivo
```
