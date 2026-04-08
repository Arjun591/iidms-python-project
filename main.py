# main.py - Entry point of IIDMS
# Now includes login before showing the main window

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import tkinter as tk
from views.login import LoginWindow

COLORS = {
    "bg_dark":       "#1a1a2e",
    "bg_medium":     "#16213e",
    "bg_light":      "#0f3460",
    "accent":        "#e94560",
    "text_primary":  "#eaeaea",
    "text_secondary":"#a0a0b0",
    "success":       "#4caf50",
    "warning":       "#ff9800",
    "danger":        "#f44336",
    "border":        "#0f3460",
}


class IIDMSApp(tk.Tk):
    
    def __init__(self, current_user):
        super().__init__()
        
        # Store the logged in user
        # We'll use this everywhere to control what they can see
        self.current_user = current_user
        self.clearance    = current_user["clearance_level"]
        self.user_role    = current_user["role"]
        
        # ── Window settings ───────────────────────────
        self.title(f"IIDMS — {current_user['name']} [{self.clearance}]")
        self.geometry("1200x700")
        self.minsize(1000, 600)
        self.configure(bg=COLORS["bg_dark"])
        self.center_window()
        
        self.create_layout()
        self.show_dashboard()
    
    
    def center_window(self):
        self.update_idletasks()
        x = (self.winfo_screenwidth()  // 2) - (1200 // 2)
        y = (self.winfo_screenheight() // 2) - (700  // 2)
        self.geometry(f"1200x700+{x}+{y}")
    
    
    def create_layout(self):
        
        self.sidebar = tk.Frame(
            self,
            bg    = COLORS["bg_medium"],
            width = 220,
        )
        self.sidebar.grid(row=0, column=0, sticky="ns")
        self.sidebar.grid_propagate(False)
        
        self.content_area = tk.Frame(
            self,
            bg = COLORS["bg_dark"],
        )
        self.content_area.grid(row=0, column=1, sticky="nsew")
        
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        
        self.create_sidebar()
    
    
    def create_sidebar(self):
        
        # Logo
        logo_frame = tk.Frame(self.sidebar, bg=COLORS["bg_medium"], pady=20)
        logo_frame.pack(fill="x")
        
        tk.Label(
            logo_frame,
            text = "⚔ IIDMS",
            font = ("Helvetica", 18, "bold"),
            bg   = COLORS["bg_medium"],
            fg   = COLORS["accent"],
        ).pack()
        
        tk.Label(
            logo_frame,
            text = "Intelligence System",
            font = ("Helvetica", 9),
            bg   = COLORS["bg_medium"],
            fg   = COLORS["text_secondary"],
        ).pack()
        
        # Logged in user info
        tk.Frame(
            self.sidebar,
            bg     = COLORS["border"],
            height = 1
        ).pack(fill="x", padx=15)
        
        user_frame = tk.Frame(self.sidebar, bg=COLORS["bg_medium"], pady=12)
        user_frame.pack(fill="x", padx=15)
        
        tk.Label(
            user_frame,
            text = f"👤 {self.current_user['name']}",
            font = ("Helvetica", 9, "bold"),
            bg   = COLORS["bg_medium"],
            fg   = COLORS["text_primary"],
            anchor = "w",
            wraplength = 180,
        ).pack(fill="x")
        
        # Clearance badge with color based on level
        clearance_colors = {
            "L1": "#4caf50",
            "L2": "#2196f3",
            "L3": "#ff9800",
            "L4": "#e94560",
        }
        badge_color = clearance_colors.get(self.clearance, "#888")
        
        tk.Label(
            user_frame,
            text   = f"  {self.clearance} — {self.user_role}",
            font   = ("Helvetica", 9),
            bg     = badge_color,
            fg     = "white",
            anchor = "w",
            padx   = 6,
            pady   = 2,
        ).pack(fill="x", pady=(4,0))
        
        tk.Frame(
            self.sidebar,
            bg     = COLORS["border"],
            height = 1
        ).pack(fill="x", padx=15, pady=(8,0))
        
        # ── Navigation items based on clearance ───────
        # Everyone sees Dashboard and Incidents
        # Higher clearances see more options
        
        nav_items = [("🏠  Dashboard", self.show_dashboard, "L1")]
        nav_items.append(("⚠   Incidents",  self.show_incidents, "L1"))
        
        # L2 and above see Personnel
        if self.clearance in ["L2", "L3", "L4"]:
            nav_items.append(("👤  Personnel", self.show_personnel, "L2"))
        
        # L3 and above see Analytics
        if self.clearance in ["L3", "L4"]:
            nav_items.append(("📊  Analytics", self.show_analytics, "L3"))
        
        # L4 only sees Export
        if self.clearance == "L4":
            nav_items.append(("📤  Export", self.show_export, "L4"))
        
        self.nav_buttons = []
        
        for label, command, _ in nav_items:
            btn = tk.Button(
                self.sidebar,
                text             = label,
                command          = command,
                font             = ("Helvetica", 11),
                bg               = COLORS["bg_medium"],
                fg               = COLORS["text_primary"],
                activebackground = COLORS["bg_light"],
                activeforeground = COLORS["accent"],
                relief           = "flat",
                anchor           = "w",
                padx             = 20,
                pady             = 12,
                cursor           = "hand2",
                bd               = 0,
            )
            btn.pack(fill="x")
            self.nav_buttons.append(btn)
        
        # Logout button at bottom
        tk.Frame(
            self.sidebar,
            bg     = COLORS["border"],
            height = 1
        ).pack(fill="x", padx=15, side="bottom", pady=(0,5))
        
        tk.Button(
            self.sidebar,
            text             = "🔒  Logout",
            command          = self.logout,
            font             = ("Helvetica", 10),
            bg               = COLORS["bg_medium"],
            fg               = COLORS["danger"],
            activebackground = COLORS["bg_light"],
            activeforeground = COLORS["danger"],
            relief           = "flat",
            anchor           = "w",
            padx             = 20,
            pady             = 10,
            cursor           = "hand2",
            bd               = 0,
        ).pack(fill="x", side="bottom")
        
        tk.Label(
            self.sidebar,
            text = "v1.0 — Classified",
            font = ("Helvetica", 8),
            bg   = COLORS["bg_medium"],
            fg   = COLORS["text_secondary"],
        ).pack(side="bottom", pady=4)
    
    
    def clear_content(self):
        for widget in self.content_area.winfo_children():
            widget.destroy()
    
    
    def set_active_nav(self, index):
        for i, btn in enumerate(self.nav_buttons):
            if i == index:
                btn.configure(bg=COLORS["bg_light"], fg=COLORS["accent"])
            else:
                btn.configure(bg=COLORS["bg_medium"], fg=COLORS["text_primary"])
    
    
    def show_dashboard(self):
        self.clear_content()
        self.set_active_nav(0)
        tk.Label(
            self.content_area,
            text = f"🏠 Dashboard\n\nWelcome, {self.current_user['name']}\nClearance: {self.clearance}",
            font = ("Helvetica", 18),
            bg   = COLORS["bg_dark"],
            fg   = COLORS["text_primary"],
            justify = "center",
        ).pack(expand=True)
    
    
    def show_incidents(self):
        self.clear_content()
        self.set_active_nav(1)
        tk.Label(
            self.content_area,
            text = "⚠ Incidents\n\nComing soon...",
            font = ("Helvetica", 18),
            bg   = COLORS["bg_dark"],
            fg   = COLORS["text_primary"],
        ).pack(expand=True)
    
    
    def show_personnel(self):
        self.clear_content()
        self.set_active_nav(2)
        tk.Label(
            self.content_area,
            text = "👤 Personnel\n\nComing soon...",
            font = ("Helvetica", 18),
            bg   = COLORS["bg_dark"],
            fg   = COLORS["text_primary"],
        ).pack(expand=True)
    
    
    def show_analytics(self):
        self.clear_content()
        self.set_active_nav(3)
        tk.Label(
            self.content_area,
            text = "📊 Analytics\n\nComing soon...",
            font = ("Helvetica", 18),
            bg   = COLORS["bg_dark"],
            fg   = COLORS["text_primary"],
        ).pack(expand=True)
    
    
    def show_export(self):
        self.clear_content()
        self.set_active_nav(4)
        tk.Label(
            self.content_area,
            text = "📤 Export\n\nComing soon...",
            font = ("Helvetica", 18),
            bg   = COLORS["bg_dark"],
            fg   = COLORS["text_primary"],
        ).pack(expand=True)
    
    
    def logout(self):
        # Close main window and reopen login screen
        self.destroy()
        launch_app()


def launch_app():
    # This function runs the login window first
    # Then launches the main app with the logged in user
    
    def on_login_success(user):
        # Once login succeeds, open the main app
        app = IIDMSApp(current_user=user)
        app.mainloop()
    
    login = LoginWindow(on_login_success=on_login_success)
    login.mainloop()


if __name__ == "__main__":
    launch_app()