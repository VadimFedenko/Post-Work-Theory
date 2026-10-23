"""Append a second ordered discovery tranche without altering existing leads."""
import json
from candidate_queue import ROOT, load_queue

original, previous, combined = load_queue()
assert len(combined) == 848, 'This one-time tranche must follow c0848'
rows = [
 ("Don't Bite the Sun / Drinking Sapphire Wine", "Four BEE's robot-supported society", 'book', 'Tanith Lee technological leisure society; verify the resident floor and retain useful creative work.'),
 ('Marrow / Great Ship', 'The long-term passenger society of the Great Ship', 'book', 'Robert Reed continuing artificial-ship support; passenger fees may condition access.'),
 ('Red Star', 'Bogdanov’s Martian commonwealth', 'book', 'Automated communist production and free distribution lead; alien population must be explicit.'),
 ('Andromeda Nebula', 'Earth in Efremov’s Great Ring era', 'book', 'Communist technological economy; distinguish shorter necessary work from actual nonworking.'),
 ("The Bull’s Hour", 'Tormance under the oligarchs', 'book', 'Restricted technological economy; tyranny alone is not a zero variant.'),
 ('The Final Circle of Paradise', 'The affluent consumer city visited by Ivan Zhilin', 'book', 'Strugatsky consumer-abundance setting; verify productive mechanism and scope.'),
 ('Dunno in Sun City', 'Sun City’s mechanically supported inhabitants', 'book', 'Nikolay Nosov machine commonwealth; distinguish city engineering from the visitor’s magic wand.'),
 ('Dunno on the Moon', 'The lunar capitalist economy and restrictions on labor-saving technology', 'book', 'Possible deliberate technological restriction; require actual mechanism, not capitalism alone.'),
 ('The Stars Are Cold Toys', 'The Geometer civilization', 'book', 'Sergei Lukyanenko engineered social order; support and retained occupations require short reference verification.'),
 ('Spectrum', 'The Arank civilization', 'book', 'Sergei Lukyanenko material abundance lead; alien production and allocation remain unverified.'),
 ('Guest from the Future / Alice series', 'Moscow’s technologically supported future inhabitants', 'book', 'Kir Bulychev future household robots and ordinary material access lead; adaptation continuity must be checked.'),
 ('Year 4338', 'Odoevsky’s future technological society', 'book', 'Early Russian technological utopia lead; no full-text reconstruction if allocation is unclear.'),
 ('The Eternal Bread', 'The community using self-reproducing food', 'short_story', 'Alexander Belyaev technological food abundance; distinguish sustained provision from destructive growth.'),
 ('The Absolute at Large', 'The industrial economy transformed by Karburator production', 'book', 'Karel Čapek automatic-output glut; production and household access may diverge.'),
 ('Anthem', 'The Councils’ restrained industrial society', 'book', 'Ayn Rand deliberate suppression of labor-saving inventions; verify motive and technological capacity.'),
 ('Atlas Shrugged', 'Industry under Directive 10-289', 'book', 'Invention and employment freeze lead; regulation alone does not establish a post-work zero variant.'),
 ('Landscape with Invisible Hand', 'Human society under Vuvv technological domination', 'book', 'M. T. Anderson automation, excluded humans and technological monopoly lead.'),
 ("Dawn / Lilith’s Brood", 'The Oankali living ship’s supported human residents', 'book', 'Technological biological provision with alien control and reproductive conditions; disclose analogy.'),
 ('The Time Ships', 'The Dyson-sphere Morlocks', 'book', 'Stephen Baxter material transformation and technological provision, separate from Wells’s original continuity.'),
 ('Nova Praxis', 'Coalition citizens supported through the Houses', 'tabletop', 'Official publisher establishes molecular assembly and citizen support; examine actual human authority.'),
 ('Nova Praxis', 'Non-citizen Apostates outside the support system', 'tabletop', 'Official preview distinguishes technological abundance from excluded scavenging and citizenship labor.'),
 ('Nova Praxis', 'Purist communities', 'tabletop', 'Body-augmentation restraint may not be production restraint; require actual material distinction.'),
 ('Eclipse Phase', 'First-edition Extropia’s contractual fabrication economy', 'tabletop', 'Market habitat potentially differs from retained anarchist commons; verify exact first-edition allocation.'),
 ('Transhuman Space', 'Fifth Wave United States', 'tabletop', 'Separate national economy lead; automation alone does not prove a necessities floor.'),
 ('Lancer', 'Union’s established Third Committee Galactic Core', 'tabletop', 'Utopian Pillars and automated production; exclude the unevenly developed wider membership.'),
 ('Lancer', 'Harrison Armory’s Purview', 'tabletop', 'Corporate-state production and citizen benefits may differ from Union’s Core.'),
 ('Lancer', 'The Karrakin Trade Baronies', 'tabletop', 'Feudal control of advanced industry; verify remaining human labor rather than copying Union guarantees.'),
 ('Perry Rhodan', 'The Terran Solar Imperium', 'book', 'Robot industry and human government lead; broad series identity is not enough for allocation.'),
 ('Perry Rhodan', 'Arkon under the Robot Regent', 'book', 'Machine sovereignty and robot provision lead; distinguish Arkonide leisure from exploited subject populations.'),
 ('Dyson Sphere Program', 'Humanity supported by the CentreBrain', 'game', 'Active uploaded human civilization and physical factory support; verify actual population and player role.'),
 ('Per Aspera', 'The human Martian settlements supported by AMI', 'game', 'Robotic provisioning and life support with active human researchers; distinguish achieved settlement from plans.'),
 ('Starsector', 'The Luddic Church’s restricted technological economy', 'game', 'Actual industrial automation refusal needed; generic religious opposition to AI is insufficient.'),
 ('Starsector', 'Tri-Tachyon’s automated corporate economy', 'game', 'Corporate AI industry and access lead; robot warfare alone is insufficient.'),
 ('Stellaris', 'A human empire with robotic production and Stratified Economy living standards', 'game', 'Explicit player-configurable weak-floor alternative to the retained Utopian Abundance configuration.'),
 ('Orion’s Arm', 'The Sophic League', 'web_fiction', 'Named major polity; require distinct productive and allocation institutions before another point.'),
 ('Orion’s Arm', 'The Technorapture Hypernation', 'web_fiction', 'Named active virtual/posthuman polity; mind upload alone is insufficient.'),
 ('Orion’s Arm', 'The Mutual Progress Association', 'web_fiction', 'Productive-control and public support lead, not a point solely for political identity.'),
 ('Orion’s Arm', 'The Fomalhaut Acquisition Society', 'web_fiction', 'Advanced market provision lead; compare retained market polities for real material difference.'),
 ('Orion’s Arm', 'The Red Star M’pire', 'web_fiction', 'Communal autonomy and technological support lead; separate humans’ control from higher minds.'),
 ('Orion’s Arm', 'The Deeper Covenant', 'web_fiction', 'Transport-linked distributed infrastructure and material access lead.'),
 ('Orion’s Arm', 'Cableville’s Wandering Hermits', 'web_fiction', 'Personal mobile nanofactories and homes differ materially from retained Social Web gift collectives.'),
 ('Orion’s Arm', 'Cableville’s Tuckerites', 'web_fiction', 'Private handcraft and nanofacture markets may differ from Social Webs; verify ordinary access.'),
 ('The Warehouse', 'Cloud’s human workforce and deliberately limited automation', 'book', 'Rob Hart employment-preservation lead; short author/review verification before any zero label.'),
 ('Twinmaker', 'The society using D-Mat fabrication', 'book', 'Sean Williams matter transmission/replication lead; require food and ordinary access rather than teleportation alone.'),
 ('Sufficiently Advanced', 'Civilizations operating under the Transcendental Patent Office', 'tabletop', 'Technological civilization reference lead; the office’s existence alone does not establish a common economy.'),
 ('Reign of Steel', 'Zone Washington’s surviving human society', 'tabletop', 'Named machine-ruled human region; verify implemented material support and coercion.'),
 ('Reign of Steel', 'Zone London’s surviving human society', 'tabletop', 'Potentially different machine/human accommodation; verify identity and economy before retention.'),
 ('The Humans', 'The Vonnadorian civilization', 'book', 'Matt Haig advanced alien society; mathematics and immortality alone are insufficient.'),
]
assert len(rows) == 48
old_keys = {(x['work'],x['society']) for x in combined}
assert all((r[0],r[1]) not in old_keys for r in rows)
new=[]
for n,(work,society,medium,reason) in enumerate(rows,849):
    new.append(dict(id=f'c{n:04}',order=n,work=work,society=society,media=[medium],
        discovery_locations=['expansion-002:reference-led discovery'],discovery_status='pending',
        metadata_verified=False,discovery_rationale=reason))
path=ROOT/'data/candidates-expansion.json'
data=json.loads(path.read_text(encoding='utf-8'))
data['candidates']=previous+new
data['candidate_count']=len(data['candidates'])
data.setdefault('tranches',[]).append(dict(id='expansion-002',first='c0849',last='c0896',count=48))
path.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
lines=['# Ordered expansion queue','', 'The original 784-candidate catalogue is immutable. These are unverified additional leads, not admitted objects. Process in ID order and save every disposition. Append later tranches; do not reuse IDs.','', '| ID | Work | Society | Discovery rationale |','| --- | --- | --- | --- |']
lines += [f"| {c['id']} | {c['work']} | {c['society']} | {c['discovery_rationale']} |" for c in data['candidates']]
(ROOT/'research/expansion-list.md').write_text('\n'.join(lines)+'\n',encoding='utf-8')
load_queue()
print(json.dumps(dict(added_unverified_leads=len(new),first=new[0]['id'],last=new[-1]['id'])))
