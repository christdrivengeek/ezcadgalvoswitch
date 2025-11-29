# 🪟 Building GalvoSwap.exe on Windows

## ⚠️ Important Note

The Linux environment cannot create Windows executables. You **must run the build process on Windows** to get a working .exe file for your ComMarker B4 laser.

## 🛠️ Windows Build Instructions

### Method 1: Quick Build (Recommended)

1. **Install Python** (if not already installed)
   - Download from [python.org](https://python.org)
   - Version 3.6 or later
   - Check "Add Python to PATH" during installation

2. **Install PyInstaller**
   ```cmd
   pip install pyinstaller
   ```

3. **Download the files**
   - Copy `GalvoSwap_v2.py` to your Windows machine
   - (Optional) Copy `BUILD_WINDOWS_EXE.py`

4. **Build the executable**
   
   **Option A: Direct Command**
   ```cmd
   pyinstaller --onefile --noconsole --name=GalvoSwap GalvoSwap_v2.py
   ```
   
   **Option B: Using Build Script**
   ```cmd
   python BUILD_WINDOWS_EXE.py
   ```

5. **Find your executable**
   - Location: `dist\GalvoSwap.exe`
   - This is the file to distribute and use!

### Method 2: Alternative Command

If you encounter issues, try this command:
```cmd
pyinstaller --onefile --windowed --name=GalvoSwap --clean GalvoSwap_v2.py
```

## 📁 What You'll Get

After successful build, you'll have:
```
your-folder\
├── dist\
│   └── GalvoSwap.exe  ⭐ THIS IS WHAT YOU NEED
├── build\              (temporary files, can delete)
├── GalvoSwap_v2.spec   (can delete)
└── other files...
```

## 🚀 Using GalvoSwap.exe

### First Time Setup:
1. **Right-click** `GalvoSwap.exe`
2. Select **"Run as Administrator"**
3. Click **"Yes"** to the UAC prompt
4. Complete the setup wizard:
   - Browse to your EZCAD2 driver .inf file
   - Browse to your LightBurn driver .inf file
   - Hardware ID should be: `VID_9588&PID_9899`
   - Enable "Force Install" (recommended)
5. Click "Save Settings"

### Daily Use:
1. Run as Administrator
2. Click the big button to switch drivers
3. Wait for completion
4. Reconnect your laser

## 🔧 Troubleshooting Windows Build

### "PyInstaller not found"
```cmd
pip install --upgrade pyinstaller
```

### "Python not recognized"
- Make sure Python is installed and added to PATH
- Restart Command Prompt after installation

### Antivirus warnings
- PyInstaller executables sometimes trigger false positives
- Add an exception in your antivirus during testing
- For distribution, consider code signing

### Build fails with errors
- Try the alternative command above
- Make sure you're using Python 3.6+
- Run Command Prompt as Administrator

## 📦 Distribution Package

For end users, provide:
- `GalvoSwap.exe` (the executable)
- `QUICK_START.md` (quick reference)
- Instructions to run as Administrator

## 🎯 Why Windows Build is Required

The Linux environment I'm working in creates Linux executables (ELF format), but Windows needs Windows executables (PE format). They are not compatible because:

- **Different system calls** (Windows API vs Linux syscalls)
- **Different executable formats** (PE vs ELF)
- **Different libraries** (Windows DLL vs Linux .so)
- **tkinter differences** between platforms

## 🔄 Alternative: Online Build Services

If you don't have Windows available:

1. **GitHub Actions** (free)
   - Create a GitHub repository
   - Set up Actions workflow to build on Windows runners
   - Download the built executable

2. **Replit** (free tier)
   - Use their Windows environment
   - Install PyInstaller and build

3. **Cloud Build Services**
   - Various services offer Windows build environments
   - Some are free for open-source projects

## ✅ Verification

After building, test the executable:
1. Right-click → "Run as Administrator"
2. Should show the GalvoSwap interface
3. Should detect your laser (if connected)
4. Should complete setup wizard successfully

---

## 🎉 Success!

Once built, you'll have a professional standalone executable that:
- Works on any Windows 10/11 PC
- Requires no Python installation
- Is ~8-12 MB in size
- Handles admin privileges automatically
- Provides one-click driver switching

**Remember: Always run as Administrator for driver operations!**