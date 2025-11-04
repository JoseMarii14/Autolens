import cv2
import numpy as np
from tkinter import messagebox, filedialog
import os

class PhotoCropper:
    def __init__(self):
        self.image = None
        self.original_image = None
        self.clone = None
        self.cropping = False
        self.start_point = None
        self.end_point = None
        self.crop_rectangle = None
        
    def mouse_callback(self, event, x, y, flags, param):
        """Callback para manejar eventos del mouse durante la selección"""
        if event == cv2.EVENT_LBUTTONDOWN:
            # Iniciar selección
            self.cropping = True
            self.start_point = (x, y)
            self.end_point = (x, y)
            
        elif event == cv2.EVENT_MOUSEMOVE:
            # Actualizar selección mientras se arrastra
            if self.cropping:
                self.end_point = (x, y)
                # Crear copia de la imagen para dibujar el rectángulo
                temp_image = self.clone.copy()
                cv2.rectangle(temp_image, self.start_point, self.end_point, (0, 255, 0), 2)
                cv2.imshow("Seleccionar área para recortar", temp_image)
                
        elif event == cv2.EVENT_LBUTTONUP:
            # Finalizar selección
            self.cropping = False
            self.end_point = (x, y)
            
            # Asegurar que las coordenadas estén en orden correcto
            x1, y1 = self.start_point
            x2, y2 = self.end_point
            
            # Ordenar coordenadas
            self.crop_rectangle = (
                min(x1, x2), min(y1, y2),
                max(x1, x2), max(y1, y2)
            )
            
            # Dibujar rectángulo final
            temp_image = self.clone.copy()
            cv2.rectangle(temp_image, (self.crop_rectangle[0], self.crop_rectangle[1]), 
                         (self.crop_rectangle[2], self.crop_rectangle[3]), (0, 255, 0), 2)
            cv2.imshow("Seleccionar área para recortar", temp_image)

    def crop_image_interactive(self, image_path):
        """
        Función principal para recortar imagen de forma interactiva
        
        Args:
            image_path (str): Ruta de la imagen a recortar
            
        Returns:
            tuple: (success, cropped_image_path, message)
        """
        try:
            # Verificar que el archivo existe
            if not os.path.exists(image_path):
                return False, None, f"El archivo no existe: {image_path}"
            
            # Cargar imagen usando método alternativo para manejar caracteres especiales
            try:
                # Método 1: Usar cv2.imread con encoding UTF-8
                self.original_image = cv2.imread(image_path, cv2.IMREAD_COLOR)
                
                # Método 2: Si falla, usar numpy y PIL como alternativa
                if self.original_image is None:
                    from PIL import Image
                    pil_image = Image.open(image_path)
                    # Convertir PIL a OpenCV (RGB a BGR)
                    pil_image = pil_image.convert('RGB')
                    self.original_image = cv2.cvtColor(np.array(pil_image), cv2.COLOR_RGB2BGR)
                
                if self.original_image is None:
                    return False, None, f"No se pudo cargar la imagen. Formato no soportado o archivo corrupto.\nRuta: {image_path}"
                    
            except Exception as load_error:
                return False, None, f"Error al cargar la imagen: {str(load_error)}\nRuta: {image_path}"
            
            # Crear copia para trabajar
            self.image = self.original_image.copy()
            self.clone = self.original_image.copy()
            
            # Redimensionar si la imagen es muy grande para mejor visualización
            height, width = self.image.shape[:2]
            max_display_size = 800
            
            if width > max_display_size or height > max_display_size:
                scale = min(max_display_size / width, max_display_size / height)
                new_width = int(width * scale)
                new_height = int(height * scale)
                
                self.image = cv2.resize(self.image, (new_width, new_height))
                self.clone = self.image.copy()
                self.scale_factor = scale
            else:
                self.scale_factor = 1.0
            
            # Crear ventana y configurar callback del mouse
            cv2.namedWindow("Seleccionar área para recortar", cv2.WINDOW_AUTOSIZE)
            cv2.setMouseCallback("Seleccionar área para recortar", self.mouse_callback)
            
            # Mostrar instrucciones
            instructions = """
            INSTRUCCIONES PARA RECORTAR:

            1. Haz clic y arrastra para seleccionar el área a recortar
            2. Presiona 'c' o 'C' para confirmar el recorte
            3. Presiona 'r' o 'R' para reiniciar la selección
            4. Presiona 'ESC' o 'q' para cancelar

            Selecciona el área que deseas recortar...
                        """
            print(instructions)
            
            # Mostrar imagen inicial
            cv2.imshow("Seleccionar área para recortar", self.image)
            
            # Loop principal
            while True:
                key = cv2.waitKey(1) & 0xFF
                
                # Confirmar recorte
                if key in [ord('c'), ord('C')]:
                    if self.crop_rectangle is not None:
                        success, cropped_path, message = self._perform_crop(image_path)
                        cv2.destroyAllWindows()
                        return success, cropped_path, message
                    else:
                        print("Por favor, selecciona un área primero")
                
                # Reiniciar selección
                elif key in [ord('r'), ord('R')]:
                    self.crop_rectangle = None
                    self.image = self.clone.copy()
                    cv2.imshow("Seleccionar área para recortar", self.image)
                    print("Selección reiniciada. Selecciona una nueva área.")
                
                # Cancelar
                elif key == 27 or key in [ord('q'), ord('Q')]:  # ESC o 'q'
                    cv2.destroyAllWindows()
                    return False, None, "Operación cancelada por el usuario"
            
        except Exception as e:
            cv2.destroyAllWindows()
            return False, None, f"Error durante el recorte: {str(e)}"
    
    def _perform_crop(self, original_image_path):
        """Realizar el recorte y guardar la imagen"""
        try:
            if self.crop_rectangle is None:
                return False, None, "No hay área seleccionada"
            
            x1, y1, x2, y2 = self.crop_rectangle
            
            # Ajustar coordenadas si la imagen fue redimensionada
            if self.scale_factor != 1.0:
                x1 = int(x1 / self.scale_factor)
                y1 = int(y1 / self.scale_factor)
                x2 = int(x2 / self.scale_factor)
                y2 = int(y2 / self.scale_factor)
            
            # Validar coordenadas
            orig_height, orig_width = self.original_image.shape[:2]
            x1 = max(0, min(x1, orig_width))
            y1 = max(0, min(y1, orig_height))
            x2 = max(0, min(x2, orig_width))
            y2 = max(0, min(y2, orig_height))
            
            # Verificar que el área sea válida
            if x2 <= x1 or y2 <= y1:
                return False, None, "Área de recorte inválida"
            
            # Recortar imagen
            cropped_image = self.original_image[y1:y2, x1:x2]
            
            if cropped_image.size == 0:
                return False, None, "El área seleccionada es demasiado pequeña"
            
            # Generar nombre para imagen recortada
            base_name = os.path.splitext(os.path.basename(original_image_path))[0]
            extension = os.path.splitext(original_image_path)[1]
            directory = os.path.dirname(original_image_path)
            
            # Verificar que el directorio sea escribible
            if not os.access(directory, os.W_OK):
                return False, None, f"No se tiene permiso de escritura en el directorio: {directory}"
            
            cropped_filename = f"{base_name}_recortada{extension}"
            cropped_path = os.path.join(directory, cropped_filename)
            
            # Si el archivo ya existe, agregar número
            counter = 1
            while os.path.exists(cropped_path):
                cropped_filename = f"{base_name}_recortada_{counter}{extension}"
                cropped_path = os.path.join(directory, cropped_filename)
                counter += 1
            
            # Guardar imagen recortada usando método alternativo para manejar caracteres especiales
            try:
                # Método 1: Intentar cv2.imwrite estándar
                success = cv2.imwrite(cropped_path, cropped_image)
                
                # Método 2: Si falla, usar PIL como alternativa
                if not success:
                    from PIL import Image
                    # Convertir de BGR a RGB para PIL
                    rgb_image = cv2.cvtColor(cropped_image, cv2.COLOR_BGR2RGB)
                    pil_image = Image.fromarray(rgb_image)
                    pil_image.save(cropped_path)
                    success = True
                
                if success:
                    return True, cropped_path, f"Imagen recortada guardada como: {cropped_filename}"
                else:
                    return False, None, "Error al guardar la imagen recortada"
                    
            except Exception as save_error:
                return False, None, f"Error al guardar la imagen: {str(save_error)}"
                
        except Exception as e:
            return False, None, f"Error al procesar el recorte: {str(e)}"

def crop_photo_for_interface(image_path):
    """
    Función principal para ser llamada desde la interfaz
    
    Args:
        image_path (str): Ruta de la imagen a recortar
        
    Returns:
        tuple: (success, cropped_image_path, message)
    """
    try:
        # Verificar que OpenCV esté disponible
        try:
            import cv2
        except ImportError:
            return False, None, "OpenCV no está instalado. Ejecuta: pip install opencv-python"
        
        cropper = PhotoCropper()
        return cropper.crop_image_interactive(image_path)
        
    except Exception as e:
        return False, None, f"Error en el módulo de recorte: {str(e)}"

# Función de prueba independiente
def main():
    """Función para probar el módulo de forma independiente"""
    print("=== MÓDULO DE RECORTE DE FOTOS ===")
    print("Selecciona una imagen para recortar...")
    
    # Usar tkinter para seleccionar archivo (solo si se ejecuta independientemente)
    try:
        import tkinter as tk
        from tkinter import filedialog
        
        root = tk.Tk()
        root.withdraw()  # Ocultar ventana principal
        
        file_path = filedialog.askopenfilename(
            title="Seleccionar imagen para recortar",
            filetypes=[
                ("Archivos de imagen", "*.jpg *.jpeg *.png *.bmp *.tiff"),
                ("Todos los archivos", "*.*")
            ]
        )
        
        root.destroy()
        
        if file_path:
            success, cropped_path, message = crop_photo_for_interface(file_path)
            
            if success:
                print(f"✅ {message}")
                print(f"📁 Imagen recortada: {cropped_path}")
            else:
                print(f"❌ {message}")
        else:
            print("No se seleccionó ninguna imagen")
            
    except ImportError:
        print("Error: tkinter no está disponible para la selección de archivos")
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    main()