#!/usr/bin/env python3
"""
Build script for EZ LightBurn Driver Switch
Automated build process with error checking and validation
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path


def run_command(cmd, description):
    """Run a command and handle errors."""
    print(f"\n{'='*50}")
    print(f"Running: {description}")
    print(f"Command: {cmd}")
    print('='*50)
    
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        
        if result.returncode == 0:
            print(f"✅ SUCCESS: {description}")
            if result.stdout:
                print("Output:", result.stdout[:500])
        else:
            print(f"❌ FAILED: {description}")
            print("Error:", result.stderr)
            return False
            
    except Exception as e:
        print(f"❌ EXCEPTION: {description}")
        print("Error:", str(e))
        return False
    
    return True


def check_dependencies():
    """Check if required dependencies are available."""
    print("🔍 Checking dependencies...")
    
    # Check Python version
    if sys.version_info < (3, 6):
        print("❌ Python 3.6 or higher is required")
        return False
    
    print(f"✅ Python {sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}")
    
    # Check PyInstaller
    try:
        result = subprocess.run([sys.executable, "-m", "pyinstaller", "--version"], 
                              capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ PyInstaller {result.stdout.strip()}")
        else:
            print("❌ PyInstaller not found")
            return False
    except:
        print("❌ PyInstaller not found")
        return False
    
    return True


def validate_source_files():
    """Validate that required source files exist."""
    print("\n🔍 Validating source files...")
    
    required_files = [
        "EZ_LightBurn_Driver_Switch.py",
        "README.md",
        "LICENSE"
    ]
    
    for file in required_files:
        if Path(file).exists():
            print(f"✅ {file}")
        else:
            print(f"❌ {file} - Missing!")
            return False
    
    return True


def clean_build():
    """Clean previous build artifacts."""
    print("\n🧹 Cleaning previous build artifacts...")
    
    dirs_to_clean = ["build", "dist", "__pycache__"]
    files_to_clean = ["*.spec"]
    
    for dir_name in dirs_to_clean:
        if Path(dir_name).exists():
            try:
                shutil.rmtree(dir_name)
                print(f"✅ Removed {dir_name}/")
            except Exception as e:
                print(f"⚠️  Could not remove {dir_name}/: {e}")
    
    return True


def build_executable():
    """Build the executable using PyInstaller."""
    print("\n🔨 Building executable...")
    
    # PyInstaller command
    cmd = (
        'pyinstaller '
        '--onefile '
        '--noconsole '
        '--name="EZ LightBurn Driver Switch" '
        '--uac-admin '
        '--clean '
        '--add-data="README.md;." '
        '--add-data="LICENSE;." '
        'EZ_LightBurn_Driver_Switch.py'
    )
    
    success = run_command(cmd, "Building executable with PyInstaller")
    
    if not success:
        return False
    
    # Check if executable was created
    exe_path = Path("dist/EZ LightBurn Driver Switch.exe")
    if exe_path.exists():
        size_mb = exe_path.stat().st_size / 1024 / 1024
        print(f"✅ Executable created: {exe_path}")
        print(f"📦 File size: {size_mb:.1f} MB")
        return True
    else:
        print("❌ Executable not found in dist/")
        return False


def create_release_package():
    """Create a release package with documentation."""
    print("\n📦 Creating release package...")
    
    # Create release directory
    release_dir = Path("release")
    if release_dir.exists():
        shutil.rmtree(release_dir)
    release_dir.mkdir()
    
    # Copy executable
    exe_source = Path("dist/EZ LightBurn Driver Switch.exe")
    exe_dest = release_dir / "EZ LightBurn Driver Switch.exe"
    shutil.copy2(exe_source, exe_dest)
    print(f"✅ Copied executable to release/")
    
    # Copy documentation
    doc_files = ["README.md", "LICENSE", "CHANGELOG.md"]
    for doc in doc_files:
        if Path(doc).exists():
            shutil.copy2(doc, release_dir / doc)
            print(f"✅ Copied {doc}")
    
    # Create quick start guide
    quick_start = """# EZ LightBurn Driver Switch - Quick Start

1. Run EZ LightBurn Driver Switch.exe (double-click)
2. Click "Yes" on the UAC prompt
3. Complete the setup wizard (first time only)
4. Switch drivers with one click!

## Requirements
- Windows 7 or later
- Administrator privileges
- EZCAD2 and/or LightBurn installed
- ComMarker B4 or compatible fiber laser

## Support
- GitHub Issues: https://github.com/christdrivengeek/ez-lightburn-driver-switch/issues
- Documentation: README.md

Made with ❤️ by William Sorensen (Christ Driven Geek)
"""
    
    with open(release_dir / "QUICK_START.txt", "w") as f:
        f.write(quick_start)
    print("✅ Created QUICK_START.txt")
    
    # Create zip archive
    import zipfile
    zip_name = "ez-lightburn-driver-switch-v2.1.zip"
    with zipfile.ZipFile(zip_name, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for file_path in release_dir.rglob("*"):
            if file_path.is_file():
                zipf.write(file_path, file_path.relative_to(release_dir))
    
    print(f"✅ Created release package: {zip_name}")
    
    return True


def main():
    """Main build process."""
    print("🚀 EZ LightBurn Driver Switch - Build Script")
    print("=" * 60)
    
    # Check if we're on Windows
    if os.name != 'nt':
        print("❌ This script must be run on Windows to build the executable")
        print("The build process requires Windows-specific libraries")
        return 1
    
    # Step 1: Check dependencies
    if not check_dependencies():
        print("\n❌ Dependency check failed")
        return 1
    
    # Step 2: Validate source files
    if not validate_source_files():
        print("\n❌ Source file validation failed")
        return 1
    
    # Step 3: Clean previous builds
    if not clean_build():
        print("\n❌ Clean failed")
        return 1
    
    # Step 4: Build executable
    if not build_executable():
        print("\n❌ Build failed")
        return 1
    
    # Step 5: Create release package
    if not create_release_package():
        print("\n❌ Release package creation failed")
        return 1
    
    print("\n🎉 Build completed successfully!")
    print("=" * 60)
    print("📦 Release package created: ez-lightburn-driver-switch-v2.1.zip")
    print("📂 Executable location: dist/EZ LightBurn Driver Switch.exe")
    print("📖 Documentation: release/ folder")
    print("\n✅ Ready for distribution!")
    
    return 0


if __name__ == "__main__":
    sys.exit(main())