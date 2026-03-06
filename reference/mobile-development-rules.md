# Mobile Development Rules

> **RFC 2119 Compliance**: The key words "MUST", "MUST NOT", "REQUIRED", "SHALL", "SHALL NOT",
> "SHOULD", "SHOULD NOT", "FORBIDDEN", "REJECTED" in this document are to be interpreted as
> described in [RFC 2119](https://www.rfc-editor.org/rfc/rfc2119).

This document enforces **non-negotiable** rules for mobile development projects.
Violations are REJECTED. No exceptions.

---

## 1. Project Structure

### Android (Java/Kotlin) Projects

- `app/src/main/java/` — Application source code
- `app/src/main/res/` — Resources (layouts, drawables, values)
- `app/src/main/AndroidManifest.xml` — Application manifest
- `app/build.gradle` — Module build configuration
- `build.gradle` — Project build configuration
- `gradle.properties` — Gradle settings
- `gradlew`, `gradlew.bat` — Gradle wrapper scripts
- `settings.gradle` — Module inclusion settings

### iOS (Swift) Projects

- `{ProjectName}/` — Main application source directory
- `{ProjectName}/Assets.xcassets/` — Image and asset catalog
- `{ProjectName}/Base.lproj/` — Storyboard and localization files
- `{ProjectName}.xcodeproj/` — Xcode project bundle
- `Podfile` — CocoaPods dependency manager file
- `Podfile.lock` — Locked dependency versions

### Cross-Platform (React Native/Flutter) Projects

#### React Native
- `index.js` — Entry point
- `package.json` — Dependencies and scripts
- `android/`, `ios/` — Native platform directories
- `src/` — Source code
- `assets/` — Static assets

#### Flutter
- `lib/` — Dart source code
- `assets/` — Static assets
- `ios/`, `android/` — Platform-specific code
- `pubspec.yaml` — Dependencies and assets

---

## 2. Version Management

### Android Versioning
- `versionCode` — Incremental integer, MUST be unique per release
- `versionName` — Semantic version string (e.g., "1.2.3")
- Both MUST be updated before each release
- `versionCode` MUST be incremented for every build (even internal)

### iOS Versioning
- `CFBundleShortVersionString` — Marketing version (e.g., "1.2.3")
- `CFBundleVersion` — Build number (e.g., "123")
- Build number MUST be incremented for every build
- Marketing version SHOULD follow SemVer 2.0.0

---

## 3. Build Configuration

### Android (Gradle)
- Use `minSdk`, `targetSdk`, `compileSdk` appropriately
- Enable code shrinking and obfuscation for release builds
- Use `buildTypes` for debug/release configurations
- Use `productFlavors` for different app variants

### iOS (Xcode)
- Use different build configurations for Debug/Release
- Properly set bundle identifiers for different environments
- Use build settings inheritance appropriately

### Cross-Platform
- Use environment variables for configuration
- Separate build configurations for different environments
- Properly configure platform-specific settings

---

## 4. Security Rules

### Data Storage
- Sensitive data MUST NOT be stored in plain text
- Use platform-specific secure storage:
  - Android: Android Keystore System, EncryptedSharedPreferences
  - iOS: Keychain Services
- For cross-platform: Use secure storage libraries (e.g., react-native-keychain)
- Temporary files MUST be encrypted or cleared after use

### Network Security
- All network requests MUST use HTTPS with TLS 1.2 or higher
- Certificate pinning SHOULD be implemented for sensitive apps
- Never trust user-provided certificates in production
- API keys MUST NOT be hardcoded in source code

### Authentication
- Use platform-appropriate authentication methods
- Implement proper session management
- Use refresh token mechanisms when appropriate
- Biometric authentication when available and appropriate

---

## 5. Performance Requirements

### Memory Management
- Android: Monitor for memory leaks with LeakCanary
- iOS: Use Instruments to detect retain cycles
- Cross-platform: Follow platform-specific memory management patterns
- Profile memory usage regularly

### Battery Optimization
- Minimize background operations
- Use platform-specific background processing APIs appropriately
- Optimize network requests to reduce battery drain
- Use location services efficiently

### UI Responsiveness
- Main/UI thread MUST remain responsive
- Heavy operations MUST be performed on background threads
- Use platform-specific async patterns appropriately
- Implement proper loading states

---

## 6. UI/UX Guidelines

### Platform Compliance
- Android: Follow Material Design guidelines
- iOS: Follow Human Interface Guidelines
- Cross-platform: Adapt to platform-specific patterns
- Use native navigation patterns

### Accessibility
- Support screen readers (TalkBack/VoiceOver)
- Provide adequate color contrast
- Support dynamic font sizes
- Use semantic labels appropriately

### Internationalization
- All user-facing strings MUST be externalized
- Support RTL languages where appropriate
- Consider cultural differences in UI
- Use platform-specific localization tools

---

## 7. Testing Requirements

### Unit Tests
- Android: JUnit for Java/Kotlin, Espresso for UI
- iOS: XCTest for unit tests, UI tests with XCTest
- Cross-platform: Jest for React Native, flutter_test for Flutter
- Achieve minimum 80% code coverage

### Integration Tests
- Test critical user flows
- Mock external dependencies appropriately
- Test error conditions and edge cases
- Test different network conditions

### Device Testing
- Test on multiple screen sizes and resolutions
- Test on different OS versions (minimum supported + latest)
- Test on different device capabilities (performance, memory)
- Use emulators/simulators and real devices

---

## 8. Distribution Rules

### App Store Requirements
- Follow platform-specific app store guidelines
- Proper app metadata (descriptions, screenshots, privacy policy)
- App review compliance
- Privacy policy MUST be accessible

### Release Process
- All code MUST pass CI checks before release
- Beta testing for significant features
- Staged rollouts for major updates
- Rollback plan for critical issues

### Version Control
- Git tags MUST follow format: `v{MAJOR}.{MINOR}.{PATCH}`
- Release branches MUST follow format: `release/v{MAJOR}.{MINOR}`
- Hotfix branches MUST follow format: `hotfix/{issue-number}`

---

## 9. Termux/Android-Specific Rules

### Environment Considerations
- When developing on Termux, ensure proper Android SDK setup
- Use `termux-setup-storage` to access device storage when needed
- Be mindful of Termux's limitations compared to full Android Studio
- For production builds, use proper Android development environment

### Permissions
- Declare all required permissions in manifest
- Implement runtime permission requests where appropriate
- Explain permission rationale to users
- Follow privacy best practices

### Dependencies
- Keep native dependencies up-to-date
- Audit for security vulnerabilities
- Prefer stable versions over alpha/beta releases
- Document any custom native modules

---

## 10. Common Violations (FORBIDDEN)

- Hardcoded API keys, secrets, or sensitive data
- Direct SQL queries without parameterization (SQL injection)
- Improper input validation leading to security vulnerabilities
- Using deprecated platform APIs without proper migration plan
- Pushing to main branch without proper review process
- Committing build artifacts or intermediate files
- Using debug builds for production distribution
- Violating platform-specific content policies
- Not following accessibility guidelines
- Ignoring performance bottlenecks

---

## 11. Compliance Verification

Run `scripts/mobile-audit.sh` to verify compliance with these rules:

```bash
# Check project structure
# Verify security configurations
# Validate build configurations
# Audit dependencies
# Check for common vulnerabilities
```

All checks MUST pass before code is accepted for review.