"""Create the first ordered expansion tranche without editing the frozen catalogue."""
import json
from pathlib import Path
from candidate_queue import load_queue

ROOT=Path(__file__).resolve().parents[1]
frozen,existing,_=load_queue()
rows=[
 ('Earth 2150','United Civilized States before the evacuation crisis','game','Saved new-faction lead; src-b83-earth2150 explicitly describes all-robot workforce.'),
 ('Autofac','Original short-story human survivors and autonomous factory network','short_story','Original story, distinct from the already checked television adaptation.'),
 ('Emphyrio','Halma’s enforced handicraft welfare economy','book','Technological prohibition and patronage allocation; verify a zero-variant scope.'),
 ('Wyst: Alastor 1716','Arrabus egalitarian industrial society','book','Short assigned work and common provision; verify automation and allocation.'),
 ('The Towers of Utopia','Reynolds’s automated arcology communities','book','Separate Bat Hardin title; compare arrangements against Rolltown before retaining.'),
 ('Commune 2000 A.D.','The communes investigated by Bat Hardin','book','SFE links it to Reynolds’s socioeconomic utopias; check distinctness and actual machinery.'),
 ('Equality: in the Year 2000','Later Reynoldsian commonwealth under its challenged selection system','book','Potential sequel-period change; require material difference from the earlier retained point.'),
 ('Mercenary from Tomorrow','Joe Mauser’s automated caste society','book','Potential guaranteed-support caste order; merge same-setting sequels if economically identical.'),
 ('Ultima Thule','United Planets Earth’s post-employment order','book','Reynolds automation/ability-selection lead; verify exact story and scope.'),
 ('Depression or Bust','Machine-displaced society and its response','book','Reynolds economic-transition lead; exact mechanism unverified.'),
 ('The Happy Breed','Machine-protected human household society','short_story','John Sladek automation/protection story, potentially clear technological dependence.'),
 ('The Reproductive System','Self-replicating factory expansion and its human dependents','book','John Sladek’s production-machine satire; distinguish destruction from provision.'),
 ('The Country of the Kind','Technologically supported society surrounding the ostracized narrator','short_story','Damon Knight abundance/exclusion lead; verify public material access.'),
 ('Natural State','The City’s machine-dependent inhabitants','short_story','Damon Knight city/biological society comparison; verify actual allocation.'),
 ('Natural State','The Muckfeet’s engineered biological economy','short_story','Same story, potentially different productive ownership; do not count merely for rural aesthetics.'),
 ('The Prize of Peril','Automated society with public income and lethal entertainment','short_story','Robert Sheckley labor-redundancy lead; verify the actual support floor.'),
 ('A Ticket to Tranai','Tranai’s technology, ownership and coercive institutions','short_story','Robert Sheckley social satire; distinguish robot labor from the productive-control rules.'),
 ('The Ophiuchi Hotline','Eight Worlds human settlements under advanced machine support','book','John Varley setting; compare later Luna governance before splitting.'),
 ('Steel Beach','Luna under the Central Computer','book','Specific later Varley computer-provision order; verify consistency/continuity with the previous lead.'),
 ('Triton','Triton’s subsidized heterotopia','book','Samuel R. Delany necessities access and varied voluntary services lead.'),
 ('Stars in My Pocket Like Grains of Sand','Velm’s labor and supported population','book','Human/alien social economy; do not mistake recognized personhood for automation.'),
 ('Aristoi','Reconstructed human worlds under the Aristoi','book','Walter Jon Williams nano-production and elite control lead.'),
 ('Implied Spaces','The civilization supporting pocket universes','book','Walter Jon Williams abundance and virtual-person support lead.'),
 ('Riding the Torch','The continuing interstellar refugee fleet','short_story','Norman Spinrad technological abundance and leisure lead.'),
 ('The Cassini Division','The Solar Union','book','Ken MacLeod explicitly post-scarcity socialist setting; verify effective productive ownership.'),
 ('The Cassini Division','New Republic of New Mars','book','Market counterpart to the Solar Union; verify actual labor/access distinction.'),
 ('The Stone Canal','New Mars in the earlier colonial period','book','Require actual economic-period change from later New Republic, otherwise duplicate.'),
 ('Newton’s Wake','Post-Singularity communities visited by Lucinda Carlyle','book','Ken MacLeod abundance and restricted technology lead; exact local population unverified.'),
 ('The Sky Road','The later low-industry civilization','book','Potential deliberate restriction zero variant; verify actual retained productive labor.'),
 ('Lady of Mazes','Teven Coronal’s technology-mediated societies','book','Karl Schroeder technology access and reality-control lead.'),
 ('Ventus','Planetary human communities under the Winds','book','Engineered environmental infrastructure versus actual household labor; possible technological ceiling.'),
 ('Lockstep','The functioning lockstep civilization','book','Robot production during hibernation may support active waking life; sleeping intervals are not leisure.'),
 ('Permanence','Cycler civilization and machine property','book','Ownership/access lead; technological infrastructure alone is insufficient.'),
 ('Gridlinked','Established AI Polity civilian worlds','book','Neal Asher post-scarcity/AI sovereignty lead; do not substitute military technology for access.'),
 ('The Departure','Committee-controlled Earth','book','Separate Owner-series dictatorship and productive exclusion lead.'),
 ('Genesis','Earth’s later machine-guided human order','book','Poul Anderson advanced machine governance; distinguish uploaded rulers from external AI.'),
 ('Harvest of Stars','Earth under the Avantist order','book','Poul Anderson restricted human/machine society; actual productive access unverified.'),
 ('The Boat of a Million Years','The later robot-supported Earth','book','Late period of Poul Anderson’s novel; not historical immortals’ earlier wealth.'),
 ('The Dancers at the End of Time','The End of Time’s energy-ring society','book','Michael Moorcock technological abundance and leisure; verify machinery as opposed to unscoped magic.'),
 ('Mockingbird','The machine-maintained illiterate human population','book','Walter Tevis robot provision and human dependency lead.'),
 ('The World Inside','Urban Monad populations','book','Robert Silverberg dense housing and industrial support; verify remaining human work.'),
 ('Tower of Glass','Earth’s android production and elite households','book','Robert Silverberg biological/artificial labor and ownership lead, not automatic human leisure.'),
 ('Emergency Skin','The restored Earth civilization','short_story','N. K. Jemisin communal advanced technology and actual provision lead.'),
 ('Emergency Skin','The departed founders’ enclave','short_story','Distinct exclusion/elite support lead; verify implemented economy rather than propaganda.'),
 ('2312','The established space-settlement terrarium economy','book','Kim Stanley Robinson basic provision and qube-supported political economy; keep local variations visible.'),
 ('Marooned in Realtime','Late pre-Singularity technological society','book','Vernor Vinge post-scarcity lead; do not count bobble stasis as active leisure.'),
 ('Rainbows End','Rejuvenated human society and ubiquitous automation','book','Vernor Vinge access and employment lead; advanced interfaces alone are insufficient.'),
 ('A Psalm for the Wild-Built','Panga’s post-robot human communities','book','Becky Chambers social support and technology-choice lead; robots have left ordinary human labor.'),
 ('Record of a Spaceborn Few','The Exodan Fleet’s resource commons','book','Becky Chambers non-wage basics and continuing useful maintenance; verify technological contribution.'),
 ('Engine Summer','Little Belaire and inherited technological support','book','John Crowley low-industry/advanced-infrastructure lead; no full novel rescue.'),
 ('Mizora','The subterranean women’s technological commonwealth','book','Mary E. Bradley Lane automation/chemical food utopia lead.'),
 ('News from Nowhere','The future commonwealth’s chosen technology and work','book','William Morris deliberate productive choices, potential interpretive zero variant.'),
 ('The Republic of the Future','New York’s machine-supported collective','book','Anna Bowman Dodd mechanized utopia satire; verify access and retained work.'),
 ('Three Hundred Years Hence','Future technological American society','book','Mary Griffith early technological-utopia lead; reject if brief reference does not establish allocation.'),
 ('A.D. 2000','The technological future civilization','book','Alvarado M. Fuller utopia lead from SFE; no title-based assumption of post-work.'),
 ('Last and First Men','The technologically supported later human species','book','Olaf Stapledon broad evolutionary sequence; require a specific evidenced period and population.'),
 ('Star Maker','The symbiotic civilization and its machine economy','book','Olaf Stapledon specific social-unit lead; do not count abstract cosmic minds as humans.'),
 ('The Call of the Mech-Men','Machine succession and surviving human society','short_story','Laurence Manning automation lead from SFE; verify applicable active population.'),
 ('Mechanistria','The self-sustaining mechanical civilization','short_story','Eric Frank Russell automation lead from SFE; artificial ecology alone may be a boundary.'),
 ('Mr Jonnemacher’s Machine','The automated economy’s displaced human workers','book','Walter Doty Reynolds, writing as Lord Prime; historical automation dystopia lead.'),
 ('The Seams','The Dole-supported human-derived denizens','web_fiction','OA official reference explicitly lists universal basic access; distinct polity from retained Sephirotic empires.'),
 ('Orion’s Arm','Sacredtree’s engineered Biotopia','web_fiction','Potential local variation within Zoeific Flow; compare actual economics before any separate retention.'),
 ('Orion’s Arm','Niuearth’s modern baseline reserve','web_fiction','Specific relaxed reserve differs from primitive Wurm; hospitality alone may not establish continuing household access.'),
 ('Orion’s Arm','Cableville’s Bolos and social webs','web_fiction','Gift-economy collectives with higher-mind infrastructure; verify distinct controls and provision.'),
]
assert not existing, 'Expansion already exists; append a new tranche rather than overwrite it'
cs=[]
for number,(work,society,medium,reason) in enumerate(rows,start=785):
    cs.append({'id':f'c{number:04}','order':number,'work':work,'society':society,'media':[medium],
               'discovery_locations':['expansion-001:reference-led discovery'], 'discovery_status':'pending',
               'metadata_verified':False,'discovery_rationale':reason})
data={'schema_version':'1.0','created_on':'2026-10-16','scope':'Append-only unverified ordered expansion; not retained societies',
      'frozen_initial_count':784,'candidate_count':len(cs),'candidates':cs}
(ROOT/'data/candidates-expansion.json').write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
lines=['# Ordered expansion queue','', 'The original 784-candidate catalogue is immutable. These are unverified additional leads, not admitted objects. Process in ID order and save every disposition. Append later tranches; do not reuse IDs.','', '| ID | Work | Society | Discovery rationale |','| --- | --- | --- | --- |']
lines += [f"| {c['id']} | {c['work']} | {c['society']} | {c['discovery_rationale']} |" for c in cs]
(ROOT/'research/expansion-list.md').write_text('\n'.join(lines)+'\n',encoding='utf-8')
print(json.dumps({'added_unverified_leads':len(cs),'first':cs[0]['id'],'last':cs[-1]['id']}))
