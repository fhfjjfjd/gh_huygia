# Mobile Development Rules

## Overview
This document defines rules specific to mobile application development. These rules supplement the general GitHub event management rules and should be applied when developing mobile applications.

## Mobile-Specific Repository Hygiene

### Core Rules
- `README.md` MUST include mobile-specific information:
  - Supported platforms (iOS/Android/both)
  - Minimum OS versions
  - Device requirements
  - Installation instructions for mobile platforms
- Mobile project files MUST be organized properly:
  - iOS: `ios/` directory with Xcode project
  - Android: `android/` directory with Gradle project
  - React Native: `ios/` and `android/` directories with platform-specific code
- Mobile-specific assets MUST be stored properly:
  - App icons in proper sizes for all required densities
  - Splash screens for all required sizes
  - App store screenshots (if available)

### Mobile Assets Requirements
- App icons MUST be provided in all required sizes:
  - iOS: 20x20, 29x29, 40x40, 57x57, 60x60, 76x76, 83.5x83.5, 1024x1024
  - Android: 48x48, 72x72, 96x96, 144x144, 192x192, 512x512
- Images MUST be optimized for mobile devices (WebP format preferred when possible)
- Video assets MUST be compressed to minimize app bundle size
- FORBIDDEN: Committing files >50MB without explicit approval

### Mobile-Specific Branch Management
- Mobile release branches MUST use format: `release/[platform]/v{MAJOR}.{MINOR}.{PATCH}`
  - Examples: `release/ios/v1.2.0`, `release/android/v1.2.0`
- Platform-specific feature branches SHOULD use format: `feat/[platform]/feature-name`
  - Examples: `feat/ios/push-notifications`, `feat/android/location-services`

## Mobile-Specific Commit Rules

### Mobile-Specific Commit Types
- `ios`: Changes specific to iOS platform
- `android`: Changes specific to Android platform
- `mobile`: Changes affecting both mobile platforms
- `perf(mobile)`: Performance improvements specific to mobile
- `fix(ios)`: Bug fixes specific to iOS
- `fix(android)`: Bug fixes specific to Android
- `feat(ios)`: New features for iOS
- `feat(android)`: New features for Android

### Examples
```
✅ feat(ios): add push notification support
✅ feat(android): implement fingerprint authentication
✅ fix(mobile): resolve memory leak in image loading
✅ perf(ios): optimize image caching for lower-end devices
❌ feat: add push notification support  (too generic for mobile project)
```

## Mobile-Specific Issue Management

### Mobile Bug Reports
Mobile bug reports MUST additionally include:
- Device model and OS version
- App version
- Network conditions (WiFi/Cellular/Offline)
- Battery level (if relevant to issue)
- Any custom device configurations (rooted/jailbroken)

### Mobile Feature Requests
Mobile feature requests SHOULD specify:
- Target platform(s) (iOS/Android/both)
- Any platform-specific design guidelines (Material Design for Android, Human Interface Guidelines for iOS)
- Performance requirements (frame rate, loading times)
- Offline capability requirements

## Mobile-Specific PR Rules

### Mobile PR Requirements
- PR description MUST specify testing devices and OS versions
- PR description MUST include performance impact (if applicable)
- Screenshots REQUIRED for UI changes
- Video demonstration RECOMMENDED for complex UI interactions
- Testing on multiple device sizes REQUIRED for UI changes

### Mobile-Specific Review Process
- iOS changes MUST be reviewed by iOS developer
- Android changes MUST be reviewed by Android developer
- Cross-platform changes MUST be reviewed by developers from both platforms
- Performance changes MUST be reviewed by performance specialist

## Mobile-Specific Release Management

### Mobile Release Requirements
- Mobile releases MUST include platform-specific changelogs
- Release notes MUST be written in language appropriate for app store users
- App store metadata MUST be updated with each release
- Beta testing MUST be completed before public release

### Mobile Versioning
- Mobile apps SHOULD follow SemVer but consider platform-specific requirements:
  - Major: Breaking API changes, significant UI redesigns, platform migrations
  - Minor: New features, UI enhancements, platform-specific improvements
  - Patch: Bug fixes, security patches, performance improvements
- iOS and Android versions SHOULD be kept in sync when possible

## Mobile-Specific Security

### Mobile Security Requirements
- Hardcoded credentials MUST NOT be committed (API keys, secrets, certificates)
- Sensitive data MUST NOT be stored in plain text on device
- Network calls MUST use HTTPS with certificate pinning when possible
- App MUST implement proper permissions handling
- Biometric authentication SHOULD be implemented when appropriate

### Mobile-Specific Vulnerabilities
- FORBIDDEN: Storing sensitive data in app preferences without encryption
- FORBIDDEN: Using insecure protocols (HTTP, FTP) for sensitive data
- FORBIDDEN: Implementing custom encryption algorithms
- Sensitive data MUST be cleared from memory when no longer needed

## Mobile CI/CD Rules

### Mobile-Specific CI Requirements
- Builds MUST be tested on multiple device configurations
- Automated UI tests MUST run on both simulators/emulators and real devices
- Performance tests MUST be run for each platform
- App store validation MUST be performed before release builds

### Mobile-Specific CD Requirements
- Beta releases MUST be distributed through appropriate platform services
  - iOS: TestFlight
  - Android: Google Play Console Internal Testing/Beta
- Production releases MUST follow platform-specific approval processes
- Rollback procedures MUST be ready before production releases