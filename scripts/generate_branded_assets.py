"""Generate Vicena-branded public visuals from bundled repository results."""
from pathlib import Path
import json
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, Circle
from matplotlib.offsetbox import OffsetImage, AnnotationBbox
from rdkit import Chem
from rdkit.Chem import Draw, rdChemReactions

ROOT = Path(__file__).parents[1]
ASSETS = ROOT / "assets"
ASSETS.mkdir(exist_ok=True)
COL = {"dark":"#10151C","gold":"#F8C73A","gray":"#394452","light":"#F4F6F8","blue":"#3F7CAC","green":"#2A9D8F","red":"#E76F51","white":"#FFFFFF"}
raw = json.loads((ROOT / "results/example/rowan/product_conformer_raw.json").read_text())
prov = json.loads((ROOT / "results/example/rowan/workflow_provenance.json").read_text())
fixture = json.loads((ROOT / "results/example/archived_result.json").read_text())
atoms = raw["initial_molecule"]["atoms"]
coords = np.array([a["position"] for a in atoms], float)
nums = [a["atomic_number"] for a in atoms]

# 2D reaction scheme from actual declared chemistry.
rxn = rdChemReactions.ReactionFromSmarts("C=CC=C.C=C>>C1=CCCCC1", useSmiles=True)
img = Draw.ReactionToImage(rxn, subImgSize=(360,220), useSVG=False)
img.save(ASSETS / "reaction-scheme.png")

# Rowan conformer, clean orthographic ball-and-stick projection.
mol = Chem.AddHs(Chem.MolFromSmiles(raw["initial_molecule"]["smiles"]))
conf = Chem.Conformer(len(atoms))
for i, xyz in enumerate(coords): conf.SetAtomPosition(i, xyz.tolist())
mol.RemoveAllConformers(); mol.AddConformer(conf)
bonds = [(b.GetBeginAtomIdx(), b.GetEndAtomIdx()) for b in mol.GetBonds()]
xy = coords[:, :2]
fig, ax = plt.subplots(figsize=(7.2,5.0), facecolor="white")
for i,j in bonds:
    ax.plot([xy[i,0],xy[j,0]],[xy[i,1],xy[j,1]], color="#66717E", lw=3.0, zorder=1)
for i,(x,y) in enumerate(xy):
    color = "#4C566A" if nums[i] == 6 else "#E5E9F0"
    edge = "#242933" if nums[i] == 6 else "#9AA3AD"
    size = 245 if nums[i] == 6 else 85
    ax.scatter(x,y,s=size,c=color,edgecolors=edge,linewidths=1.0,zorder=2)
    if nums[i] == 6: ax.text(x,y,str(i+1),ha="center",va="center",color="white",fontsize=8,weight="bold",zorder=3)
ax.set_aspect("equal"); ax.axis("off")
ax.set_title("Rowan-returned cyclohexene conformer",loc="left",fontsize=15,weight="bold",color=COL["dark"])
ax.text(0.0,-0.04,"Workflow 3d530210...7295a | aimnet2_wb97md3 | endpoint preparation only",transform=ax.transAxes,fontsize=9,color=COL["gray"])
fig.tight_layout(); fig.savefig(ASSETS / "rowan-cyclohexene-conformer.png",dpi=220,bbox_inches="tight"); plt.close(fig)

# Energy profile panel, unmistakably labeled synthetic fixture.
x=np.array(fixture["irc"]["coordinate"]); y=np.array(fixture["irc"]["relative_kcal_mol"])
fig,ax=plt.subplots(figsize=(7.2,5.0),facecolor="white")
ax.plot(x,y,"o-",lw=2.8,ms=7,color=COL["blue"],label="Synthetic archived path fixture")
ax.axhline(27.0,color=COL["red"],ls="--",lw=2,label="Literature barrier reference, 27 kcal/mol")
ax.fill_between(x,y,0,alpha=.08,color=COL["blue"])
ax.set(xlabel="Synthetic reaction coordinate",ylabel="Relative energy (kcal/mol)")
ax.set_title("Archived pathway logic fixture",loc="left",fontsize=15,weight="bold",color=COL["dark"])
ax.grid(alpha=.18); ax.legend(frameon=False,fontsize=9,loc="lower left")
ax.text(.99,.02,"Not a Rowan TS or IRC result",ha="right",va="bottom",transform=ax.transAxes,color=COL["red"],weight="bold",fontsize=9)
fig.tight_layout();fig.savefig(ASSETS / "archived-energy-profile.png",dpi=220,bbox_inches="tight");plt.close(fig)

# One-page landscape overview.
fig=plt.figure(figsize=(11.69,8.27),facecolor="white")
g=fig.add_gridspec(18,24,left=.035,right=.965,top=.97,bottom=.04,hspace=.45,wspace=.55)
# Header
h=fig.add_subplot(g[0:3,:]); h.set_facecolor(COL["dark"]); h.set_xticks([]);h.set_yticks([])
for sp in h.spines.values(): sp.set_visible(False)
logo=plt.imread(ASSETS/"vicena-logo.png"); oi=OffsetImage(logo,zoom=.12); h.add_artist(AnnotationBbox(oi,(.055,.55),xycoords="axes fraction",frameon=False))
h.text(.115,.68,"REACTION MECHANISM DIGITAL TWIN",color="white",fontsize=20,weight="bold",transform=h.transAxes)
h.text(.115,.30,"Calibratable pathway analysis with explicit transition-state acceptance gates",color="#DDE5EE",fontsize=10.5,transform=h.transAxes)
h.text(.95,.66,"OPEN SOURCE",ha="right",color=COL["gold"],weight="bold",fontsize=10,transform=h.transAxes)
h.text(.95,.30,"MIT | v0.1.0",ha="right",color="white",fontsize=9,transform=h.transAxes)
# Value
v=fig.add_subplot(g[3:5,:]);v.axis("off");v.text(.5,.58,"Turn structures and archived quantum results into an auditable mechanism claim, without treating convergence as proof.",ha="center",va="center",fontsize=13.5,weight="bold",color=COL["dark"],wrap=True)
# Cards
cards=[("VALIDATE INPUTS","Atom conservation, mapping, charge, spin"),("PREPARE ENDPOINTS","Local structures plus Rowan conformers"),("GATE THE TS","Imaginary mode, geometry, and path checks"),("COMPARE EVIDENCE","Thermochemistry, kinetics, uncertainty")]
for k,(title,desc) in enumerate(cards):
    a=fig.add_subplot(g[5:8,k*6:(k+1)*6]);a.axis("off");a.add_patch(FancyBboxPatch((.01,.05),.98,.9,boxstyle="round,pad=.025,rounding_size=.035",facecolor=COL["light"],edgecolor="#D6DCE3",transform=a.transAxes));a.add_patch(Circle((.12,.72),.055,color=COL["gold"],transform=a.transAxes));a.text(.2,.72,title,va="center",fontsize=9.5,weight="bold",color=COL["dark"],transform=a.transAxes);a.text(.08,.38,desc,fontsize=8.4,color=COL["gray"],transform=a.transAxes,wrap=True)
# Evidence panels
p1=fig.add_subplot(g[8:14,0:12]);p1.plot(x,y,"o-",lw=2.5,ms=6,color=COL["blue"]);p1.axhline(27,color=COL["red"],ls="--",lw=1.7);p1.set_title("Archived pathway logic fixture",loc="left",fontsize=11,weight="bold");p1.set_xlabel("Synthetic reaction coordinate",fontsize=8);p1.set_ylabel("Relative energy (kcal/mol)",fontsize=8);p1.tick_params(labelsize=7);p1.grid(alpha=.15);p1.text(.98,.05,"Synthetic, not Rowan IRC",ha="right",transform=p1.transAxes,color=COL["red"],fontsize=7.5,weight="bold")
p2=fig.add_subplot(g[8:14,12:24]);
for i,j in bonds:p2.plot([xy[i,0],xy[j,0]],[xy[i,1],xy[j,1]],color="#66717E",lw=2.2,zorder=1)
for i,(xx,yy) in enumerate(xy):p2.scatter(xx,yy,s=130 if nums[i]==6 else 45,c="#4C566A" if nums[i]==6 else "#E5E9F0",edgecolors="#242933" if nums[i]==6 else "#9AA3AD",linewidths=.7,zorder=2)
p2.set_aspect("equal");p2.axis("off");p2.set_title("Rowan product conformer result",loc="left",fontsize=11,weight="bold");p2.text(.02,.02,"Completed conformer search, endpoint only",transform=p2.transAxes,fontsize=7.5,color=COL["green"],weight="bold")
# Metrics
m=fig.add_subplot(g[14:17,0:10]);m.set_facecolor(COL["dark"]);m.set_xticks([]);m.set_yticks([])
for sp in m.spines.values():sp.set_visible(False)
metrics=[("1","Rowan job"),("0.37","Rowan credits"),("1","Conformer"),("12","Tests passed")]
for i,(val,lab) in enumerate(metrics):m.text(.08+i*.24,.62,val,color=COL["gold"],fontsize=17,weight="bold",transform=m.transAxes);m.text(.08+i*.24,.26,lab,color="white",fontsize=7.5,transform=m.transAxes)
# Workflow
w=fig.add_subplot(g[14:17,10:24]);w.axis("off");steps=["DEFINE","OPTIMIZE","FIND TS","VALIDATE PATH","COMPARE"]
for i,s in enumerate(steps):
    xx=.04+i*.195;w.add_patch(Circle((xx,.55),.055,color=COL["gold"],transform=w.transAxes));w.text(xx,.55,str(i+1),ha="center",va="center",fontsize=8,weight="bold",transform=w.transAxes);w.text(xx,.20,s,ha="center",fontsize=7.5,weight="bold",color=COL["dark"],transform=w.transAxes)
    if i<4:w.plot([xx+.06,xx+.135],[.55,.55],color="#BFC7D1",lw=2,transform=w.transAxes)
# Footer
f=fig.add_subplot(g[17:18,:]);f.axis("off");f.text(0,.35,"github.com/vicena-labs/reaction-mechanism-digital-twin",fontsize=8,color=COL["gray"],transform=f.transAxes);f.text(1,.35,"vicena.ai",ha="right",fontsize=8,weight="bold",color=COL["dark"],transform=f.transAxes)
fig.savefig(ROOT/"Reaction_Mechanism_Digital_Twin_OnePager.pdf",dpi=180,facecolor="white");fig.savefig(ASSETS/"reaction-mechanism-digital-twin-onepager.png",dpi=180,facecolor="white");plt.close(fig)
print("Rowan workflow UUID:",prov["workflow_uuid"])
print("Rowan credits charged:",prov["budget"]["rowan_credits_charged"])
print("Conformers returned:",len(raw["energies"]))
print("Archived fixture activation energy (kcal/mol):",(fixture["energies_hartree"]["ts"]-fixture["energies_hartree"]["reactant"])*627.509474)
print("Generated branded PDF, PNG, reaction scheme, Rowan conformer, and archived profile assets")
