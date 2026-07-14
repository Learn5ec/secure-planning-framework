#!/usr/bin/env python3
import os
import re

repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Define tiers for each rule
tiers = {
    # Agentic AI
    "ASI-01": "baseline",
    "ASI-02": "baseline",
    "ASI-03": "elevated",
    "ASI-04": "high-assurance",
    "ASI-05": "baseline",
    "ASI-06": "elevated",
    "ASI-07": "high-assurance",
    "ASI-08": "high-assurance",
    "ASI-09": "elevated",
    "ASI-10": "high-assurance",
    
    # LLM Governance
    "LLM-GOV-001": "baseline",
    "LLM-GOV-002": "elevated",
    "LLM-GOV-003": "baseline",
    "LLM-GOV-004": "high-assurance",
    "LLM-GOV-005": "elevated",
    "LLM-GOV-006": "elevated",
    "LLM-GOV-007": "baseline",
    "LLM-GOV-008": "elevated",
    "LLM-GOV-009": "baseline",
    
    # MCP Server
    "MCP-001": "baseline",
    "MCP-002": "high-assurance",
    "MCP-003": "baseline",
    "MCP-004": "baseline",
    "MCP-005": "elevated",
    "MCP-006": "high-assurance",
    "MCP-007": "elevated"
}

files_to_update = [
    "domains/ai/agentic_ai_rules_baseline.md",
    "domains/ai/agentic_ai_rules_extended.md",
    "domains/ai/llm_governance_rules_baseline.md",
    "domains/ai/llm_governance_rules_extended.md",
    "domains/mcp/mcp_server_rules_baseline.md",
    "domains/mcp/mcp_server_rules_extended.md"
]

def update_file(filepath):
    full_path = os.path.join(repo_root, filepath)
    with open(full_path, 'r') as f:
        content = f.read()
    
    # We will process rule by rule
    # Find all Rule IDs
    def replacer(match):
        rule_id = match.group(2)
        tier = tiers.get(rule_id, "elevated")
        
        # Replace Category with Category + Risk Tier
        block = match.group(0)
        
        # Replace existing Risk Tier or add it
        if "**Risk Tier:**" in block:
            block = re.sub(
                r'\*\*Risk Tier:\*\* .*?\n',
                r'**Risk Tier:** ' + tier + r'\n',
                block
            )
        else:
            block = re.sub(
                r'(\*\*Category:\*\*.*?\n)', 
                r'\1**Risk Tier:** ' + tier + r'\n', 
                block
            )
            
        # Replace Mandatory Controls: with Scale-with-Risk Controls: for non-baseline
        # or Baseline Controls: for baseline
        if tier == "baseline":
            block = block.replace("**Mandatory Controls:**", "**Baseline Controls:**")
            block = block.replace("**Mandatory Checks:**", "**Baseline Checks:**")
        else:
            block = block.replace("**Mandatory Controls:**", "**Controls (Scale with Risk):**")
            block = block.replace("**Mandatory Checks:**", "**Checks (Scale with Risk):**")
            block = block.replace("**Mandatory Client Controls:**", "**Client Controls (Scale with Risk):**")
        
        return block

    # Match from "# Rule ID: " up to the next "# Rule ID: " or end of file
    new_content = re.sub(
        r'(# Rule ID: ([\w-]+).*?(?=\n# Rule ID: |\Z))',
        replacer,
        content,
        flags=re.DOTALL
    )
    
    with open(full_path, 'w') as f:
        f.write(new_content)
    print(f"Updated {filepath}")

for f in files_to_update:
    update_file(f)
