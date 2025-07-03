# Configuration file for the Sphinx documentation builder.
import os
import sys
from pathlib import Path

project_root = Path(__file__).parent.parent  # Goes up two levels from docs/conf.py to project root
src_path = project_root / "src"
sys.path.insert(0, str(project_root))
sys.path.insert(0, str(src_path))


# -- Project information -----------------------------------------------------

project = 'STOCK PORTFOLIO MANAGER'
copyright = '2025, alexene22'
author = 'alexene22'
release = '1.0.0'

# -- General configuration ---------------------------------------------------
extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.viewcode'  
]

templates_path = ['_templates']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']

# -- Options for HTML output -------------------------------------------------
html_theme = 'alabaster'
html_static_path = ['_static']
