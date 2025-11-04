import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import os

class AboutWindow:
    def __init__(self, parent):
        self.parent = parent
        self.create_about_window()
    
    def create_about_window(self):
        """Create and display the About window"""
        # Color scheme matching InterfazStudio.py
        vs_code_light = "#2d2d2d"  # Same as right panel in InterfazStudio
        text_color = "#cccccc"     # Light text for dark background
        
        about_window = tk.Toplevel(self.parent)
        about_window.title("Acerca de Autolens")
        about_window.geometry("450x400")  # Made slightly taller for better content fit
        about_window.resizable(True, True)  # Allow resizing for better scroll experience
        about_window.configure(bg=vs_code_light)
        
        # Center the about window
        about_window.transient(self.parent)
        about_window.grab_set()
        
        # Center window on screen
        about_window.update_idletasks()
        x = (about_window.winfo_screenwidth() // 2) - (450 // 2)
        y = (about_window.winfo_screenheight() // 2) - (350 // 2)
        about_window.geometry(f"450x350+{x}+{y}")
        
        # Create main container with scrollbar
        # Canvas for scrolling
        canvas = tk.Canvas(about_window, bg=vs_code_light, highlightthickness=0)
        scrollbar = ttk.Scrollbar(about_window, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg=vs_code_light)
        
        # Configure scrolling
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Pack canvas and scrollbar
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Main content frame inside scrollable frame
        main_frame = tk.Frame(scrollable_frame, bg=vs_code_light, padx=30, pady=20)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Bind mousewheel to canvas for scroll functionality
        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        canvas.bind_all("<MouseWheel>", _on_mousewheel)
        
        # Logo
        logo_path = r"E:\Usuarios\Estudios\Desktop\Universidad\4º año\Imagen Digital\Practica\Proyecto\source\AutolensLogoOficial.png"
        try:
            logo_img = Image.open(logo_path)
            # Resize logo for the about window (smaller than main interface)
            logo_img.thumbnail((300, 100), Image.Resampling.LANCZOS)
            logo_photo = ImageTk.PhotoImage(logo_img)
            logo_label = tk.Label(main_frame, image=logo_photo, bg=vs_code_light, borderwidth=0, highlightthickness=0)
            logo_label.image = logo_photo  # Keep reference to avoid GC
            logo_label.pack(pady=(0, 20))
        except FileNotFoundError:
            # Fallback to text if logo not found
            fallback_label = tk.Label(
                main_frame,
                text="🚗 Autolens",
                font=("Arial", 24, "bold"),
                fg="#0e639c",
                bg=vs_code_light
            )
            fallback_label.pack(pady=(0, 20))
        
        # Program information
        info_text = """📋 ESPECIFICACIONES DEL PROGRAMA

🏷️ Nombre: Autolens Studio
📊 Versión: 1.0.0
📅 Fecha: Octubre 2025
👨‍💻 Desarrollador: José María Gordillo Gragera

🔧 FUNCIONALIDADES:
• Detección automática de matrículas
• Recorte interactivo de imágenes
• Interfaz moderna y intuitiva
• Procesamiento con OpenCV y EasyOCR

💻 TECNOLOGÍAS:
• Python 3.x
• Tkinter (Interfaz gráfica)
• OpenCV (Procesamiento de imagen)
• PIL/Pillow (Manipulación de imágenes)
• EasyOCR (Reconocimiento de texto)

📝 DESCRIPCIÓN:
Autolens Studio es una aplicación especializada
en el análisis y procesamiento de imágenes
automotrices, con enfoque en la detección
automática de matrículas vehiculares."""
        
        info_label = tk.Label(
            main_frame,
            text=info_text,
            font=("Arial", 10),
            fg=text_color,
            bg=vs_code_light,
            justify=tk.LEFT,
            anchor="nw"
        )
        info_label.pack(fill=tk.BOTH, expand=True)
        
        # Close button
        close_button = tk.Button(
            main_frame,
            text="Cerrar",
            font=("Arial", 11, "bold"),
            bg="#0e639c",
            fg="white",
            relief=tk.FLAT,
            padx=20,
            pady=8,
            cursor="hand2",
            command=about_window.destroy
        )
        close_button.pack(pady=(20, 0))
        
        # Hover effects for close button
        def on_enter(e):
            close_button.config(bg="#0a4d7a")
        def on_leave(e):
            close_button.config(bg="#0e639c")
            
        close_button.bind("<Enter>", on_enter)
        close_button.bind("<Leave>", on_leave)

def show_about_window(parent):
    """Convenience function to show the about window"""
    AboutWindow(parent)
