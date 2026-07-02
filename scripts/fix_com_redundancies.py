#!/usr/bin/env python3
import os
import re

repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
common_path = os.path.join(repo_root, "common/common-considerations.md")

with open(common_path, 'r') as f:
    content = f.read()

def replace_rule(rule_id, new_content):
    global content
    pattern = re.compile(rf'(# Rule ID: {rule_id}\n.*?### Failure Impact\n.*?)\n---', re.DOTALL)
    content = pattern.sub(new_content + '\n---', content)

# COM-010
replace_rule("COM-010", """# Rule ID: COM-010
## Title: Enforce Token Expiry and Invalidation (Superseded)

**Category:** Session Management  

### Rule
*This rule has been superseded.* Please refer to the canonical session/token lifecycle rule: **COM-039**.

### Applies When
- Token-based auth

### Validation
- See COM-039

### Failure Impact
- Session hijacking
""")

# COM-015
replace_rule("COM-015", """# Rule ID: COM-015
## Title: Prevent Long-Lived Tokens (Superseded)

**Category:** Session Security  

### Rule
*This rule has been superseded.* Please refer to the canonical session/token lifecycle rule: **COM-039**.

### Applies When
- Token-based auth

### Validation
- See COM-039

### Failure Impact
- Persistent compromise
""")

# COM-022
replace_rule("COM-022", """# Rule ID: COM-022
## Title: Prevent Session Fixation (Superseded)

**Category:** Session Management  

### Rule
*This rule has been superseded.* Please refer to the canonical session/token lifecycle rule: **COM-039**.

### Applies When
- Session creation

### Validation
- See COM-039

### Failure Impact
- Session fixation
""")

# COM-025
replace_rule("COM-025", """# Rule ID: COM-025
## Title: Validate JWT Claims (Superseded)

**Category:** Authentication  

### Rule
*This rule has been superseded.* Please refer to the canonical session/token lifecycle rule: **COM-039** and **COM-040**.

### Applies When
- JWT validation

### Validation
- See COM-039, COM-040

### Failure Impact
- Authentication bypass
""")

with open(common_path, 'w') as f:
    f.write(content)

print("Fixed COM redundancies.")
