from research_helpers import source, assessment, record, scope, evidence, decision, write_batch

S = [
    source("src-commonwealth-early-readers", "Utopian/Optimistic sci fi? Commonwealth discussion", "r/printSF readers, December 2020",
           "https://www.reddit.com/r/printSF/comments/k8k9b8/utopianoptimistic_sci_fi/", "secondary_reader_discussion",
           "Public indexed early-Commonwealth discussion read", "Market inequality, paid rejuvenation and continuing work.",
           "Unverified reader accounts, not admission proof; they only caution against importing the later Higher economy into the early novels."),
    source("src-high-angel-primary-quoted", "Commonwealth Series feats thread: Pandora's Star Chapter 10 excerpts", "Peter F. Hamilton, quotations collected by SpaceBattles readers",
           "https://forums.spacebattles.com/threads/commonwealth-series-peter-f-hamilton-feats-capabilities-thread.1194707/page-2", "primary_excerpt_in_secondary_fan_context",
           "Public indexed chapter-labelled excerpts read", "Sentient ship, uncertain biological/machine origin, human worker domes and manufacturing capacity.",
           "Excerpt selection not independently compared with the edition. Housing workers and producing goods do not establish employment-independent entitlements or AI origin."),
    source("src-raiel-reference-excerpts", "Commonwealth Series feats thread: The Raiel", "Peter F. Hamilton quotations with fan framing",
           "https://forums.spacebattles.com/threads/commonwealth-series-peter-f-hamilton-feats-capabilities-thread.1194707/", "primary_excerpt_in_secondary_fan_context",
           "Public indexed Raiel background excerpts read", "Ancient alien civilization and construction of High Angel-class ships.",
           "Power and age do not establish resident guarantees, labor participation or a justified human-population proxy."),
    source("src-commonwealth-faller-timeline", "A Night Without Stars: Commonwealth timeline", "Peter F. Hamilton; public indexed ebook preview at Everand",
           "https://www.everand.com/book/769877233/A-Night-Without-Stars-A-Novel-of-the-Commonwealth", "primary_published_timeline_indexed_excerpt",
           "Public indexed chronology entries consulted", "Biononic development, Higher culture's rejection of commercial economics, ANA migration and Earth government.",
           "Timeline excerpts only, not a novel read. Later Andromeda-colony dialogue on the same page is not used to describe Greater Commonwealth access."),
    source("src-commonwealth-abyss-dialogue", "The Abyss Beyond Dreams: Nigel and Paula's conversation", "Peter F. Hamilton; unofficial public transcription",
           "https://itexts.net/avtor-peter-f-hamilton/145233-the-abyss-beyond-dreams-peter-f-hamilton/read/page-8.html", "primary_fiction_indexed_excerpt",
           "Public indexed conversation passages read", "Existing technological post-scarcity, diverse lifestyles and the distinction between Higher and External worlds.",
           "Character statements, not omniscient constitutional facts. Nigel's proposed homogeneous colony is not treated as an enacted Commonwealth institution; no whole novel read."),
    source("src-void-deathrobots-review", "Hamilton - Peter F: Void trilogy discussion", "Death Robots From Mars review archive",
           "https://deathrobotsfrommars.wordpress.com/category/authors/hamilton-peter-f/", "secondary_literary_review_indexed",
           "Identified public Void-era discussion read", "Uploaded humans in ANA, political factions and continuity with the earlier novels.",
           "Archive contains separate books; only the identified Void discussion is used. Calling ANA an AI does not erase its human-derived resident minds."),
    source("src-void-ana-readers", "The Dreaming Void: reader discussion of ANA", "Reader reviews displayed by AllBookstores",
           "https://www.allbookstores.com/The-Dreaming-Void-Commonwealth-Void/9780345496546", "secondary_reader_reviews_indexed",
           "Public indexed ANA faction discussion read", "The uploaded community's political factions, alliances and differing goals.",
           "Corroborating reader interpretation only; no claim of a complete formal voting constitution or participant census.")
]
h = ["src-commonwealth-faller-timeline", "src-commonwealth-abyss-dialogue"]
a = ["src-commonwealth-faller-timeline", "src-void-deathrobots-review", "src-void-ana-readers"]
R = [
    record("void-higher-culture", "c0198", "The Void Trilogy (Higher culture)", "The Void Trilogy", "Embodied Higher citizens of the mature Greater Commonwealth", ["book"],
           scope("Hamilton's Commonwealth continuity; Void-era society corroborated by the published earlier chronology", "The established Higher era of the Greater Commonwealth, before the Void's resolution", "Active embodied human and human-derived Higher citizens", ["Early Intersolar Commonwealth", "All External worlds assigned Higher institutions", "ANA's active uploaded residents counted in this embodied population", "Nigel's proposed new homogeneous colony"], proxy=True, proxy_basis="Embodied human-derived citizens remain the person denominator; extreme life extension does not create additional persons."),
           "Higher culture is a later development, distinct from the early Commonwealth's commercial order. The published chronology explicitly links biononic enrichment with long lives and rejection of commercial economics. The accompanying character account describes an established technological post-scarcity society in which people choose among many ways of living. Together these support strong basic provision without ordinary wage dependence for Higher citizens, rather than for every planet bearing the Commonwealth name.\n\nThe control estimate favors substantial individual and human-derived collective agency. It remains broad because ANA's governmental authority and powerful political factions qualify a simple picture of equal control. Neither advanced automation nor the name of a computational government proves an independent AI ruling over passive humans. Chosen science, care and public service can still be work, so the sources do not supply a nonworking census. The embodied Higher community is separated from ANA's uploaded residents, whose support substrate and political participation are materially different.",
           {"guarantees": -0.85, "control": 0.55, "nonworking": None},
           {"guarantees": assessment(-0.85, [-1, -0.6], "medium", "The published Higher chronology rejects commercial economics; the primary dialogue describes existing technological post-scarcity. Scope excludes differing External worlds and proposed colonies.", h),
            "control": assessment(0.55, [0.1, 0.9], "low", "Personal lifestyle choice coexists with ANA government and factional influence. The positive point is provisional, not a verified equal ownership share.", h + ["src-void-deathrobots-review"]),
            "nonworking": assessment(None, None, "low", "Long lives and rejection of commercial economics do not count useful scientific, care or civic participation.", h)},
           2, h + ["src-void-deathrobots-review"],
           [evidence("Higher culture arises with biononics and rejection of commercial economics; ANA later becomes Earth's government.", ["src-commonwealth-faller-timeline"], "Published chronology entries 2867-3120", "primary_published_chronology"),
            evidence("The dialogue describes existing post-scarcity technology while recognizing persistent differences between worlds.", ["src-commonwealth-abyss-dialogue"], "Nigel and Paula's conversation, indexed page 8", "character_statement")],
           ["Reference-led and partly based on earlier same-continuity chronology; the later novel period is not silently equated with every earlier stage.", "Control remains an uncertain mixture of personal and collective power; regime 1 is an alternative.", "Nigel's expectation that a future colony will stay uniform is not accepted as a realized guarantee."], alternatives=[1]),
    record("void-ana-community", "c0199", "The Void Trilogy (The ANA community)", "The Void Trilogy", "ANA's active uploaded human community", ["book"],
           scope("Hamilton's Commonwealth continuity", "The functioning ANA community and its Void-era factions before final transcendence", "Active uploaded human-derived residents of ANA", ["Embodied Higher citizens counted again", "Inactive backup records", "Every ordinary Commonwealth AI treated as an ANA citizen", "A completed postphysical transcendence assumed in advance"], proxy=True, proxy_basis="The active uploaded residents are human-derived persons; ANA is not treated as one person with every resident merely an avatar."),
           "ANA supports an active community of uploaded human personalities who have left ordinary bodily life. Their continued experiences and interaction occur within its computational system, rather than through earning conventional wages for physical necessities. This supports strong provision for admitted active residents. It does not establish a right for every outsider to enter, and neither dormant backup files nor the separately embodied Higher population enlarge the resident count.\n\nANA is politically divided: factions pursue different aims and form alliances. The control estimate therefore treats its residents as participants in a human-derived collective, not passive subjects of a wholly separate machine ruler. It is qualified by powerful factions and incompletely documented decision rules. ANA's governmental role outside the community does not make all external citizens equal members of it. Political action and the creation of virtual experiences can remain useful work, so the absence of ordinary subsistence jobs supplies no exact nonworking share. The record stops before any eventual transition to another mode of existence.",
           {"guarantees": -0.85, "control": 0.7, "nonworking": None},
           {"guarantees": assessment(-0.85, [-1, -0.6], "medium", "Published chronology and setting accounts establish continuing uploaded community life apart from commercial bodily subsistence; universal admission and detailed resource rules remain unspecified.", a),
            "control": assessment(0.7, [0.25, 0.95], "medium", "Active human-derived factions participate in ANA's collective decisions. This supports real member agency but not a claim of equal political influence.", ["src-void-deathrobots-review", "src-void-ana-readers"]),
            "nonworking": assessment(None, None, "low", "The community engages in political and creative activity; no all-active-resident work census is established.", ["src-void-deathrobots-review"])},
           2, a,
           [evidence("Humans migrate into ANA and remain active within a politically divided collective.", a, "Published chronology and identified ANA faction discussions", "primary_chronology_and_secondary_lore")],
           ["The human-derived active-person proxy must stay visible despite sources' loose use of the term AI.", "The control score is relative to ANA's residents; its power over embodied outsiders is a different relationship.", "No completed transcendence or unlimited admission right is assumed."], alternatives=[1])
]
D = [
    decision("c0195", "needs_evidence", "The early commercial Commonwealth does not inherit the later Higher rejection of wage economics.", ["src-commonwealth-early-readers", "src-commonwealth-faller-timeline"], analysis="Paid rejuvenation and market institutions make a universal post-work label unsafe; the quick sources do not establish an earlier general labor-independent support arrangement.", follow_up="Skip deeper reading; retain the later Higher and ANA systems separately."),
    decision("c0196", "needs_evidence", "High Angel's manufacturing and worker housing are verified in the excerpt, but general employment-independent access is not.", ["src-high-angel-primary-quoted"], analysis="The entity's origin is explicitly uncertain between machine and biological life. Its human domes begin as housing for astroengineering workers, not a demonstrated universal welfare state.", follow_up="Skip deeper reading; do not infer AI sovereignty or free necessities from a sentient ship alone."),
    decision("c0197", "needs_evidence", "The Raiel's immense technological capacity does not establish household provision, labor participation or a justified economic population scope.", ["src-raiel-reference-excerpts"], analysis="Ancient shipbuilding and a galactic golden age are not a documented post-work distribution system.", follow_up="Skip a primary-text investigation under the faster-pass instruction."),
    decision("c0198", "included", "The broad Greater Commonwealth lead is narrowed to embodied Higher culture with an explicit rejection of commercial economics.", h + ["src-void-deathrobots-review"], society_id="void-higher-culture"),
    decision("c0199", "included", "ANA provides a separate active uploaded community with factional human-derived collective agency.", a, society_id="void-ana-community")
]
write_batch(37, [f"c{i:04}" for i in range(195, 200)], S, R, D, [
    "The faster reference pass distinguishes early commercial Commonwealth, embodied Higher culture and ANA rather than mapping an entire franchise to one coordinate.",
    "Published chronology and short indexed primary dialogue provide admission support; no full novel read or blocked-source recovery was attempted.",
    "ANA's residents remain active human-derived persons. The loosely used AI label does not decide control by itself, and inactive records do not count as leisure people.",
    "Nigel's proposed uniform colony is not an enacted Commonwealth institution. High Angel's uncertain origin and worker-housing scope remain unresolved.",
    "Second pass checked source scope, chronology and distinctions; participation rates remain open rather than invented."
])
