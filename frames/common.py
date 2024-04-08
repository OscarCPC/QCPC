import os
import shutil


def open_file_folder(path_to_files):        
    
    if not os.path.exists(path_to_files):
        os.mkdir(path_to_files)
    if os.name == 'nt':  # Windows
        os.system(f'start explorer {path_to_files}')
    else:  # Linux
        os.system(f'xdg-open {path_to_files}')
        
def delete_files(path_to_files,log):
    cont = 0;
    fail = 0;
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
    show_results(log, f'Eliminados {cont} archivos y carpetas correctamente. Fallo en {fail} elementos.')
    
    
def show_results(output_widget,text):
    #Reactiva el widget de salida.
    output_widget.setReadOnly(False)
    #vacía el contenido que este tenga.
    output_widget.clear()
    #Inserta el texto generado
    output_widget.insertPlainText(text)
    #Vuelve a deshabilitar el widgt de salida para evitar modificaciones accidentales        
    output_widget.setReadOnly(True)