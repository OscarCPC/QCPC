# QCPC - Qt CPC Games Database Manager

Un proyecto de aprendizaje de Python que implementa una interfaz gráfica para gestionar una base de datos de juegos de Amstrad CPC usando PyQt5.

## Descripción

Este proyecto fue desarrollado como ejercicio de aprendizaje con GitHub Copilot, explorando conceptos como:

- Desarrollo de interfaces gráficas con PyQt5
- Gestión de bases de datos SQLite
- Manejo de archivos y rutas en Python
- Integración con APIs externas (TheGamesDB)
- Estilos y temas personalizados (QSS)
- Patrones de diseño y arquitectura modular

## Características

- Búsqueda de juegos usando TheGamesDB API
- Visualización y descarga de carátulas y screenshots
- Gestión de desarrolladores y metadatos
- Interfaz estilo Amstrad CPC
- Manejo de archivos y directorios
- Sistema de configuración flexible
- Soporte para múltiples plataformas

## Tecnologías

- Python 3.x
- PyQt5
- SQLite
- Requests
- Pillow
- pathlib
- dataclasses

## Estructura del Proyecto

```
QCPC/
├── frames/
│   ├── config/
│   │   ├── base_config.py
│   │   └── config.json
│   ├── common.py
│   ├── menu.py
│   ├── qcpc_form.py
│   └── qcpc_search.py
├── qss/
│   └── style.qss
├── db/
│   └── qcpc.db
└── main.py
```

## Configuración

El archivo `config.json` debe contener:

```json
{
    "api_key": "your_api_key",
    "paths": {
        "db_path": "db/qcpc.db",
        "boxart_path_images": "files/downloads/boxart",
        "screenshot_path_images": "files/downloads/screenshot"
    },
    "cache_size": 100,
    "max_concurrent_requests": 5,
    "debug_mode": false
}
```

## Aprendizajes Clave

- Diseño de interfaces con Qt Designer y PyQt5
- Gestión de estados y eventos en aplicaciones GUI
- Manejo de configuraciones y rutas absolutas/relativas
- Integración con APIs externas y procesamiento de respuestas
- Estilos personalizados con QSS
- Manejo de errores y feedback al usuario
- Arquitectura modular y patrones de diseño
- Control de versiones con Git

## Mejoras Futuras

- Sistema de caché para imágenes
- Soporte para más plataformas
- Exportación/importación de datos
- Tests unitarios y de integración
- Documentación extendida
- Internacionalización

## Requisitos

- Python 3.8+
- PyQt5
- Requests
- Pillow
- SQLite3

## Instalación

```bash
git clone https://github.com/yourusername/QCPC.git
cd QCPC
pip install -r requirements.txt
python main.py
```

## Créditos

Este proyecto fue desarrollado como ejercicio de aprendizaje con la guía de GitHub Copilot, inspirado en el Amstrad CPC y usando la API de TheGamesDB.

## Licencia

MIT License - Siéntete libre de usar y modificar según necesites.