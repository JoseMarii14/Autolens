"""
DETECCIÓN DE MATRÍCULAS SIMPLIFICADA
====================================

TECNOLOGÍAS UTILIZADAS:
• OpenCV: Detección de regiones, preprocesamiento de imágenes, visualización
• EasyOCR: Reconocimiento óptico de caracteres (OCR)

FLUJO DEL SISTEMA:
1. [OpenCV] Cargar y redimensionar imagen
2. [OpenCV] Detectar regiones candidatas con Haar Cascades  
3. [OpenCV] Filtrar regiones por forma y tamaño
4. [OpenCV] Preprocesar cada región (CLAHE, umbralización)
5. [OCR] Extraer texto de regiones procesadas
6. [OpenCV] Dibujar resultados en imagen original

ESTRUCTURA DEL CÓDIGO:
• MÓDULO OCR: Funciones de reconocimiento de texto
• FUNCIONES OpenCV: Procesamiento y detección de imágenes
• FUNCIÓN PRINCIPAL: Orquesta todo el proceso
• INTERFAZ: Compatibilidad con InterfazStudio.py
"""

import cv2  # OpenCV - Procesamiento de imágenes y detección
import os
import numpy as np

# ========== MÓDULO OCR (EasyOCR) ==========
# Intentar importar EasyOCR para reconocimiento de texto
try:
    import easyocr
    EASYOCR_AVAILABLE = True
    print("EasyOCR disponible")
except ImportError:
    EASYOCR_AVAILABLE = False
    print("EasyOCR no disponible. Instalar con: pip install easyocr")







# ========== FUNCIONES OCR ==========
def get_easyocr_reader():
    """[OCR] Inicializa EasyOCR reader (singleton)"""
    if not hasattr(get_easyocr_reader, '_easyocr_reader'):
        if EASYOCR_AVAILABLE:
            print("Inicializando EasyOCR...")
            get_easyocr_reader._easyocr_reader = easyocr.Reader(['en'], gpu=False)
            print("EasyOCR listo")
        else:
            get_easyocr_reader._easyocr_reader = None
    return get_easyocr_reader._easyocr_reader





def extract_text_from_region(image_region):
    """[OCR] Extrae texto de una región usando EasyOCR"""
    if not EASYOCR_AVAILABLE:
        return "EasyOCR no disponible"
    
    try:
        reader = get_easyocr_reader()
        if reader is None:
            return "Error inicializando EasyOCR"
        
        # [OCR] Ejecutar reconocimiento de texto
        results = reader.readtext(image_region)
        
        if not results:
            return "Sin texto detectado"
        
        # [OCR] Encontrar el mejor resultado por confianza
        best_text = ""
        best_confidence = 0
        
        for (bbox, text, confidence) in results:
            clean_text = ''.join(c for c in text if c.isalnum() or c.isspace()).strip()
            if clean_text and confidence > best_confidence:
                best_text = clean_text
                best_confidence = confidence
        
        if best_text:
            return f"{best_text} (conf: {best_confidence:.2f})"
        else:
            return "Sin texto detectado"
            
    except Exception as e:
        return f"Error OCR: {str(e)}"

# ======================================




# ========== FUNCIONES OpenCV ==========

def detect_plates_simple(image_path, sensitivity=0.5):
    """
    [OpenCV + OCR] Versión simplificada de detección de matrículas
    
    FLUJO DEL PROCESO:
    1. [OpenCV] Cargar y preprocesar imagen
    2. [OpenCV] Detectar regiones de matrículas con Haar Cascades
    3. [OpenCV] Filtrar y preprocesar regiones detectadas
    4. [OCR] Extraer texto de cada región
    5. [OpenCV] Dibujar resultados en la imagen
    
    Args:
        image_path (str): Ruta a la imagen a procesar
        
    Returns:
        tuple: (imagen_procesada, lista_textos_detectados, success)
    """
    try:
        # [OpenCV] Configurar rutas de modelos Haar Cascade
        model_paths = [
            'platedetc/cascade.xml',
            'platedetc/haarcascade_licence_plate_rus_16stages.xml',
            'platedetc/haarcascade_russian_plate_number.xml'
        ]
        
        # [OpenCV] Cargar clasificadores Haar Cascade disponibles
        classifiers = []
        for model_path in model_paths:
            if os.path.exists(model_path):
                classifier = cv2.CascadeClassifier(model_path)
                if not classifier.empty():
                    classifiers.append(classifier)
        
        if not classifiers:
            return None, ["Error: No se encontraron modelos de detección"], False
        
        print("Iniciando detección simple de matrículas...")
        
        # Calcular parámetros basados en sensibilidad (0.0 = muy sensible, 1.0 = poco sensible)
        scale_factor = 1.03 + (sensitivity * 0.07)  # 1.03 a 1.1
        min_neighbors = int(2 + (sensitivity * 3))   # 2 a 5
        min_size_w = int(20 + (sensitivity * 60))    # 20 a 80
        min_size_h = int(5 + (sensitivity * 15))     # 5 a 20
        min_area = int(100 + (sensitivity * 1500))   # 100 a 1600
        
        print(f"Sensibilidad: {sensitivity:.2f} -> scaleFactor={scale_factor:.2f}, minNeighbors={min_neighbors}, minSize=({min_size_w},{min_size_h}), minArea={min_area}")
        
        # [OpenCV] Cargar imagen
        try:
            img = cv2.imread(image_path)
            if img is None:
                # Método alternativo para caracteres especiales
                with open(image_path, 'rb') as f:
                    file_bytes = f.read()
                nparr = np.frombuffer(file_bytes, np.uint8)
                img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
            
            if img is None:
                return None, [f"Error: No se pudo cargar la imagen: {image_path}"], False
                             
        except Exception as e:
            return None, [f"Error al cargar imagen: {str(e)}"], False
        
        # [OpenCV] Redimensionar si es muy grande
        height, width = img.shape[:2]
        if width > 1920 or height > 1080:
            scale = min(1920/width, 1080/height)
            new_width = int(width * scale)
            new_height = int(height * scale)
            img = cv2.resize(img, (new_width, new_height), interpolation=cv2.INTER_AREA)
        
        # [OpenCV] Convertir a escala de grises
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        
        detected_texts = []
        detection_count = 0
        
        # [OpenCV] Detectar regiones de matrículas con Haar Cascades
        all_detections = []
        
        for classifier in classifiers:
            plates = classifier.detectMultiScale(
                gray, 
                scaleFactor=scale_factor,
                minNeighbors=min_neighbors,
                minSize=(min_size_w, min_size_h),
                maxSize=(400, 150)
            )
            
            # [OpenCV] Filtrar por relación de aspecto (forma de matrícula)
            for (x, y, w, h) in plates:
                aspect_ratio = w / h
                area = w * h
                
                # Filtros básicos para matrículas (forma rectangular)
                if (2.0 <= aspect_ratio <= 6.0 and 
                    area >= min_area and 
                    w >= min_size_w and h >= min_size_h):
                    all_detections.append((x, y, w, h, area))
        
        # [OpenCV] Eliminar duplicados simples
        filtered_detections = []
        all_detections.sort(key=lambda x: x[4], reverse=True)  # Ordenar por área
        
        for detection in all_detections:
            x, y, w, h, area = detection
            is_duplicate = False
            
            for accepted in filtered_detections:
                ax, ay, aw, ah = accepted[:4]
                
                # Verificar superposición básica
                if (abs(x - ax) < 50 and abs(y - ay) < 30):
                    is_duplicate = True
                    break
            
            if not is_duplicate:
                filtered_detections.append(detection)
        
        # Limitar a máximo 3 detecciones
        # filtered_detections = filtered_detections[:3]
        
        # [OpenCV + OCR] Procesar cada matrícula detectada
        for detection in filtered_detections:
            x, y, w, h = detection[:4]
            detection_count += 1
            
            # [OpenCV] Extraer región de la matrícula
            plate_region = gray[y:y + h, x:x + w]
            
            print(f"\n=== PROCESANDO MATRÍCULA #{detection_count} ===")
            
            # [OCR] PASO 1: Región original (escala de grises)
            print("PASO 1 - Región original (escala de grises):")
            result_original = extract_text_from_region(plate_region)
            print(f"  OCR: {result_original}")
            
            # [OpenCV] PASO 2: Redimensionar si es muy pequeña
            step2_region = plate_region.copy()
            if step2_region.shape[1] < 150:
                scale_factor = 150 / step2_region.shape[1]
                new_width = int(step2_region.shape[1] * scale_factor)
                new_height = int(step2_region.shape[0] * scale_factor)
                step2_region = cv2.resize(step2_region, (new_width, new_height), interpolation=cv2.INTER_CUBIC)
                print("PASO 2 - Después de redimensionar:")
                result_resize = extract_text_from_region(step2_region)
                print(f"  OCR: {result_resize}")
            else:
                print("PASO 2 - Sin redimensionamiento necesario")
            
            # [OpenCV] PASO 3: Mejorar contraste con CLAHE
            clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
            step3_region = clahe.apply(step2_region)
            print("PASO 3 - Después de CLAHE (mejora de contraste):")
            result_clahe = extract_text_from_region(step3_region)
            print(f"  OCR: {result_clahe}")
            
            # [OpenCV] PASO 4: Umbralización adaptativa (binarización)
            step4_region = cv2.adaptiveThreshold(
                step3_region, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, 
                cv2.THRESH_BINARY, 11, 2
            )
            print("PASO 4 - Después de umbralización (blanco y negro):")
            result_final = extract_text_from_region(step4_region)
            print(f"  OCR: {result_final}")
            
            # Seleccionar el mejor resultado basado en confianza
            results = [
                ("Original", result_original),
                ("CLAHE", result_clahe),
                ("Umbralización", result_final)
            ]
            
            # Añadir resultado de redimensionamiento si se aplicó
            if 'result_resize' in locals():
                results.insert(1, ("Redimensionado", result_resize))
            
            # Encontrar el resultado con mayor confianza
            best_result = result_original
            best_step = "Original"
            best_conf = 0.0
            
            for step_name, result in results:
                if "conf:" in result:
                    try:
                        conf = float(result.split("conf: ")[1].split(")")[0])
                        if conf > best_conf:
                            best_conf = conf
                            best_result = result
                            best_step = step_name
                    except:
                        pass
            
            print(f"RESULTADO FINAL: {best_step} - {best_result}")
            detected_texts.append(f"Matrícula {detection_count}: {best_result}")
            
            # [OpenCV] Dibujar rectángulo verde y etiqueta
            cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
            cv2.putText(img, f"#{detection_count}", 
                       (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 
                       0.7, (0, 255, 0), 2)
        
        if detection_count == 0:
            detected_texts.append("No se detectaron matrículas en la imagen")
        
        print(f"Detección completada. Regiones encontradas: {detection_count}")
        
        return img, detected_texts, True
        
    except Exception as e:
        return None, [f"Error durante la detección: {str(e)}"], False





# ========== FUNCIÓN DE INTERFAZ ==========
def detect_plates_for_interface(image_path, sensitivity=0.5):
    """[INTERFAZ] Función de compatibilidad con InterfazStudio.py"""
    return detect_plates_simple(image_path, sensitivity)

