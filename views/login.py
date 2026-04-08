# This is the first screen the user sees when they launch IIDMS
# It handles username/password input and clearance verification

import tkinter as tk
from tkinter import messagebox
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from controllers.user_controller import verify_login

# Same color scheme as main.py
COLORS = {
    "bg_dark":       "#1a1a2e",
    "bg_medium":     "#16213e",
    "bg_light":      "#0f3460",
    "accent":        "#e94560",
    "text_primary":  "#eaeaea",
    "text_secondary":"#a0a0b0",
    "success":       "#4caf50",
    "danger":        "#f44336",
    "input_bg":      "#0f3460",
    "border":        "#e94560",
}


class LoginWindow(tk.Tk):
    # The login window is a separate small window
    # that appears before the main app loads
    
    def __init__(self, on_login_success):
        super().__init__()
        
        # on_login_success is a function we'll call when login works
        # We pass the logged-in user's data to the main app through it
        self.on_login_success = on_login_success
        
        # ── Window settings ───────────────────────────
        self.title("IIDMS — Secure Login")
        self.geometry("420x550")
        self.resizable(False, False)   # fixed size login window
        self.configure(bg=COLORS["bg_dark"])
        self.center_window()
        
        # Build the login UI
        self.create_widgets()
    
    
    def center_window(self):
        self.update_idletasks()
        x = (self.winfo_screenwidth()  // 2) - (420 // 2)
        y = (self.winfo_screenheight() // 2) - (550 // 2)
        self.geometry(f"420x550+{x}+{y}")
    
    
    def create_widgets(self):
        # Builds all visual elements of the login screen
        
        # ── Top logo section ──────────────────────────
        header = tk.Frame(self, bg=COLORS["bg_dark"], pady=30)
        header.pack(fill="x")
        
        tk.Label(
            header,
            text = "⚔",
            font = ("Helvetica", 48),
            bg   = COLORS["bg_dark"],
            fg   = COLORS["accent"],
        ).pack()
        
        tk.Label(
            header,
            text = "IIDMS",
            font = ("Helvetica", 24, "bold"),
            bg   = COLORS["bg_dark"],
            fg   = COLORS["text_primary"],
        ).pack()
        
        tk.Label(
            header,
            text = "Integrated Intelligence & Incident\nData Management System",
            font = ("Helvetica", 9),
            bg   = COLORS["bg_dark"],
            fg   = COLORS["text_secondary"],
            justify = "center",
        ).pack(pady=(2, 0))
        
        # ── Login form card ───────────────────────────
        card = tk.Frame(
            self,
            bg     = COLORS["bg_medium"],
            padx   = 30,
            pady   = 30,
        )
        card.pack(fill="x", padx=30)
        
        # Username field
        tk.Label(
            card,
            text = "USERNAME",
            font = ("Helvetica", 9, "bold"),
            bg   = COLORS["bg_medium"],
            fg   = COLORS["text_secondary"],
            anchor = "w",
        ).pack(fill="x")
        
        self.username_entry = tk.Entry(
            card,
            font             = ("Helvetica", 12),
            bg               = COLORS["input_bg"],
            fg               = COLORS["text_primary"],
            insertbackground = COLORS["text_primary"],  # cursor color
            relief           = "flat",
            bd               = 8,
        )
        self.username_entry.pack(fill="x", pady=(4, 16))
        
        # Password field
        tk.Label(
            card,
            text = "PASSWORD",
            font = ("Helvetica", 9, "bold"),
            bg   = COLORS["bg_medium"],
            fg   = COLORS["text_secondary"],
            anchor = "w",
        ).pack(fill="x")
        
        self.password_entry = tk.Entry(
            card,
            font             = ("Helvetica", 12),
            bg               = COLORS["input_bg"],
            fg               = COLORS["text_primary"],
            insertbackground = COLORS["text_primary"],
            relief           = "flat",
            bd               = 8,
            show             = "●",   # hides password characters
        )
        self.password_entry.pack(fill="x", pady=(4, 24))
        
        # Login button
        self.login_btn = tk.Button(
            card,
            text             = "LOGIN",
            font             = ("Helvetica", 12, "bold"),
            bg               = COLORS["accent"],
            fg               = "white",
            activebackground = "#c73652",
            activeforeground = "white",
            relief           = "flat",
            bd               = 0,
            pady             = 10,
            cursor           = "hand2",
            command          = self.attempt_login,
        )
        self.login_btn.pack(fill="x")
        
        # Status message label
        # Shows error messages or success messages
        self.status_label = tk.Label(
            card,
            text = "",
            font = ("Helvetica", 10),
            bg   = COLORS["bg_medium"],
            fg   = COLORS["danger"],
        )
        self.status_label.pack(pady=(12, 0))
        
        # ── Hint section ──────────────────────────────
        hint = tk.Frame(self, bg=COLORS["bg_dark"], pady=15)
        hint.pack(fill="x", padx=30)
        
        tk.Label(
            hint,
            text    = "Test credentials:",
            font    = ("Helvetica", 9, "bold"),
            bg      = COLORS["bg_dark"],
            fg      = COLORS["text_secondary"],
            anchor  = "w",
        ).pack(fill="x")
        
        hints = [
            "admin / Admin@1234       → L4 Full Access",
            "officer1 / Officer@123   → L3 Officer",
            "analyst1 / Analyst@123   → L2 Analyst",
            "field1 / Field@123       → L1 View Only",
        ]
        
        for hint_text in hints:
            tk.Label(
                hint,
                text   = hint_text,
                font   = ("Courier", 8),
                bg     = COLORS["bg_dark"],
                fg     = COLORS["text_secondary"],
                anchor = "w",
            ).pack(fill="x")
        
        # Press Enter key to login - more convenient than clicking
        self.bind("<Return>", lambda event: self.attempt_login())
        
        # Put cursor in username field automatically
        self.username_entry.focus()
    
    
    def attempt_login(self):
        # Called when Login button is clicked or Enter is pressed
        
        # Get what the user typed
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()
        
        # Basic validation - check fields aren't empty
        if not username:
            self.status_label.config(
                text = "⚠ Please enter your username",
                fg   = COLORS["danger"]
            )
            return
        
        if not password:
            self.status_label.config(
                text = "⚠ Please enter your password",
                fg   = COLORS["danger"]
            )
            return
        
        # Show checking message
        self.status_label.config(
            text = "Verifying credentials...",
            fg   = COLORS["text_secondary"]
        )
        self.update()  # forces the UI to refresh immediately
        
        # Attempt login through our controller
        user = verify_login(username, password)
        
        if user:
            # Login successful
            self.status_label.config(
                text = f"✓ Access granted — {user['clearance_level']}",
                fg   = COLORS["success"]
            )
            self.update()
            
            # Wait half a second so user sees the success message
            self.after(500, lambda: self.login_success(user))
        else:
            # Login failed
            self.status_label.config(
                text = "⚠ Invalid username or password",
                fg   = COLORS["danger"]
            )
            # Clear the password field
            self.password_entry.delete(0, tk.END)
    
    
    def login_success(self, user):
        # Called after successful login
        # Closes login window and passes user data to main app
        
        self.destroy()              # close the login window
        self.on_login_success(user) # call the main app with user data


# Test login window standalone
if __name__ == "__main__":
    def on_success(user):
        print(f"Logged in as: {user['name']}")
        print(f"Clearance: {user['clearance_level']}")
        print(f"Role: {user['role']}")
    
    app = LoginWindow(on_login_success=on_success)
    app.mainloop()