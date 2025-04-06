import os
from pathlib import Path
import openpyxl
from typing import Dict, Any
from PyQt5.QtWidgets import QWidget
from .qcpc_form import qcpc_form
from .config.base_config import QCPCConfig

from PyQt5.QtWidgets import QProgressDialog
from PyQt5.QtCore import Qt


class ProgressDialog:
    """Diálogo de progreso reutilizable"""

    def __init__(self, parent, title="Procesando...", message="Por favor espere..."):
        self.progress = QProgressDialog(message, "Cancelar", 0, 0, parent)
        self.progress.setWindowTitle(title)
        self.progress.setWindowModality(Qt.WindowModal)
        self.progress.setMinimumDuration(500)
        self.progress.setAutoClose(True)
        self.progress.setAutoReset(True)

    def __enter__(self):
        self.progress.show()
        return self.progress

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.progress.close()


def open_edit_form(
    parent: QWidget, item_data: Dict[Any, Any], on_close=None
) -> qcpc_form:
    """
    Abre un formulario de edición con los datos proporcionados.

    Args:
        parent: Widget padre para el formulario
        item_data: Diccionario con los datos a editar
        on_close: Función opcional a ejecutar cuando se cierre el formulario

    Returns:
        qcpc_form: Instancia del formulario
    """
    # Procesar screenshot_paths
    screenshot_paths = item_data.get("screenshot_paths", "")
    if isinstance(screenshot_paths, list):
        screenshot_paths = ",".join(screenshot_paths)
    elif isinstance(screenshot_paths, str):
        screenshot_paths = screenshot_paths.strip()

    item_data["screenshot_paths"] = screenshot_paths

    # Crear y configurar el formulario
    edit_form = qcpc_form()
    edit_form.is_editing = True
    edit_form.record_id = item_data.get("id")
    edit_form.load_data(item_data)
    edit_form.resize(900, 600)

    # Si se proporciona función on_close, conectarla
    if on_close and callable(on_close):
        edit_form.closed.connect(on_close)

    edit_form.show()
    return edit_form


def open_file_folder(path_to_files: str | Path) -> None:
    """
    Abre el explorador de archivos en la ruta especificada

    Args:
        path_to_files: Ruta a abrir
    """
    path = Path(path_to_files)
    path.mkdir(parents=True, exist_ok=True)

    if os.name == "nt":  # Windows
        os.startfile(str(path))
    else:  # Linux
        os.system(f'xdg-open "{path}"')


def show_results(output_widget, *args) -> None:
    """
    Muestra resultados en un widget de texto

    Args:
        output_widget: Widget donde mostrar el texto
        args: Textos a mostrar
    """
    output_widget.setReadOnly(False)
    output_widget.clear()

    try:
        message = " ".join(str(arg) for arg in args)
        output_widget.append(message)
        output_widget.verticalScrollBar().setValue(
            output_widget.verticalScrollBar().maximum()
        )
    except Exception as e:
        print(f"Error mostrando resultados: {str(e)}")

    output_widget.setReadOnly(True)


def clean_excel(filename):
    wb = openpyxl.load_workbook(filename)
    ws = wb.active
    print(filename)
    for column in ws.columns:
        max_length = 0
        column = [cell for cell in column]
        for cell in column:
            try:
                if len(str(cell.value)) > max_length:
                    max_length = len(str(cell.value))
            except:
                pass
        adjusted_width = max_length + 2
        ws.column_dimensions[column[0].column_letter].width = adjusted_width
    wb.save(filename)


def get_html_styles():
    return """<!DOCTYPE html>
        <html lang="es">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <style>
            @font-face {
            font-family: 'Amstrad CPC464';
            src: url('./Assets/fonts/amstrad_cpc464.ttf') format('truetype');
            font-weight: normal;
            font-style: normal;
}
            body {
                line-height: 1.6;
                font-family: 'Amstrad CPC464', monospace;
                margin: 0;
                padding: 16px;
                color: #c0c0c0;
                font-size: 10px;
                background-color: #101020;
            }

            /* Layout basado en grid */
            .grid-container {
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(320px, 1fr));
                gap: 16px;
                margin: 15px 0;
            }

            .grid-item {
                background-color: rgba(30, 30, 60, 0.4);
                border: 1px solid #303060;
                border-radius: 4px;
                padding: 15px;
                box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
            }

            /* Tablas más limpias y legibles */
            table {
                border-collapse: collapse;
                width: 100%;
                margin: 16px 0;
                border: 1px solid #303060;
            }

            th, td {
                border: 1px solid #303060;
                padding: 8px 12px;
                text-align: left;
            }

            th {
                background-color: rgba(40, 40, 80, 0.6);
                color: #f0f0f0;
                font-weight: bold;
                font-family: 'Amstrad CPC464', monospace;
            }

            td {
                color: #c0c0c0;
            }

            td b, td strong {
                color: #f0f0f0;
            }

            tr:nth-child(even) {
                background-color: rgba(30, 30, 60, 0.3);
            }

            tr:hover {
                background-color: rgba(50, 50, 100, 0.3);
            }

            /* Encabezados más claros */
            h1, h2, h3, h4, h5, h6 {
                font-family: 'Amstrad CPC464', monospace;
                color: #f0f0f0;
                margin-top: 20px;
                margin-bottom: 16px;
                border-bottom: 1px solid #303060;
                padding-bottom: 8px;
            }

            h3 {
                font-size: 18px;
            }

            /* Párrafos y listas */
            p {
                margin: 12px 0;
            }

            ul, ol {
                margin: 12px 0;
                padding-left: 24px;
            }

            li {
                margin: 6px 0;
            }

            /* Código y preformateado */
            code {
                background-color: rgba(50, 50, 100, 0.3);
                color: #80e080;
                padding: 2px 5px;
                border-radius: 3px;
                font-family: 'IBM Plex Mono', monospace;
                font-size: 14px;
            }

            pre {
                background-color: rgba(30, 30, 60, 0.4);
                color: #a0e0a0;
                padding: 12px;
                overflow-x: auto;
                border-radius: 4px;
                border: 1px solid #303060;
                margin: 16px 0;
            }

            /* Cajas informativas */
            .info-box {
                background-color: rgba(30, 30, 80, 0.3);
                border-left: 4px solid #4080f0;
                padding: 12px;
                margin: 16px 0;
                border-radius: 4px;
            }

            .warning-box {
                background-color: rgba(80, 60, 0, 0.3);
                border-left: 4px solid #f0c040;
                padding: 12px;
                margin: 16px 0;
                border-radius: 4px;
            }

            .error-box {
                background-color: rgba(80, 0, 0, 0.3);
                border-left: 4px solid #f04040;
                padding: 12px;
                margin: 16px 0;
                border-radius: 4px;
            }

            .success-box {
                background-color: rgba(0, 80, 40, 0.3);
                border-left: 4px solid #40f080;
                padding: 12px;
                margin: 16px 0;
                border-radius: 4px;
            }

            /* Resumen */
            .summary-container {
                background-color: rgba(30, 30, 60, 0.4);
                padding: 16px;
                margin-top: 24px;
                border-radius: 4px;
                border: 1px solid #303060;
            }

            .summary-title {
                color: #f0f0f0;
                border-bottom: 1px solid #303060;
                padding-bottom: 10px;
                margin-top: 0;
                font-family: 'Amstrad CPC464', monospace;
            }

            .summary-section {
                margin: 16px 0;
                padding: 12px;
                background-color: rgba(40, 40, 80, 0.3);
                border-radius: 4px;
            }

            .summary-label {
                font-weight: bold;
                color: #f0c040;
                margin-bottom: 8px;
                display: block;
                font-family: 'Amstrad CPC464', monospace;
            }

            /* Iconos y badges */
            .badge {
                display: inline-block;
                padding: 3px 8px;
                font-size: 14px;
                font-weight: bold;
                margin-right: 8px;
                border-radius: 3px;
            }

            .badge-success {
                background-color: rgba(0, 120, 0, 0.3);
                color: #80f080;
                border: 1px solid #40a040;
            }

            .badge-warning {
                background-color: rgba(120, 80, 0, 0.3);
                color: #f0c040;
                border: 1px solid #a08040;
            }

            .badge-error {
                background-color: rgba(120, 0, 0, 0.3);
                color: #f04040;
                border: 1px solid #a04040;
            }

            .badge-info {
                background-color: rgba(0, 80, 120, 0.3);
                color: #40c0f0;
                border: 1px solid #4080a0;
            }

            /* Separadores */
            hr {
                border: none;
                height: 1px;
                background-color: #303060;
                margin: 24px 0;
            }

            /* Énfasis */
            b, strong {
                color: #f0f0f0;
                font-weight: bold;
            }

            /* SQL y código con mejor formato */
            .sql-statement {
                background-color: rgba(20, 20, 40, 0.5);
                border: 1px solid #303060;
                border-radius: 4px;
                padding: 12px;
                margin: 12px 0;
                overflow-x: auto;
            }

            .sql-statement pre {
                font-family: 'IBM Plex Mono', monospace;
                background-color: transparent;
                border: none;
                color: #a0e0a0;
                white-space: pre-wrap;
                margin: 0;
                padding: 0;
                overflow-x: auto;
            }

            .sql-statement pre b {
                color: #f0c040;
            }

            /* ASCII art y código SQL */
            .ascii-art {
                font-family: 'IBM Plex Mono', monospace;
                white-space: pre-wrap;
                line-height: 1.4;
                color: #a0e0a0;
                margin: 12px 0;
                padding: 12px;
                display: block;
                text-align: left;
                overflow-x: auto;
                background-color: rgba(20, 20, 40, 0.5);
                border: 1px solid #303060;
                border-radius: 4px;
            }
            </style>
            </head>
            <body><br>"""


def get_html_footer():
    """
    Devuelve el footer HTML para la aplicación.
    """
    return "</body></html>"
