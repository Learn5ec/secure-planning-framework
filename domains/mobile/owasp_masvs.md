# OWASP Mobile Application Security Verification Standard (MASVS) — Security Rules

**Sources:** OWASP MASVS v2.0, MASTG (Mobile App Security Testing Guide)
**Scope:** iOS and Android Mobile Applications

> These rules apply when designing, building, or assessing mobile applications (iOS, Android, or cross-platform like Flutter/React Native). The MASVS defines the security requirements, and the MASTG provides the testing procedures.

---

# Rule ID: MASVS-STORAGE-1
## Title: Secure Storage of Sensitive Data
**Category:** Storage  

### Rule
The app securely stores sensitive data (PII, cryptographic material, secrets, API keys) ensuring it is properly protected, regardless of the target location (private internal storage or public folders).
- **Android:** Do not use `SharedPreferences` for sensitive data without encryption (use `EncryptedSharedPreferences`). Do not hardcode secrets. Ensure Realm/SQLite databases containing sensitive info are encrypted.
- **iOS:** Use the iOS Keychain for small secrets. Use Data Protection API (`NSFileProtectionComplete`) for files.
- **Flutter:** Use `flutter_secure_storage`.

### Applies When
- The app stores data locally on the device.

### Validation
- Standard testing procedures per MASTG

### Failure Impact
- Security compromise related to this control

---

# Rule ID: MASVS-STORAGE-2
## Title: Prevent Leakage of Sensitive Data
**Category:** Storage  

### Rule
The app prevents unintentional leakage of sensitive data to publicly accessible locations via system capabilities such as backups, clipboards, or logs.
- **Backups:** Exclude sensitive data from backups (`backup_rules.xml`, `dataExtractionRules`, or `android:allowBackup="false"` on Android; explicitly excluding files on iOS).
- **Logs:** Remove all logging of sensitive data in production builds. Redact sensitive data if logging is required. Avoid implicit string building in logs (`Log.v("key " + key)`).
- **Clipboard:** Clear the clipboard when the app is backgrounded if sensitive data was copied.

### Applies When
- App state is saved, backed up, logged, or sensitive data is copied.

### Validation
- Standard testing procedures per MASTG

### Failure Impact
- Security compromise related to this control

---

# Rule ID: MASVS-CRYPTO-1
## Title: Employ Strong Cryptography
**Category:** Cryptography  

### Rule
The app employs current strong cryptography according to industry best practices (e.g., NIST standards) for any sensitive data encrypted in transit or at rest.
- Avoid ECB entirely. Prefer AES-GCM/AES-CCM; if CBC unavoidable, use random IVs + encrypt-then-MAC.
- Do not use custom cryptographic algorithms.
- Use strong, cryptographically secure pseudorandom number generators (CSPRNGs) with sufficient entropy.

### Applies When
- The app encrypts data.

### Validation
- Standard testing procedures per MASTG

### Failure Impact
- Security compromise related to this control

---

# Rule ID: MASVS-CRYPTO-2
## Title: Secure Key Management
**Category:** Cryptography  

### Rule
The app performs key management securely throughout the lifecycle (generation, storage, and protection) using secure enclaves or keystores provided by the platform.
- **Android:** Use the Android Keystore system.
- **iOS:** Use the Secure Enclave and Keychain.
- Never hardcode cryptographic keys in the application binary.

### Applies When
- Cryptographic keys are generated or stored on the device.

### Validation
- Standard testing procedures per MASTG

### Failure Impact
- Security compromise related to this control

---

# Rule ID: MASVS-AUTH-1
## Title: Secure Authentication & Authorization Protocols
**Category:** Authentication and Authorization  

### Rule
The app uses secure authentication and authorization protocols to communicate with remote endpoints, enforcing proper session validation and access controls.
- Enforce authentication on the remote endpoint.
- Do not rely solely on client-side authentication or authorization checks.
- Handle session tokens securely, using standard mechanisms (e.g., OAuth 2.0, OpenID Connect).

### Applies When
- The app connects to a remote backend service.

### Validation
- Standard testing procedures per MASTG

### Failure Impact
- Security compromise related to this control

---

# Rule ID: MASVS-AUTH-2
## Title: Secure Local Authentication
**Category:** Authentication and Authorization  

### Rule
The app performs local authentication securely according to the platform best practices.
- **Android:** Use `BiometricPrompt` API. Do not use legacy fingerprint APIs.
- **iOS:** Use `LocalAuthentication` framework (TouchID/FaceID).
- Ensure fallback to PIN/passcode is secure.

### Applies When
- Biometrics, PINs, or local authentication are used to unlock the app or access features.

### Validation
- Standard testing procedures per MASTG

### Failure Impact
- Security compromise related to this control

---

# Rule ID: MASVS-AUTH-3
## Title: Additional Authentication for Sensitive Operations
**Category:** Authentication and Authorization  

### Rule
The app secures sensitive operations with additional authentication.
- Require re-authentication, MFA, or deep link validation for critical actions (e.g., money transfer, changing passwords, modifying security settings).

### Applies When
- Highly sensitive operations are executed.

### Validation
- Standard testing procedures per MASTG

### Failure Impact
- Security compromise related to this control

---

# Rule ID: MASVS-NETWORK-1
## Title: Secure Network Traffic
**Category:** Network Communication  

### Rule
The app secures all network traffic according to the current best practices.
- Enforce TLS (Transport Layer Security) for all communications. Do not allow cleartext HTTP traffic.
- **Android:** Use Network Security Configuration to enforce HTTPS.
- **iOS:** Ensure App Transport Security (ATS) is enabled and `NSAllowsArbitraryLoads` is NOT set to true globally without strict justification.
- **Flutter:** Enforce certificate pinning via `http` client configuration.
- Properly validate server certificates; do not ignore TLS errors or use insecure TLS configurations.

### Applies When
- The app communicates over the network.

### Validation
- Standard testing procedures per MASTG

### Failure Impact
- Security compromise related to this control

---

# Rule ID: MASVS-NETWORK-2
## Title: Identity Pinning
**Category:** Network Communication  

### Rule
The app performs identity pinning for all remote endpoints under the developer's control.
- Implement certificate or public key pinning to prevent Man-in-the-Middle (MitM) attacks even if a root CA is compromised or a user installs a malicious profile.
- Have a strategy for pin rotation and updates to avoid app breakage when certificates expire.

### Applies When
- The app handles highly sensitive data and communicates with known backends.

### Validation
- Standard testing procedures per MASTG

### Failure Impact
- Security compromise related to this control

---

# Rule ID: MASVS-PLATFORM-1
## Title: Secure IPC Mechanisms
**Category:** Platform Interaction  

### Rule
The app uses IPC mechanisms securely.
- **Android:** Secure Intents, Broadcast Receivers, Content Providers, and Services. Explicitly set `android:exported="false"` unless external access is required. Validate incoming intents and data.
- **iOS:** Secure custom URL schemes and Universal Links. Validate data received via IPC.
- **Verification:** Implement App Links (Android) with `android:autoVerify` and `assetlinks.json`, and Universal Links (iOS) with AASA files to prevent deep link hijacking.
- **Flutter:** Validate and authorize platform-channel messages.

### Applies When
- The app exposes activities, intents, deep links, or IPC components.

### Validation
- Standard testing procedures per MASTG

### Failure Impact
- Security compromise related to this control

---

# Rule ID: MASVS-PLATFORM-2
## Title: Secure WebViews
**Category:** Platform Interaction  

### Rule
The app uses WebViews securely.
- Disable JavaScript if not needed.
- If JavaScript is required, carefully control JavaScript bridges (e.g., `@JavascriptInterface` on Android) to prevent XSS or unauthorized access to native device functionality.
- Do not load untrusted content in WebViews that have access to sensitive native APIs.

### Applies When
- WebViews are used within the app.

### Validation
- Standard testing procedures per MASTG

### Failure Impact
- Security compromise related to this control

---

# Rule ID: MASVS-PLATFORM-3
## Title: Secure User Interface (UI)
**Category:** Platform Interaction  

### Rule
The app uses the user interface securely.
- Prevent sensitive data (passwords, OTPs, financial data) from being unintentionally leaked via platform mechanisms like auto-generated screenshots in the app switcher (background screens).
- Protect against screen recording or mirroring of sensitive screens where possible.

### Applies When
- The app displays highly sensitive information on screen.

### Validation
- Standard testing procedures per MASTG

### Failure Impact
- Security compromise related to this control

---

# Rule ID: MASVS-CODE-1
## Title: Require Up-to-Date Platform Version
**Category:** Code Quality  

### Rule
The app requires an up-to-date platform version.
- Set a minimum SDK/OS version (minSdk >= 29 / Android 10 required) that still receives security patches. Note: cleartext blocked by default from API 28+; Network Security Config from API 24+.

### Applies When
- Defining the target deployment platforms for the app.

### Validation
- Standard testing procedures per MASTG

### Failure Impact
- Security compromise related to this control

---

# Rule ID: MASVS-CODE-2
## Title: Enforce App Updates
**Category:** Code Quality  

### Rule
The app has a mechanism for enforcing app updates.
- Implement a forced-update mechanism to block usage of obsolete app versions when a critical vulnerability is patched.

### Applies When
- Designing the app lifecycle and backend API versioning strategy.

### Validation
- Standard testing procedures per MASTG

### Failure Impact
- Security compromise related to this control

---

# Rule ID: MASVS-CODE-3
## Title: Avoid Vulnerable Components
**Category:** Code Quality  

### Rule
The app only uses software components without known vulnerabilities.
- Perform Software Composition Analysis (SCA) on all third-party SDKs, libraries, and dependencies.
- Keep all dependencies updated to their secure versions.

### Applies When
- Integrating external libraries, SDKs, or open-source components.

### Validation
- Standard testing procedures per MASTG

### Failure Impact
- Security compromise related to this control

---

# Rule ID: MASVS-CODE-4
## Title: Input Validation and Sanitization
**Category:** Code Quality  

### Rule
The app validates and sanitizes all untrusted inputs.
- Validate data coming from the UI, IPC, Deep Links, the network, or the file system.
- Prevent classic injection attacks (SQL injection in local SQLite, XSS in WebViews, insecure deserialization) and logic bypasses.

### Applies When
- The app accepts external, untrusted, or user-provided input.

### Validation
- Standard testing procedures per MASTG

### Failure Impact
- Security compromise related to this control

---

# Rule ID: MASVS-RESILIENCE-1
## Title: Validate Platform Integrity
**Category:** Resilience  

### Rule
The app validates the integrity of the platform.
- Detect if the device is rooted (Android) or jailbroken (iOS) to ensure OS-level security features (like the Keystore/Keychain and sandboxing) can be trusted.
- Respond appropriately (e.g., warn the user, block access, or wipe sensitive data) based on the app's risk profile.

### Applies When
- ONLY for L2/\'R\' profile apps (financial, health, DRM, anti-cheat, or high-value intellectual property).

### Validation
- Standard testing procedures per MASTG

### Failure Impact
- Security compromise related to this control

---

# Rule ID: MASVS-RESILIENCE-2
## Title: Implement Anti-Tampering
**Category:** Resilience  

### Rule
The app implements anti-tampering mechanisms.
- Detect if the app has been modified or resigned.
- Verify the integrity of the app's code and resources at runtime to prevent unauthorized modifications or repackaging.

### Applies When
- ONLY for L2/\'R\' profile apps (financial, health, DRM, anti-cheat, or high-value intellectual property).

### Validation
- Standard testing procedures per MASTG

### Failure Impact
- Security compromise related to this control

---

# Rule ID: MASVS-RESILIENCE-3
## Title: Anti-Static Analysis Mechanisms
**Category:** Resilience  

### Rule
The app implements anti-static analysis mechanisms.
- Use code obfuscation, string encryption, and control flow obfuscation to make reverse engineering difficult.
- Use tools like ProGuard/R8 (Android) and ensure debug symbols are stripped.
- **Flutter:** Use `--obfuscate --split-debug-info` for Dart code.

### Applies When
- ONLY for L2/\'R\' profile apps (financial, health, DRM, anti-cheat, or high-value intellectual property).

### Validation
- Standard testing procedures per MASTG

### Failure Impact
- Security compromise related to this control

---

# Rule ID: MASVS-RESILIENCE-4
## Title: Anti-Dynamic Analysis Techniques
**Category:** Resilience  

### Rule
The app implements anti-dynamic analysis techniques.
- Detect debuggers, emulators, and dynamic instrumentation frameworks (like Frida or Xposed).
- Terminate or alter behavior if dynamic analysis is detected.

### Applies When
- ONLY for L2/\'R\' profile apps (financial, health, DRM, anti-cheat, or high-value intellectual property).

### Validation
- Standard testing procedures per MASTG

### Failure Impact
- Security compromise related to this control

---

# Rule ID: MASVS-PRIVACY-1
## Title: Minimize Data Access
**Category:** Privacy  

### Rule
The app minimizes access to sensitive data and resources.
- Request only the permissions absolutely necessary for functionality.
- Require informed user consent.
- Enforce that third-party SDKs operate strictly on user consent and do not collect data by default.
- Monitor and restrict third-party SDK network exfiltration behaviors.

### Applies When
- The app requests device permissions, location, contacts, or collects user data.

### Validation
- Standard testing procedures per MASTG

### Failure Impact
- Security compromise related to this control

---

# Rule ID: MASVS-PRIVACY-2
## Title: Prevent Identification of the User
**Category:** Privacy  

### Rule
The app prevents identification of the user where possible.
- Use data abstraction, anonymization, and pseudonymization to prevent tracking.
- Do not repurpose complex device signals (like device IDs or behavioral patterns) collected for fraud detection for marketing or analytics.

### Applies When
- Designing telemetry, analytics, and tracking features.

### Validation
- Standard testing procedures per MASTG

### Failure Impact
- Security compromise related to this control

---

# Rule ID: MASVS-PRIVACY-3
## Title: Transparent Data Collection
**Category:** Privacy  

### Rule
The app is transparent about data collection and usage.
- Provide clear information about data collection, storage, and sharing practices.
- Disclose background data collection clearly. Adhere to Apple/Google privacy declaration guidelines.

### Applies When
- Planning the app's privacy policy and App Store/Play Store privacy labels.

### Validation
- Standard testing procedures per MASTG

### Failure Impact
- Security compromise related to this control

---

# Rule ID: MASVS-PRIVACY-4
## Title: User Control Over Data
**Category:** Privacy  

### Rule
The app offers user control over their data.
- Provide mechanisms for users to manage, delete, and modify their data, and change privacy settings (revoke consent).
- Re-prompt for consent if more data is required than initially specified.

### Applies When
- Designing account management and privacy settings workflows.

### Validation
- Standard testing procedures per MASTG

### Failure Impact
- Security compromise related to this control

