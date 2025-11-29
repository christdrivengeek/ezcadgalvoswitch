# GalvoSwap - Build Instructions

## Quick Build Command

The simplest and recommended command to build GalvoSwap into a standalone executable:

```bash
pyinstaller --onefile --noconsole --name=GalvoSwap GalvoSwap.py
```

## Detailed Build Process

### Prerequisites
1. **Install Python 3.6+** (if not already installed)
2. **Install PyInstaller**:
   ```bash
   pip install pyinstaller
   ```

### Build Steps

#### Step 1: Navigate to Project Directory
```bash
cd path/to/GalvoSwap
```

#### Step 2: Run PyInstaller
```bash
pyinstaller --onefile --noconsole --name=GalvoSwap GalvoSwap.py
```

#### Step 3: Locate the Executable
The compiled executable will be in the `dist` folder:
```
dist/GalvoSwap.exe
```

### Command Options Explained

- `--onefile`: Packages everything into a single .exe file
- `--noconsole`: Hides the console window (GUI-only mode)
- `--name=GalvoSwap`: Sets the output filename to "GalvoSwap.exe"
- `GalvoSwap.py`: The source Python file to compile

### Alternative Build Commands

#### With Custom Icon
```bash
pyinstaller --onefile --noconsole --name=GalvoSwap --icon=icon.ico GalvoSwap.py
```

#### Debug Build (shows console for troubleshooting)
```bash
pyinstaller --onefile --name=GalvoSwap GalvoSwap.py
```

#### With UPX Compression (smaller file size)
```bash
pyinstaller --onefile --noconsole --name=GalvoSwap --upx-dir=path/to/upx GalvoSwap.py
```

### Clean Build

If you need to rebuild from scratch:

```bash
# Remove build artifacts
rmdir /s /q build dist
del GalvoSwap.spec

# Rebuild
pyinstaller --onefile --noconsole --name=GalvoSwap GalvoSwap.py
```

### Build Output

After successful build, you'll have:
- `dist/GalvoSwap.exe` - The standalone executable (distribute this)
- `build/` - Temporary build files (can be deleted)
- `GalvoSwap.spec` - PyInstaller specification file (can be deleted)

### Distribution

The `GalvoSwap.exe` file is completely standalone and can be:
- Copied to any Windows computer
- Run without Python installed
- Distributed to users

**Important**: Users must run the executable with Administrator privileges for driver swapping to work.

### Testing the Executable

1. Copy `GalvoSwap.exe` to a test location
2. Right-click and select "Run as Administrator"
3. Complete the setup wizard
4. Test driver detection and swapping

### Troubleshooting Build Issues

#### "PyInstaller not found"
```bash
pip install --upgrade pyinstaller
```

#### "Module not found" errors
Ensure all imports in GalvoSwap.py are from the standard library.

#### Large executable size
Use UPX compression or consider using `--exclude-module` for unused modules.

#### Antivirus false positives
This is common with PyInstaller executables. You may need to:
- Add an exception in your antivirus
- Sign the executable with a code signing certificate
- Build on a clean system

## Advanced Configuration

### Custom Spec File

For advanced builds, you can modify the generated `.spec` file:

```bash
# Generate spec file
pyi-makespec --onefile --noconsole --name=GalvoSwap GalvoSwap.py

# Edit GalvoSwap.spec as needed

# Build from spec file
pyinstaller GalvoSwap.spec
```

### Adding Version Information (Windows)

Create a `version_info.txt`:
```
VSVersionInfo(
  ffi=FixedFileInfo(
    filevers=(1, 0, 0, 0),
    prodvers=(1, 0, 0, 0),
    mask=0x3f,
    flags=0x0,
    OS=0x40004,
    fileType=0x1,
    subtype=0x0,
    date=(0, 0)
  ),
  kids=[
    StringFileInfo(
      [
      StringTable(
        u'040904B0',
        [StringStruct(u'CompanyName', u'Your Company'),
        StringStruct(u'FileDescription', u'GalvoSwap - Galvo Driver Switcher'),
        StringStruct(u'FileVersion', u'1.0.0.0'),
        StringStruct(u'InternalName', u'GalvoSwap'),
        StringStruct(u'LegalCopyright', u'Copyright (c) 2024'),
        StringStruct(u'OriginalFilename', u'GalvoSwap.exe'),
        StringStruct(u'ProductName', u'GalvoSwap'),
        StringStruct(u'ProductVersion', u'1.0.0.0')])
      ]),
    VarFileInfo([VarStruct(u'Translation', [1033, 1200])])
  ]
)
```

Then build with:
```bash
pyinstaller --onefile --noconsole --name=GalvoSwap --version-file=version_info.txt GalvoSwap.py
```

## Final Checklist

Before distributing:
- [ ] Test the executable on a clean Windows system
- [ ] Verify admin privilege elevation works
- [ ] Test driver detection
- [ ] Test driver swapping
- [ ] Verify setup wizard functionality
- [ ] Check file size is reasonable
- [ ] Test on different Windows versions (7, 10, 11)
- [ ] Create user documentation
- [ ] Consider code signing for production use