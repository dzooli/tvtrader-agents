import sys
from pathlib import Path

currpath = Path(__file__)
sys.path.append(str(currpath.parents[3].resolve().absolute()))
