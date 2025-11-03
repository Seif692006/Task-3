import tkinter as tk

class CardiacWindow:
    def __init__(self, parent):
        self.window = tk.Toplevel(parent)
        self.window.title("Cardiac System - Human Body Systems Viewer")
        self.window.configure(bg="#2a2a2a")
        self.window.state('zoomed')

        # Force window creation before applying dark title bar
        self.window.update_idletasks()
        self.window.update()

        # Try dark title bar (Windows 10/11)
        try:
            from ctypes import windll, byref, sizeof, c_int

            HWND = windll.user32.GetParent(self.window.winfo_id())
            if HWND == 0:
                HWND = self.window.winfo_id()

            # Use immersive dark mode attribute
            DWMWA_USE_IMMERSIVE_DARK_MODE = 20  # works on most Windows 11 builds
            value = c_int(1)
            result = windll.dwmapi.DwmSetWindowAttribute(
                HWND, DWMWA_USE_IMMERSIVE_DARK_MODE, byref(value), sizeof(value)
            )

            # Fallback for older Windows 10 builds
            if result != 0:
                DWMWA_USE_IMMERSIVE_DARK_MODE = 19
                windll.dwmapi.DwmSetWindowAttribute(
                    HWND, DWMWA_USE_IMMERSIVE_DARK_MODE, byref(value), sizeof(value)
                )
        except Exception as e:
            print(f"Could not set dark title bar: {e}")

        # ESC to close
        self.window.bind("<Escape>", lambda e: self.window.destroy())

        # Sidebar (left)
        sidebar = tk.Frame(self.window, bg="#2a2a2a", width=300)
        sidebar.pack(side=tk.LEFT, fill=tk.Y)
        sidebar.pack_propagate(False)

        header = tk.Frame(sidebar, bg="#2a2a2a")
        header.pack(pady=30, padx=20)

        tk.Label(header, text="❤️", font=("Segoe UI Emoji", 36), bg="#2a2a2a", fg="white").pack()
        tk.Label(header, text="Cardiac System", font=("Segoe UI", 16, "bold"), bg="#2a2a2a", fg="white").pack(pady=(10, 0))
        tk.Frame(sidebar, bg="#404040", height=1).pack(fill=tk.X, padx=20, pady=20)

        # Visualization area
        viz_area = tk.Frame(self.window, bg="#1a1a1a")
        viz_area.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        center = tk.Frame(viz_area, bg="#1a1a1a")
        center.place(relx=0.5, rely=0.5, anchor="center")

        tk.Label(center, text="❤️", font=("Segoe UI Emoji", 64), bg="#1a1a1a", fg="white").pack()
        tk.Label(center, text="Cardiac System Visualization Area", font=("Segoe UI", 24, "bold"),
                 bg="#1a1a1a", fg="white").pack(pady=(20, 10))
        tk.Label(center, text="Content will be displayed here", font=("Segoe UI", 14),
                 bg="#1a1a1a", fg="#888888").pack()

        tk.Label(viz_area, text="Press ESC to return", font=("Segoe UI", 10),
                 bg="#1a1a1a", fg="#555555").pack(side=tk.BOTTOM, pady=20)

