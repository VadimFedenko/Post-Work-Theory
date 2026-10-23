from research_helpers import source, decision, write_batch

S = [
    source("src-rapture-shelf-awareness", "The Rapture of the Nerds", "Shelf Awareness, 7 September 2012",
           "https://www.shelf-awareness.com/ar/readers/2012-09-07/the_rapture_of_the_nerds.html", "secondary_trade_review",
           "Public indexed setting summary read", "Terrestrial preserve, Huw's pottery and the distinction from uploaded humanity.",
           "A preserve/paradise description does not establish production or enforceable access; no novel read was attempted."),
    source("src-quantum-thief-reference", "The Quantum Thief", "Wikipedia contributors",
           "https://en.wikipedia.org/wiki/The_Quantum_Thief", "secondary_plot_and_setting_reference",
           "Public indexed setting and economy account read", "Quiet labor, time balances, hidden rulers, Sobornost emulations and Zoku.",
           "General reference; human brain emulations must not silently become nonhuman automatic labor. No primary novel read claimed."),
    source("src-rajaniemi-gill-glossary", "Wiki/Glossary for The Quantum Thief / The Fractal Prince / Jean le Flambeur", "Karan Gill",
           "https://www.karangill.com/glossary-quantum-thief-fractal-prince-jean-le-flambeur/", "secondary_fan_glossary",
           "Public entries on Time, Quiet, gogols and locations read", "Time purchases goods; uploaded citizens operate city-maintenance bodies; visitors have different rules.",
           "Fan terminology sometimes calls emulations AI; no automatic admission follows from that label. The glossary is not a constitution or census."),
    source("src-quantum-thief-random-review", "The Quantum Thief - Hannu Rajaniemi", "Random's 23 cents, 4 October 2012",
           "https://mybiochemicalsky.wordpress.com/2012/10/04/the-quantum-thief/", "secondary_literary_review_indexed",
           "Public indexed faction discussion read", "Specialized human gogol labor and Zoku virtual-world capabilities.",
           "Review only; world creation and a gaming culture do not establish universal economic entitlements."),
    source("src-fractal-prince-truslow", "The Fractal Prince by Hannu Rajaniemi", "Tori Truslow, Strange Horizons",
           "https://strangehorizons.com/wordpress/non-fiction/reviews/the-fractal-prince-by-hannu-rajaniemi/", "secondary_literary_review_indexed",
           "Public indexed Sirr setting discussion read", "Elite families, utility fog, jinn and the city's conflict with the Sobornost.",
           "Technological explanation of apparent magic does not supply household allocation rules or free necessities."),
    source("src-rajaniemi-characters-reference", "List of characters in the Jean le Flambeur series", "Wikipedia contributors",
           "https://en.wikipedia.org/wiki/List_of_characters_in_the_Jean_le_Flambeur_series", "secondary_series_reference",
           "Public indexed Oortian and faction entries read", "Mieli, Oortian cultural origin and the distinct factions.",
           "Character background does not establish the Oortian general material economy; no trilogy read was attempted.")
]

D = [
    decision("c0158", "needs_evidence", "The terrestrial preserve is identified, but short references do not establish how its basic goods are produced and allocated.", ["src-rapture-author-about", "src-rapture-shelf-awareness"], analysis="Huw's chosen pottery and a paradise label do not establish all residents' work independence or control of support systems.", follow_up="Skip further reading in the faster pass; reopen only on a clear economic reference."),
    decision("c0159", "boundary_case", "Oubliette's machine bodies are operated by uploaded citizens performing real work in exchange for time.", ["src-quantum-thief-reference", "src-rajaniemi-gill-glossary"], analysis="The Quiet are active human emulations maintaining the city. Counting embodied citizens' leisure while erasing their working uploaded phases would distort both the labor mechanism and denominator. No independently automated replacement or unnecessary-work policy was established.", follow_up="Preserve as a body/upload labor-cycle comparison; skip a deeper novel investigation."),
    decision("c0160", "boundary_case", "The Sobornost's productive miracle relies on specialized human brain emulations, not an established independent post-work support system.", ["src-quantum-thief-reference", "src-quantum-thief-random-review"], analysis="Gogols are human-derived workers. Their enslavement and vast infrastructure do not establish freedom from labor for the scoped population, and no arbitrary AI/person distinction is used to erase their work.", follow_up="Skip deeper reading; a narrower elite-support point would require clear allocation evidence rather than presumed privilege."),
    decision("c0161", "needs_evidence", "Sirr's technological capabilities and elite hierarchy are documented, but general labor-independent provision is not.", ["src-fractal-prince-truslow", "src-rajaniemi-gill-glossary"], analysis="Utility fog, jinn and trade in minds do not themselves establish reliable material access for residents.", follow_up="Skip primary-text recovery under the user's pace instruction."),
    decision("c0162", "needs_evidence", "The quick faction references establish Zoku virtual-world capabilities without settling a scoped Causal Angel economy.", ["src-quantum-thief-random-review", "src-rajaniemi-characters-reference"], analysis="A quantum gaming community does not by itself establish necessities, member entitlements or useful-work participation in the target period.", follow_up="Skip deeper reading; do not manufacture a point from technological rank or franchise-wide assumptions."),
    decision("c0163", "needs_evidence", "Oortian culture and Mieli's service are identifiable, but the references do not establish general production/access arrangements.", ["src-rajaniemi-characters-reference"], analysis="One capable Oortian agent and her contract cannot determine the whole civilization's economy.", follow_up="Skip further investigation in the faster pass unless a direct economic reference becomes readily available.")
]
write_batch(30, [f"c{i:04}" for i in range(158, 164)], S, [], D, [
    "Previous goal turn was progress: the authoritative checkpoint advanced from 127 to 157, retained records from 59 to 71 and sources from 205 to 247, with the user's new faster-pass policy saved. It was neither a verified wait nor a no-progress turn.",
    "This short reference pass does not rescue unclear leads by reading novels. Non-inclusions remain explicit and do not inflate the retained count.",
    "Quiet and gogol work is human-derived useful labor. Hardware bodies or uploads alone do not make a worker disappear from the labor denominator.",
    "No new society is admitted on magical appearance, computational power, a pleasant setting or a character's employment alone."
])
