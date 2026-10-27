from research_helpers import source, assessment, record, scope, evidence, decision, write_batch

S = [
    source("src-quantum-magician-hayakawa", "Technology will fundamentally change us: The Quantum Magician", "Hayakawa Books & Magazines, Japanese publisher",
           "https://www.hayakawabooks.com/n/n573d281746ce?hl=en", "official_publisher_introduction",
           "Public indexed setting and character introduction read", "Congregate personnel, engineered human groups, Gates-15 and the Numen relationship.",
           "Publisher overview in an English rendering, not a novel read or general production/allocation account."),
    source("src-quantum-magician-fantasylit", "The Quantum Magician: A fun, light heist novel", "Fantasy Literature review",
           "https://fantasyliterature.com/reviews/the-quantum-magician/", "secondary_literary_review_indexed",
           "Public indexed engineered-species discussion read", "The Puppets' engineered devotion, overthrow of the Numen and subsequent captivity of their former masters.",
           "Engineered human workers do not automatically constitute independent automation; no household provision system established."),
    source("src-quantum-war-synopsis", "Quantum War", "Publisher-supplied synopsis reproduced by BingeBooks",
           "https://bingebooks.com/book/quantum-war", "publisher_synopsis_reproduction",
           "Public synopsis read", "The Union/Congregate war and engineered pilots.",
           "Military capability and a series title do not establish one homogeneous economic society or post-work distribution."),
    source("src-permutation-reference", "Permutation City", "Wikipedia contributors",
           "https://en.wikipedia.org/wiki/Permutation_City", "secondary_plot_and_setting_reference",
           "Public setting and two-part plot account read", "Commercial QIPS access, wealthy/poor Copies, TVC growth and the later Autoverse conflict.",
           "Broad reference; a running Copy is a person proxy, not a passive backup. The TVC and Autoverse are distinct structures."),
    source("src-permutation-ebsco", "Permutation City by Greg Egan", "EBSCO Research Starters",
           "https://www.ebsco.com/research-starters/literature-and-writing/permutation-city-greg-egan/", "secondary_literary_reference_indexed",
           "Public indexed Copy and property discussion read", "Copies' assets, shutdown fears and Durham's proposed alternative.",
           "Selected indexed reference passages, not a complete primary read. Economic control through assets does not establish full legal personhood."),
    source("src-permutation-tvc-scholarship", "Discussion of Elysium and the TVC universe in Facta Simonidis 1 (2008)", "Facta Simonidis scholarly article, indexed pages 216-217",
           "https://bibliotekanauki.pl/articles/26850772.pdf", "secondary_scholarly_analysis_indexed_excerpt",
           "Public indexed page 217 discussion read", "Growing self-replicating processing substrate, private worlds and collectively agreed city architecture.",
           "Indexed passage only, not a complete PDF read or visual check. Used as literary interpretation, not a claim that the fictional physics is true."),
    source("src-permutation-cthulhu", "Book Review: Permutation City", "Cthulhu Writes, 15 January 2016",
           "https://cthulhuwrites.blogspot.com/2016/01/book-review-permutation-city.html", "secondary_literary_review_indexed",
           "Public indexed Elysium account read", "The independent system operates and expands before the later conflict.",
           "Review interpretation; no exact census or general admission rights for outsiders.")
]
early = ["src-permutation-reference", "src-permutation-ebsco"]
late = ["src-permutation-tvc-scholarship", "src-permutation-cthulhu"]
R = [
    record("permutation-city-elysium", "c0167", "Permutation City (Independent Elysium)", "Permutation City", "The active Copy community supported by the TVC universe", ["book"],
           scope("Egan's Permutation City", "The operating, expanding Elysium period before the Lambertian conflict threatens its basis", "Active human-derived Copies living in Elysium", ["Earth-hosted commercial Copies", "Indigenous Lambertians given human status without justification", "Dormant snapshots counted as active residents", "A mere sales pitch treated as the completed system"], proxy=True, proxy_basis="Active human-derived digital persons are the explicit denominator; avatars and inactive records are not separate people."),
           "Elysium's Copies inhabit an implemented computational world whose processing substrate expands through self-replication. Continued existence and the creation of everyday surroundings no longer depend on buying cycles from Earth's commercial market. Residents can construct private worlds and alter their surroundings. This supplies a technological equivalent of material provision for active digital people, with strong guarantees during the established operating period. It is an admitted community, not a claim that everyone outside received entry.\n\nControl is broadly distributed among residents over their environments, while the common city's architecture and underlying rules constrain what can change. A self-replicating cellular substrate is not, by itself, an autonomous AI sovereign. The later conflict with the Autoverse demonstrates that the arrangement is not invulnerable; that crisis does not retroactively make its earlier support depend on wages. Research and creative construction remain useful work, so the sources do not justify a precise nonworking fraction. Dormant records and the indigenous Lambertians are excluded from this population.",
           {"guarantees": -0.9, "control": 0.85, "nonworking": None},
           {"guarantees": assessment(-0.9, [-1, -0.65], "medium", "The operating self-expanding substrate removes residents' dependence on external purchased processing. Admission limits and the later systemic threat qualify the scope.", late),
            "control": assessment(0.85, [0.6, 1], "medium", "Residents create private environments and agree on the common city's form, subject to fixed substrate rules. Automatic growth is not verified AI government.", ["src-permutation-tvc-scholarship"]),
            "nonworking": assessment(None, None, "low", "The community pursues research and creative activity; unlimited surroundings do not measure useful-work participation.", late)},
           2, late + ["src-permutation-reference"],
           [evidence("The TVC substrate supports resident-controlled private worlds and a shared city.", ["src-permutation-tvc-scholarship"], "Indexed journal page 217", "secondary_literary_interpretation"),
            evidence("The independent system actually operates before a later conflict, rather than remaining an investment promise.", ["src-permutation-cthulhu"], "Review's Elysium launch and later-crisis summary", "secondary_lore_report")],
           ["Reference-led assessment with an explicit active-person proxy; no whole-novel read.", "Elysium and the separately evolving Autoverse population must not be collapsed into one society.", "Physical credibility of Dust Theory is irrelevant to whether the arrangement is depicted in the fiction."] ),
    record("permutation-city-commercial-copies", "c0168", "Permutation City (Earth's commercial Copy economy)", "Permutation City", "Active Copies dependent on privately traded computing resources", ["book"],
           scope("Egan's Permutation City", "The Earth-hosted commercial order before independent Elysium", "Active human-derived Copies in the commercial hosting economy, including wealthy and low-resource users", ["Biological Earth's entire population", "Independent Elysium", "Frozen snapshots counted as nonworking people"], proxy=True, proxy_basis="The digital Copies are active persons; slowdown affects subjective time, not automatic person-count multiplication."),
           "Earth's Copies receive their experienced surroundings from computational infrastructure, but access to the resource sustaining their lives is bought and sold. Wealthy Copies can rely on substantial assets and dedicated arrangements; poorer ones run slowly or risk suspension when resources become unaffordable. This is post-work capacity without universal security: ordinary human biology no longer dictates subsistence, yet continued active existence remains exposed to property, investment income and market competition.\n\nControl is unequal. Wealthy Copies can influence their environments and the assets supporting them, while weaker users depend on external hosts and legal decisions. The low positive control estimate captures concentrated human economic power without claiming a single monopoly or an AI government. More dispersed ownership is a plausible alternative reading. Some Copies may still earn income or perform useful work, and being poor or slowed does not establish inactivity. Suspended snapshots are excluded from participation rather than counted as people enjoying leisure. The independent Elysium community belongs to a different record.",
           {"guarantees": 0.8, "control": 0.2, "nonworking": None},
           {"guarantees": assessment(0.8, [0.6, 1], "high", "Market access and assets determine continued processing; low-resource Copies risk suspension and political insecurity.", early),
            "control": assessment(0.2, [0, 0.65], "low", "Wealthy asset holders have real influence while weaker Copies rely on hosts and outside authority. Ownership is plural but unequal; no single sovereign AI is established.", early),
            "nonworking": assessment(None, None, "low", "The sources distinguish wealth, subjective speed and earning ability, not an all-active-person work census.", ["src-permutation-reference"])},
           3, early,
           [evidence("Copies' ability to remain active depends on assets and commercial compute access.", early, "Setting account of the QIPS market and rich/poor Copies", "secondary_lore_report")],
           ["The post-work analogy concerns provision for digital persons, not a claim that all physical Earth labor has disappeared.", "The ownership score is a broad interpretation and does not deny plural competing providers.", "No exact participation rate is inferred from slowdown or suspension."], alternatives=[4])
]
D = [
    decision("c0164", "needs_evidence", "The Congregate's strategic power and engineered personnel do not establish its general automatic provision system.", ["src-quantum-magician-hayakawa"], analysis="A navy, an AI character and control of passage between systems do not settle civilian production or labor-dependent access.", follow_up="Skip deeper reading under the faster-pass instruction."),
    decision("c0165", "boundary_case", "The Puppets are engineered humans with a coercive religious history, not verified independent automatic producers.", ["src-quantum-magician-hayakawa", "src-quantum-magician-fantasylit"], analysis="Their revolt and captivity of the Numen do not supply a post-work mechanism. Genetically modified human labor still counts as human-derived work.", follow_up="Preserve as an engineered-labor comparison; skip a novel investigation."),
    decision("c0166", "needs_evidence", "The broad Union lead is a series-level aggregation without documented uniform household access.", ["src-quantum-war-synopsis"], analysis="War and engineered pilots identify factions and technology, not a post-work production/allocation arrangement.", follow_up="Skip further reading; admit a narrower polity only if clear economic reference material appears."),
    decision("c0167", "included", "An operating self-expanding substrate provides resident-controlled environments independently of the commercial hosting market.", late + ["src-permutation-reference"], society_id="permutation-city-elysium"),
    decision("c0168", "included", "Computational provision exists but active life remains conditional on assets and market access.", early, society_id="permutation-city-commercial-copies")
]
write_batch(31, [f"c{i:04}" for i in range(164, 169)], S, R, D, [
    "Continues the reference-led pass. Three engineered-species/military leads are disposed without full-text recovery; advanced people are not automatically post-work societies.",
    "Permutation City's operating Elysium and Earth-hosted commercial Copies have materially different guarantees and access mechanisms. Neither a frozen record nor every alien digital organism becomes a human leisure resident.",
    "The active-person proxy and the distinction between blind automatic support and sovereign AI remain explicit.",
    "Second pass challenged admission and coordinate claims against the references; no full novel read or independent review is claimed."
])
