import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from PIL import Image, ImageTk
import os

class StudioInterface:
    def __init__(self, image_path=None):
        self.root = tk.Tk()
        self.root.title("Autolens Studio")
        self.root.geometry("1280x720")
        self.root.resizable(False, False)
        
        # Center the window on screen
        self.center_window()
        
        # VS Code dark theme color
        self.vs_code_dark = "#1e1e1e"
        self.vs_code_light = "#2d2d2d"  # Lighter shade for right panel
        
        # Store reference to right panel for image updates
        self.right_panel = None
        
        # Store path of currently selected image
        self.current_image_path = image_path
        
        # Sensitivity setting for license plate detection (0.0 = very sensitive, 1.0 = less sensitive)
        self.detection_sensitivity = 0.5
        
        # Add rounded rectangle method to Canvas
        self.add_rounded_rect_to_canvas()
        
        self.setup_interface()
        
        # Load the image if provided
        if self.current_image_path:
            self.display_image(self.current_image_path)
    
    def center_window(self):
        """Center the window on the screen"""
        # Update the window to get actual dimensions
        self.root.update_idletasks()
        
        # Get window dimensions
        window_width = 1280
        window_height = 720
        
        # Get screen dimensions
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        
        # Calculate center position
        center_x = int((screen_width - window_width) / 2)
        center_y = int((screen_height - window_height) / 2)
        
        # Set window position
        self.root.geometry(f"{window_width}x{window_height}+{center_x}+{center_y}")
    
    def add_rounded_rect_to_canvas(self):
        """Add create_rounded_rect method to Canvas class"""
        def create_rounded_rect(self, x1, y1, x2, y2, radius=10, **kwargs):
            points = []
            for x, y in [(x1, y1 + radius), (x1, y1), (x1 + radius, y1),
                        (x2 - radius, y1), (x2, y1), (x2, y1 + radius),
                        (x2, y2 - radius), (x2, y2), (x2 - radius, y2),
                        (x1 + radius, y2), (x1, y2), (x1, y2 - radius)]:
                points.extend([x, y])
            return self.create_polygon(points, smooth=True, **kwargs)
        
        tk.Canvas.create_rounded_rect = create_rounded_rect
        
    def setup_interface(self):
        # Create main container
        main_frame = tk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Left panel (320x720) - Menu lateral
        left_panel = tk.Frame(main_frame, bg=self.vs_code_dark, width=320, height=720)
        left_panel.pack(side=tk.LEFT, fill=tk.Y)
        left_panel.pack_propagate(False)
        
        # Right panel (960x720) - Image display
        self.right_panel = tk.Frame(main_frame, bg=self.vs_code_light, width=960, height=720)
        self.right_panel.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        self.right_panel.pack_propagate(False)
        
        # Add content to left panel (menu)
        self.setup_left_panel(left_panel)
        # Setup right panel for image display
        self.setup_right_panel(self.right_panel)
        
    def setup_left_panel(self, parent):
        # Title
        title_label = tk.Label(
            parent,
            text="Autolens Studio",
            font=("Arial", 18, "bold"),
            fg="white",
            bg=self.vs_code_dark
        )
        title_label.pack(pady=(30, 40))
        
        # Separator line
        separator = tk.Frame(parent, height=2, bg="#404040")
        separator.pack(fill=tk.X, padx=20, pady=(0, 30))
        
        # Menu buttons container
        buttons_frame = tk.Frame(parent, bg=self.vs_code_dark)
        buttons_frame.pack(fill=tk.X, padx=20)
        
        # Button: Detección de Matrículas
        self.create_menu_button(
            buttons_frame,
            text="Detección de Matrículas",
            command=self.detect_license_plates,
            y_offset=0
        )
        
        # Button: Recorte de Foto
        self.create_menu_button(
            buttons_frame,
            text="Recorte de Foto",
            command=self.crop_photo,
            y_offset=80
        )
        
        # Button: Cargar Nueva Imagen
        self.create_menu_button(
            buttons_frame,
            text="Cargar Nueva Imagen",
            command=self.load_new_image,
            y_offset=160
        )
        
        # Button: Volver al Inicio
        self.create_menu_button(
            buttons_frame,
            text="Volver al Inicio",
            command=self.return_to_main,
            y_offset=240,
            bg_color="#dc3545"
        )
        
        # Sensitivity control section
        sensitivity_frame = tk.Frame(parent, bg=self.vs_code_dark)
        sensitivity_frame.pack(fill=tk.X, padx=20, pady=(40, 20))
        
        # Sensitivity title
        sensitivity_title = tk.Label(
            sensitivity_frame,
            text="Sensibilidad de Detección",
            font=("Arial", 12, "bold"),
            fg="white",
            bg=self.vs_code_dark
        )
        sensitivity_title.pack(anchor=tk.W, pady=(0, 10))
        
        # Sensitivity scale
        self.sensitivity_scale = tk.Scale(
            sensitivity_frame,
            from_=0.0,
            to=1.0,
            resolution=0.1,
            orient=tk.HORIZONTAL,
            length=280,
            bg=self.vs_code_dark,
            fg="white",
            highlightthickness=0,
            troughcolor="#404040",
            activebackground="#0e639c",
            command=self.on_sensitivity_change
        )
        self.sensitivity_scale.set(self.detection_sensitivity)
        self.sensitivity_scale.pack(fill=tk.X, pady=(0, 5))
        
        # Sensitivity labels
        labels_frame = tk.Frame(sensitivity_frame, bg=self.vs_code_dark)
        labels_frame.pack(fill=tk.X)
        
        tk.Label(
            labels_frame,
            text="Muy Sensible",
            font=("Arial", 8),
            fg="#cccccc",
            bg=self.vs_code_dark
        ).pack(side=tk.LEFT)
        
        tk.Label(
            labels_frame,
            text="Poco Sensible",
            font=("Arial", 8),
            fg="#cccccc",
            bg=self.vs_code_dark
        ).pack(side=tk.RIGHT)
        
        # Current sensitivity display
        self.sensitivity_display = tk.Label(
            sensitivity_frame,
            text=f"Actual: {self.detection_sensitivity:.1f}",
            font=("Arial", 9),
            fg="#0e639c",
            bg=self.vs_code_dark
        )
        self.sensitivity_display.pack(pady=(5, 0))
        
        # Image info section
        info_frame = tk.Frame(parent, bg=self.vs_code_dark)
        info_frame.pack(side=tk.BOTTOM, fill=tk.X, padx=20, pady=20)
        
        # Image info label
        self.info_label = tk.Label(
            info_frame,
            text="Imagen cargada:\nNinguna",
            font=("Arial", 10),
            fg="#cccccc",
            bg=self.vs_code_dark,
            justify=tk.LEFT,
            wraplength=280
        )
        self.info_label.pack(anchor=tk.W)
        
    def create_menu_button(self, parent, text, command, y_offset, bg_color="#0e639c"):
        """Create a menu button with rounded corners"""
        # Create canvas for the button
        canvas = tk.Canvas(
            parent,
            width=280,
            height=60,
            bg=self.vs_code_dark,
            highlightthickness=0
        )
        canvas.pack(pady=(y_offset if y_offset == 0 else 20, 0))
        
        # Draw rounded rectangle
        radius = 8
        canvas.create_rounded_rect(
            2, 2, 278, 58,
            radius=radius,
            fill=bg_color,
            outline=""
        )
        
        # Add text
        canvas.create_text(
            140, 30,
            text=text,
            fill="white",
            font=("Arial", 12, "bold")
        )
        
        # Bind click event
        canvas.bind("<Button-1>", lambda e: command())
        canvas.bind("<Enter>", lambda e: self.on_menu_button_hover(canvas, bg_color, True, text))
        canvas.bind("<Leave>", lambda e: self.on_menu_button_hover(canvas, bg_color, False, text))
        canvas.configure(cursor="hand2")
        
        return canvas
    
    def on_menu_button_hover(self, canvas, original_color, is_hover, text):
        """Handle menu button hover effects"""
        if is_hover:
            # Darken color on hover
            hover_color = self.darken_color(original_color)
        else:
            hover_color = original_color
        
        # Redraw button with new color
        canvas.delete("all")
        radius = 8
        
        canvas.create_rounded_rect(
            2, 2, 278, 58,
            radius=radius,
            fill=hover_color,
            outline=""
        )
        
        canvas.create_text(
            140, 30,
            text=text,
            fill="white",
            font=("Arial", 12, "bold")
        )
    
    def darken_color(self, color):
        """Darken a hex color for hover effect"""
        if color == "#0e639c":
            return "#0a4d7a"
        elif color == "#28a745":
            return "#1e7e34"
        elif color == "#dc3545":
            return "#c82333"
        return color
    
    def on_sensitivity_change(self, value):
        """Handle sensitivity scale changes"""
        self.detection_sensitivity = float(value)
        self.sensitivity_display.config(text=f"Actual: {self.detection_sensitivity:.1f}")
        
        # Show tooltip with current settings
        if hasattr(self, 'sensitivity_tooltip_id'):
            self.root.after_cancel(self.sensitivity_tooltip_id)
        
        # Calculate current parameters for display
        scale_factor = 1.03 + (self.detection_sensitivity * 0.07)
        min_neighbors = int(2 + (self.detection_sensitivity * 3))
        min_size_w = int(20 + (self.detection_sensitivity * 60))
        min_size_h = int(5 + (self.detection_sensitivity * 15))
        
        tooltip_text = f"scaleFactor={scale_factor:.2f}, minNeighbors={min_neighbors}, minSize=({min_size_w},{min_size_h})"
        
        # Update display with current parameters (temporary)
        original_text = self.sensitivity_display.cget("text")
        self.sensitivity_display.config(text=tooltip_text, fg="#888888")
        
        # Restore original text after 2 seconds
        self.sensitivity_tooltip_id = self.root.after(2000, 
            lambda: self.sensitivity_display.config(text=original_text, fg="#0e639c"))
        
    def setup_right_panel(self, parent):
        # Default placeholder
        self.placeholder_label = tk.Label(
            parent,
            text="Selecciona una imagen para comenzar\n\n📸 Usa el menú lateral para cargar una imagen\no realizar operaciones",
            font=("Arial", 16),
            fg="#cccccc",
            bg=self.vs_code_light,
            justify=tk.CENTER
        )
        self.placeholder_label.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
    
    def display_image(self, image_path):
        """Display the selected image in the right panel"""
        try:
            # Clear the right panel
            for widget in self.right_panel.winfo_children():
                widget.destroy()
            
            # Load and display the image
            image = Image.open(image_path)
            
            # Resize to fit the right panel (960x720) preserving aspect ratio
            panel_width = 960
            panel_height = 720
            
            orig_w, orig_h = image.size
            
            # Calculate scale to fit within panel
            scale_w = panel_width / orig_w
            scale_h = panel_height / orig_h
            scale = min(scale_w, scale_h)
            
            new_w = max(1, int(orig_w * scale))
            new_h = max(1, int(orig_h * scale))
            
            resized = image.resize((new_w, new_h), Image.Resampling.LANCZOS)
            
            # Convert to PhotoImage
            photo = ImageTk.PhotoImage(resized)
            
            # Create label to display image
            image_label = tk.Label(self.right_panel, image=photo, bg=self.vs_code_light)
            image_label.image = photo  # Keep reference
            image_label.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
            
            # Update image info
            filename = os.path.basename(image_path)
            self.info_label.config(text=f"Imagen cargada:\n{filename}\n\nDimensiones: {orig_w}x{orig_h}")
            
            # Update window title
            self.root.title(f"Autolens Studio - {filename}")
            
        except Exception as e:
            print(f"Error displaying image: {str(e)}")
            messagebox.showerror("Error", f"No se pudo cargar la imagen:\n{str(e)}")
    
    def detect_license_plates(self):
        """Función para detección de matrículas"""
        if not self.current_image_path:
            messagebox.showwarning("Sin imagen", "Por favor, carga una imagen primero.")
            return
        
        try:
            # Verificar que DetectLicenseSimple.py existe
            import sys
            import os
            
            # Agregar el directorio actual al path si no está
            current_dir = os.path.dirname(os.path.abspath(__file__))
            if current_dir not in sys.path:
                sys.path.insert(0, current_dir)
            
            # Intentar importar función de detección
            try:
                from DetectLicenseSimple import detect_plates_for_interface
            except ImportError as ie:
                messagebox.showerror("Error de Importación", 
                                   f"No se pudo importar DetectLicenseSimple.py:\n{str(ie)}\n\n" +
                                   "Posibles causas:\n" +
                                   "• Falta instalar opencv-python: pip install opencv-python\n" +
                                   "• Falta instalar easyocr: pip install easyocr\n" +
                                   "• El archivo DetectLicenseSimple.py tiene errores de sintaxis")
                return
            except Exception as ee:
                messagebox.showerror("Error", f"Error al importar DetectLicenseSimple.py:\n{str(ee)}")
                return
            
            # Mostrar ventana de progreso
            progress_window = tk.Toplevel(self.root)
            progress_window.title("Detectando Matrículas...")
            progress_window.geometry("300x100")
            progress_window.resizable(False, False)
            progress_window.transient(self.root)
            progress_window.grab_set()
            
            # Centrar ventana
            progress_window.update_idletasks()
            x = (progress_window.winfo_screenwidth() // 2) - (300 // 2)
            y = (progress_window.winfo_screenheight() // 2) - (100 // 2)
            progress_window.geometry(f"300x100+{x}+{y}")
            
            progress_label = tk.Label(
                progress_window, 
                text="🚗 Detectando matrículas...\nPor favor espere...", 
                font=("Arial", 10), 
                justify=tk.CENTER
            )
            progress_label.pack(expand=True)
            
            # Actualizar interfaz
            self.root.update()
            progress_window.update()
            
            # Ejecutar detección con sensibilidad configurada
            print(f"Ruta de imagen en InterfazStudio: {self.current_image_path}")
            print(f"Sensibilidad configurada: {self.detection_sensitivity}")
            processed_img, detected_texts, success = detect_plates_for_interface(self.current_image_path, self.detection_sensitivity)
            
            # Cerrar ventana de progreso
            progress_window.destroy()
            
            if success:
                # Mostrar imagen procesada si hay detecciones
                if processed_img is not None:
                    self.display_processed_image(processed_img)
                
                # Mostrar resultados
                result_message = "🚗 DETECCIÓN COMPLETADA\n\n"
                result_message += "📋 RESULTADOS:\n"
                for text in detected_texts:
                    result_message += f"• {text}\n"
                
                messagebox.showinfo("Resultados de Detección", result_message)
            else:
                # Mostrar errores
                error_message = "❌ ERROR EN LA DETECCIÓN\n\n"
                for text in detected_texts:
                    error_message += f"• {text}\n"
                
                messagebox.showerror("Error de Detección", error_message)
                
        except Exception as e:
            if 'progress_window' in locals():
                progress_window.destroy()
            
            messagebox.showerror("Error Inesperado", 
                               f"Error durante la detección:\n{str(e)}")
    
    def display_processed_image(self, cv2_image):
        """Mostrar imagen procesada con detecciones"""
        try:
            import cv2
            from PIL import Image, ImageTk
            
            # Convertir de BGR a RGB
            rgb_image = cv2.cvtColor(cv2_image, cv2.COLOR_BGR2RGB)
            pil_image = Image.fromarray(rgb_image)
            
            # Limpiar panel derecho
            for widget in self.right_panel.winfo_children():
                widget.destroy()
            
            # Redimensionar para el panel
            panel_width = 960
            panel_height = 720
            
            orig_w, orig_h = pil_image.size
            scale_w = panel_width / orig_w
            scale_h = panel_height / orig_h
            scale = min(scale_w, scale_h)
            
            new_w = max(1, int(orig_w * scale))
            new_h = max(1, int(orig_h * scale))
            
            resized = pil_image.resize((new_w, new_h), Image.Resampling.LANCZOS)
            
            # Mostrar imagen
            photo = ImageTk.PhotoImage(resized)
            image_label = tk.Label(self.right_panel, image=photo, bg=self.vs_code_light)
            image_label.image = photo
            image_label.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
            
            # Actualizar título
            filename = os.path.basename(self.current_image_path)
            self.root.title(f"Autolens Studio - {filename} [Procesada]")
            
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo mostrar la imagen procesada:\n{str(e)}")
    
    def crop_photo(self):
        """Función para recorte de foto"""
        if not self.current_image_path:
            messagebox.showwarning("Sin imagen", "Por favor, carga una imagen primero.")
            return
        
        try:
            # Verificar que CutPhoto.py existe
            import sys
            import os
            
            # Agregar el directorio actual al path si no está
            current_dir = os.path.dirname(os.path.abspath(__file__))
            if current_dir not in sys.path:
                sys.path.insert(0, current_dir)
            
            # Intentar importar función de recorte
            try:
                from CutPhoto import crop_photo_for_interface
            except ImportError as ie:
                messagebox.showerror("Error de Importación", 
                                   f"No se pudo importar CutPhoto.py:\n{str(ie)}\n\n" +
                                   "Posibles causas:\n" +
                                   "• Falta instalar opencv-python: pip install opencv-python\n" +
                                   "• El archivo CutPhoto.py tiene errores de sintaxis")
                return
            except Exception as ee:
                messagebox.showerror("Error", f"Error al importar CutPhoto.py:\n{str(ee)}")
                return
            
            # Mostrar instrucciones antes de abrir OpenCV
            instruction_msg = """✂️ RECORTE DE FOTO

Se abrirá una ventana de OpenCV para seleccionar el área a recortar.

INSTRUCCIONES:
• Haz clic y arrastra para seleccionar el área
• Presiona 'C' para confirmar el recorte
• Presiona 'R' para reiniciar la selección  
• Presiona 'ESC' o 'Q' para cancelar

¿Continuar con el recorte?"""
            
            result = messagebox.askyesno("Instrucciones de Recorte", instruction_msg)
            if not result:
                return
            
            # Ejecutar recorte
            print(f"Iniciando recorte de imagen: {self.current_image_path}")
            success, cropped_path, message = crop_photo_for_interface(self.current_image_path)
            
            if success and cropped_path:
                # Cargar automáticamente la imagen recortada en el visor
                self.current_image_path = cropped_path
                self.display_image(cropped_path)
                
                # Actualizar título de ventana
                filename = os.path.basename(cropped_path)
                self.root.title(f"Autolens Studio - {filename}")
                
                # Mostrar mensaje de éxito
                messagebox.showinfo("Recorte Completado", 
                                  f"✅ RECORTE EXITOSO\n\n{message}\n\nLa imagen recortada se ha cargado automáticamente en el visor.")
            else:
                # Mostrar error
                if message:
                    messagebox.showerror("Error en Recorte", f"❌ {message}")
                else:
                    messagebox.showinfo("Recorte Cancelado", "La operación de recorte fue cancelada.")
                    
        except Exception as e:
            messagebox.showerror("Error Inesperado", 
                               f"Error durante el recorte:\n{str(e)}")
    
    def load_new_image(self):
        """Cargar una nueva imagen"""
        file_path = filedialog.askopenfilename(
            title="Seleccionar imagen",
            filetypes=[
                ("Archivos de imagen", "*.jpg *.jpeg *.png *.bmp *.gif *.tiff"),
                ("JPEG", "*.jpg *.jpeg"),
                ("PNG", "*.png"),
                ("Todos los archivos", "*.*")
            ]
        )
        
        if file_path:
            self.current_image_path = file_path
            self.display_image(file_path)
    
    def return_to_main(self):
        """Volver a la interfaz principal"""
        self.root.destroy()
        # Importar y abrir la interfaz principal
        from Interfaz import PhotoInterface
        main_app = PhotoInterface()
        main_app.run()
    
    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = StudioInterface()
    app.run()