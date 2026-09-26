"""
Vercel Serverless Function entrypoint for SYNAPS FastAPI Backend.
Exposes the existing FastAPI application instance from backend/main.py.
"""

import sys
import types
from pathlib import Path

# Ensure project root and backend directory are in sys.path
_CURRENT_DIR = Path(__file__).resolve().parent   # backend/api
_BACKEND_DIR = _CURRENT_DIR.parent              # backend
_PROJECT_ROOT = _BACKEND_DIR.parent             # SYNAPS repo root

for _p in (_PROJECT_ROOT, _BACKEND_DIR):
    _p_str = str(_p)
    if _p_str not in sys.path:
        sys.path.insert(0, _p_str)

# Ensure 'backend' package namespace is resolvable
if "backend" not in sys.modules:
    try:
        import importlib
        importlib.import_module("backend")
    except ModuleNotFoundError:
        _backend_pkg = types.ModuleType("backend")
        _backend_pkg.__path__ = [str(_BACKEND_DIR)]
        _backend_pkg.__file__ = str(_BACKEND_DIR / "__init__.py")
        sys.modules["backend"] = _backend_pkg

# Import existing FastAPI application
try:
    from backend.main import app
except ImportError:
    from main import app
