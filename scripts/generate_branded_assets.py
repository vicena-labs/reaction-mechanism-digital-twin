"""Generate Vicena Research Twins visuals from bundled repository results."""
from pathlib import Path
import json
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, Circle, FancyArrowPatch
from matplotlib.offsetbox import OffsetImage, AnnotationBbox
from rdkit import Chem
from rdkit.Chem import Draw, rdChemReactions

ROOT = Path(__file__).parents[1]
A = ROOT / "assets"
A.mkdir(exist_ok=True)
C = {"dark":"#10151C","gold":"#F8C73A","text":"#394452","light":"#F4F6F8","line":"#D7DEE6","blue":"#3F7CAC","green":"#2A9D8F","red":"#E76F51","white":"#FFFFFF"}
raw = json.loads((ROOT/"results/example/rowan/product_conformer_raw.json").read_text())
prov = json.loads((ROOT/"results/example/rowan/workflow_provenance.json").read_text())
fixture = json.loads((ROOT/"results/example/archived_result.json").read_text())
coords = np.array([a["position"] for a in raw["initial_molecule"]["atoms"]], float)
nums = [a["atomic_number"] for a in raw["initial_molecule"]["atoms"]]

# Reaction scheme asset
rxn = rdChemReactions.ReactionFromSmarts("C=CC=C.C=C>>C1=CCCCC1", useSmiles=True)
Draw.ReactionToImage(rxn, subImgSize=(430,220), useSVG=False).save(A/"reaction-scheme.png")

# Build the molecule using returned coordinates and declared connectivity.
mol = Chem.AddHs(Chem.MolFromSmiles(raw["initial_molecule"]["smiles"]))
conf = Chem.Conformer(len(coords))
for i, xyz in enumerate(coords): conf.SetAtomPosition(i, xyz.tolist())
mol.RemoveAllConformers(); mol.AddConformer(conf)
bonds = [(b.GetBeginAtomIdx(), b.GetEndAtomIdx()) for b in mol.GetBonds()]
xy = coords[:,:2]

def molecule_panel(ax, title=True):
    for i,j in bonds:
        ax.plot([xy[i,0],xy[j,0]],[xy[i,1],xy[j,1]],color="#66717E",lw=3.2,zorder=1,solid_capstyle="round")
    for i,(x,y) in enumerate(xy):
        carbon=nums[i]==6
        ax.scatter(x,y,s=230 if carbon else 72,c="#4C566A" if carbon else "#EEF1F4",edgecolors="#242933" if carbon else "#9AA3AD",linewidths=1,zorder=2)
        if carbon: ax.text(x,y,str(i+1),ha="center",va="center",color="white",fontsize=7.5,weight="bold",zorder=3)
    ax.set_aspect("equal"); ax.axis("off")
    if title: ax.set_title("Rowan-returned cyclohexene conformer",loc="left",fontsize=16,weight="bold",color=C["dark"])

fig,ax=plt.subplots(figsize=(7.2,5),facecolor="white"); molecule_panel(ax)
ax.text(0,-.04,"Bonded view from saved provider coordinates | endpoint preparation only",transform=ax.transAxes,fontsize=9,color=C["text"])
fig.tight_layout();fig.savefig(A/"rowan-cyclohexene-conformer.png",dpi=220,bbox_inches="tight");plt.close(fig)

# Archived energy panel
x=np.array(fixture["irc"]["coordinate"]); y=np.array(fixture["irc"]["relative_kcal_mol"])
fig,ax=plt.subplots(figsize=(7.2,5),facecolor="white")
ax.plot(x,y,"o-",lw=3,ms=7,color=C["blue"])
ax.axhline(27,color=C["red"],ls="--",lw=2,label="Literature barrier reference")
ax.set(xlabel="Synthetic reaction coordinate",ylabel="Relative energy (kcal/mol)")
ax.set_title("Archived pathway logic fixture",loc="left",fontsize=16,weight="bold",color=C["dark"])
ax.grid(alpha=.18);ax.legend(frameon=False,fontsize=9,loc="lower left")
ax.text(.98,.04,"Synthetic fixture, not Rowan TS or IRC",ha="right",transform=ax.transAxes,color=C["red"],fontsize=9,weight="bold")
fig.tight_layout();fig.savefig(A/"archived-energy-profile.png",dpi=220,bbox_inches="tight");plt.close(fig)

# Reference-family A4 landscape one pager
fig=plt.figure(figsize=(14.03,9.92),facecolor="white")
g=fig.add_gridspec(100,100,left=0,right=1,top=1,bottom=0)

# Header
h=fig.add_subplot(g[0:17,:]); h.set_facecolor(C["dark"]); h.set_xticks([]);h.set_yticks([])
for s in h.spines.values(): s.set_visible(False)
logo=plt.imread(A/"vicena-logo.png")
h.add_artist(AnnotationBbox(OffsetImage(logo,zoom=.19),(0.075,.56),xycoords="axes fraction",frameon=False))
h.text(.137,.66,"REACTION MECHANISM ANALYSIS STARTER",transform=h.transAxes,color="white",fontsize=25,weight="bold")
h.text(.137,.31,"Analyze and validate pathway evidence with explicit limits on what has actually been computed",transform=h.transAxes,color="#DCE2EA",fontsize=12.5)
h.text(.965,.65,"OPEN SOURCE",transform=h.transAxes,ha="right",color=C["gold"],fontsize=11.5,weight="bold")
h.text(.965,.33,"MIT  •  Commercial use allowed",transform=h.transAxes,ha="right",color="white",fontsize=10.5)

# Mission
m=fig.add_subplot(g[18:27,4:96]);m.axis("off")
m.text(0,.72,"Analyze supplied results without implying that an unexecuted mechanism was computed.",fontsize=17.5,weight="bold",color=C["dark"],transform=m.transAxes)
m.text(0,.28,"Define the system, validate mapping, prepare endpoints, authorize methods, search candidates, validate paths, preserve failures, and compare uncertainty.",fontsize=11,color=C["text"],transform=m.transAxes)

# Four capability cards
cards=[("DEFINE + VALIDATE","Structures • mapping • charge • spin","Units • conditions • provenance"),("ANALYZE RESULTS","Energy • rates • conformers","Saved UUIDs • raw outputs"),("GATE THE TS","Imaginary mode • geometry • mapping","IRC or equivalent path evidence"),("HONEST BOUNDARY","One real conformer workflow","TS, frequency and IRC not executed")]
for i,(title,l1,l2) in enumerate(cards):
    ax=fig.add_subplot(g[27:40,3+i*24:27+i*24]);ax.axis("off")
    ax.add_patch(FancyBboxPatch((.01,.02),.98,.95,boxstyle="round,pad=.02,rounding_size=.07",facecolor=C["light"],edgecolor=C["line"],lw=1.2,transform=ax.transAxes))
    ax.add_patch(FancyBboxPatch((.035,.77),.93,.17,boxstyle="round,pad=.01,rounding_size=.06",facecolor=C["gold"],edgecolor="none",transform=ax.transAxes))
    ax.text(.09,.56,title,fontsize=10.5,weight="bold",color=C["dark"],transform=ax.transAxes)
    ax.text(.09,.35,l1,fontsize=9,color=C["text"],transform=ax.transAxes)
    ax.text(.09,.19,l2,fontsize=9,color=C["text"],transform=ax.transAxes)

# Evidence plot 1
p1=fig.add_subplot(g[44:72,5:34]);p1.plot(x,y,"o-",lw=2.6,ms=6,color=C["blue"]);p1.axhline(27,color=C["red"],ls="--",lw=1.7)
p1.set_title("Archived energy logic fixture",loc="left",fontsize=12.5,weight="bold",pad=10);p1.set_xlabel("Synthetic reaction coordinate",fontsize=9);p1.set_ylabel("Relative energy (kcal/mol)",fontsize=9);p1.tick_params(labelsize=8);p1.grid(alpha=.17)
p1.text(.98,.04,"Not a Rowan IRC",ha="right",transform=p1.transAxes,color=C["red"],fontsize=8,weight="bold")

# Evidence plot 2
p2=fig.add_subplot(g[44:72,38:70]);molecule_panel(p2,False);p2.set_title("Rowan product conformer",loc="left",fontsize=12.5,weight="bold",pad=10)
p2.text(.01,.03,"Bonded view from saved Rowan coordinates",transform=p2.transAxes,color=C["green"],fontsize=8,weight="bold")

# Metrics block
met=fig.add_subplot(g[43:73,74:97]);met.set_facecolor(C["dark"]);met.set_xticks([]);met.set_yticks([])
for s in met.spines.values():s.set_visible(False)
metrics=[("1 completed","Rowan conformer workflow"),("0.37 credits","Provider charge"),("1 conformer","Saved endpoint geometry"),("12 tests","Repository baseline checks")]
for i,(v,l) in enumerate(metrics):
    yy=.82-i*.22;met.text(.13,yy,v,transform=met.transAxes,color=C["gold"],fontsize=15,weight="bold");met.text(.13,yy-.09,l,transform=met.transAxes,color="white",fontsize=8.6)

# Workflow strip
wf=fig.add_subplot(g[76:91,3:97]);wf.axis("off");wf.text(.02,.88,"EIGHT EXPLICIT STAGES, WITH STATUS AT EVERY GATE",fontsize=12.5,weight="bold",color=C["dark"],transform=wf.transAxes)
steps=[("DEFINE","system"),("VALIDATE","mapping"),("PREPARE","endpoints"),("AUTHORIZE","method"),("SEARCH","TS"),("CHECK","freq + IRC"),("PRESERVE","failures"),("COMPARE","uncertainty")]
for i,(a,b) in enumerate(steps):
    xx=.005+i*.124
    wf.add_patch(FancyBboxPatch((xx,.05),.105,.58,boxstyle="round,pad=.012,rounding_size=.035",facecolor=C["light"],edgecolor=C["line"],lw=1.0,transform=wf.transAxes))
    wf.text(xx+.0525,.39,a,ha="center",fontsize=7.5,weight="bold",color=C["dark"],transform=wf.transAxes)
    wf.text(xx+.0525,.19,b,ha="center",fontsize=6.8,color=C["text"],transform=wf.transAxes)
    if i<7: wf.add_patch(FancyArrowPatch((xx+.107,.34),(xx+.122,.34),arrowstyle="-|>",mutation_scale=10,color=C["gold"],lw=1.5,transform=wf.transAxes))

# Footer
f=fig.add_subplot(g[93:100,:]);f.set_facecolor(C["light"]);f.set_xticks([]);f.set_yticks([])
for s in f.spines.values():s.set_visible(False)
f.text(.04,.48,"github.com/vicena-labs/reaction-mechanism-analysis-starter",fontsize=10,weight="bold",color=C["dark"],transform=f.transAxes)
f.text(.96,.48,"vicena.ai  •  Validate the path before trusting the barrier",ha="right",fontsize=9.5,color=C["text"],transform=f.transAxes)

fig.savefig(ROOT/"Reaction_Mechanism_Analysis_Starter_OnePager.pdf",dpi=180,facecolor="white")
fig.savefig(A/"reaction-mechanism-analysis-starter-onepager.png",dpi=180,facecolor="white")
plt.close(fig)
print("Rowan workflow UUID:",prov["workflow_uuid"])
print("Rowan credits charged:",prov["budget"]["rowan_credits_charged"])
print("Conformers returned:",len(raw["energies"]))
print("Archived fixture activation energy (kcal/mol):",(fixture["energies_hartree"]["ts"]-fixture["energies_hartree"]["reactant"])*627.509474)
print("Generated reference-family PDF, PNG, reaction scheme, Rowan conformer, and archived profile")
