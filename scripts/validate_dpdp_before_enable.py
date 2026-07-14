#!/usr/bin/env python3
import os
import re
import sys

def validate_dpdp():
    repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    dpdp_dir = os.path.join(repo_root, 'compliance', 'dpdp')
    
    files_to_check = [
        os.path.join(dpdp_dir, 'dpdp_rules.md'),
        os.path.join(dpdp_dir, 'dpdpa-compliance.md')
    ]
    
    rules = {}
    for fp in files_to_check:
        if os.path.exists(fp):
            with open(fp, 'r') as f:
                content = f.read()
                parts = content.split('# Rule ID: ')
                for part in parts[1:]:
                    rule_id = part.split('\n')[0].strip()
                    rules[rule_id] = part

    success = True
    
    if 'DPDP-019' in rules:
        if 'allowlist' not in rules['DPDP-019'].lower():
            print("::error::DPDP-019 missing 'allowlist' transfer model.")
            success = False
            
    if 'DPDP-016' in rules:
        if '18' not in rules['DPDP-016']:
            print("::error::DPDP-016 missing '18' threshold.")
            success = False
            
    for rid in ['DPDP-007', 'DPDP-021']:
        if rid in rules:
            if 'data protection board' not in rules[rid].lower():
                print(f"::error::{rid} missing 'Data Protection Board' reference.")
                success = False

    for rid, content in rules.items():
        m = re.search(r'\*\*Source:\*\*\s*(.+)', content)
        if m:
            source_text = m.group(1)
            if not re.search(r'\d', source_text):
                print(f"::error::{rid} Source field lacks section numbers: '{source_text}'")
                success = False
                
    if not success:
        sys.exit(1)
        
    print("DPDP rules are ready to be enabled.")

if __name__ == '__main__':
    validate_dpdp()
