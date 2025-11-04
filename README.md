# 🚗 Autolens - Sistema de Detección de Matrículas

**Proyecto de Imagen Digital** - Herramienta avanzada para procesamiento de imágenes y detección automática de matrículas vehiculares.

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![OpenCV](https://img.shields.io/badge/OpenCV-4.5+-green.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

## 📋 Descripción

Autolens Studio es una aplicación de escritorio desarrollada en Python que combina técnicas avanzadas de procesamiento de imágenes y reconocimiento óptico de caracteres (OCR) para la detección automática de matrículas en fotografías de vehículos.

### ✨ Características Principales

- **🎯 Detección Inteligente**: Sistema de detección de matrículas con sensibilidad ajustable
- **✂️ Recorte Interactivo**: Herramienta de recorte de fotos con selección visual
- **🖼️ Interfaz Moderna**: Diseño inspirado en VS Code con temas oscuros
- **📊 Múltiples Algoritmos**: Combinación de Haar Cascades y EasyOCR
- **🔧 Configuración Flexible**: Parámetros de detección ajustables en tiempo real

## 🛠️ Tecnologías Utilizadas

| Tecnología | Propósito |
|------------|-----------|
| **OpenCV** | Procesamiento de imágenes y detección de regiones |
| **EasyOCR** | Reconocimiento óptico de caracteres |
| **Tkinter** | Interfaz gráfica de usuario |
| **Pygame** | Reproducción de video en splash screen |
| **Pillow (PIL)** | Manipulación de imágenes para GUI |
| **NumPy** | Operaciones matemáticas y arrays |

## 📦 Instalación

### Prerrequisitos
- Python 3.8 o superior
- pip (gestor de paquetes de Python)

### Pasos de instalación

1. **Clonar el repositorio**
```bash
git clone https://github.com/tu-usuario/autolens-studio.git
cd autolens-studio
```

2. **Instalar dependencias**
```bash
pip install -r requirements.txt
```

3. **Ejecutar la aplicación**
```bash
python main.py
```

## 🚀 Uso

### Inicio de la Aplicación
1. Ejecuta `python main.py`
2. Selecciona "Seleccionar Foto" para cargar una imagen
3. Accede a Autolens Studio para procesar la imagen

### Funcionalidades Principales

#### 🎯 Detección de Matrículas
- Carga una imagen con vehículos
- Ajusta la sensibilidad de detección (0.0 = muy sensible, 1.0 = poco sensible)
- Haz clic en "Detección de Matrículas"
- Visualiza los resultados con rectángulos verdes y texto extraído

#### ✂️ Recorte de Fotos
- Selecciona "Recorte de Foto"
- Usa el mouse para seleccionar el área a recortar
- Controles: `C` (confirmar), `R` (reiniciar), `ESC` (cancelar)
- La imagen recortada se carga automáticamente

## 📁 Estructura del Proyecto

```
autolens-studio/
├── main.py                    # Punto de entrada principal
├── Interfaz.py               # Interfaz principal de selección
├── InterfazStudio.py         # Interfaz del estudio de edición
├── SplashScreen.py           # Pantalla de inicio con video
├── DetectLicenseSimple.py    # Sistema de detección optimizado
├── DetectLicense.py          # Sistema de detección completo
├── CutPhoto.py               # Herramienta de recorte
├── AboutWindow.py            # Ventana "Acerca de"
├── SelectImg.py              # Selector de imágenes
├── requirements.txt          # Dependencias del proyecto
├── source/                   # Recursos multimedia
│   ├── Final.mp4            # Video del splash screen
│   ├── AutolensLogoOficial.png
│   └── wallpaperCoche.jpg
└── platedetc/               # Modelos de detección
    ├── cascade.xml
    ├── haarcascade_licence_plate_rus_16stages.xml
    └── haarcascade_russian_plate_number.xml
```

## ⚙️ Configuración

### Parámetros de Detección
La sensibilidad de detección controla varios parámetros internos:

| Sensibilidad | scaleFactor | minNeighbors | minSize | Uso Recomendado |
|--------------|-------------|--------------|---------|-----------------|
| 0.0 (Muy sensible) | 1.03 | 2 | (20,5) | Vehículos lejanos |
| 0.5 (Equilibrado) | 1.065 | 3-4 | (50,12) | Uso general |
| 1.0 (Poco sensible) | 1.1 | 5 | (80,20) | Vehículos cercanos |

## 📝 Licencia

Este proyecto está bajo la Licencia MIT. Ver el archivo `LICENSE` para más detalles.

## 👥 Autor

- **José María Gordillo Gragera** - *Desarrollo inicial* - [Github]([https://github.com/tu-usuario](https://github.com/JoseMarii14))

## 📞 Soporte

Si tienes problemas o preguntas:
- 🐛 [Reportar un bug](https://github.com/tu-usuario/autolens-studio/issues)
- 💡 [Solicitar una feature](https://github.com/tu-usuario/autolens-studio/issues)
- 📧 Contacto: jgordillsq@alumnos.unex.es

---

⭐ **¡No olvides dar una estrella al proyecto si te ha sido útil!** ⭐
