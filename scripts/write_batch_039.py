from research_helpers import source, assessment, record, scope, evidence, decision, write_batch

S = [
    source('src-bitchun-economics-author', 'The economics of Whuffie', 'Cory Doctorow quoting Dave Green, 2003',
           'https://craphound.com/down/2003/02/06/the-economics-of-whuffie/', 'author_endorsed_secondary_economic_account',
           'Public economic explanation read', 'Nanotechnological necessities, lack of ordinary money and reputational allocation.',
           'An author-selected critical account, not a complete constitution; material abundance does not remove status or access inequalities.'),
    source('src-bitchun-lowesteem-excerpt', 'Down and Out in the Magic Kingdom: Chapter 7', 'Cory Doctorow, public Authorama edition',
           'https://www.authorama.com/down-and-out-in-the-magic-kingdom-8.html', 'primary_fiction_indexed_excerpt',
           'Public indexed low-esteem population passage read', 'People with low Whuffie still live, socialize and create.',
           'A bounded passage only, not a full novel read or a census of their useful work.'),
    source('src-doctorow-walkaway-reason', 'Cory Doctorow on Cyber Warfare, Lawbreaking, and His New Novel Walkaway', 'Cory Doctorow interviewed by Katherine Mangu-Ward, Reason, 2017',
           'https://reason.com/podcast/2017/05/25/cory-doctorow-walkaway/', 'primary_author_interview',
           'Targeted transcript passages on Whuffie, Default and walkaway institutions read', 'Reputational inequality, automated oligarchy, surplus people and deliberative open communities.',
           'Rush transcript, not checked against audio; no verbatim quotation used. Authorial explanation supports interpretation but not precise participation statistics.'),
    source('src-walkaway-reference', 'Walkaway (Doctorow novel)', 'Wikipedia contributors',
           'https://en.wikipedia.org/wiki/Walkaway_%28Doctorow_novel%29', 'secondary_plot_and_economic_reference_indexed',
           'Public indexed printers, recycling and gift-economy paragraphs read', 'Technological independence from Default for food, clothing and shelter.',
           'Summary evidence, not proof that all labor or all resource constraints disappear.'),
    source('src-walkaway-ch2-excerpt', 'Walkaway: You All Meet in a Tavern', 'Cory Doctorow, authorized excerpt at Reactor, 2017',
           'https://reactormag.com/excerpts-cory-doctorow-walkaway-chapter-2/', 'primary_fiction_excerpt_and_publisher_introduction',
           'Public indexed gift-economy passage and introduction read', 'Printed essentials and rejection of a contribution-versus-benefit ledger.',
           'One excerpt, not the whole novel. Wartime destruction and later uploaded lives are not treated as one unchanging economy.'),
    source('src-walkaway-kirkus-author', 'Cory Doctorow', 'Kirkus Reviews author profile and interview, 2017',
           'https://www.kirkusreviews.com/news-and-features/articles/cory-doctorow/', 'secondary_author_profile_indexed',
           'Public indexed automated employment and food discussion read', 'Machines displace jobs while synthetic biology supplies abundant food.',
           'Qualitative presentation; the broad phrase about jobs is not a literal census excluding scientists, maintainers or care workers.'),
    source('src-makers-publisher', 'Makers', 'Macmillan',
           'https://us.macmillan.com/books/9781429969284/makers/', 'publisher_synopsis_indexed',
           'Public indexed New Work boom and bust synopsis read', 'Maker ventures, desktop fabrication and loss of funds after the boom.',
           'Cheap fabrication and entrepreneurship do not establish automatic common provision.'),
    source('src-unauthorized-bread-author', 'Cory Doctorow, March 28 2019 event transcript', 'Cory Doctorow; Seattle Public Library',
           'https://www.spl.org/Seattle-Public-Library/documents/transcriptions/2019/19-03-28_Cory-Doctorow.pdf', 'primary_author_event_transcript_indexed',
           'Public indexed opening story explanation read', 'Refugee housing with appliances restricted to authorized consumables.',
           'No PDF rendering or full novella reading. Licensing coercion is established, society-wide labor replacement is not.')
]
b = ['src-bitchun-economics-author', 'src-bitchun-lowesteem-excerpt', 'src-doctorow-walkaway-reason']
w = ['src-walkaway-reference', 'src-walkaway-ch2-excerpt', 'src-doctorow-walkaway-reason']
d = ['src-doctorow-walkaway-reason', 'src-walkaway-kirkus-author']
R = [
    record('bitchun-society', 'c0210', 'Down and Out in the Magic Kingdom (Bitchun Society)', 'Down and Out in the Magic Kingdom', 'The established Bitchun Society', ['book'],
           scope('The novel continuity', 'The functioning Bitchun era depicted in the novel', 'Living human residents of Bitchun Society', ['Dormant backups counted as active people', 'Every related Doctorow future assigned identical institutions', 'Whuffie treated as a subsistence wage']),
           'Nanotechnology supplies basic material needs, so ordinary wages are no longer the gate to survival. Whuffie measures social esteem and influences access to scarce experiences, desirable places and authority. Low esteem can therefore be painful without being identical to the loss of food and shelter. The strong guarantee estimate concerns necessities, rather than a promise that everyone receives equal prestige or every preferred resource.\n\nControl remains with people and their organizations, rather than a separate machine sovereign. Its positive estimate is qualified: Doctorow explicitly describes how reputation can concentrate power and let established winners dominate others. Publicly contestable control of an attraction is not proof of equal influence over every productive asset. People still operate attractions, make art and pursue other useful projects; voluntary activity counts as work in this database. Neither free necessities nor the end of ordinary money establishes the proportion doing none of that, so the participation axis remains unresolved.',
           {'guarantees': -0.8, 'control': 0.55, 'nonworking': None},
           {'guarantees': assessment(-0.8, [-1, -0.5], 'medium', 'Nanotechnological basic provision and the continuing lives of low-esteem people support strong material security; scarce privileges remain unequal.', b[:2]),
            'control': assessment(0.55, [0.1, 0.9], 'low', 'Human contestation and adhocracy coexist with reputational concentration. The point is an interpretation of effective control, not an equal ownership census.', b),
            'nonworking': assessment(None, None, 'low', 'Creative and operational activity persists without a population participation count.', b)},
           2, b, [evidence('Basic needs are technologically provided while Whuffie allocates status and scarce advantages.', b, 'Economic explanation, low-esteem passage and interview lines 185-205', 'author_commentary_and_primary_excerpt')],
           ['Regime 1 remains an alternative if effective reputational concentration outweighs contestability.', 'Basic provision does not imply equal prestige, guaranteed preferred housing or universal admission from outside the setting.', 'No entire novel read in this reference-led pass.'], alternatives=[1]),
    record('walkaway-communities', 'c0211', 'Walkaway (Walkaway communities)', 'Walkaway', 'Established walkaway gift-economy communities', ['book'],
           scope('Doctorow novel continuity', 'Functioning embodied communities before their later institutions are generalized', 'Human residents and guests supported by the walkaway network', ['All Default residents', 'Every future uploaded person', 'A single destroyed settlement treated as proof the whole network is provisionless']),
           'Walkaway communities use fabrication, recycling and scavenging systems to make essentials outside Default\'s wage economy. Food, clothing and shelter become shared output rather than payment earned through an employer. Their gift norm rejects keeping a personal balance of what someone contributed against what they received. That makes the guarantee estimate strong, although it describes practical community access rather than an invulnerable state entitlement.\n\nMembers can alter shared arrangements, leave, build alternatives and deliberate over common projects. This supports broadly distributed human control; the software is a tool for coordination rather than an independent sovereign. Disputes, maintenance and outside attacks remain real constraints. The people building and running these communities still perform useful work, even when they choose it freely. Their break with wages is therefore not evidence that everyone stops working. No population-wide participation rate is supplied by the short sources, and the record does not merge their embodied communities with all later experiments in uploaded existence.',
           {'guarantees': -0.75, 'control': 0.85, 'nonworking': None},
           {'guarantees': assessment(-0.75, [-0.95, -0.45], 'medium', 'Shared fabricated essentials are available without a contribution ledger; war and local disruption qualify practical security.', w),
            'control': assessment(0.85, [0.6, 1], 'medium', 'Open community projects and deliberation give members substantial effective agency, without proving perfect equality.', w),
            'nonworking': assessment(None, None, 'low', 'Fabrication reduces compulsory labor but useful building, maintenance and care continue; no census is available.', w)},
           2, w, [evidence('Fabricated essentials and gift provision let people live outside Default; community coordination is participatory.', w, 'Chapter 2 gift-economy passage; author interview lines 217-225', 'primary_excerpt_author_commentary_and_reference')],
           ['Guarantees measure access in functioning communities, not immunity from military attack.', 'The gift norm is not a claim of zero maintenance or zero conflict.', 'Participation is unresolved; changing later digital institutions require a separate scope.']),
    record('walkaway-default', 'c0212', 'Walkaway (Default society)', 'Walkaway', 'The automated oligarchic Default economy', ['book'],
           scope('Doctorow novel continuity', 'The established Default order confronting the walkaway movement', 'Embodied humans remaining within Default, including the wealthy and economically surplus', ['Walkaway communities assigned Default conditions', 'All technologically displaced people counted as inactive', 'A completed future settlement after the conflict']),
           'Default combines productive abundance with concentrated control. Automation makes many people unnecessary to production, while a small wealthy group retains decisive economic and legal power. Remaining workers and people vulnerable to replacement face precarious access. The weak guarantee estimate reflects that arrangement: the technical ability to supply needs has not become a secure claim for everyone within it.\n\nControl lies chiefly with a human oligarchy, so the score sits near the concentrated-human end of the axis rather than the autonomous-AI end. This is a transition driven by substantial technological displacement, not merely an imagined future machine capacity. It also does not mean all useful work disappears: people still maintain systems, conduct research and do other tasks. The sources distinguish needed workers from surplus people without supplying a complete denominator. The nonworking share therefore remains unresolved. The walkaway network receives its own record because it uses related technology under materially different access and control rules.',
           {'guarantees': 0.85, 'control': 0.05, 'nonworking': None},
           {'guarantees': assessment(0.85, [0.55, 1], 'medium', 'Author commentary describes precarious people and surplus lives despite automated abundance; no broad secure entitlement is established.', d),
            'control': assessment(0.05, [0, 0.2], 'high', 'A small wealthy human group rigs economic and legal institutions to its advantage.', d),
            'nonworking': assessment(None, None, 'low', 'Many are technologically displaced, but maintainers and other useful workers remain; no complete rate is given.', d)},
           3, d, [evidence('Default combines automated systems, surplus people and concentrated human power.', d, 'Author interview lines 217-218; Kirkus setting discussion', 'author_commentary')],
           ['A retained transition case, not a claim that all wage allocation has ended.', 'No arbitrary nonworking percentage is derived from the rhetorical 99 percent.', 'The public-source check does not establish a later uniform resolution.'])
]
D = [
    decision('c0210', 'included', 'Nanotechnological necessities and reputational scarce-resource allocation establish a distinct post-work arrangement.', b, society_id='bitchun-society'),
    decision('c0211', 'included', 'Fabricated essentials and non-ledger gift provision support a scoped walkaway record.', w, society_id='walkaway-communities'),
    decision('c0212', 'included', 'Automated displacement under oligarchic human control supports a separate weak-guarantee transition record.', d, society_id='walkaway-default'),
    decision('c0213', 'boundary_case', 'New Work is a precarious maker-enterprise economy, without verified common labor-independent provision.', ['src-makers-publisher'], analysis='Desktop fabrication and a boom-bust business model do not by themselves establish post-work distribution or deliberate unnecessary employment.', follow_up='Keep as a maker-economy comparison and skip deeper reading.'),
    decision('c0214', 'boundary_case', 'Proprietary appliances establish coercive access restrictions, without society-wide replacement of human labor.', ['src-unauthorized-bread-author'], analysis='Digitally restricted toasters and elevators are not a general automated-production economy. Ordinary housing support is not enough to meet the technological admission rule.', follow_up='Skip the broad lead; do not import the newly advertised graphic adaptation into the novella record.')
]
write_batch(39, [f'c{i:04}' for i in range(210, 215)], S, R, D, [
    'Reference-led pass using short economic explanations, author commentary and bounded authorized excerpts; no whole novel read.',
    'Walkaway and Default differ in both access and effective control. Default is a transition, with no fabricated exact unemployment rate.',
    'Bitchun guarantees concern necessities; Whuffie inequalities remain visible and qualify the control estimate.',
    'Voluntary useful work counts; all three new records leave unsupported participation percentages unresolved.'
])
