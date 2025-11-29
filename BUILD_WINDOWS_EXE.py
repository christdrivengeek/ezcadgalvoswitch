"""
Build Script for Windows Executable
This script should be run on Windows to create the .exe file
"""

import PyInstaller.__main__
import os
import sys

def build_windows_exe():
    """Build Windows executable for GalvoSwap"""
    
    # PyInstaller command for Windows
    args = [
        'GalvoSwap_v2.py',
        '--onefile',
        '--noconsole',
        '--name=GalvoSwap',
        '--windowed',
        '--icon=NONE',
        '--add-data=driver_paths.json;.' if os.path.exists('driver_paths.json') else '',
        '--clean'
    ]
    
    # Remove empty args
    args = [arg for arg in args if arg]
    
    print("Building GalvoSwap.exe for Windows...")
    print(f"Command: pyinstaller {' '.join(args)}")
    print()
    
    try:
        PyInstaller.__main__.run(args)
        print("\n✅ Build successful!")
        print(f"Executable location: {os.path.abspath('dist/GalvoSwap.exe')}")
        print(f"File size: {os.path.getsize('dist/GalvoSwap.exe') / 1024 / 1024:.1f} MB")
        
        # Test if executable exists
        if os.path.exists('dist/GalvoSwap.exe'):
            print("\n🎯 Windows executable ready!")
            print("\nTo use:")
            print("1. Run as Administrator")
            print("2. Complete setup wizard (first time)")
            print("3. Switch drivers with one click!")
        else:
            print("❌ Executable not found!")
            
    except Exception as e:
        print(f"❌ Build failed: {e}")
        return False
    
    return True

if __name__ == "__main__":
    print("GalvoSwap Windows Build Script")
    print("=" * 40)
    
    # Check if we're on Windows
    if sys.platform != 'win32':
        print("❌ This script must be run on Windows!")
        print("The Linux environment cannot create Windows executables.")
        print("\nTo build on Windows:")
        print("1. Install Python 3.6+")
        print("2. pip install pyinstaller")
        print("3. Copy this script and GalvoSwap_v2.py to Windows")
        print("4. Run: python BUILD_WINDOWS_EXE.py")
        sys.exit(1)
    
    build_windows_exe()