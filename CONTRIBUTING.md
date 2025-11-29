# Contributing to EZ LightBurn Driver Switch

Thank you for your interest in contributing to EZ LightBurn Driver Switch! This document provides guidelines and information for contributors.

## 🤝 How to Contribute

### Reporting Bugs

- Use the [GitHub Issues](https://github.com/christdrivengeek/ez-lightburn-driver-switch/issues) page
- Provide detailed information about:
  - Your operating system and version
  - Laser model and controller
  - Step-by-step reproduction steps
  - Expected vs actual behavior
  - Any error messages

### Suggesting Features

- Open an issue with the "enhancement" label
- Describe the feature and why it would be useful
- Consider including mockups or examples

### Submitting Changes

1. **Fork the repository**
2. **Create a feature branch:**
   ```bash
   git checkout -b feature/your-feature-name
   ```
3. **Make your changes:**
   - Follow the existing code style
   - Add comments where appropriate
   - Update documentation if needed
4. **Test your changes:**
   - Test on Windows if possible
   - Ensure the application builds correctly
5. **Commit your changes:**
   ```bash
   git commit -m "Brief description of changes"
   ```
6. **Push to your fork:**
   ```bash
   git push https://x-access-token:$GITHUB_TOKEN@github.com/christdrivengeek/ez-lightburn-driver-switch.git feature/your-feature-name
   ```
7. **Create a Pull Request**

## 📝 Code Style

- Use Python 3.6+ syntax
- Follow PEP 8 style guidelines
- Use descriptive variable names
- Add docstrings for new functions
- Keep lines under 100 characters when possible

## 🧪 Testing

- Test on Windows 10/11 if possible
- Verify admin privilege handling
- Test with both EZCAD2 and LightBurn
- Check error handling for edge cases

## 📖 Documentation

- Update README.md for user-facing changes
- Add inline comments for complex logic
- Update version history in README.md

## 🏷️ Pull Request Guidelines

- Use descriptive titles
- Link to relevant issues
- Include screenshots for UI changes
- Describe testing performed

## 🚀 Release Process

Releases are created manually by the maintainer:
1. Update version number in code
2. Update CHANGELOG.md
3. Create GitHub release with tagged version
4. Upload built executable

## 💬 Getting Help

- Create an issue for questions
- Join discussions in GitHub Discussions
- Contact the maintainer directly for urgent matters

Thank you for contributing to the fiber laser community! 🚀