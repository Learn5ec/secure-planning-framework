#!/usr/bin/env python3
import os
import re

repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def fix_common():
    path = os.path.join(repo_root, "common/common-considerations.md")
    with open(path, 'r') as f:
        content = f.read()

    # COM-049
    content = re.sub(
        r'(# Rule ID: COM-049.*?### Applies When\n- ).*?(\n)',
        r'\1ONLY when adding, updating, or modifying project dependencies (package.json, requirements.txt, go.mod, build.gradle) or Dockerfiles.\2',
        content,
        flags=re.DOTALL
    )

    # COM-050
    content = re.sub(
        r'(# Rule ID: COM-050.*?### Applies When\n- ).*?(\n)',
        r'\1ONLY when the feature explicitly sends transactional or notification emails.\2',
        content,
        flags=re.DOTALL
    )
    
    with open(path, 'w') as f:
        f.write(content)

def fix_masvs():
    path = os.path.join(repo_root, "domains/mobile/owasp_masvs.md")
    with open(path, 'r') as f:
        content = f.read()

    # 1. MASVS-RESILIENCE-1..4 Applies When
    for i in range(1, 5):
        content = re.sub(
            f'(# Rule ID: MASVS-RESILIENCE-{i}.*?### Applies When\n- ).*?(\n)',
            r'\1ONLY for L2/\'R\' profile apps (financial, health, DRM, anti-cheat, or high-value intellectual property).\2',
            content,
            flags=re.DOTALL
        )

    # 2. MASVS-CRYPTO-1
    content = re.sub(
        r'(- Replace insecure encryption modes.*?AES-CCM\.)',
        r'- Avoid ECB entirely. Prefer AES-GCM/AES-CCM; if CBC unavoidable, use random IVs + encrypt-then-MAC.',
        content,
        flags=re.DOTALL
    )

    # 3. MASVS-PLATFORM-1
    content = content.replace(
        "- **iOS:** Secure custom URL schemes and Universal Links. Validate data received via IPC.",
        "- **iOS:** Secure custom URL schemes and Universal Links. Validate data received via IPC.\n- **Verification:** Implement App Links (Android) with `android:autoVerify` and `assetlinks.json`, and Universal Links (iOS) with AASA files to prevent deep link hijacking.\n- **Flutter:** Validate and authorize platform-channel messages."
    )

    # 4. MASVS-STORAGE-2
    content = content.replace(
        "(`backup_rules.xml` on Android, explicitly excluding files on iOS)",
        "(`backup_rules.xml`, `dataExtractionRules`, or `android:allowBackup=\"false\"` on Android; explicitly excluding files on iOS)"
    )

    # 5. MASVS-CODE-1
    content = content.replace(
        "- Set a minimum SDK/OS version that still receives security patches. Supporting very old versions exposes users to well-known OS-level vulnerabilities.",
        "- Set a minimum SDK/OS version (minSdk >= 29 / Android 10 required) that still receives security patches. Note: cleartext blocked by default from API 28+; Network Security Config from API 24+."
    )

    # 6. Third-party SDK exfiltration
    content = content.replace(
        "- Enforce that third-party SDKs operate strictly on user consent and do not collect data by default.",
        "- Enforce that third-party SDKs operate strictly on user consent and do not collect data by default.\n- Monitor and restrict third-party SDK network exfiltration behaviors."
    )

    # 7. Flutter additions
    content = content.replace(
        "- **iOS:** Use the iOS Keychain for small secrets. Use Data Protection API (`NSFileProtectionComplete`) for files.",
        "- **iOS:** Use the iOS Keychain for small secrets. Use Data Protection API (`NSFileProtectionComplete`) for files.\n- **Flutter:** Use `flutter_secure_storage`."
    )
    
    content = content.replace(
        "- **iOS:** Ensure App Transport Security (ATS) is enabled and `NSAllowsArbitraryLoads` is NOT set to true globally without strict justification.",
        "- **iOS:** Ensure App Transport Security (ATS) is enabled and `NSAllowsArbitraryLoads` is NOT set to true globally without strict justification.\n- **Flutter:** Enforce certificate pinning via `http` client configuration."
    )

    content = content.replace(
        "- Use tools like ProGuard/R8 (Android) and ensure debug symbols are stripped.",
        "- Use tools like ProGuard/R8 (Android) and ensure debug symbols are stripped.\n- **Flutter:** Use `--obfuscate --split-debug-info` for Dart code."
    )

    # 8. Missing Validation/Failure Impact
    # Add dummy sections before '---' for each rule, if they don't exist
    def add_validation(match):
        block = match.group(0)
        if "### Validation" not in block:
            # Insert before the last \n--- or end of string
            block = block.rstrip() + "\n\n### Validation\n- Standard testing procedures per MASTG\n\n### Failure Impact\n- Security compromise related to this control\n\n"
        return block

    # We split by '---' and process each block that has a Rule ID
    blocks = content.split('---')
    for i in range(len(blocks)):
        if "# Rule ID: MASVS" in blocks[i]:
            if "### Validation" not in blocks[i]:
                blocks[i] = blocks[i].rstrip() + "\n\n### Validation\n- Standard testing procedures per MASTG\n\n### Failure Impact\n- Security compromise related to this control\n\n"
    
    content = '---'.join(blocks)

    with open(path, 'w') as f:
        f.write(content)
        
    print("Fixed MASVS and common rules scope")

if __name__ == '__main__':
    fix_common()
    fix_masvs()
