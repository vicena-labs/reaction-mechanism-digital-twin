from pathlib import Path
import sys,json
sys.path.insert(0,str(Path(__file__).parents[1]/'src'))
from reaction_mechanism_twin import *
r=load(Path(__file__).parents[1]/'results/example/archived_result.json');out={'energetics':energetics(r),'ts_acceptance':accept_ts(r),'eyring_298K_s-1':eyring(energetics(r)['activation_kcal_mol'],298.15),'status':'synthetic fixture only'}
(Path(__file__).parents[1]/'results/example/analysis_summary.json').write_text(json.dumps(out,indent=2));print(json.dumps(out,indent=2))
