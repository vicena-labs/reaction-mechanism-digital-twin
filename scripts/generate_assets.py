from pathlib import Path
import json
from rdkit import Chem
from rdkit.Chem import AllChem
R=Path(__file__).parents[1]; out=R/'results/example/structures';out.mkdir(parents=True,exist_ok=True)
def xyz(smiles,name):
 m=Chem.AddHs(Chem.MolFromSmiles(smiles));AllChem.EmbedMolecule(m,randomSeed=7);AllChem.MMFFOptimizeMolecule(m);c=m.GetConformer();lines=[str(m.GetNumAtoms()),name+' RDKit MMFF local geometry']
 for a in m.GetAtoms():
  p=c.GetAtomPosition(a.GetIdx());lines.append(f'{a.GetSymbol()} {p.x:.7f} {p.y:.7f} {p.z:.7f}')
 (out/f'{name}.xyz').write_text('\n'.join(lines)+'\n');return m
xyz('C=CC=C.C=C','reactant');xyz('C1C=CCCC1','product')
# TS proxy is a labeled geometric interpolation for visualization only, not a stationary point.
a=(out/'reactant.xyz').read_text().splitlines();b=(out/'product.xyz').read_text().splitlines();
if len(a)==len(b):
 q=[a[0],'Synthetic midpoint proxy, not a computed TS']
 for x,y in zip(a[2:],b[2:]):
  X=x.split();Y=y.split();q.append(X[0]+' '+' '.join(f'{(float(X[i])+float(Y[i]))/2:.7f}' for i in range(1,4)))
 (out/'ts_proxy.xyz').write_text('\n'.join(q)+'\n')
scene={'version':1,'title':'Diels-Alder archived endpoint and TS-proxy scene','description':'RDKit MMFF endpoint geometries and a labeled midpoint proxy. No quantum TS claim.','layout':{'rows':1,'cols':3,'sync':True},'structures':[{'path':'reactant.xyz','title':'Reactant endpoint','format':'xyz','style':'sticks','viewer':[0,0]},{'path':'ts_proxy.xyz','title':'TS visual proxy','format':'xyz','style':'sticks','viewer':[0,1]},{'path':'product.xyz','title':'Product endpoint','format':'xyz','style':'sticks','viewer':[0,2]}],'result':{'provider':'Local archived fixture','workflow':'visualization proxy','status':'SYNTHETIC','summary':'No Rowan job submitted'},'properties':[{'label':'Literature barrier reference','value':27.0,'unit':'kcal/mol'}],'annotations':[{'type':'label','viewer':[0,1],'text':'Not a computed transition state','position':{'x':0,'y':3,'z':0}}]}
(out/'reaction_path.molscene.json').write_text(json.dumps(scene,indent=2))
