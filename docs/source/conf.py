"""Sphinx configuration for the package's guides, API and examples."""

import importlib
import inspect
import os
import re
import sys
from pathlib import Path
from urllib.parse import quote

PROJECT_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(PROJECT_ROOT / "src"))
package = importlib.import_module("travelwhiz_dl")
project = "travelwhiz-dl"
author = "James Hulse"
copyright = "2026, " + author
version = release = str(package.__version__)

extensions = [
    "sphinx.ext.autodoc", "sphinx.ext.autosummary", "sphinx.ext.napoleon",
    "sphinx.ext.intersphinx", "sphinx.ext.linkcode", "sphinx.ext.todo",
    "sphinx.ext.doctest", "sphinx.ext.duration", "sphinx.ext.autosectionlabel",
    "sphinx_gallery.gen_gallery",
]
root_doc = "index"
templates_path = ["_templates", "_templates/autosummary"]
exclude_patterns = []
autosummary_generate = True
autosummary_imported_members = True
autosectionlabel_prefix_document = True
modindex_common_prefix = ["travelwhiz_dl."]
autosummary_context = {
    "include_inherited_methods": False,
    "include_inherited_attributes": False,
    "show_inherited": [],
    "exclude_inherited": [],
}
autodoc_member_order = "groupwise"
autodoc_typehints = "description"
autoclass_content = "class"
autodoc_default_options = {
    "undoc-members": True,
    "show-inheritance": True,
    "special-members": False,
    "private-members": False,
    "exclude-members": "__dict__, __module__, __weakref__",
}
napoleon_numpy_docstring = True
napoleon_google_docstring = False
numpydoc_show_class_members = False
intersphinx_mapping = {"python": ("https://docs.python.org/3", None)}
intersphinx_timeout = 30
todo_include_todos = os.getenv("SPHINX_INCLUDE_TODOS", "true").strip().lower() in {
    "true", "yes", "y", "t", "1",
}
todo_emit_warnings = True
sphinx_gallery_conf = {
    "examples_dirs": "../../examples",
    "gallery_dirs": "_generated/examples",
    "backreferences_dir": "_generated/examples/backrefs",
    "doc_module": ("travelwhiz_dl",),
    "filename_pattern": rf"{re.escape(os.sep)}run_.*\.py",
}

html_theme = "pydata_sphinx_theme"
html_static_path = ["_static"]
html_css_files = ["css/logo.css"]
html_show_sourcelink = False
html_theme_options = {
    "logo": {"text": f"{project} {version}", "alt_text": project},
    "use_edit_page_button": True,
    "header_links_before_dropdown": 3,
    "icon_links": [{
        "name": "GitHub", "url": "https://github.com/hulsiejames/travelwhiz-dl",
        "icon": "fa-brands fa-github", "type": "fontawesome",
    }],
    "external_links": [
        {"name": "Releases", "url": "https://github.com/hulsiejames/travelwhiz-dl/releases"},
        {"name": "Issues", "url": "https://github.com/hulsiejames/travelwhiz-dl/issues"},
        {"name": "GitHub Account", "url": "https://github.com/hulsiejames"},
    ],
    "primary_sidebar_end": ["indices.html", "sidebar-ethical-ads.html"],
    "announcement": (
        'These guides are being developed. Suggestions are welcome on the '
        '<a href="https://github.com/hulsiejames/travelwhiz-dl/issues">issue tracker</a>.'
    ),
}
html_context = {
    "github_url": "https://github.com", "github_user": "hulsiejames",
    "github_repo": "travelwhiz-dl", "github_version": "main",
    "doc_path": "docs/source",
}


def linkcode_resolve(domain: str, info: dict) -> str | None:
    """Link an API object to its source lines within this repository."""
    if domain != "py" or not info.get("module"):
        return None
    try:
        obj = importlib.import_module(info["module"])
        for part in info.get("fullname", "").split("."):
            if part:
                obj = getattr(obj, part)
        obj = inspect.unwrap(obj)
        if isinstance(obj, property):
            obj = obj.fget
        filename = inspect.getsourcefile(obj)
        if filename is None:
            return None
        relative = Path(filename).resolve().relative_to(PROJECT_ROOT).as_posix()
        lines, start = inspect.getsourcelines(obj)
    except (ImportError, AttributeError, TypeError, OSError, ValueError):
        return None
    revision = "main" if "+" in version else "v" + version
    return (
        "https://github.com/hulsiejames/travelwhiz-dl/blob/" + quote(revision, safe="")
        + "/" + quote(relative, safe="/") + f"#L{start}-L{start + len(lines) - 1}"
    )
