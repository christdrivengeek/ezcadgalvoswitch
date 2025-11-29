"""
GalvoSwap - Galvo Laser Driver Switcher
Allows users to switch between EZCAD2 and LightBurn drivers with a single click.
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import subprocess
import ctypes
import sys
import os
import json
import re

# Configuration file path
CONFIG_FILE = "driver_paths.json"
HARDWARE_ID = "VID_9588&PID_9899"
LIGHTBURN_DEFAULT_PATH = r"C:\Program Files\LightBurn\EzCad2Driver\EzCad2Driver.inf"


class GalvoSwap:
    def __init__(self, root):
        self.root = root
        self.root.title("GalvoSwap - Galvo Driver Switcher")
        self.root.geometry("500x350")
        self.root.resizable(False, False)
        
        # Configuration
        self.config = {}
        self.current_driver = "Unknown"
        
        # Load or create configuration
        if not self.load_config():
            self.show_setup_wizard()
        else:
            self.create_main_ui()
            self.detect_current_driver()
    
    def is_admin(self):
        """Check if the application is running with administrator privileges."""
        try:
            return ctypes.windll.shell32.IsUserAnAdmin()
        except:
            return False
    
    def restart_as_admin(self):
        """Restart the application with administrator privileges."""
        try:
            if sys.argv[0].endswith('.py'):
                # Running as Python script
                ctypes.windll.shell32.ShellExecuteW(
                    None, "runas", sys.executable, f'"{sys.argv[0]}"', None, 1
                )
            else:
                # Running as compiled executable
                ctypes.windll.shell32.ShellExecuteW(
                    None, "runas", sys.executable, " ".join(sys.argv), None, 1
                )
            sys.exit(0)
        except Exception as e:
            messagebox.showerror(
                "Error",
                f"Failed to restart with admin privileges:\n{str(e)}\n\n"
                "Please run this application as Administrator manually."
            )
            sys.exit(1)
    
    def load_config(self):
        """Load configuration from JSON file."""
        if not os.path.exists(CONFIG_FILE):
            return False
        
        try:
            with open(CONFIG_FILE, 'r') as f:
                self.config = json.load(f)
            
            # Validate configuration
            if 'ezcad_driver' not in self.config or 'lightburn_driver' not in self.config:
                return False
            
            # Check if files exist
            if not os.path.exists(self.config['ezcad_driver']) or \
               not os.path.exists(self.config['lightburn_driver']):
                messagebox.showwarning(
                    "Configuration Error",
                    "One or more driver paths in the configuration are invalid.\n"
                    "Please reconfigure the driver paths."
                )
                return False
            
            return True
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load configuration:\n{str(e)}")
            return False
    
    def save_config(self):
        """Save configuration to JSON file."""
        try:
            with open(CONFIG_FILE, 'w') as f:
                json.dump(self.config, f, indent=4)
            return True
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save configuration:\n{str(e)}")
            return False
    
    def show_setup_wizard(self):
        """Display the setup wizard for first-time configuration."""
        wizard = tk.Toplevel(self.root)
        wizard.title("GalvoSwap - Setup Wizard")
        wizard.geometry("600x400")
        wizard.resizable(False, False)
        wizard.grab_set()
        
        # Title
        title_label = tk.Label(
            wizard,
            text="Welcome to GalvoSwap Setup",
            font=("Arial", 16, "bold")
        )
        title_label.pack(pady=20)
        
        # Instructions
        instructions = tk.Label(
            wizard,
            text="Please select the driver .inf files for both EZCAD2 and LightBurn.\n"
                 "These files are required to switch between drivers.",
            font=("Arial", 10),
            justify=tk.LEFT
        )
        instructions.pack(pady=10, padx=20)
        
        # EZCAD Driver Selection
        ezcad_frame = tk.LabelFrame(wizard, text="EZCAD2 Driver", padx=10, pady=10)
        ezcad_frame.pack(fill=tk.X, padx=20, pady=10)
        
        self.ezcad_path_var = tk.StringVar()
        ezcad_entry = tk.Entry(ezcad_frame, textvariable=self.ezcad_path_var, width=50)
        ezcad_entry.pack(side=tk.LEFT, padx=5)
        
        ezcad_browse_btn = tk.Button(
            ezcad_frame,
            text="Browse...",
            command=lambda: self.browse_driver_file(self.ezcad_path_var, "EZCAD2")
        )
        ezcad_browse_btn.pack(side=tk.LEFT)
        
        # LightBurn Driver Selection
        lightburn_frame = tk.LabelFrame(wizard, text="LightBurn Driver", padx=10, pady=10)
        lightburn_frame.pack(fill=tk.X, padx=20, pady=10)
        
        self.lightburn_path_var = tk.StringVar()
        
        # Try to auto-detect LightBurn driver
        if os.path.exists(LIGHTBURN_DEFAULT_PATH):
            self.lightburn_path_var.set(LIGHTBURN_DEFAULT_PATH)
        
        lightburn_entry = tk.Entry(lightburn_frame, textvariable=self.lightburn_path_var, width=50)
        lightburn_entry.pack(side=tk.LEFT, padx=5)
        
        lightburn_browse_btn = tk.Button(
            lightburn_frame,
            text="Browse...",
            command=lambda: self.browse_driver_file(self.lightburn_path_var, "LightBurn")
        )
        lightburn_browse_btn.pack(side=tk.LEFT)
        
        # Auto-detect message
        if os.path.exists(LIGHTBURN_DEFAULT_PATH):
            auto_detect_label = tk.Label(
                wizard,
                text="✓ LightBurn driver auto-detected",
                font=("Arial", 9),
                fg="green"
            )
            auto_detect_label.pack(pady=5)
        
        # Save button
        save_btn = tk.Button(
            wizard,
            text="Save Configuration",
            command=lambda: self.save_wizard_config(wizard),
            bg="#4CAF50",
            fg="white",
            font=("Arial", 12, "bold"),
            padx=20,
            pady=10
        )
        save_btn.pack(pady=20)
        
        # Center the wizard window
        wizard.update_idletasks()
        x = (wizard.winfo_screenwidth() // 2) - (wizard.winfo_width() // 2)
        y = (wizard.winfo_screenheight() // 2) - (wizard.winfo_height() // 2)
        wizard.geometry(f"+{x}+{y}")
    
    def browse_driver_file(self, path_var, driver_name):
        """Open file browser to select driver .inf file."""
        filename = filedialog.askopenfilename(
            title=f"Select {driver_name} Driver .inf File",
            filetypes=[("Driver Files", "*.inf"), ("All Files", "*.*")]
        )
        if filename:
            path_var.set(filename)
    
    def save_wizard_config(self, wizard):
        """Save configuration from setup wizard."""
        ezcad_path = self.ezcad_path_var.get().strip()
        lightburn_path = self.lightburn_path_var.get().strip()
        
        # Validate paths
        if not ezcad_path or not lightburn_path:
            messagebox.showerror("Error", "Please select both driver files.")
            return
        
        if not os.path.exists(ezcad_path):
            messagebox.showerror("Error", f"EZCAD2 driver file not found:\n{ezcad_path}")
            return
        
        if not os.path.exists(lightburn_path):
            messagebox.showerror("Error", f"LightBurn driver file not found:\n{lightburn_path}")
            return
        
        # Save configuration
        self.config = {
            'ezcad_driver': ezcad_path,
            'lightburn_driver': lightburn_path
        }
        
        if self.save_config():
            messagebox.showinfo("Success", "Configuration saved successfully!")
            wizard.destroy()
            self.create_main_ui()
            self.detect_current_driver()
    
    def create_main_ui(self):
        """Create the main user interface."""
        # Clear any existing widgets
        for widget in self.root.winfo_children():
            widget.destroy()
        
        # Title
        title_label = tk.Label(
            self.root,
            text="Galvo Driver Swapper",
            font=("Arial", 18, "bold"),
            bg="#2196F3",
            fg="white",
            pady=15
        )
        title_label.pack(fill=tk.X)
        
        # Status Frame
        status_frame = tk.Frame(self.root, pady=20)
        status_frame.pack(fill=tk.X)
        
        status_title = tk.Label(
            status_frame,
            text="Current Driver Status:",
            font=("Arial", 12)
        )
        status_title.pack()
        
        self.status_label = tk.Label(
            status_frame,
            text="Detecting...",
            font=("Arial", 14, "bold"),
            fg="gray"
        )
        self.status_label.pack(pady=5)
        
        # Main Swap Button
        self.swap_button = tk.Button(
            self.root,
            text="Detecting Driver...",
            command=self.swap_driver,
            bg="#4CAF50",
            fg="white",
            font=("Arial", 14, "bold"),
            padx=30,
            pady=20,
            state=tk.DISABLED
        )
        self.swap_button.pack(pady=30)
        
        # Settings Button
        settings_btn = tk.Button(
            self.root,
            text="⚙ Settings",
            command=self.show_setup_wizard,
            bg="#757575",
            fg="white",
            font=("Arial", 10),
            padx=15,
            pady=5
        )
        settings_btn.pack(pady=10)
        
        # Info Label
        info_label = tk.Label(
            self.root,
            text="Note: Administrator privileges required for driver swapping",
            font=("Arial", 8),
            fg="gray"
        )
        info_label.pack(side=tk.BOTTOM, pady=10)
        
        # Center the window
        self.root.update_idletasks()
        x = (self.root.winfo_screenwidth() // 2) - (self.root.winfo_width() // 2)
        y = (self.root.winfo_screenheight() // 2) - (self.root.winfo_height() // 2)
        self.root.geometry(f"+{x}+{y}")
    
    def detect_current_driver(self):
        """Detect the currently installed driver for the hardware ID."""
        try:
            # Use PowerShell to query the driver information
            ps_command = f'''
            Get-PnpDevice | Where-Object {{$_.HardwareID -like "*{HARDWARE_ID}*"}} | 
            Select-Object -ExpandProperty Service
            '''
            
            result = subprocess.run(
                ["powershell", "-Command", ps_command],
                capture_output=True,
                text=True,
                timeout=10
            )
            
            service_name = result.stdout.strip().lower()
            
            # Determine driver based on service name
            if "winusb" in service_name or "usblmc" in service_name:
                self.current_driver = "LightBurn"
                self.status_label.config(text="LightBurn Driver", fg="green")
                self.swap_button.config(
                    text="Switch to EZCAD2",
                    bg="#FF9800",
                    state=tk.NORMAL
                )
            elif "lmc" in service_name or "bjjcz" in service_name or service_name:
                self.current_driver = "EZCAD"
                self.status_label.config(text="EZCAD2 Driver", fg="blue")
                self.swap_button.config(
                    text="Switch to LightBurn",
                    bg="#2196F3",
                    state=tk.NORMAL
                )
            else:
                self.current_driver = "Unknown"
                self.status_label.config(text="Driver Not Detected", fg="red")
                self.swap_button.config(
                    text="Install Driver",
                    bg="#9E9E9E",
                    state=tk.NORMAL
                )
        
        except subprocess.TimeoutExpired:
            messagebox.showerror("Error", "Driver detection timed out.")
            self.status_label.config(text="Detection Failed", fg="red")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to detect driver:\n{str(e)}")
            self.status_label.config(text="Detection Error", fg="red")
    
    def swap_driver(self):
        """Swap the driver to the opposite one."""
        # Determine target driver
        if self.current_driver == "LightBurn":
            target_driver = "EZCAD2"
            target_path = self.config['ezcad_driver']
        elif self.current_driver == "EZCAD":
            target_driver = "LightBurn"
            target_path = self.config['lightburn_driver']
        else:
            # Unknown state - ask user which driver to install
            response = messagebox.askyesno(
                "Select Driver",
                "Current driver is unknown.\n\n"
                "Yes = Install EZCAD2\n"
                "No = Install LightBurn"
            )
            if response:
                target_driver = "EZCAD2"
                target_path = self.config['ezcad_driver']
            else:
                target_driver = "LightBurn"
                target_path = self.config['lightburn_driver']
        
        # Confirm action
        confirm = messagebox.askyesno(
            "Confirm Driver Swap",
            f"Are you sure you want to switch to {target_driver} driver?\n\n"
            "This will replace the current driver."
        )
        
        if not confirm:
            return
        
        # Disable button during operation
        self.swap_button.config(state=tk.DISABLED, text="Swapping Driver...")
        self.root.update()
        
        try:
            # Run pnputil command to install driver
            command = ["pnputil", "/add-driver", target_path, "/install"]
            
            result = subprocess.run(
                command,
                capture_output=True,
                text=True,
                timeout=30
            )
            
            if result.returncode == 0:
                messagebox.showinfo(
                    "Success",
                    f"Successfully switched to {target_driver} driver!\n\n"
                    "Please reconnect your device if necessary."
                )
                # Refresh driver status
                self.detect_current_driver()
            else:
                error_msg = result.stderr if result.stderr else result.stdout
                messagebox.showerror(
                    "Driver Installation Failed",
                    f"Failed to install {target_driver} driver.\n\n"
                    f"Error: {error_msg}\n\n"
                    "Make sure you're running as Administrator."
                )
                self.swap_button.config(state=tk.NORMAL)
        
        except subprocess.TimeoutExpired:
            messagebox.showerror("Error", "Driver installation timed out.")
            self.swap_button.config(state=tk.NORMAL)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to swap driver:\n{str(e)}")
            self.swap_button.config(state=tk.NORMAL)


def main():
    """Main entry point for the application."""
    # Check for admin privileges
    try:
        is_admin = ctypes.windll.shell32.IsUserAnAdmin()
    except:
        is_admin = False
    
    if not is_admin:
        # Show warning and attempt to restart with admin privileges
        root = tk.Tk()
        root.withdraw()
        
        response = messagebox.askyesno(
            "Administrator Privileges Required",
            "GalvoSwap requires Administrator privileges to swap drivers.\n\n"
            "Would you like to restart with Administrator privileges?"
        )
        
        if response:
            try:
                if sys.argv[0].endswith('.py'):
                    # Running as Python script
                    ctypes.windll.shell32.ShellExecuteW(
                        None, "runas", sys.executable, f'"{sys.argv[0]}"', None, 1
                    )
                else:
                    # Running as compiled executable
                    ctypes.windll.shell32.ShellExecuteW(
                        None, "runas", sys.executable, " ".join(sys.argv), None, 1
                    )
            except Exception as e:
                messagebox.showerror(
                    "Error",
                    f"Failed to restart with admin privileges:\n{str(e)}\n\n"
                    "Please run this application as Administrator manually."
                )
        
        sys.exit(0)
    
    # Create and run the application
    root = tk.Tk()
    app = GalvoSwap(root)
    root.mainloop()


if __name__ == "__main__":
    main()