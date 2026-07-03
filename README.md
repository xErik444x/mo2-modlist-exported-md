# mo2-modlist-exported-md

A [Mod Organizer 2](https://www.nexusmods.com/skyrimspecialedition/mods/6194) plugin that exports your entire mod list to a clean Markdown file, ready to be fed to an LLM for troubleshooting, optimisation, or load-order review.

---

## How it works

This plugin adds an *Export Mod List for LLM* entry to the Tools menu inside MO2.  
When clicked, it iterates through every mod in your current profile, reads metadata from each mod's `meta.ini`, and writes a structured report (`modlist_llm_report.md`) to your MO2 root folder.

A progress dialog shows you what mod is being processed, and a final message box reports where the file was saved.

### What the report includes

- **Summary** — total mods, active, inactive, separators
- **Active Mods** (by priority) — mod name, version, Nexus Mod ID, Nexus category, and any user notes
- **Inactive Mods** — same info
- **Separators** — listed separately for reference

No file inventory, no conflict analysis, no bloat.  
Just the data an LLM needs to understand your mod setup.

### Example output

```markdown
# Mod List Report

**Generated:** 2026-07-02 22:30:00
**Game:** Skyrim Special Edition
**Profile:** Default

## Summary
| Metric | Count |
|---|---|
| Total mods | 207 |
| Active | 200 |
| Inactive | 4 |
| Separators | 3 |

## Active Mods

### #0: DynDOLOD Output
- **Status:** Active
- **Version:** 3.0.0.0

### #1: Address Library for SKSE Plugins
- **Status:** Active
- **Version:** 11.0.0.0
- **Nexus Mod ID:** 32444
- **Nexus Category:** 82
```

---

## Requirements

- Mod Organizer 2 (v2.5+ recommended)
- Python 3.12+ (bundled with MO2)

---

## Installation

1. Close Mod Organizer 2.
2. Copy the `ModListExportedMd` folder into your MO2 `plugins/` directory.  
   The final path should look like:  
   `.../Mod Organizer/plugins/ModListExportedMd/__init__.py`
3. Launch MO2, open the **Tools** menu, and click **Export Mod List for LLM**.

---

## Usage

1. In MO2, go to **Tools → Export Mod List for LLM**.
2. A progress dialog will appear showing each mod as it's scanned.
3. When finished, a popup tells you where the report was saved.
4. Open `modlist_llm_report.md` in your MO2 root folder and copy its contents into your favourite LLM.

---

## What to ask your LLM

Once you have the report, try prompts like:

- *"Review my mod list for known conflicts or outdated mods."*
- *"Check for missing compatibility patches based on what's installed."*
- *"Suggest performance optimisations or mods I should replace."*
- *"Analyse my load order for potential issues."*

---

## License

GNU General Public License v3.0
