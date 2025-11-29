# GalvoSwap - User Guide

## Table of Contents
1. [Getting Started](#getting-started)
2. [First-Time Setup](#first-time-setup)
3. [Daily Usage](#daily-usage)
4. [Troubleshooting](#troubleshooting)
5. [FAQ](#faq)

## Getting Started

### What is GalvoSwap?
GalvoSwap is a tool that makes it easy to switch your Galvo Laser between two different software programs:
- **EZCAD2**: The standard laser control software
- **LightBurn**: An alternative laser control software

Normally, switching between these requires manual driver installation through Device Manager. GalvoSwap automates this process with a single click.

### System Requirements
- Windows 7 or later
- Administrator access on your computer
- Galvo Laser with Hardware ID: VID_9588&PID_9899

## First-Time Setup

### Step 1: Launch GalvoSwap
1. Locate `GalvoSwap.exe`
2. **Right-click** on the file
3. Select **"Run as Administrator"**

![Admin Prompt](https://via.placeholder.com/400x200?text=Right-click+%3E+Run+as+Administrator)

**Why Administrator?** Driver installation requires elevated privileges in Windows.

### Step 2: Administrator Confirmation
You'll see a dialog asking to restart with admin privileges:
- Click **"Yes"** to continue
- The application will restart with proper permissions

### Step 3: Setup Wizard
On first run, the Setup Wizard will appear:

#### A. EZCAD2 Driver Selection
1. Click **"Browse..."** next to "EZCAD2 Driver"
2. Navigate to your EZCAD2 installation folder
3. Find the driver `.inf` file (usually in a "Driver" subfolder)
4. Select the file and click **"Open"**

**Common EZCAD2 Driver Locations:**
- `C:\Program Files\EZCAD2\Driver\`
- `C:\EZCAD2\Driver\`
- `C:\BJJCZ\EZCAD2\Driver\`

#### B. LightBurn Driver Selection
1. The LightBurn driver may be **auto-detected** (you'll see a green checkmark)
2. If not auto-detected, click **"Browse..."**
3. Navigate to: `C:\Program Files\LightBurn\EzCad2Driver\`
4. Select `EzCad2Driver.inf`

**Default LightBurn Driver Path:**
```
C:\Program Files\LightBurn\EzCad2Driver\EzCad2Driver.inf
```

#### C. Save Configuration
1. Verify both paths are correct
2. Click **"Save Configuration"**
3. You'll see a success message

## Daily Usage

### Main Interface Overview

```
┌─────────────────────────────────────┐
│     Galvo Driver Swapper            │
├─────────────────────────────────────┤
│                                     │
│   Current Driver Status:            │
│   ● LightBurn Driver                │
│                                     │
│   ┌───────────────────────────┐    │
│   │   Switch to EZCAD2        │    │
│   └───────────────────────────┘    │
│                                     │
│         [⚙ Settings]                │
│                                     │
└─────────────────────────────────────┘
```

### Switching Drivers

#### To Switch from LightBurn to EZCAD2:
1. Ensure your laser is **disconnected** (recommended)
2. The status will show "LightBurn Driver" in green
3. Click the **"Switch to EZCAD2"** button
4. Confirm the action in the dialog
5. Wait for the installation to complete
6. You'll see a success message
7. **Reconnect your laser**
8. Launch EZCAD2

#### To Switch from EZCAD2 to LightBurn:
1. Ensure your laser is **disconnected** (recommended)
2. The status will show "EZCAD2 Driver" in blue
3. Click the **"Switch to LightBurn"** button
4. Confirm the action in the dialog
5. Wait for the installation to complete
6. You'll see a success message
7. **Reconnect your laser**
8. Launch LightBurn

### Best Practices
1. **Close Software First**: Always close EZCAD2 or LightBurn before switching
2. **Disconnect Laser**: Unplug your laser before switching drivers (optional but recommended)
3. **Reconnect After**: Reconnect your laser after the driver switch completes
4. **Wait for Confirmation**: Don't interrupt the driver installation process

## Troubleshooting

### Problem: "Administrator Privileges Required"
**Solution:**
- Right-click `GalvoSwap.exe`
- Select "Run as Administrator"
- Click "Yes" when prompted

### Problem: "Driver Installation Failed"
**Possible Causes & Solutions:**

1. **Not Running as Admin**
   - Restart the application as Administrator

2. **Incorrect Driver Path**
   - Click "⚙ Settings"
   - Verify both driver paths are correct
   - Browse to the correct `.inf` files

3. **Driver Files Missing**
   - Reinstall EZCAD2 or LightBurn
   - Verify the driver files exist at the specified paths

4. **Device Connected**
   - Disconnect your laser
   - Try the switch again
   - Reconnect after success

### Problem: "Driver Not Detected"
**Solution:**
1. Ensure your laser is connected
2. Check Device Manager:
   - Press `Win + X`
   - Select "Device Manager"
   - Look for your device under "Universal Serial Bus devices" or "Other devices"
3. Verify the Hardware ID matches: VID_9588&PID_9899

### Problem: "Configuration Error"
**Solution:**
1. Delete `driver_paths.json` from the GalvoSwap folder
2. Restart GalvoSwap
3. Complete the setup wizard again

### Problem: Software Doesn't Recognize Laser After Switch
**Solution:**
1. Disconnect and reconnect the laser
2. Restart the laser control software (EZCAD2 or LightBurn)
3. Check Device Manager to verify the driver is installed
4. Try switching back and forth once more

## FAQ

### Q: Do I need to keep GalvoSwap running?
**A:** No. GalvoSwap only needs to run when you want to switch drivers. You can close it after switching.

### Q: Can I use both EZCAD2 and LightBurn at the same time?
**A:** No. Only one driver can be active at a time. You must switch drivers to change software.

### Q: How long does switching take?
**A:** Usually 5-10 seconds. The application will show a "Swapping Driver..." message during the process.

### Q: Will this damage my laser?
**A:** No. This tool only changes the Windows driver. It doesn't modify your laser's firmware or hardware.

### Q: Can I switch while the laser is running?
**A:** Not recommended. Always close your laser software and disconnect the laser before switching.

### Q: What if I lose the driver files?
**A:** You'll need to reinstall EZCAD2 or LightBurn to restore the driver files, then reconfigure GalvoSwap.

### Q: Does this work with other laser types?
**A:** This tool is specifically designed for Galvo Lasers with Hardware ID VID_9588&PID_9899. Other lasers may not be compatible.

### Q: Can I run this on Windows 7?
**A:** Yes, GalvoSwap supports Windows 7 and later versions.

### Q: Do I need Python installed?
**A:** No. The compiled `.exe` file is standalone and doesn't require Python.

### Q: How do I update my driver paths?
**A:** Click the "⚙ Settings" button in the main window to reopen the setup wizard.

### Q: What if the auto-detection fails?
**A:** Manually browse to the driver location using the "Browse..." button in the setup wizard.

## Advanced Tips

### Creating a Desktop Shortcut
1. Right-click `GalvoSwap.exe`
2. Select "Create shortcut"
3. Drag the shortcut to your desktop
4. Right-click the shortcut → Properties
5. Click "Advanced..."
6. Check "Run as administrator"
7. Click OK

### Quick Switch Workflow
1. Close laser software
2. Run GalvoSwap (as admin)
3. Click switch button
4. Wait for confirmation
5. Close GalvoSwap
6. Open new laser software

### Backing Up Configuration
The `driver_paths.json` file contains your settings. You can:
- Copy it to backup your configuration
- Share it with other computers (if driver paths are the same)
- Edit it manually if needed (advanced users)

## Getting Help

If you encounter issues not covered in this guide:
1. Check the README.md file for technical details
2. Verify your system meets the requirements
3. Try deleting `driver_paths.json` and reconfiguring
4. Check Windows Event Viewer for driver installation errors

## Safety Notes

⚠️ **Important Safety Information:**
- Always follow your laser manufacturer's safety guidelines
- Wear appropriate laser safety glasses
- Ensure proper ventilation when operating your laser
- Never leave your laser unattended while operating
- This software only changes drivers - it doesn't affect laser safety features

---

**Version:** 1.0  
**Last Updated:** 2024  
**Compatible With:** Windows 7, 8, 10, 11