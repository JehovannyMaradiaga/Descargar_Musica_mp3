import os
from yt_dlp import YoutubeDL

# Crear carpeta Downloads_Music automáticamente
def crear_carpeta_descargas():
    carpeta = "Downloads_Music"
    if not os.path.exists(carpeta):
        os.makedirs(carpeta)
    return carpeta

# Descargar canción desde una URL específica
def descargar_cancion(url, formato, carpeta):
    opciones_descarga = {
        'format': 'bestaudio/best',  # Aseguramos que descargue solo el audio
        'outtmpl': os.path.join(carpeta, '%(title)s.%(ext)s'),
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',   # Extraemos solo el audio
            'preferredcodec': formato,     # Usamos el formato preferido (MP3)
            'preferredquality': '192',     # Calidad del audio
        }],
        'quiet': False,
        'progress_hooks': [progreso_descarga],
    }
    try:
        with YoutubeDL(opciones_descarga) as ydl:
            ydl.download([url])
    except Exception as e:
        print(f"Error al descargar: {e}")

# Buscar y descargar canción desde múltiples plataformas
def buscar_y_descargar(nombre_cancion, formato, carpeta):
    plataformas = ["ytsearch", "scsearch", "bcsearch"]  # YouTube, SoundCloud, Bandcamp
    for plataforma in plataformas:
        consulta = f"{plataforma}:{nombre_cancion}"
        try:
            print(f"Buscando en {plataforma}...")
            opciones_busqueda = {
                'format': 'bestaudio/best',
                'quiet': True,
                'extract_flat': True,  # Solo obtener resultados sin descargar
            }
            with YoutubeDL(opciones_busqueda) as ydl:
                resultados = ydl.extract_info(consulta, download=False)['entries']

            if resultados:
                print(f"Encontrado: {resultados[0]['title']} ({resultados[0]['url']})")
                descargar_cancion(resultados[0]['url'], formato, carpeta)
                return
        except Exception as e:
            print(f"Error al buscar en {plataforma}: {e}")
    print("No se encontró la canción en ninguna plataforma.")

# Mostrar progreso de descarga
def progreso_descarga(d):
    if d['status'] == 'downloading':
        print(f"Progreso: {d['_percent_str']} - Velocidad: {d['_speed_str']} - ETA: {d['_eta_str']}", end="\r")
    elif d['status'] == 'finished':
        print("\nDescarga completada.")

# Cargar lista de canciones desde archivo
def cargar_lista_canciones():
    print("\n=== Cargar Lista de Canciones ===")
    archivo = input("Ingrese la ruta del archivo .txt con los nombres de las canciones: ").strip()
    if not os.path.isfile(archivo):
        print("Error: El archivo no existe.")
        return
    with open(archivo, "r", encoding="utf-8") as f:
        canciones = [linea.strip() for linea in f if linea.strip()]
    if not canciones:
        print("Error: El archivo está vacío.")
        return

    carpeta = crear_carpeta_descargas()
    formato = seleccionar_formato()
    for cancion in canciones:
        print(f"\nBuscando y descargando: {cancion}")
        buscar_y_descargar(cancion, formato, carpeta)

# Descargar canción individual
def descargar_cancion_individual():
    print("\n=== Descargar Canción Individual ===")
    nombre_cancion = input("Ingrese el nombre de la canción: ").strip()
    if not nombre_cancion:
        print("Error: No se ingresó un nombre.")
        return
    carpeta = crear_carpeta_descargas()
    formato = seleccionar_formato()
    buscar_y_descargar(nombre_cancion, formato, carpeta)

# Selección de formato (MP3 por defecto, MP4 opcional)
def seleccionar_formato():
    while True:
        formato = input("\nSeleccione el formato de descarga (mp3/mp4), presione Enter para mp3: ").strip().lower()
        if formato == "mp4":
            return formato
        # Si no se selecciona "mp4", por defecto se selecciona "mp3"
        if formato == "" or formato == "mp3":
            return "mp3"
        print("Opción inválida. Intente nuevamente.")

# Menú principal
def mostrar_menu():
    print("\n=== Menú Principal ===")
    print("1. Cargar lista de canciones desde archivo")
    print("2. Buscar y descargar canción individual")
    print("3. Salir")

# Función principal
def main():
    while True:
        mostrar_menu()
        opcion = input("Seleccione una opción: ").strip()
        if opcion == "1":
            cargar_lista_canciones()
        elif opcion == "2":
            descargar_cancion_individual()
        elif opcion == "3":
            print("Gracias por usar el descargador de música. ¡Hasta luego!")
            break
        else:
            print("Opción inválida. Intente nuevamente.")

if __name__ == "__main__":
    main()
