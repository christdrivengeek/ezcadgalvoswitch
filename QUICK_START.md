# GalvoSwap - Quick Start Guide

## For End Users (Using the .exe)

### 1. Download
- Get `GalvoSwap.exe`

### 2. Run as Administrator
- **Right-click** `GalvoSwap.exe`
- Select **"Run as Administrator"**
- Click **"Yes"** when prompted

### 3. First-Time Setup
- Browse to your **EZCAD2 driver .inf file**
- Browse to your **LightBurn driver .inf file** (or use auto-detected path)
- Click **"Save Configuration"**

### 4. Switch Drivers
- Click the big button to switch drivers
- Confirm the action
- Wait for completion
- Reconnect your laser

**That's it!** 🎉

---

## For Developers (Building from Source)

### 1. Install PyInstaller
```bash
pip install pyinstaller
```

### 2. Build the Executable
```bash
pyinstaller --onefile --noconsole --name=GalvoSwap GalvoSwap.py
```

### 3. Find Your Executable
```
dist/GalvoSwap.exe
```

### 4. Distribute
Share the `GalvoSwap.exe` file with users.

---

## Common Issues

### "Administrator Privileges Required"
→ Right-click and select "Run as Administrator"

### "Driver Installation Failed"
→ Check that driver paths are correct in Settings

### "Driver Not Detected"
→ Ensure your laser is connected and recognized by Windows

---

## Need More Help?

- See `README.md` for detailed documentation
- See `USAGE_GUIDE.md` for step-by-step instructions
- See `BUILD_INSTRUCTIONS.md` for advanced build options

---

**Hardware ID:** VID_9588&PID_9899  
**Supported OS:** Windows 7, 8, 10, 11  
**Required:** Administrator privileges