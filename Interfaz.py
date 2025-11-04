import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import os
from SelectImg import select_and_display_image

class PhotoInterface:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Autolens")
        self.root.geometry("1280x720")
        self.root.resizable(False, False)
        
        # Center the window on screen
        self.center_window()
        
        # VS Code dark theme color
        self.vs_code_dark = "#1e1e1e"
        
        # Store reference to right panel for image updates
        self.right_panel = None
        
        # Store path of currently selected image for enhancement
        self.current_image_path = None
        
        # Add rounded rectangle method to Canvas
        self.add_rounded_rect_to_canvas()
        
        self.setup_interface()
    
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
        
        # Left panel (640x720) - VS Code dark color
        left_panel = tk.Frame(main_frame, bg=self.vs_code_dark, width=640, height=720)
        left_panel.pack(side=tk.LEFT, fill=tk.BOTH)
        left_panel.pack_propagate(False)
        
        # Right panel (640x720) - Image
        self.right_panel = tk.Frame(main_frame, width=640, height=720)
        self.right_panel.pack(side=tk.RIGHT, fill=tk.BOTH)
        self.right_panel.pack_propagate(False)
        
        # Add content to left panel
        self.setup_left_panel(left_panel)
        # Add image to right panel
        self.setup_right_panel(self.right_panel)
        
    def setup_left_panel(self, parent):
        # Logo image replacing "Photo" text
        logo_path = r"E:\Usuarios\Estudios\Desktop\Universidad\4º año\Imagen Digital\Practica\Proyecto\source\AutolensLogoOficial.png"
        try:
            logo_img = Image.open(logo_path)
            # Fit logo in the header area of the left panel (larger size for better visibility)
            logo_img.thumbnail((640, 280), Image.Resampling.LANCZOS)
            logo_photo = ImageTk.PhotoImage(logo_img)
            logo_label = tk.Label(parent, image=logo_photo, bg=self.vs_code_dark, borderwidth=0, highlightthickness=0)
            logo_label.image = logo_photo  # Keep reference to avoid GC
            logo_label.place(relx=0.5, rely=0.25, anchor=tk.CENTER)
        except FileNotFoundError:
            # Fallback to text if logo not found
            fallback_label = tk.Label(
                parent,
                text="Photo",
                font=("Arial", 36, "bold"),
                fg="white",
                bg=self.vs_code_dark
            )
            fallback_label.place(relx=0.5, rely=0.25, anchor=tk.CENTER)
        
        # Create rounded Select Photo button
        self.create_rounded_button(
            parent,
            text="Seleccionar Foto",
            x=320, y=400,  # Moved down from y=324 to y=400
            width=240, height=50,  # Made wider from 180 to 240
            bg_color="#0e639c",
            text_color="white",
            command=self.button_clicked
        )
        
        # Create rounded Acerca de button
        self.create_rounded_button(
            parent,
            text="Acerca de",
            x=320, y=480,  # Below Select Photo button
            width=240, height=50,
            bg_color="#612BC4",  # Purple color
            text_color="white",
            command=self.show_about
        )
    
    def create_rounded_button(self, parent, text, x, y, width, height, bg_color, text_color, command):
        """Create a button with rounded corners using Canvas"""
        # Create canvas for the button
        canvas = tk.Canvas(
            parent,
            width=width,
            height=height,
            bg=self.vs_code_dark,
            highlightthickness=0
        )
        canvas.place(x=x-width//2, y=y-height//2)
        
        # Draw rounded rectangle
        radius = 10
        canvas.create_rounded_rect(
            2, 2, width-2, height-2,
            radius=radius,
            fill=bg_color,
            outline=""
        )
        
        # Add text
        canvas.create_text(
            width//2, height//2,
            text=text,
            fill=text_color,
            font=("Arial", 14, "bold")
        )
        
        # Bind click event
        canvas.bind("<Button-1>", lambda e: command())
        canvas.bind("<Enter>", lambda e: self.on_button_hover(canvas, bg_color, True))
        canvas.bind("<Leave>", lambda e: self.on_button_hover(canvas, bg_color, False))
        canvas.configure(cursor="hand2")
        
        return canvas
    
    def on_button_hover(self, canvas, original_color, is_hover):
        """Handle button hover effects"""
        if is_hover:
            # Darken color on hover
            hover_color = self.darken_color(original_color)
        else:
            hover_color = original_color
        
        # Redraw button with new color
        canvas.delete("all")
        width = canvas.winfo_width()
        height = canvas.winfo_height()
        radius = 10
        
        canvas.create_rounded_rect(
            2, 2, width-2, height-2,
            radius=radius,
            fill=hover_color,
            outline=""
        )
        
        # Get text from canvas (we'll store it)
        if "#0e639c" in original_color:
            text = "Seleccionar Foto"
        elif "#612BC4" in original_color:
            text = "Acerca de"
        else:
            text = "Button"
        canvas.create_text(
            width//2, height//2,
            text=text,
            fill="white",
            font=("Arial", 14, "bold")
        )
    
    def darken_color(self, color):
        """Darken a hex color for hover effect"""
        if color == "#0e639c":
            return "#0a4d7a"
        elif color == "#612BC4":
            return "#4a1f9a"
        return color
        
    def setup_right_panel(self, parent):
        # Load and display the wallpaper image
        candidate_paths = [
            r"E:\\Usuarios\\Estudios\\Desktop\\Universidad\\4º año\\Imagen Digital\\Practica\\Proyecto\\source\\wallpaperCoche.jpg",
            r"E:\\Usuarios\\Estudios\\Desktop\\Universidad\\4º año\\Imagen Digital\\Practica\\Proyecto\\source\\wallpape.jpg",
            r"E:\\Usuarios\\Estudios\\Desktop\\Universidad\\4º año\\Imagen Digital\\Practica\\Proyecto\\source\\wallpaper1.png",
            r"E:\\Usuarios\\Estudios\\Desktop\\Universidad\\4º año\\Imagen Digital\\Practica\\Proyecto\\source\\wallpaper.png",
        ]
        image_path = next((p for p in candidate_paths if os.path.exists(p)), None)
        
        try:
            if image_path is None:
                raise FileNotFoundError("No wallpaper image found in candidate paths")
            # Load the image
            image = Image.open(image_path)
            
            # Resize image to match panel height (720px) preserving aspect ratio
            orig_w, orig_h = image.size
            target_h = 720
            if orig_h == 0:
                orig_h = 1
            scale = target_h / orig_h
            new_w = max(1, int(orig_w * scale))
            resized = image.resize((new_w, target_h), Image.Resampling.LANCZOS)
            
            # Convert to PhotoImage
            photo = ImageTk.PhotoImage(resized)
            
            # Create label to display image
            image_label = tk.Label(parent, image=photo, bg="white")
            image_label.image = photo  # Keep a reference to prevent garbage collection
            image_label.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
            
        except FileNotFoundError:
            # If image not found, show placeholder with tried paths
            tried = "\n".join(candidate_paths)
            placeholder_label = tk.Label(
                parent,
                text=f"Wallpaper not found. Tried paths:\n{tried}",
                font=("Arial", 12),
                fg="red",
                bg="white",
                justify=tk.CENTER
            )
            placeholder_label.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
        except Exception as e:
            # Handle other errors
            error_label = tk.Label(
                parent,
                text=f"Error loading image:\n{str(e)}",
                font=("Arial", 12),
                fg="red",
                bg="white",
                justify=tk.CENTER
            )
            error_label.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
    
    def button_clicked(self):
        """Open file dialog to select an image and open Studio interface"""
        selected_image_path = select_and_display_image(self.right_panel, self.root)
        if selected_image_path:
            self.current_image_path = selected_image_path
            print(f"Image selected: {selected_image_path}")
            print("🎨 Abriendo Autolens Studio...")
            
            # Close current window
            self.root.destroy()
            
            # Open Studio interface with the selected image
            from InterfazStudio import StudioInterface
            studio_app = StudioInterface(selected_image_path)
            studio_app.run()
    
    def show_about(self):
        """Show About dialog with program specifications"""
        from AboutWindow import show_about_window
        show_about_window(self.root)

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = PhotoInterface()
    app.run()