import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import os

def select_and_display_image(right_panel, root_window):
    """
    Opens a file dialog to select an image and displays it in the provided panel.
    
    Args:
        right_panel: The tkinter Frame where the image will be displayed
        root_window: The main tkinter window (for updating title)
    
    Returns:
        str: Path of the selected image file, or None if no file was selected
    """
    # Define supported image formats
    filetypes = [
        ("Image files", "*.png *.jpg *.jpeg *.gif *.bmp *.tiff *.webp"),
        ("PNG files", "*.png"),
        ("JPEG files", "*.jpg *.jpeg"),
        ("GIF files", "*.gif"),
        ("BMP files", "*.bmp"),
        ("TIFF files", "*.tiff"),
        ("WEBP files", "*.webp"),
        ("All files", "*.*")
    ]
    
    # Open file dialog
    file_path = filedialog.askopenfilename(
        title="Select an image",
        filetypes=filetypes,
        initialdir=os.path.expanduser("~")
    )
    
    # If user selected a file, load and display it
    if file_path:
        success = display_image_in_panel(file_path, right_panel, root_window)
        if success:
            return file_path
    
    return None

def display_image_in_panel(image_path, panel, root_window=None):
    """
    Load and display an image in the specified panel.
    
    Args:
        image_path: Path to the image file
        panel: The tkinter Frame where the image will be displayed
        root_window: Optional main window for updating title
    
    Returns:
        bool: True if image was loaded successfully, False otherwise
    """
    try:
        # Clear the panel
        for widget in panel.winfo_children():
            widget.destroy()
        
        # Load the image
        image = Image.open(image_path)
        
        # Get panel dimensions (assuming 640x720 based on interface)
        panel_width = 640
        panel_height = 720
        
        # Resize image to fit the panel while maintaining aspect ratio
        image.thumbnail((panel_width, panel_height), Image.Resampling.LANCZOS)
        
        # Convert to PhotoImage
        photo = ImageTk.PhotoImage(image)
        
        # Create label to display image
        image_label = tk.Label(panel, image=photo, bg="white")
        image_label.image = photo  # Keep a reference to prevent garbage collection
        image_label.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
        
        # Update window title with filename if root_window is provided
        if root_window:
            filename = os.path.basename(image_path)
            root_window.title(f"Photo Interface - {filename}")
        
        print(f"Successfully loaded image: {image_path}")
        return True
        
    except FileNotFoundError:
        error_msg = f"Image file not found: {image_path}"
        print(error_msg)
        _show_error_in_panel(panel, "File not found", error_msg)
        return False
        
    except Exception as e:
        error_msg = f"Error loading image: {str(e)}"
        print(error_msg)
        messagebox.showerror("Error", f"Could not load image:\n{str(e)}")
        _show_error_in_panel(panel, "Error loading image", error_msg)
        return False

def _show_error_in_panel(panel, title, message):
    """
    Display an error message in the panel.
    
    Args:
        panel: The tkinter Frame where the error will be displayed
        title: Error title
        message: Error message
    """
    # Clear the panel
    for widget in panel.winfo_children():
        widget.destroy()
    
    # Show error in panel
    error_label = tk.Label(
        panel,
        text=f"{title}\n{message}",
        font=("Arial", 12),
        fg="red",
        bg="white",
        justify=tk.CENTER,
        wraplength=600
    )
    error_label.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

def get_image_info(image_path):
    """
    Get basic information about an image file.
    
    Args:
        image_path: Path to the image file
    
    Returns:
        dict: Dictionary with image information (width, height, format, size)
    """
    try:
        with Image.open(image_path) as img:
            file_size = os.path.getsize(image_path)
            return {
                'width': img.width,
                'height': img.height,
                'format': img.format,
                'mode': img.mode,
                'file_size': file_size,
                'file_size_mb': round(file_size / (1024 * 1024), 2)
            }
    except Exception as e:
        print(f"Error getting image info: {e}")
        return None