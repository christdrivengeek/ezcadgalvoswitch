# Changelog

All notable changes to EZ LightBurn Driver Switch will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [2.1.0] - 2024-11-21

### Added
- ✨ **Auto-uninstall old driver before installing new one** - Prevents Windows from reverting driver changes
- ✨ **Enhanced setup wizard with new options** - More control over driver switching process
- ✨ **Better error handling and recovery** - More informative error messages
- ✨ **Improved UI feedback during switching** - Shows uninstalling, installing, scanning steps
- ✨ **Hardware ID display in main UI** - Easy to verify which hardware is being detected
- ✨ **Force install by default** - Better compatibility with Windows 10/11

### Changed
- 🔄 **Renamed from GalvoSwap to EZ LightBurn Driver Switch** - Clearer branding
- 🔄 **Improved UI design** - More professional appearance
- 🔄 **Enhanced driver detection logic** - More reliable status detection
- 🔄 **Better PowerShell integration** - More robust device management

### Fixed
- 🐛 **Driver switching reverting back** - Main issue resolved with auto-uninstall
- 🐛 **UI freezing during operations** - Better threading implementation
- 🐛 **Timeout handling improvements** - More responsive during long operations

## [2.0.0] - 2024-11-20

### Added
- ✨ **Threading support** - UI no longer freezes during driver operations
- ✨ **Force install option** - Overcomes Windows 10/11 driver stubbornness
- ✨ **Configurable Hardware ID** - Support for different laser controllers
- ✨ **Auto-detection of LightBurn driver** - Saves time during setup
- ✨ **Enhanced error messages** - More user-friendly feedback

### Changed
- 🔄 **Modern UI redesign** - Cleaner, more professional interface
- 🔄 **Improved setup wizard** - Better user experience
- 🔄 **Better admin privilege handling** - More reliable elevation

## [1.0.0] - 2024-11-19

### Added
- ✨ **Initial release** - Basic driver switching functionality
- ✨ **Setup wizard** - First-time configuration
- ✨ **Admin privilege detection** - Automatic elevation
- ✨ **Driver detection** - PowerShell-based device detection
- ✨ **JSON configuration** - Persistent settings storage
- ✨ **Basic UI** - Functional interface for driver switching

---

## Legend

- ✨ Added - New features
- 🔄 Changed - Changes in existing functionality
- 🐛 Fixed - Bug fixes
- 📝 Documentation - Documentation changes