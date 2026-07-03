import os
import sys
import configparser
from datetime import datetime

from PyQt6.QtCore import QCoreApplication, Qt
from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QMessageBox, QProgressDialog, QApplication
import mobase


class ModListExportedMd(mobase.IPluginTool):

    def __init__(self):
        super().__init__()
        self.__organizer = None
        self.__parentWidget = None

    def init(self, organizer):
        self.__organizer = organizer
        return True

    def name(self):
        return "ModListExportedMd"

    def localizedName(self):
        return self.tr("ModListExportedMd")

    def author(self):
        return "mo2-modlist-exported-md"

    def description(self):
        return self.tr("Exports all mods to an LLM-readable Markdown report for troubleshooting and optimisation analysis.")

    def version(self):
        return mobase.VersionInfo(1, 0, 0, 0)

    def settings(self):
        return []

    def displayName(self):
        return self.tr("Export Mod List for LLM")

    def tooltip(self):
        return self.tr("Generates a Markdown report of every mod with metadata for LLM analysis.")

    def icon(self):
        return QIcon()

    def setParentWidget(self, widget):
        self.__parentWidget = widget

    def display(self):
        plugin_dir = os.path.dirname(os.path.abspath(__file__))
        mo_root = os.path.dirname(plugin_dir)
        output_path = os.path.join(mo_root, "modlist_llm_report.md")
        self._generate_report(output_path)

    def tr(self, text):
        return QCoreApplication.translate("ModListExportedMd", text)

    def _generate_report(self, output_path):
        game = self.__organizer.managedGame()
        profile = self.__organizer.profile()
        modlist = self.__organizer.modList()

        all_mod_names = modlist.allModsByProfilePriority()
        total = len(all_mod_names)

        progress = QProgressDialog(
            self.tr("Scanning mods..."), self.tr("Cancel"), 0, total, self.__parentWidget
        )
        progress.setWindowTitle(self.tr("ModListExportedMd"))
        progress.setWindowModality(Qt.WindowModality.WindowModal)
        progress.setMinimumDuration(0)
        progress.show()

        mods_active = []
        mods_inactive = []
        separators = []

        for priority, mod_name in enumerate(all_mod_names):
            if progress.wasCanceled():
                progress.close()
                return

            progress.setLabelText(
                self.tr("Scanning: {0} ({1}/{2})").format(mod_name, priority + 1, total)
            )
            progress.setValue(priority)
            QApplication.processEvents()

            mod = modlist.getMod(mod_name)
            if not mod:
                continue

            mod_path = mod.absolutePath()
            meta = self._read_meta(mod_path)

            entry = {
                "name": mod_name,
                "priority": priority,
                "separator": mod.isSeparator(),
                "meta": meta,
            }

            state = modlist.state(mod_name)
            if mod.isSeparator():
                separators.append(entry)
            elif state & mobase.ModState.ACTIVE:
                mods_active.append(entry)
            else:
                mods_inactive.append(entry)

        with open(output_path, "w", encoding="utf-8") as f:
            f.write("# Mod List Report\n\n")
            f.write(f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            f.write(f"**Game:** {game.gameName()}\n")
            f.write(f"**Profile:** {profile.name()}\n\n")

            f.write("## Summary\n\n")
            f.write(f"| Metric | Count |\n")
            f.write(f"|---|---|\n")
            f.write(f"| Total mods | {total} |\n")
            f.write(f"| Active | {len(mods_active)} |\n")
            f.write(f"| Inactive | {len(mods_inactive)} |\n")
            f.write(f"| Separators | {len(separators)} |\n\n")

            f.write("## Active Mods (ordered by priority)\n\n")
            self._write_mod_entries(f, mods_active)

            if mods_inactive:
                f.write("\n---\n\n## Inactive Mods\n\n")
                self._write_mod_entries(f, mods_inactive)

            if separators:
                f.write("\n---\n\n## Separators\n\n")
                for sep in separators:
                    f.write(f"- {sep['name']}\n")
                f.write("\n")

            f.write("\n---\n\n## End of Report\n")

        progress.setValue(total)
        progress.close()

        file_size = os.path.getsize(output_path) // 1024
        QMessageBox.information(
            self.__parentWidget,
            self.tr("Export Complete"),
            self.tr(
                "Report saved to:\n{0}\n\n"
                "{1} active  \u00b7  {2} inactive  \u00b7  {3} separators\n"
                "Size: {4} KB"
            ).format(
                output_path,
                len(mods_active),
                len(mods_inactive),
                len(separators),
                file_size,
            ),
        )

    def _write_mod_entries(self, f, mods):
        for entry in mods:
            m = entry["meta"]

            f.write(f"### #{entry['priority']}: {entry['name']}\n\n")
            f.write(f"- **Status:** Active\n")

            if m:
                if m.get("version"):
                    f.write(f"- **Version:** {m['version']}\n")
                if m.get("modid"):
                    f.write(f"- **Nexus Mod ID:** {m['modid']}\n")
                if m.get("category"):
                    f.write(f"- **Nexus Category:** {m['category'].strip('\" ')}\n")
                if m.get("notes"):
                    f.write(f"- **Notes:** {m['notes']}\n")
            else:
                f.write("- **Metadata:** none\n")

            f.write("\n")

    def _read_meta(self, mod_path):
        meta_path = os.path.join(mod_path, "meta.ini")
        if not os.path.isfile(meta_path):
            return None
        try:
            cfg = configparser.ConfigParser()
            cfg.read(meta_path, encoding="utf-8")
            result = {}
            if cfg.has_section("General"):
                for key in cfg.options("General"):
                    result[key] = cfg.get("General", key)
            return result
        except Exception:
            return None


def createPlugin():
    return ModListExportedMd()
