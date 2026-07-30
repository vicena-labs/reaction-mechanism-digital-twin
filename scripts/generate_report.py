from pathlib import Path
import json
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
R=Path(__file__).parents[1];r=json.loads((R/'results/example/archived_result.json').read_text());x=r['irc']['coordinate'];y=r['irc']['relative_kcal_mol']
fig=plt.figure(figsize=(11.69,8.27));gs=fig.add_gridspec(3,4,height_ratios=[.7,1.7,.8]);fig.patch.set_facecolor('#f5f7fb')
ax=fig.add_subplot(gs[0,:]);ax.set_facecolor('#13233b');ax.axis('off');ax.text(.02,.65,'Reaction Mechanism Analysis and Validation Starter',color='white',fontsize=24,weight='bold');ax.text(.02,.25,'Open-source, vendor-neutral pathway validation | MIT | vicena.ai',color='#b9d7ff',fontsize=11)
for i,(t,s) in enumerate([('Validate','Mapping, charge, spin'),('Calculate','Saved quantum outputs'),('Interrogate','TS frequency and IRC'),('Compare','Kinetics and uncertainty')]):
 a=fig.add_subplot(gs[1,i]);a.set_facecolor('white');a.set_xticks([]);a.set_yticks([]);a.text(.08,.82,t,fontsize=15,weight='bold');a.text(.08,.66,s,fontsize=9);a.text(.08,.1,['16 atoms conserved','27 kcal/mol fixture','1 imaginary fixture','0 live Rowan jobs'][i],fontsize=12,color='#1967d2')
a=fig.add_subplot(gs[2,:2]);a.plot(x,y,'o-',color='#1967d2');a.set_xlabel('IRC coordinate, synthetic');a.set_ylabel('Relative energy, kcal/mol');a.set_title('Archived synthetic energy profile');a.grid(alpha=.25)
b=fig.add_subplot(gs[2,2:]);b.axis('off');b.text(.02,.9,'Define  >  Optimize  >  Find TS  >  Validate Path  >  Compare',fontsize=12,weight='bold');b.text(.02,.6,'Verified release metrics: 12 local tests, 0 paid jobs,\n1 synthetic imaginary mode, 2 synthetic IRC directions.\nThese values test software, not chemical validity.',fontsize=10);b.text(.02,.15,'https://github.com/vicena-labs/reaction-mechanism-analysis-starter',fontsize=9)
fig.tight_layout();fig.savefig(R/'assets/reaction-mechanism-analysis-starter-onepager.png',dpi=160);fig.savefig(R/'Reaction_Mechanism_Analysis_Starter_OnePager.pdf');plt.close(fig)
