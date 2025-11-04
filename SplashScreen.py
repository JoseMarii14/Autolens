import pygame
import cv2
import sys
import os
import numpy as np
from PIL import Image, ImageDraw
import threading
import time

class VideoSplashScreen:
    def __init__(self, video_path, on_complete_callback=None):
        self.video_path = video_path
        self.on_complete_callback = on_complete_callback
        self.is_playing = False
        self.cap = None
        
        # Corner radius for rounded corners
        self.corner_radius = 20
        self.use_rounded_corners = True
        
        # Initialize pygame
        pygame.init()
        pygame.mixer.quit()  # Disable audio to avoid conflicts
        
        # Get video dimensions
        self.video_width, self.video_height = self.get_video_dimensions()
        
        # Scale down the video (same as tkinter version)
        scale_factor = 0.45
        self.window_width = int(self.video_width * scale_factor)
        self.window_height = int(self.video_height * scale_factor)
        
        # Create pygame window with per-pixel alpha support
        self.screen = pygame.display.set_mode((self.window_width, self.window_height), pygame.NOFRAME)
        pygame.display.set_caption("Loading...")
        
        # Set window to support transparency
        if sys.platform == "win32":
            import ctypes
            from ctypes import wintypes
            hwnd = pygame.display.get_wm_info()["window"]
            # Make window layered for transparency
            ctypes.windll.user32.SetWindowLongW(hwnd, -20, 0x80000 | 0x20)
            # Set transparency color key (black will be transparent)
            ctypes.windll.user32.SetLayeredWindowAttributes(hwnd, 0x000000, 0, 1)
        
        # Center window on screen
        self.center_window()
        
        # Clock for FPS control
        self.clock = pygame.time.Clock()
        
    def center_window(self):
        """Center the pygame window on screen"""
        import tkinter as tk
        root = tk.Tk()
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        root.destroy()
        
        x = (screen_width - self.window_width) // 2
        y = (screen_height - self.window_height) // 2
        
        os.environ['SDL_VIDEO_WINDOW_POS'] = f'{x},{y}'
        
    def get_video_dimensions(self):
        """Get the actual dimensions of the video file"""
        try:
            if not os.path.exists(self.video_path):
                print(f"Video file not found: {self.video_path}")
                return 800, 600
                
            temp_cap = cv2.VideoCapture(self.video_path)
            if not temp_cap.isOpened():
                print(f"Could not open video file: {self.video_path}")
                temp_cap.release()
                return 800, 600
            
            width = int(temp_cap.get(cv2.CAP_PROP_FRAME_WIDTH))
            height = int(temp_cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
            temp_cap.release()
            
            if width <= 0 or height <= 0:
                print(f"Invalid video dimensions: {width}x{height}")
                return 800, 600
            
            print(f"Video dimensions: {width}x{height}")
            return width, height
            
        except Exception as e:
            print(f"Error getting video dimensions: {e}")
            return 800, 600
    
    def create_rounded_mask(self, width, height, radius):
        """Create a rounded corner mask manually"""
        mask = Image.new('L', (width, height), 0)
        draw = ImageDraw.Draw(mask)
        
        # Draw main rectangle
        draw.rectangle([(radius, 0), (width - radius, height)], fill=255)
        draw.rectangle([(0, radius), (width, height - radius)], fill=255)
        
        # Draw corner circles
        # Top-left
        draw.ellipse([(0, 0), (2 * radius, 2 * radius)], fill=255)
        # Top-right  
        draw.ellipse([(width - 2 * radius, 0), (width, 2 * radius)], fill=255)
        # Bottom-left
        draw.ellipse([(0, height - 2 * radius), (2 * radius, height)], fill=255)
        # Bottom-right
        draw.ellipse([(width - 2 * radius, height - 2 * radius), (width, height)], fill=255)
        
        return np.array(mask)
    
    def apply_rounded_corners(self, frame):
        """Apply rounded corners to a frame"""
        if not self.use_rounded_corners:
            return frame
            
        h, w = frame.shape[:2]
        
        # Create mask
        mask = self.create_rounded_mask(w, h, self.corner_radius)
        
        # Create a black background for the rounded corners
        background = np.zeros_like(frame)
        
        # Apply mask to each channel
        for i in range(frame.shape[2]):
            frame[:, :, i] = np.where(mask > 0, frame[:, :, i], background[:, :, i])
        
        return frame
    
    def load_video(self):
        """Load the video file"""
        try:
            if not os.path.exists(self.video_path):
                print(f"Video file not found: {self.video_path}")
                return False
                
            self.cap = cv2.VideoCapture(self.video_path)
            if not self.cap.isOpened():
                print(f"Could not open video file: {self.video_path}")
                return False
                
            return True
        except Exception as e:
            print(f"Error loading video: {e}")
            return False
    
    def show_fallback(self):
        """Show fallback content if video fails"""
        font = pygame.font.Font(None, 48)
        text_lines = [
            "Photo Enhancement Tool",
            "",
            "Loading..."
        ]
        
        self.screen.fill((0, 0, 0))
        
        y_offset = self.window_height // 2 - (len(text_lines) * 30) // 2
        for line in text_lines:
            if line:
                text_surface = font.render(line, True, (255, 255, 255))
                text_rect = text_surface.get_rect(center=(self.window_width // 2, y_offset))
                self.screen.blit(text_surface, text_rect)
            y_offset += 60
        
        pygame.display.flip()
        
        # Wait 3 seconds then close
        start_time = time.time()
        while time.time() - start_time < 3:
            for event in pygame.event.get():
                if event.type == pygame.QUIT or event.type == pygame.KEYDOWN:
                    return
            self.clock.tick(30)
    
    def play_video(self):
        """Play the video at 60 FPS"""
        if not self.load_video():
            self.show_fallback()
            return
        
        self.is_playing = True
        
        # Get video properties
        fps = self.cap.get(cv2.CAP_PROP_FPS)
        if fps <= 0:
            fps = 60  # Default to 60 FPS
        
        print(f"Video FPS: {fps}")
        
        running = True
        while running and self.is_playing:
            # Handle events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    running = False  # Click to skip
            
            # Read frame
            ret, frame = self.cap.read()
            if not ret:
                # Video ended
                break
            
            # Resize frame to window size
            frame = cv2.resize(frame, (self.window_width, self.window_height), interpolation=cv2.INTER_AREA)
            
            # Apply rounded corners if enabled
            if self.use_rounded_corners:
                frame = self.apply_rounded_corners(frame)
            
            # Convert BGR to RGB for pygame
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            
            # Convert to pygame surface
            frame = np.rot90(frame)
            frame = np.flipud(frame)
            surface = pygame.surfarray.make_surface(frame)
            
            # Clear screen with transparent black (will be transparent in corners)
            self.screen.fill((0, 0, 0))
            self.screen.blit(surface, (0, 0))
            pygame.display.flip()
            
            # Control FPS - pygame is much more precise than tkinter
            self.clock.tick(int(fps))
        
        self.cleanup()
    
    def cleanup(self):
        """Clean up resources"""
        self.is_playing = False
        if self.cap:
            self.cap.release()
        pygame.quit()
        
        # Call completion callback
        if self.on_complete_callback:
            self.on_complete_callback()
    
    def show(self):
        """Show the splash screen and start video playback"""
        self.play_video()

def show_splash_screen(on_complete=None):
    """Convenience function to show splash screen"""
    video_path = os.path.join(
        os.path.dirname(__file__), 
        "source", 
        "Final.mp4"
    )
    
    splash = VideoSplashScreen(video_path, on_complete)
    splash.show()

if __name__ == "__main__":
    def on_splash_complete():
        print("Splash screen completed!")
    
    show_splash_screen(on_splash_complete)
