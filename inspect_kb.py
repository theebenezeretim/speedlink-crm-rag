from pathlib import Path

KB_PATH = Path("data/speedlink_crm_knowledge_base.md")

content = KB_PATH.read_text(encoding="utf-8")

print("Knowledge base loaded successfully.")
print(f"Characters: {len(content):,}")
print(f"Lines: {len(content.splitlines()):,}")

print("\n--- MAIN SECTIONS ---")

for line in content.splitlines():
    if line.startswith("# "):
        print(line)