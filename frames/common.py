import os
import shutil
import openpyxl
import json


def load_config():
    path = os.getcwd()
    path_to_json = os.path.join(path, "frames", "config", "config.json")
    with open(path_to_json, "r") as archivo_config:
        config = json.load(archivo_config)
    return config


def open_file_folder(path_to_files):

    if not os.path.exists(path_to_files):
        os.mkdir(path_to_files)
    if os.name == "nt":  # Windows
        os.system(f"start explorer {path_to_files}")
    else:  # Linux
        os.system(f"xdg-open {path_to_files}")


def delete_files(path_to_files, log):
    cont = 0
    fail = 0
    for filename in os.listdir(path_to_files):
        file_path = os.path.join(path_to_files, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
                cont += 1
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
                cont += 1
        except Exception as e:
            show_results(log, f"No se pudo eliminar {file_path} debido a {e}")
            fail += 1
    show_results(
        log,
        f"Eliminados {cont} archivos y carpetas correctamente. Fallo en {fail} elementos.",
    )


def show_results(output_widget, text):
    # Reactiva el widget de salida.
    output_widget.setReadOnly(False)
    # vacía el contenido que este tenga.
    output_widget.clear()
    # Inserta el texto generado
    output_widget.insertPlainText(text)
    # Vuelve a deshabilitar el widgt de salida para evitar modificaciones accidentales
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
