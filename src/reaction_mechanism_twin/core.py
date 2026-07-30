import json,math,hashlib
from pathlib import Path
EH=627.509474; R=8.314462618; KB=1.380649e-23; H=6.62607015e-34
def load(p): return json.loads(Path(p).read_text())
def validate(m):
 a=[x for s in m['reactants'] for x in s['elements']]; b=[x for s in m['products'] for x in s['elements']]
 if sorted(a)!=sorted(b): raise ValueError('element conservation failed')
 if sorted(m['atom_mapping'])!=list(range(1,len(a)+1)): raise ValueError('invalid mapping')
 if [b[i-1] for i in m['atom_mapping']]!=a: raise ValueError('mapping element mismatch')
 if m['charge']!=sum(x['charge'] for x in m['reactants']) or m['charge']!=sum(x['charge'] for x in m['products']): raise ValueError('charge mismatch')
 if any(x['multiplicity']!=m['multiplicity'] for x in m['reactants']+m['products']): raise ValueError('multiplicity mismatch')
 return {'atoms':len(a),'charge':m['charge'],'multiplicity':m['multiplicity']}
def energetics(r):
 e=r['energies_hartree']; return {'activation_kcal_mol':(e['ts']-e['reactant'])*EH,'reaction_kcal_mol':(e['product']-e['reactant'])*EH}
def eyring(dg,T): return KB*T/H*math.exp(-dg*4184/(R*T))
def arrhenius(A,Ea,T): return A*math.exp(-Ea*4184/(R*T))
def accept_ts(r):
 im=[x for x in r['frequencies_cm1'] if x<0]; c={'one_relevant_imaginary':len(im)==1 and r['imaginary_mode_relevant'],'mapping':r['mapping_consistent'],'geometry':r['geometry_plausible'],'irc_backward':r['irc']['backward_endpoint']=='reactant','irc_forward':r['irc']['forward_endpoint']=='product'}
 return {'accepted':all(c.values()),'checks':c,'imaginary_count':len(im)}
def task_key(x): return hashlib.sha256(json.dumps(x,sort_keys=True).encode()).hexdigest()
def parse_rowan(p):
 d=load(p)
 for k in ['workflow_uuid','task_key','workflow_type','status','settings','result']:
  if k not in d: raise ValueError('missing Rowan provenance')
 return d
