import tkinter as tk
from tkinter import filedialog
from tkinter import font

from Systems.Cardiac_System import CardiacWindow
from Systems.Nervous_System import NervousWindow
from Systems.Musculoskeletal_System import MusculoskeletalWindow
from Systems.Dental_System import DentalWindow


class ModernButton(tk.Canvas):
    """Custom modern button with rounded corners and hover effects"""
    def __init__(self, parent, text, emoji, command=None, **kwargs):
        super().__init__(parent, **kwargs)
        self.text = text
        self.emoji = emoji
        self.command = command
        
        # Colors
        self.bg_color = "#2a2a2a"
        self.hover_color = "#3a3a3a"
        self.active_color = "#4a4a4a"
        self.current_color = self.bg_color
        
        # Configure canvas - larger size
        self.configure(
            bg="#1a1a1a",
            highlightthickness=0,
            width=450,
            height=200
        )
        
        # Create rounded rectangle
        self.create_rounded_rect()
        
        # Calculate center positions based on canvas size
        center_x = 450 / 2
        center_y = 200 / 2
        
        # Add emoji - centered in upper portion
        self.emoji_text = self.create_text(
            center_x, center_y - 35,
            text=self.emoji,
            font=("Segoe UI Emoji", 48),
            fill="#ffffff",
            tags="content",
            anchor="center"
        )
        
        # Add title - centered in lower portion
        self.title_text = self.create_text(
            center_x, center_y + 45,
            text=self.text,
            font=("Segoe UI", 17, "bold"),
            fill="#ffffff",
            tags="content",
            anchor="center"
        )
        
        # Bind events
        self.bind("<Enter>", self.on_enter)
        self.bind("<Leave>", self.on_leave)
        self.bind("<Button-1>", self.on_click)
        self.bind("<ButtonRelease-1>", self.on_release)
        
    def create_rounded_rect(self):
        """Create a rounded rectangle with smooth edges"""
        x1, y1, x2, y2 = 10, 10, 440, 190
        radius = 24
        
        # Create smooth rounded rectangle using arc-based approach
        self.rect = self.create_rectangle(
            x1 + radius, y1,
            x2 - radius, y2,
            fill=self.current_color,
            outline="",
            tags="rect"
        )
        
        # Top and bottom rectangles
        self.create_rectangle(x1, y1 + radius, x2, y2 - radius, fill=self.current_color, outline="", tags="rect")
        
        # Four corner circles
        self.create_oval(x1, y1, x1 + radius * 2, y1 + radius * 2, fill=self.current_color, outline="", tags="rect")
        self.create_oval(x2 - radius * 2, y1, x2, y1 + radius * 2, fill=self.current_color, outline="", tags="rect")
        self.create_oval(x1, y2 - radius * 2, x1 + radius * 2, y2, fill=self.current_color, outline="", tags="rect")
        self.create_oval(x2 - radius * 2, y2 - radius * 2, x2, y2, fill=self.current_color, outline="", tags="rect")
        
        # Subtle border
        self.create_rounded_rect_border(x1, y1, x2, y2, radius, "#404040", 1)
        
        # Raise content to top
        self.tag_raise("content")
        
    def create_rounded_rect_border(self, x1, y1, x2, y2, radius, color, width):
        """Create border for rounded rectangle"""
        points = []
        # Top side
        for i in range(x1 + radius, x2 - radius + 1):
            points.append((i, y1))
        # Right top arc
        for angle in range(0, 91, 5):
            import math
            x = x2 - radius + radius * math.cos(math.radians(angle))
            y = y1 + radius - radius * math.sin(math.radians(angle))
            points.append((x, y))
        # Right side
        for i in range(y1 + radius, y2 - radius + 1):
            points.append((x2, i))
        # Right bottom arc
        for angle in range(90, 181, 5):
            import math
            x = x2 - radius + radius * math.cos(math.radians(angle))
            y = y2 - radius - radius * math.sin(math.radians(angle))
            points.append((x, y))
        # Bottom side
        for i in range(x2 - radius, x1 + radius - 1, -1):
            points.append((i, y2))
        # Left bottom arc
        for angle in range(180, 271, 5):
            import math
            x = x1 + radius + radius * math.cos(math.radians(angle))
            y = y2 - radius - radius * math.sin(math.radians(angle))
            points.append((x, y))
        # Left side
        for i in range(y2 - radius, y1 + radius - 1, -1):
            points.append((x1, i))
        # Left top arc
        for angle in range(270, 361, 5):
            import math
            x = x1 + radius + radius * math.cos(math.radians(angle))
            y = y1 + radius - radius * math.sin(math.radians(angle))
            points.append((x, y))
        
        if len(points) > 2:
            flat_points = [coord for point in points for coord in point]
            self.create_line(flat_points, fill=color, width=width, smooth=True, tags="border")
        
    def update_color(self, color):
        """Update button color with smooth transition"""
        self.current_color = color
        self.itemconfig("rect", fill=color)
        
    def on_enter(self, event):
        """Handle mouse enter"""
        self.update_color(self.hover_color)
        self.config(cursor="hand2")
        
    def on_leave(self, event):
        """Handle mouse leave"""
        self.update_color(self.bg_color)
        self.config(cursor="")
        
    def on_click(self, event):
        """Handle mouse click"""
        self.update_color(self.active_color)
        
    def on_release(self, event):
        """Handle mouse release"""
        self.update_color(self.hover_color)
        if self.command:
            self.command()


class MedicalSystemsGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Human Body Systems Viewer")
        
        # Remove white title bar and use dark theme
        try:
            # Windows 10/11 dark title bar
            self.root.tk.call('tk', 'scaling', 2.0)  # Increase DPI scaling for sharper text
            root.tk.call("wm", "attributes", ".", "-alpha", 0.0)
            root.update()
            root.tk.call("wm", "attributes", ".", "-alpha", 1.0)
            
            # Try to set dark title bar (Windows 11)
            try:
                from ctypes import windll, byref, sizeof, c_int
                HWND = windll.user32.GetParent(root.winfo_id())
                DWMWA_USE_IMMERSIVE_DARK_MODE = 20
                value = c_int(2)
                windll.dwmapi.DwmSetWindowAttribute(HWND, DWMWA_USE_IMMERSIVE_DARK_MODE, byref(value), sizeof(value))
            except:
                pass
        except:
            pass
        
        # Make window fullscreen
        self.root.state('zoomed')  # Windows
        # For cross-platform fullscreen, uncomment below:
        # self.root.attributes('-fullscreen', True)
        
        self.root.configure(bg="#1a1a1a")
        
        # Bind escape key to exit fullscreen
        self.root.bind('<Escape>', lambda e: self.root.quit())
        
        # Create main container
        self.create_widgets()
        
    def create_widgets(self):
        """Create all GUI widgets"""
        # Header frame with dark background
        header_frame = tk.Frame(self.root, bg="#1a1a1a")
        header_frame.pack(pady=(50, 20))
        
        # App icon/logo
        icon_label = tk.Label(
            header_frame,
            text="🏥",
            font=("Segoe UI Emoji", 32),
            bg="#1a1a1a",
            fg="#ffffff"
        )
        icon_label.pack()
        
        # Title with antialiasing
        title_label = tk.Label(
            header_frame,
            text="Human Body Systems Viewer",
            font=("Segoe UI", 28, "bold"),
            bg="#1a1a1a",
            fg="#ffffff",
            bd=0,
            highlightthickness=0
        )
        title_label.pack(pady=(8, 0))
        
        # Subtitle with antialiasing
        subtitle_label = tk.Label(
            header_frame,
            text="Select a system to explore",
            font=("Segoe UI", 12),
            bg="#1a1a1a",
            fg="#888888",
            bd=0,
            highlightthickness=0
        )
        subtitle_label.pack(pady=(8, 0))
        
        # Main content frame
        content_frame = tk.Frame(self.root, bg="#1a1a1a")
        content_frame.pack(pady=50, padx=80, expand=True)
        
        # System buttons data
        systems = [
            {"text": "Cardiac System", "emoji": "❤️", "command": lambda: self.open_system("Cardiac System", "❤️")},
            {"text": "Nervous System", "emoji": "🧠", "command": lambda: self.open_system("Nervous System", "🧠")},
            {"text": "Musculoskeletal System", "emoji": "💪", "command": lambda: self.open_system("Musculoskeletal System", "💪")},
            {"text": "Dental System", "emoji": "🦷", "command": lambda: self.open_system("Dental System", "🦷")}
        ]
        
        # Create buttons in 2x2 grid with proper spacing
        for i, system in enumerate(systems):
            row = i // 2
            col = i % 2
            
            button = ModernButton(
                content_frame,
                text=system["text"],
                emoji=system["emoji"],
                command=system["command"]
            )
            button.grid(row=row, column=col, padx=25, pady=25, sticky="nsew")
        
        # Configure grid weights for centering
        content_frame.grid_rowconfigure(0, weight=1)
        content_frame.grid_rowconfigure(1, weight=1)
        content_frame.grid_columnconfigure(0, weight=1)
        content_frame.grid_columnconfigure(1, weight=1)
        
        # Footer with antialiasing
        footer_label = tk.Label(
            self.root,
            text="MedViz Pro v1.0 • Advanced Medical Visualization • Press ESC to exit",
            font=("Segoe UI", 10),
            bg="#1a1a1a",
            fg="#555555",
            bd=0,
            highlightthickness=0
        )
        footer_label.pack(side=tk.BOTTOM, pady=30)
    
    
    def open_system(self, system_name, emoji):

        """Open detail window for a specific system"""
        if system_name == "Cardiac System":
            CardiacWindow(self.root)
        elif system_name == "Nervous System":
            NervousWindow(self.root)
        elif system_name == "Musculoskeletal System":
            MusculoskeletalWindow(self.root)
        elif system_name == "Dental System":
            DentalWindow(self.root)



def main():
    root = tk.Tk()
    
    # Enable high DPI awareness for sharper text on Windows
    try:
        from ctypes import windll
        windll.shcore.SetProcessDpiAwareness(1)  # System DPI aware
    except:
        try:
            from ctypes import windll
            windll.user32.SetProcessDPIAware()  # Older Windows versions
        except:
            pass
    
    app = MedicalSystemsGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()