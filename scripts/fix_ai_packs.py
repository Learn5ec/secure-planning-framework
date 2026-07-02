#!/usr/bin/env python3
import os

repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def fix_ai_packs():
    print("Fixing AI packs...")
    
    # 1. ASI-06 typo
    asi_path = os.path.join(repo_root, "domains/ai/agentic_ai_rules.md")
    with open(asi_path, 'r') as f:
        asi_content = f.read()
    asi_content = asi_content.replace("Auto-Reingestiom", "Auto-Reingestion")
    with open(asi_path, 'w') as f:
        f.write(asi_content)
        
    # 2. LLM-GOV-002 and LLM-GOV-008
    llm_path = os.path.join(repo_root, "domains/ai/llm_governance_rules.md")
    with open(llm_path, 'r') as f:
        llm_content = f.read()
    llm_content = llm_content.replace(
        "Only 37% of organizations have policies to manage or detect Shadow AI — this is a critical gap.",
        "Only 37% of organizations have policies to manage or detect Shadow AI (Source: 2024 industry survey) — this is a critical gap."
    )
    llm_content = llm_content.replace(
        "**DORA (EU, financial entities)**: Four-hour notification requirement for major ICT incidents including AI-related failures.",
        "> **INFORMATIONAL:** DORA sets phased notification windows for major incidents (e.g., initial notification by end of business day), not a flat 4-hour rule."
    )
    with open(llm_path, 'w') as f:
        f.write(llm_content)
        
    # 3. MCP resource/prompt poisoning
    mcp_path = os.path.join(repo_root, "domains/mcp/mcp_server_rules.md")
    with open(mcp_path, 'r') as f:
        mcp_content = f.read()
        
    mcp_content = mcp_content.replace(
        "Adding or updating any tool description or functionality requires:",
        "Adding or updating any tool description, prompt, or resource requires:"
    )
    
    mcp_content = mcp_content.replace(
        "Maintain and audit all fields of each tool.",
        "Maintain and audit all fields of each tool, prompt, and resource."
    )
    
    with open(mcp_path, 'w') as f:
        f.write(mcp_content)
        
    # 4. Provenance qualifier on AI/MCP sources dated >= Dec 2025
    for file_path in [asi_path, llm_path, mcp_path]:
        with open(file_path, 'r') as f:
            content = f.read()
        if "December 2025" in content or "Feb 2026" in content or "Oct 2025" in content:
            # We insert a qualifier after the sources
            content = content.replace(
                "**Sources:**",
                "**Sources:** (Provisional/draft — verify against genai.owasp.org before citing externally)\n"
            )
            content = content.replace(
                "**Source:** OWASP",
                "**Source:** (Provisional/draft — verify against genai.owasp.org) OWASP"
            )
        with open(file_path, 'w') as f:
            f.write(content)
            
    # 5. Delete cheatsheets
    import shutil
    try:
        shutil.rmtree(os.path.join(repo_root, "knowledge/ai"))
    except:
        pass
    try:
        shutil.rmtree(os.path.join(repo_root, "knowledge/mobile"))
    except:
        pass

if __name__ == '__main__':
    fix_ai_packs()
