#!/usr/bin/env python3
import json
import os
import re
import sys

def check_orphans():
    repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    
    # Load rule_index.json
    index_path = os.path.join(repo_root, 'meta', 'rule_index.json')
    with open(index_path, 'r') as f:
        index_data = json.load(f)
    
    indexed_rules = set()
    for cat, blocks in index_data.items():
        if cat.startswith('_'):
            continue
        if 'rules' in blocks:
            indexed_rules.update(blocks['rules'])
        for key, arr in blocks.items():
            if isinstance(arr, list) and key != 'triggers':
                indexed_rules.update(arr)
    
    # Find all Markdown files in rule dirs
    rule_dirs = ['common', 'domains', 'compliance', 'cwe']
    found_rules = set()
    
    for d in rule_dirs:
        dir_path = os.path.join(repo_root, d)
        for root, _, files in os.walk(dir_path):
            for file in files:
                if file.endswith('.md'):
                    with open(os.path.join(root, file), 'r') as f:
                        content = f.read()
                        # Match "# Rule ID: <RULE-ID>" or "## CWE-<ID>"
                        matches = re.findall(r'^#+ (?:Rule ID: )?((?:COM|OWASP|API|MASVS|ASI|LLM-GOV|MCP|CWE|DPDP)-[A-Z0-9-]+)', content, re.MULTILINE)
                        found_rules.update(matches)
    
    orphans = found_rules - indexed_rules
    missing = indexed_rules - found_rules
    
    success = True
    if orphans:
        print(f"::error::Found {len(orphans)} orphaned rules defined in Markdown but missing from rule_index.json: {', '.join(orphans)}")
        success = False
    
    # We might have rules in index not in markdown if disabled or something, 
    # but ideally they should match.
    if missing:
        print(f"::warning::Found rules in index that are missing from Markdown: {', '.join(missing)}")
    
    if not success:
        sys.exit(1)
    print("Rule index integrity check passed.")

if __name__ == '__main__':
    check_orphans()
