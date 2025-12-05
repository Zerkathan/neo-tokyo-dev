import os
import logging
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import yaml

# Configuración inicial
CONFIG_FILE = 'diccionario.yaml'

def load_config():
    with open(CONFIG_FILE, 'r') as f:
        config = yaml.safe_load(f)
    return config

config = load_config()

# Configuración de logging
logging.basicConfig(filename='file_organizer.log', level=logging.INFO, format='%(asctime)s [%(levelname)s] %(message)s')

class FileOrganizerHandler(FileSystemEventHandler):
    def on_created(self, event):
        self.organize_file(event.src_path)

    def organize_file(self, filepath):
        extension = os.path.splitext(filepath)[1]
        categoria = config['mappings_extensión_categoria'].get(extension)

        if not categoria:
            logging.warning(f"NO CATEGORY FOUND FOR: {filepath}")
            return

        ruta_destino = f"{config['carpeta_monitoreo']}/{categoria[0]}"
        self.create_directory(ruta_destino)

        archivo_nombre = os.path.basename(filepath)
        new_filepath = self.handle_collision(ruta_destino, archivo_nombre)

        if new_filepath != filepath:
            logging.info(f"MOVED: {filepath} → {new_filepath}")
            os.rename(filepath, new_filepath)

    def create_directory(self, path):
        try:
            os.makedirs(path)
        except FileExistsError:
            pass

    def handle_collision(self, directory, filename):
        cont = 1
        while os.path.exists(f"{directory}/{filename}"):
            archivo_nombre = f"{os.path.splitext(filename)[0]}_{cont}{os.path.splitext(filename)[1]}"
            cont += 1
        return f"{directory}/{archivo_nombre}"

def configurar_rutas():
    print("Ingrese la ruta de la carpeta de descargas:")
    config['carpeta_monitoreo'] = input()
    print("\nIngrese el diccionario de extensiones y categorías (formato: '.extension': ['categoria', ...]:")
    mappings = {}
    for line in open('/path/to/diccionario.yaml').readlines():
        k, v = line.strip().split(':')
        mappings[k] = [x.strip() for x in v.split(',')]
    config['mappings_extensión_categoria'] = mappings

def inicio():
    configurar_rutas()
    event_handler = FileOrganizerHandler()
    observer = Observer()
    observer.schedule(event_handler, path=config['carpeta_monitoreo'], recursive=True)
    observer.start()

    try:
        while True:
            # Verificar si hay cambios en la carpeta
            for root, dirs, files in os.walk(config['carpeta_monitoreo']):
                for file in files:
                    organize_file(os.path.join(root, file))
            print("\nLogs:")
            with open('file_organizer.log', 'r') as f:
                log = f.read()
                print(log)
    except KeyboardInterrupt:
        observer.stop()

    observer.join()

if __name__ == '__main__':
    inicio()