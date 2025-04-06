import json
from dataclasses import dataclass
from typing import Dict, Optional
from pathlib import Path


@dataclass
class QCPCConfig:
    """Configuración base para la aplicación QCPC"""

    api_key: str
    db_path: Path
    paths: Dict[str, Path]
    cache_size: int = 100
    max_concurrent_requests: int = 5
    debug_mode: bool = False

    def validate(self) -> bool:
        """Valida que todos los paths existan y la configuración sea correcta"""
        try:
            # Validar API key
            if not self.api_key:
                raise ValueError("API key no configurada")

            # Validar path de base de datos
            if not self.db_path.parent.exists():
                self.db_path.parent.mkdir(parents=True)

            # Validar y crear paths necesarios
            for path_name, path in self.paths.items():
                if not path.exists():
                    path.mkdir(parents=True)
                    print(f"Creado directorio: {path}")

            return True

        except Exception as e:
            print(f"Error en validación: {str(e)}")
            return False

    @classmethod
    def from_json(cls, config_path: str = None) -> "QCPCConfig":
        """Crea una instancia de configuración desde un archivo JSON"""
        try:
            # Si no se proporciona ruta, buscar en ubicaciones predeterminadas
            if config_path is None:
                root_dir = Path(__file__).parent.parent.parent.absolute()
                possible_paths = [
                    root_dir / "config.json",
                    root_dir / "frames/config/config.json",
                ]

                for path in possible_paths:
                    if path.exists():
                        config_path = str(path)
                        break
                else:
                    raise FileNotFoundError(
                        "No se encontró config.json en ninguna ubicación predeterminada"
                    )

            # Convertir config_path a Path absoluta
            config_path = Path(config_path).absolute()

            if not config_path.exists():
                raise FileNotFoundError(f"No se encontró el archivo: {config_path}")

            # Leer y procesar configuración
            with open(config_path, "r") as f:
                config_data = json.load(f)

            # Validar estructura básica del JSON
            if "paths" not in config_data:
                raise KeyError(
                    "La clave 'paths' no existe en el archivo de configuración"
                )
            if "api_key" not in config_data:
                raise KeyError(
                    "La clave 'api_key' no existe en el archivo de configuración"
                )

            # Usar la raíz del proyecto como base para rutas absolutas
            root_path = Path(__file__).parent.parent.parent.absolute()

            # Obtener db_path como ruta absoluta
            db_path = root_path / config_data["paths"].get("db_path", "db/qcpc.db")

            # Construir diccionario de paths absolutos excluyendo db_path
            paths = {
                k: root_path / v
                for k, v in config_data["paths"].items()
                if k != "db_path"
            }

            # Crear instancia de configuración
            config = cls(
                api_key=config_data["api_key"],
                db_path=db_path,
                paths=paths,
                cache_size=config_data.get("cache_size", 100),
                max_concurrent_requests=config_data.get("max_concurrent_requests", 5),
                debug_mode=config_data.get("debug_mode", False),
            )

            if not config.validate():
                raise ValueError("Falló la validación de la configuración")

            return config

        except Exception as e:
            raise RuntimeError(f"Error cargando configuración: {str(e)}")

    def get_path(self, path_name: str) -> Path:
        """Obtiene un path específico de la configuración"""
        if path_name not in self.paths:
            raise KeyError(f"Path '{path_name}' no encontrado en la configuración")
        return self.paths[path_name]
