#!/usr/bin/env python3
import os

repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def fix_file(path, replacements):
    full_path = os.path.join(repo_root, path)
    if not os.path.exists(full_path):
        return
    with open(full_path, 'r') as f:
        content = f.read()
    for old, new in replacements:
        content = content.replace(old, new)
    with open(full_path, 'w') as f:
        f.write(content)

def main():
    # SKILL.md
    fix_file("SKILL.md", [
        ("Fires automatically on every task unless the user explicitly opts out by saying \"Do not use SPF skill\" (SPF = Secure Planning Framework).",
         "Fires automatically on every feature planning task. Do NOT use while writing, fixing, or refactoring code. To suppress, explicitly state \"Do not use SPF skill\" (SPF = Secure Planning Framework)."),
        ("This skill is **always-on** — it fires on every planning and development task by default.",
         "This skill is **always-on for planning** — it fires on every feature planning task by default.\n\n**Exclusion:** Do NOT use this skill while writing, fixing, or refactoring code."),
        ("Your task is to enforce security and compliance requirements at the **planning and development phase** of software development.",
         "Your task is to enforce security and compliance requirements at the **planning phase** of software development (not implementation/coding).")
    ])

    # Changelog 1
    fix_file("reference-and-planning-docs/improvement-plan.md", [
        ("The SPF skill fires **by default on every plan/development task**.",
         "The SPF skill fires **by default on every planning task**.")
    ])

    # V2 Post Audit Changelog
    fix_file("brain/50e2b3c4-299a-4294-85dc-0e66f8a39a87/v2_0_post_audit_changelog.md", [
        ("The framework now fires automatically on *every* planning and development task.",
         "The framework now fires automatically on *every* planning task. It remains dormant during coding, fixing, or refactoring.")
    ])

    # Sprint 4-6 Changelog
    fix_file("brain/50e2b3c4-299a-4294-85dc-0e66f8a39a87/sprint_4_to_6_changelog.md", [
        ("fires on every planning and development task",
         "fires on every planning task")
    ])

if __name__ == "__main__":
    main()
