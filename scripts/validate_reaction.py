from pathlib import Path
import sys,json
sys.path.insert(0,str(Path(__file__).parents[1]/'src'))
from reaction_mechanism_twin import *
print(json.dumps(validate(load(sys.argv[1])),indent=2))
