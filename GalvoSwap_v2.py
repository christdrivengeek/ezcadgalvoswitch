"""
GalvoSwap v2.0 - Driver Switcher for Fiber Lasers
Author: William Sorensen (Christ Driven Geek)
Target System: Windows 10/11 (Requires Admin)
Description: Switches between EZCAD2 (LMC) and LightBurn (WinUSB) drivers.

Improvements in v2.0:
- Threading to prevent UI freeze
- Force install by default (critical for Windows 10/11)
- CREATE_NO_WINDOW flag to prevent console flash
- Handles return code 3010 (reboot suggested) as success
- Configurable Hardware ID for different laser boards
- Better error messages and status indicators
- Cleaner, more modern UI
"""

import tkinter as tk
from tkinter import messagebox, filedialog
import subprocess
import ctypes
import sys
import os
import json
import threading

# --- CONFIGURATION DEFAULTS ---
CONFIG_FILE = "driver_paths.json"
# Standard ID for BJJCZ boards (ComMarker B4, Cloudray, Monport, etc.)
DEFAULT_HARDWARE_ID = "VID_9588&PID_9899" 
LIGHTBURN_DEFAULT_PATH = r"C:\Program Files\LightBurn\EzCad2Driver\EzCad2Driver.inf"


class GalvoSwap:
    def __init__(self, root):
        self.root = root
        self.root.title("GalvoSwap v2.0 - Driver Switcher")
        self.root.geometry("540x440")
        self.root.resizable(False, False)
        
        # Data State
        self.config = {}
        self.current_driver = "Unknown"
        self.is_working = False
        
        # Load config; if missing or invalid, show wizard
        if not self.load_config():
            self.show_setup_wizard()
        else:
            self.create_main_ui()
            # Small delay to allow UI to render before checking drivers
            self.root.after(200, self.detect_current_driver)
    
    def load_config(self):
        """Loads and validates configuration from JSON."""
        if not os.path.exists(CONFIG_FILE):
            return False
        try:
            with open(CONFIG_FILE, 'r') as f:
                self.config = json.load(f)
            
            # Ensure all keys exist (backward compatibility for older json files)
            if 'hardware_id' not in self.config:
                self.config['hardware_id'] = DEFAULT_HARDWARE_ID
            if 'force_install' not in self.config:
                self.config['force_install'] = True  # Default to True for Windows 10/11

            # Validate file existence
            if not os.path.exists(self.config.get('ezcad_driver', '')) or \
               not os.path.exists(self.config.get('lightburn_driver', '')):
                return False
            return True
        except Exception:
            return False

    def save_config(self):
        """Writes configuration to JSON."""
        try:
            with open(CONFIG_FILE, 'w') as f:
                json.dump(self.config, f, indent=4)
            return True
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save config: {e}")
            return False

    def show_setup_wizard(self):
        """First-time setup or Settings menu."""
        wizard = tk.Toplevel(self.root)
        wizard.title("GalvoSwap - Setup")
        wizard.geometry("620x580")
        wizard.resizable(False, False)
        wizard.grab_set()  # Modal window
        
        # Title
        tk.Label(
            wizard, 
            text="Driver Configuration", 
            font=("Segoe UI", 16, "bold")
        ).pack(pady=15)
        
        # Instructions
        tk.Label(
            wizard,
            text="Configure the paths to your EZCAD2 and LightBurn driver files.\n"
                 "These settings will be saved for future use.",
            font=("Segoe UI", 9),
            fg="gray",
            justify=tk.LEFT
        ).pack(padx=20, pady=(0, 10))
        
        # --- EZCAD Section ---
        f1 = tk.LabelFrame(wizard, text="EZCAD2 Driver Location (.inf)", padx=10, pady=10)
        f1.pack(fill=tk.X, padx=20, pady=5)
        
        ez_var = tk.StringVar(value=self.config.get('ezcad_driver', ''))
        tk.Entry(f1, textvariable=ez_var, width=55).pack(side=tk.LEFT, padx=(0, 5))
        tk.Button(
            f1, 
            text="Browse...", 
            command=lambda: self.browse_file(ez_var)
        ).pack(side=tk.LEFT)

        # --- LightBurn Section ---
        f2 = tk.LabelFrame(wizard, text="LightBurn Driver Location (.inf)", padx=10, pady=10)
        f2.pack(fill=tk.X, padx=20, pady=5)
        
        lb_var = tk.StringVar(value=self.config.get('lightburn_driver', ''))
        # Auto-fill default if empty
        if not lb_var.get() and os.path.exists(LIGHTBURN_DEFAULT_PATH):
            lb_var.set(LIGHTBURN_DEFAULT_PATH)
        
        tk.Entry(f2, textvariable=lb_var, width=55).pack(side=tk.LEFT, padx=(0, 5))
        tk.Button(
            f2, 
            text="Browse...", 
            command=lambda: self.browse_file(lb_var)
        ).pack(side=tk.LEFT)
        
        # Auto-detect indicator
        if lb_var.get() == LIGHTBURN_DEFAULT_PATH:
            tk.Label(
                wizard,
                text="✓ LightBurn driver auto-detected",
                font=("Segoe UI", 8),
                fg="green"
            ).pack(pady=(2, 0))

        # --- Advanced Section ---
        f3 = tk.LabelFrame(wizard, text="Advanced Options", padx=10, pady=10)
        f3.pack(fill=tk.X, padx=20, pady=10)
        
        tk.Label(
            f3, 
            text="Hardware ID (Check Device Manager if your laser doesn't detect):",
            font=("Segoe UI", 9)
        ).pack(anchor=tk.W)
        
        hw_var = tk.StringVar(value=self.config.get('hardware_id', DEFAULT_HARDWARE_ID))
        hw_entry = tk.Entry(f3, textvariable=hw_var, width=45, font=("Consolas", 9))
        hw_entry.pack(anchor=tk.W, pady=(2, 10))
        
        tk.Label(
            f3,
            text="Default: VID_9588&PID_9899 (Standard JCZ/BJJCZ boards)",
            font=("Segoe UI", 8),
            fg="gray"
        ).pack(anchor=tk.W, padx=20)
        
        # Force install option
        force_var = tk.BooleanVar(value=self.config.get('force_install', True))
        force_check = tk.Checkbutton(
            f3, 
            text="Force Install (Recommended for Windows 10/11)", 
            variable=force_var,
            font=("Segoe UI", 9)
        )
        force_check.pack(anchor=tk.W, pady=(10, 0))
        
        tk.Label(
            f3,
            text="This adds the /force flag to pnputil. Enable if Windows refuses to switch drivers.",
            font=("Segoe UI", 8),
            fg="gray",
            wraplength=550,
            justify=tk.LEFT
        ).pack(anchor=tk.W, padx=20, pady=(2, 0))

        def save_wiz():
            # Validation
            if not os.path.exists(ez_var.get()):
                messagebox.showerror("Error", "EZCAD2 driver file not found.\n\nPlease select a valid .inf file.")
                return
            if not os.path.exists(lb_var.get()):
                messagebox.showerror("Error", "LightBurn driver file not found.\n\nPlease select a valid .inf file.")
                return
            if not hw_var.get().strip():
                messagebox.showerror("Error", "Hardware ID cannot be empty.")
                return
            
            # Save configuration
            self.config['ezcad_driver'] = ez_var.get()
            self.config['lightburn_driver'] = lb_var.get()
            self.config['hardware_id'] = hw_var.get().strip()
            self.config['force_install'] = force_var.get()
            
            if self.save_config():
                messagebox.showinfo("Success", "Configuration saved successfully!")
                wizard.destroy()
                self.create_main_ui()
                self.detect_current_driver()

        # Save button
        tk.Button(
            wizard, 
            text="Save Settings", 
            command=save_wiz, 
            bg="#0078D7", 
            fg="white", 
            font=("Segoe UI", 11, "bold"), 
            height=2, 
            width=20,
            cursor="hand2"
        ).pack(pady=20)
        
        # Center the wizard
        wizard.update_idletasks()
        x = (wizard.winfo_screenwidth() // 2) - (wizard.winfo_width() // 2)
        y = (wizard.winfo_screenheight() // 2) - (wizard.winfo_height() // 2)
        wizard.geometry(f"+{x}+{y}")

    def browse_file(self, var):
        """Open file browser for .inf file selection."""
        f = filedialog.askopenfilename(
            title="Select Driver .inf File", 
            filetypes=[("Driver Info Files", "*.inf"), ("All Files", "*.*")]
        )
        if f:
            var.set(f)

    def create_main_ui(self):
        """Create the main application interface."""
        # Clear existing widgets
        for w in self.root.winfo_children():
            w.destroy()
        
        # Header
        header = tk.Frame(self.root, bg="#2c3e50", pady=20)
        header.pack(fill=tk.X)
        
        tk.Label(
            header, 
            text="GalvoSwap", 
            font=("Segoe UI", 20, "bold"), 
            bg="#2c3e50", 
            fg="white"
        ).pack()
        
        tk.Label(
            header, 
            text="Driver Switcher for EZCAD2 & LightBurn", 
            font=("Segoe UI", 10), 
            bg="#2c3e50", 
            fg="#bdc3c7"
        ).pack(pady=(2, 0))
        
        # Status Area
        status_frame = tk.Frame(self.root)
        status_frame.pack(pady=30)
        
        self.status_lbl = tk.Label(
            status_frame, 
            text="Initializing...", 
            font=("Segoe UI", 14, "bold")
        )
        self.status_lbl.pack()
        
        self.detail_lbl = tk.Label(
            status_frame, 
            text="Checking laser connection...", 
            font=("Segoe UI", 9), 
            fg="gray"
        )
        self.detail_lbl.pack(pady=(5, 0))

        # Action Button
        self.swap_btn = tk.Button(
            self.root, 
            text="Please Wait", 
            command=self.start_swap_thread, 
            font=("Segoe UI", 14, "bold"), 
            width=25, 
            height=2, 
            state=tk.DISABLED,
            bd=0,
            cursor="hand2"
        )
        self.swap_btn.pack(pady=10)
        
        # Footer
        footer_frame = tk.Frame(self.root)
        footer_frame.pack(side=tk.BOTTOM, pady=15)
        
        tk.Button(
            footer_frame, 
            text="⚙ Settings", 
            command=self.show_setup_wizard, 
            relief=tk.FLAT, 
            fg="#555",
            font=("Segoe UI", 9),
            cursor="hand2"
        ).pack()
        
        tk.Label(
            footer_frame,
            text="v2.0 - For ComMarker B4 & JCZ Controllers",
            font=("Segoe UI", 8),
            fg="#888"
        ).pack(pady=(5, 0))

    def detect_current_driver(self):
        """Detect the currently installed driver."""
        if self.is_working:
            return
        self.status_lbl.config(text="Checking Driver Status...", fg="black")
        self.detail_lbl.config(text="Querying Windows device manager...")
        # Run detection in thread to avoid UI lag
        threading.Thread(target=self._detect_thread, daemon=True).start()

    def _detect_thread(self):
        """Run driver detection in background thread."""
        hw_id = self.config.get('hardware_id', DEFAULT_HARDWARE_ID)
        
        # PowerShell command to identify the active service for the USB device
        cmd = f"Get-PnpDevice | Where-Object {{$_.HardwareID -like '*{hw_id}*'}} | Select-Object -ExpandProperty Service"
        
        try:
            # CREATE_NO_WINDOW prevents black console flash
            res = subprocess.run(
                ["powershell", "-Command", cmd], 
                capture_output=True, 
                text=True, 
                creationflags=subprocess.CREATE_NO_WINDOW,
                timeout=10
            )
            svc = res.stdout.strip().lower()
            self.root.after(0, lambda: self._update_ui_after_detect(svc))
        except subprocess.TimeoutExpired:
            self.root.after(0, lambda: self._update_ui_after_detect("timeout"))
        except Exception:
             self.root.after(0, lambda: self._update_ui_after_detect("error"))

    def _update_ui_after_detect(self, svc):
        """Update UI based on driver detection results."""
        if svc == "timeout":
            self.current_driver = "Timeout"
            self.status_lbl.config(text="Detection Timeout", fg="#ff9800")  # Orange
            self.detail_lbl.config(text="Try reconnecting your laser")
            self.swap_btn.config(
                text="Retry Detection", 
                bg="#ff9800", 
                fg="white", 
                state=tk.NORMAL
            )
        elif svc == "error":
            self.current_driver = "Error"
            self.status_lbl.config(text="Detection Error", fg="#f44336")  # Red
            self.detail_lbl.config(text="Ensure laser is powered ON and USB connected")
            self.swap_btn.config(
                text="Retry Detection", 
                bg="#f44336", 
                fg="white", 
                state=tk.NORMAL
            )
        elif "winusb" in svc or "usblmc" in svc:
            self.current_driver = "LightBurn"
            self.status_lbl.config(text="Active: LightBurn Driver", fg="#4CAF50")  # Green
            self.detail_lbl.config(text="(WinUSB Protocol Active)")
            self.swap_btn.config(
                text="Switch to EZCAD", 
                bg="#2196F3", 
                fg="white", 
                state=tk.NORMAL
            )
        elif "lmc" in svc or "bjjcz" in svc:
            self.current_driver = "EZCAD"
            self.status_lbl.config(text="Active: EZCAD2 Driver", fg="#2196F3")  # Blue
            self.detail_lbl.config(text="(LMC V4/V2 Protocol Active)")
            self.swap_btn.config(
                text="Switch to LightBurn", 
                bg="#4CAF50", 
                fg="white", 
                state=tk.NORMAL
            )
        else:
            self.current_driver = "Unknown"
            self.status_lbl.config(text="Laser Not Detected", fg="#f44336")  # Red
            self.detail_lbl.config(text="Ensure laser is powered ON and USB is connected")
            self.swap_btn.config(
                text="Attempt Install Anyway", 
                bg="gray", 
                fg="white", 
                state=tk.NORMAL
            )

    def start_swap_thread(self):
        """Start the driver swap process in a separate thread."""
        if self.is_working:
            return  # Prevent multiple simultaneous swaps
        
        self.is_working = True
        self.swap_btn.config(
            state=tk.DISABLED, 
            text="Installing... Please Wait", 
            bg="#666"
        )
        
        # Run swap process in background thread
        threading.Thread(target=self._swap_process, daemon=True).start()

    def _swap_process(self):
        """Execute the driver swap process."""
        # Determine which file we need
        if self.current_driver == "EZCAD":
            target_path = self.config['lightburn_driver']
            target_name = "LightBurn"
        elif self.current_driver == "LightBurn":
            target_path = self.config['ezcad_driver']
            target_name = "EZCAD2"
        else:
            # Default to EZCAD if currently Unknown/Error/Timeout
            target_path = self.config['ezcad_driver']
            target_name = "EZCAD2"
        
        # Build command
        cmd = ["pnputil", "/add-driver", target_path, "/install"]
        if self.config.get('force_install', True):
            cmd.append("/force")
        
        try:
            # CREATE_NO_WINDOW prevents black console flash
            res = subprocess.run(
                cmd, 
                capture_output=True, 
                text=True, 
                creationflags=subprocess.CREATE_NO_WINDOW,
                timeout=30
            )
            
            # 0 = Success, 3010 = Success (Reboot required, but usually fine for USB)
            success = (res.returncode == 0 or res.returncode == 3010)
            log_msg = res.stdout if success else res.stderr
            
        except subprocess.TimeoutExpired:
            success = False
            log_msg = "Driver installation timed out (30 seconds)"
        except Exception as e:
            success = False
            log_msg = str(e)
            
        # Update UI from main thread
        self.root.after(0, lambda: self._finish_swap(success, log_msg, target_name))

    def _finish_swap(self, success, log, target_name):
        """Handle completion of driver swap."""
        self.is_working = False
        
        if success:
            messagebox.showinfo(
                "Success", 
                f"{target_name} driver installed successfully!\n\n"
                "You may need to reconnect your laser."
            )
        else:
            messagebox.showerror(
                "Failed", 
                f"Driver installation failed.\n\n"
                f"Error details:\n{log}\n\n"
                "Ensure you're running as Administrator."
            )
        
        # Re-detect driver status
        self.detect_current_driver()


if __name__ == "__main__":
    # Robust Admin Check
    def is_admin():
        try:
            return ctypes.windll.shell32.IsUserAnAdmin()
        except:
            return False

    if is_admin():
        root = tk.Tk()
        app = GalvoSwap(root)
        root.mainloop()
    else:
        # Relaunch as Admin (Handles both .py and compiled .exe)
        if getattr(sys, 'frozen', False):
            # Running as compiled executable
            ctypes.windll.shell32.ShellExecuteW(
                None, "runas", sys.executable, 
                " ".join(sys.argv[1:]), None, 1
            )
        else:
            # Running as Python script
            ctypes.windll.shell32.ShellExecuteW(
                None, "runas", sys.executable, 
                " ".join(sys.argv), None, 1
            )
        sys.exit()