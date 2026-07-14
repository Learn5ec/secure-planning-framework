#!/usr/bin/env python3
import json
import os
import re
import sys
from collections import defaultdict
import subprocess

def check_orphans():
    repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    
    # Load rule_index.json
    index_path = os.path.join(repo_root, 'meta', 'rule_index.json')
    with open(index_path, 'r') as f:
        index_data = json.load(f)
        
    # Load tag_index.json
    tag_path = os.path.join(repo_root, 'meta', 'tag_index.json')
    with open(tag_path, 'r') as f:
        tag_data = json.load(f)
    
    indexed_rules = set()
    for cat, blocks in index_data.items():
        if cat.startswith('_'):
            continue
        if 'rules' in blocks:
            indexed_rules.update(blocks['rules'])
        for key, arr in blocks.items():
            if isinstance(arr, list) and key != 'triggers':
                indexed_rules.update(arr)
                
    tag_rules = set()
    for theme, rules in tag_data.get('security_themes', {}).items():
        tag_rules.update(rules)
    for cat, rules in tag_data.get('rule_categories', {}).items():
        tag_rules.update(rules)
    for theme, rules in tag_data.get('privacy_compliance', {}).items():
        tag_rules.update(rules)
    
    # Find all Markdown files in rule dirs
    rule_dirs = ['common', 'domains', 'compliance', 'cwe']
    
    # For duplicate checking
    rule_to_files = defaultdict(list)
    found_rules = set()
    
    for d in rule_dirs:
        dir_path = os.path.join(repo_root, d)
        for root, _, files in os.walk(dir_path):
            for file in files:
                if file.endswith('.md'):
                    file_path = os.path.join(root, file)
                    with open(file_path, 'r') as f:
                        content = f.read()
                        # Match "# Rule ID: <RULE-ID>" or "## CWE-<ID>"
                        matches = set(re.findall(r'^#+ (?:Rule ID: )?((?:COM|OWASP|API|MASVS|ASI|LLM-GOV|MCP|CWE|DPDP)-[A-Z0-9-]+)', content, re.MULTILINE))
                        for match in matches:
                            # We only care about the file name for reporting
                            rel_path = os.path.relpath(file_path, repo_root)
                            # slim_core.md is allowed to duplicate rules since it's a generated subset.
                            if not rel_path.endswith('slim_core.md'):
                                rule_to_files[match].append(rel_path)
                            found_rules.add(match)
    
    success = True
    
    orphans = found_rules - indexed_rules
    missing = indexed_rules - found_rules
    
    if orphans:
        print(f"::error::Found {len(orphans)} orphaned rules defined in Markdown but missing from rule_index.json: {', '.join(orphans)}")
        success = False
        
    if missing:
        print(f"::warning::Found rules in index that are missing from Markdown: {', '.join(missing)}")
        
    # Check 1: Duplicate rule IDs (except slim_core.md)
    duplicates = {rule: files for rule, files in rule_to_files.items() if len(files) > 1}
    if duplicates:
        print(f"::error::Found duplicate rule definitions across files:")
        for rule, files in duplicates.items():
            print(f"  - {rule}: {', '.join(files)}")
        success = False
        
    # Check 2: tag_index validation
    invalid_tags = tag_rules - found_rules
    if invalid_tags:
        print(f"::error::Found rules in tag_index.json that are missing from Markdown: {', '.join(invalid_tags)}")
        success = False

    # Check 3: output_example.json against output_schema.json
    try:
        schema_path = os.path.join(repo_root, 'core', 'output_schema.json')
        example_path = os.path.join(repo_root, 'core', 'output_example.json')
        import jsonschema
        with open(schema_path, 'r') as sf, open(example_path, 'r') as ef:
            schema = json.load(sf)
            example = json.load(ef)
            jsonschema.validate(instance=example, schema=schema)
    except ImportError:
        print("::warning::jsonschema not installed, skipping schema validation")
    except Exception as e:
        print(f"::error::Schema validation failed for output_example.json: {e}")
        success = False
    
    if not success:
        sys.exit(1)
    print("Rule index and schema integrity checks passed.")

if __name__ == '__main__':
    check_orphans()
