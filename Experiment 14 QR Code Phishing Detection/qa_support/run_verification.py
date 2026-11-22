"""Isolated-process entry point; add only this verified package to sys.path."""
from pathlib import Path
import runpy
import sys
ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))
runpy.run_path(str(ROOT / 'verify_package.py'), run_name='__main__')
