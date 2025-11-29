"""
EZ LightBurn Driver Switch v2.1
Automatically switches between EZCAD2 and LightBurn drivers for fiber lasers
Features: Auto-uninstall old driver, force install, configurable hardware ID
Author: William Sorensen (Christ Driven Geek)
Target: Windows 10/11 (Requires Administrator)
"""

import tkinter as tk
from tkinter import messagebox, filedialog
import subprocess
import ctypes
import sys
import os
import json
import threading
import time

# Configuration
CONFIG_FILE = "driver_paths.json"
DEFAULT_HARDWARE_ID = "VID_9588&PID_9899"
LIGHTBURN_DEFAULT_PATH = r"C:\Program Files\LightBurn\EzCad2Driver\EzCad2Driver.inf"


class EZLightBurnDriverSwitch:
    def __init__(self, root):
        self.root = root
        self.root.title("EZ LightBurn Driver Switch")
        self.root.geometry("560x480")
        self.root.resizable(False, False)
        
        # State variables
        self.config = {}
        self.current_driver = "Unknown"
        self.is_working = False
        
        # Load config or show setup
        if not self.load_config():
            self.show_setup_wizard()
        else:
            self.create_main_ui()
            # Small delay to allow UI to render before checking drivers
            self.root.after(300, self.detect_current_driver)
    
    def load_config(self):
        """Load and validate configuration."""
        if not os.path.exists(CONFIG_FILE):
            return False
        try:
            with open(CONFIG_FILE, 'r') as f:
                self.config = json.load(f)
            
            # Ensure all required keys exist
            required_keys = ['ezcad_driver', 'lightburn_driver', 'hardware_id', 'force_install']
            for key in required_keys:
                if key not in self.config:
                    if key == 'hardware_id':
                        self.config[key] = DEFAULT_HARDWARE_ID
                    elif key == 'force_install':
                        self.config[key] = True
                    else:
                        return False
            
            # Validate driver files exist
            if not os.path.exists(self.config['ezcad_driver']) or \
               not os.path.exists(self.config['lightburn_driver']):
                return False
                
            return True
        except Exception:
            return False

    def save_config(self):
        """Save configuration to JSON."""
        try:
            with open(CONFIG_FILE, 'w') as f:
                json.dump(self.config, f, indent=4)
            return True
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save config: {e}")
            return False

    def show_setup_wizard(self):
        """Display setup wizard for first-time configuration."""
        wizard = tk.Toplevel(self.root)
        wizard.title("EZ LightBurn Driver Switch - Setup")
        wizard.geometry("640x620")
        wizard.resizable(False, False)
        wizard.grab_set()
        
        # Title
        title_frame = tk.Frame(wizard, bg="#2c3e50", pady=15)
        title_frame.pack(fill=tk.X)
        tk.Label(
            title_frame,
            text="EZ LightBurn Driver Switch",
            font=("Segoe UI", 18, "bold"),
            bg="#2c3e50",
            fg="white"
        ).pack()
        tk.Label(
            title_frame,
            text="Configuration Wizard",
            font=("Segoe UI", 10),
            bg="#2c3e50",
            fg="#bdc3c7"
        ).pack()
        
        main_frame = tk.Frame(wizard, padx=20, pady=20)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Instructions
        tk.Label(
            main_frame,
            text="Configure the paths to your driver files.\n"
                 "These settings will be saved for future use.",
            font=("Segoe UI", 9),
            fg="gray",
            justify=tk.LEFT
        ).pack(pady=(0, 15))
        
        # EZCAD Driver
        ez_frame = tk.LabelFrame(main_frame, text="EZCAD2 Driver Location (.inf)", padx=10, pady=10)
        ez_frame.pack(fill=tk.X, pady=5)
        
        ez_var = tk.StringVar(value=self.config.get('ezcad_driver', ''))
        tk.Entry(ez_frame, textvariable=ez_var, width=55).pack(side=tk.LEFT, padx=(0, 5))
        tk.Button(ez_frame, text="Browse...", command=lambda: self.browse_file(ez_var, "EZCAD2")).pack(side=tk.LEFT)

        # LightBurn Driver
        lb_frame = tk.LabelFrame(main_frame, text="LightBurn Driver Location (.inf)", padx=10, pady=10)
        lb_frame.pack(fill=tk.X, pady=5)
        
        lb_var = tk.StringVar(value=self.config.get('lightburn_driver', ''))
        if not lb_var.get() and os.path.exists(LIGHTBURN_DEFAULT_PATH):
            lb_var.set(LIGHTBURN_DEFAULT_PATH)
        
        tk.Entry(lb_frame, textvariable=lb_var, width=55).pack(side=tk.LEFT, padx=(0, 5))
        tk.Button(lb_frame, text="Browse...", command=lambda: self.browse_file(lb_var, "LightBurn")).pack(side=tk.LEFT)
        
        if lb_var.get() == LIGHTBURN_DEFAULT_PATH:
            tk.Label(main_frame, text="✓ LightBurn driver auto-detected", font=("Segoe UI", 8), fg="green").pack(pady=(5, 10))

        # Advanced Options
        adv_frame = tk.LabelFrame(main_frame, text="Advanced Options", padx=10, pady=10)
        adv_frame.pack(fill=tk.X, pady=10)
        
        tk.Label(adv_frame, text="Hardware ID:", font=("Segoe UI", 9)).pack(anchor=tk.W)
        hw_var = tk.StringVar(value=self.config.get('hardware_id', DEFAULT_HARDWARE_ID))
        hw_entry = tk.Entry(adv_frame, textvariable=hw_var, width=45, font=("Consolas", 9))
        hw_entry.pack(anchor=tk.W, pady=(2, 8))
        
        tk.Label(
            adv_frame,
            text="Default: VID_9588&PID_9899 (Standard JCZ/BJJCZ boards)",
            font=("Segoe UI", 8),
            fg="gray"
        ).pack(anchor=tk.W, padx=5, pady=(0, 10))
        
        # Checkboxes
        force_var = tk.BooleanVar(value=self.config.get('force_install', True))
        force_check = tk.Checkbutton(
            adv_frame, 
            text="Force Install (Recommended for Windows 10/11)", 
            variable=force_var,
            font=("Segoe UI", 9)
        )
        force_check.pack(anchor=tk.W, pady=(5, 0))
        
        uninstall_var = tk.BooleanVar(value=self.config.get('uninstall_first', True))
        uninstall_check = tk.Checkbutton(
            adv_frame,
            text="Uninstall Old Driver First (Fixes switching issues)",
            variable=uninstall_var,
            font=("Segoe UI", 9),
            fg="blue"
        )
        uninstall_check.pack(anchor=tk.W, pady=(5, 0))
        
        tk.Label(
            adv_frame,
            text="Uninstalling first prevents Windows from reverting the driver change.",
            font=("Segoe UI", 8),
            fg="gray",
            wraplength=550,
            justify=tk.LEFT
        ).pack(anchor=tk.W, padx=5, pady=(5, 0))

        def save_wizard():
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
            self.config['uninstall_first'] = uninstall_var.get()
            
            if self.save_config():
                messagebox.showinfo("Success", "Configuration saved successfully!")
                wizard.destroy()
                self.create_main_ui()
                self.detect_current_driver()

        # Save button
        btn_frame = tk.Frame(main_frame)
        btn_frame.pack(pady=15)
        
        tk.Button(
            btn_frame,
            text="Save Settings",
            command=save_wizard,
            bg="#27ae60",
            fg="white",
            font=("Segoe UI", 11, "bold"),
            height=2,
            width=20,
            cursor="hand2"
        ).pack()
        
        # Center the wizard
        wizard.update_idletasks()
        x = (wizard.winfo_screenwidth() // 2) - (wizard.winfo_width() // 2)
        y = (wizard.winfo_screenheight() // 2) - (wizard.winfo_height() // 2)
        wizard.geometry(f"+{x}+{y}")

    def browse_file(self, var, driver_name):
        """Open file browser for .inf file selection."""
        f = filedialog.askopenfilename(
            title=f"Select {driver_name} Driver .inf File",
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
        header = tk.Frame(self.root, bg="#3498db", pady=20)
        header.pack(fill=tk.X)
        tk.Label(
            header,
            text="EZ LightBurn Driver Switch",
            font=("Segoe UI", 20, "bold"),
            bg="#3498db",
            fg="white"
        ).pack()
        tk.Label(
            header,
            text="Automatic Driver Switching for Fiber Lasers",
            font=("Segoe UI", 10),
            bg="#3498db",
            fg="#ecf0f1"
        ).pack(pady=(2, 0))
        
        # Status Frame
        status_container = tk.Frame(self.root)
        status_container.pack(pady=25, padx=20, fill=tk.X)
        
        # Current status
        self.status_lbl = tk.Label(
            status_container,
            text="Initializing...",
            font=("Segoe UI", 16, "bold"),
            pady=10
        )
        self.status_lbl.pack()
        
        # Status details
        self.detail_lbl = tk.Label(
            status_container,
            text="Checking laser connection...",
            font=("Segoe UI", 9),
            fg="#7f8c8d"
        )
        self.detail_lbl.pack()
        
        # Hardware ID info
        hw_id = self.config.get('hardware_id', DEFAULT_HARDWARE_ID)
        hw_label = tk.Label(
            status_container,
            text=f"Hardware ID: {hw_id}",
            font=("Consolas", 8),
            fg="#95a5a6"
        )
        hw_label.pack(pady=(5, 0))

        # Action Button
        button_frame = tk.Frame(self.root)
        button_frame.pack(pady=15)
        
        self.swap_btn = tk.Button(
            button_frame,
            text="Please Wait",
            command=self.start_swap_thread,
            font=("Segoe UI", 14, "bold"),
            width=25,
            height=2,
            state=tk.DISABLED,
            bd=0,
            cursor="hand2"
        )
        self.swap_btn.pack()
        
        # Feature indicators
        features_frame = tk.Frame(self.root)
        features_frame.pack(pady=10)
        
        features_text = "Auto-uninstall • Force Install • Admin Required"
        tk.Label(
            features_frame,
            text=features_text,
            font=("Segoe UI", 8),
            fg="#95a5a6"
        ).pack()
        
        # Footer
        footer_frame = tk.Frame(self.root)
        footer_frame.pack(side=tk.BOTTOM, pady=15)
        
        settings_btn = tk.Button(
            footer_frame,
            text="⚙ Settings",
            command=self.show_setup_wizard,
            relief=tk.FLAT,
            fg="#555",
            font=("Segoe UI", 9),
            cursor="hand2"
        )
        settings_btn.pack()
        
        tk.Label(
            footer_frame,
            text="v2.1 - Enhanced Driver Switching",
            font=("Segoe UI", 8),
            fg="#888"
        ).pack(pady=(5, 0))

    def detect_current_driver(self):
        """Detect the currently installed driver."""
        if self.is_working:
            return
        
        self.status_lbl.config(text="Detecting Driver...", fg="#2c3e50")
        self.detail_lbl.config(text="Querying Windows Device Manager...")
        
        # Run detection in background thread
        threading.Thread(target=self._detect_thread, daemon=True).start()

    def _detect_thread(self):
        """Run driver detection in background thread."""
        hw_id = self.config.get('hardware_id', DEFAULT_HARDWARE_ID)
        
        # PowerShell command to find the device and its service
        ps_cmd = f"""
        $device = Get-PnpDevice | Where-Object {{$_.HardwareID -like "*{hw_id}*"}}
        if ($device) {{
            $device.Status
            $device | Select-Object -ExpandProperty Service
        }} else {{
            "Not Found"
        }}
        """
        
        try:
            res = subprocess.run(
                ["powershell", "-Command", ps_cmd],
                capture_output=True,
                text=True,
                creationflags=subprocess.CREATE_NO_WINDOW,
                timeout=10
            )
            
            output = res.stdout.strip().split('\n')
            status = output[0] if output else "Unknown"
            service = output[1] if len(output) > 1 else ""
            
            self.root.after(0, lambda: self._update_ui_after_detect(status.lower(), service.lower()))
            
        except subprocess.TimeoutExpired:
            self.root.after(0, lambda: self._update_ui_after_detect("timeout", ""))
        except Exception as e:
            self.root.after(0, lambda: self._update_ui_after_detect("error", ""))

    def _update_ui_after_detect(self, status, service):
        """Update UI based on driver detection results."""
        if status == "timeout":
            self.current_driver = "Timeout"
            self.status_lbl.config(text="Detection Timeout", fg="#f39c12")
            self.detail_lbl.config(text="Try reconnecting your laser USB")
            self.swap_btn.config(
                text="Retry Detection",
                bg="#f39c12",
                fg="white",
                state=tk.NORMAL
            )
        elif status == "error" or status == "not found":
            self.current_driver = "Unknown"
            self.status_lbl.config(text="Laser Not Detected", fg="#e74c3c")
            self.detail_lbl.config(text="Ensure laser is powered ON and USB connected")
            self.swap_btn.config(
                text="Install EZCAD2 Driver",
                bg="#3498db",
                fg="white",
                state=tk.NORMAL
            )
        elif "winusb" in service or "usblmc" in service:
            self.current_driver = "LightBurn"
            self.status_lbl.config(text="LightBurn Driver Active", fg="#27ae60")
            self.detail_lbl.config(text="(WinUSB Protocol - Ready for LightBurn)")
            self.swap_btn.config(
                text="Switch to EZCAD2",
                bg="#3498db",
                fg="white",
                state=tk.NORMAL
            )
        elif "lmc" in service or "bjjcz" in service:
            self.current_driver = "EZCAD"
            self.status_lbl.config(text="EZCAD2 Driver Active", fg="#3498db")
            self.detail_lbl.config(text="(LMC Protocol - Ready for EZCAD2)")
            self.swap_btn.config(
                text="Switch to LightBurn",
                bg="#27ae60",
                fg="white",
                state=tk.NORMAL
            )
        else:
            self.current_driver = "Unknown"
            self.status_lbl.config(text="Unknown Driver", fg="#95a5a6")
            self.detail_lbl.config(text="Switching to EZCAD2 recommended")
            self.swap_btn.config(
                text="Install EZCAD2 Driver",
                bg="#3498db",
                fg="white",
                state=tk.NORMAL
            )

    def start_swap_thread(self):
        """Start the driver swap process."""
        if self.is_working:
            return
        
        self.is_working = True
        self.swap_btn.config(
            state=tk.DISABLED,
            text="Switching Driver...",
            bg="#95a5a6"
        )
        
        # Run swap process in background thread
        threading.Thread(target=self._swap_process, daemon=True).start()

    def _swap_process(self):
        """Execute the complete driver swap process."""
        try:
            hw_id = self.config.get('hardware_id', DEFAULT_HARDWARE_ID)
            uninstall_first = self.config.get('uninstall_first', True)
            
            # Find device instance ID
            device_cmd = f"""
            $device = Get-PnpDevice | Where-Object {{$_.HardwareID -like "*{hw_id}*"}}
            if ($device) {{
                $device.InstanceId
            }} else {{
                "Not Found"
            }}
            """
            
            try:
                res = subprocess.run(
                    ["powershell", "-Command", device_cmd],
                    capture_output=True,
                    text=True,
                    creationflags=subprocess.CREATE_NO_WINDOW,
                    timeout=10
                )
                device_instance = res.stdout.strip()
                
                if device_instance == "Not Found":
                    self.root.after(0, lambda: self._finish_swap(False, "Device not found. Ensure laser is connected."))
                    return
                    
            except Exception as e:
                self.root.after(0, lambda: self._finish_swap(False, f"Failed to find device: {str(e)}"))
                return
            
            # Step 1: Uninstall old driver if enabled
            if uninstall_first:
                self.root.after(0, lambda: self.detail_lbl.config(text="Uninstalling old driver..."))
                
                uninstall_cmd = f"""
                $device = Get-PnpDevice -InstanceId "{device_instance}"
                if ($device) {{
                    try {{
                        $device | Uninstall-PnpDevice -Confirm:$false
                        "Uninstall Success"
                    }} catch {{
                        "Uninstall Failed: $_"
                    }}
                }} else {{
                    "Device Not Found"
                }}
                """
                
                try:
                    res = subprocess.run(
                        ["powershell", "-Command", uninstall_cmd],
                        capture_output=True,
                        text=True,
                        creationflags=subprocess.CREATE_NO_WINDOW,
                        timeout=15
                    )
                    
                    if "Uninstall Success" not in res.stdout:
                        # Don't fail if uninstall fails, just continue
                        pass
                    
                    # Wait for Windows to process the uninstall
                    time.sleep(2)
                    
                except Exception:
                    # Continue even if uninstall fails
                    pass
            
            # Step 2: Install new driver
            if self.current_driver == "LightBurn":
                target_path = self.config['ezcad_driver']
                target_name = "EZCAD2"
            else:
                target_path = self.config['lightburn_driver']
                target_name = "LightBurn"
            
            self.root.after(0, lambda: self.detail_lbl.config(text=f"Installing {target_name} driver..."))
            
            # Build pnputil command
            cmd = ["pnputil", "/add-driver", target_path, "/install"]
            if self.config.get('force_install', True):
                cmd.append("/force")
            
            try:
                res = subprocess.run(
                    cmd,
                    capture_output=True,
                    text=True,
                    creationflags=subprocess.CREATE_NO_WINDOW,
                    timeout=30
                )
                
                # Check for success
                success = res.returncode == 0 or res.returncode == 3010
                log_msg = res.stdout if success else res.stderr
                
                if not success:
                    self.root.after(0, lambda: self._finish_swap(False, f"Driver installation failed:\n{log_msg}"))
                    return
                
                # Step 3: Scan for hardware changes
                self.root.after(0, lambda: self.detail_lbl.config(text="Scanning for hardware changes..."))
                
                try:
                    subprocess.run(
                        ["pnputil", "/scan-devices"],
                        capture_output=True,
                        creationflags=subprocess.CREATE_NO_WINDOW,
                        timeout=10
                    )
                except:
                    pass
                
                # Wait for Windows to detect the new driver
                time.sleep(2)
                
            except Exception as e:
                self.root.after(0, lambda: self._finish_swap(False, f"Installation error: {str(e)}"))
                return
            
            # Success!
            self.root.after(0, lambda: self._finish_swap(True, f"{target_name} driver installed successfully!"))
            
        except Exception as e:
            self.root.after(0, lambda: self._finish_swap(False, f"Unexpected error: {str(e)}"))

    def _finish_swap(self, success, message):
        """Handle completion of driver swap process."""
        self.is_working = False
        
        if success:
            messagebox.showinfo(
                "Success",
                f"{message}\n\n"
                "You may need to:\n"
                "• Reconnect your laser\n"
                "• Restart your laser software"
            )
        else:
            messagebox.showerror(
                "Driver Switch Failed",
                f"{message}\n\n"
                "Troubleshooting:\n"
                "• Ensure you're running as Administrator\n"
                "• Check laser USB connection\n"
                "• Try disconnecting/reconnecting laser"
            )
        
        # Re-detect driver status
        self.detect_current_driver()


if __name__ == "__main__":
    # Admin check and auto-elevation
    def is_admin():
        try:
            return ctypes.windll.shell32.IsUserAnAdmin()
        except:
            return False

    if is_admin():
        root = tk.Tk()
        app = EZLightBurnDriverSwitch(root)
        root.mainloop()
    else:
        # Relaunch with admin privileges
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