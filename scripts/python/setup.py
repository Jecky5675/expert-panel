from __future__ import annotations
import shutil
from pathlib import Path
from setuptools import setup
from setuptools.command.build_py import build_py

class BuildPyWithSkill(build_py):
    def run(self):
        package = Path(self.build_lib)/"expert_panel_installer"
        super().run()
        if not (package/"skills"/"expert-panel"/"SKILL.md").is_file():
            raise RuntimeError("Staged Expert Panel payload is missing from the build tree")
        if not (package/"export_formats.py").is_file():
            raise RuntimeError("Staged format exporter is missing from the build tree")

setup(cmdclass={"build_py":BuildPyWithSkill})
