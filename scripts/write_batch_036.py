from research_helpers import source, decision, write_batch

S = [
    source("src-steel-breeze-wertzone", "On the Steel Breeze by Alastair Reynolds", "The Wertzone, September 2013",
           "https://thewertzone.blogspot.com/2013/09/on-steel-breeze-by-alastair-reynolds.html", "secondary_literary_review_indexed",
           "Public indexed holoship setting paragraphs read", "The Zanzibar and the interstellar caravan's survival and political constraints.",
           "Life support for a generation ship does not by itself establish labor-independent access or one uniform shipboard constitution."),
    source("src-revenger-bonesilence-starburst", "Bone Silence", "Ed Fortune, Starburst Magazine",
           "https://www.starburstmagazine.com/reviews/bone-silence/", "secondary_literary_review_indexed",
           "Public indexed economic discussion read", "The Congregation's trade, piracy and quoin currency.",
           "Later-trilogy context only. A strange currency and ancient high technology do not establish automatic household provision."),
    source("src-troika-york-description", "Troika description in Alastair Reynolds book reviews", "Susan Stepney's University of York book page; reproduced publisher description",
           "https://www-users.york.ac.uk/~ss44/books/pages/r/AlastairReynolds.htm", "publisher_description_reproduction",
           "Identified public Troika description read", "Russian cosmonauts investigating the Matryoshka construct.",
           "The page contains descriptions of many separate works. A nearby Mechanism description is not treated as Troika's economy or continuity."),
    source("src-aquila-ldr-reference", "Beyond the Aquila Rift", "Love, Death & Robots Wiki contributors",
           "https://lovedeathrobots.fandom.com/wiki/Beyond_the_Aquila_Rift", "secondary_adaptation_reference_indexed",
           "Public indexed caretaker/simulation and adaptation-difference passages read", "Thom's simulated experience, the alien caretaker and differences from the original story.",
           "No episode watched or full story read. Simulated comfort does not verify durable bodily provision; the biological caretaker is not automatically an AI sovereign."),
    source("src-aquila-netflix-review", "Love, Death & Robots Season 1 Episode 7: Beyond the Aquila Rift Ending Explained", "What's on Netflix, 2019",
           "https://www.whats-on-netflix.com/news/love-death-robots-episode-7-beyond-the-aquila-rift-ending-explained/", "secondary_episode_explanation_indexed",
           "Public indexed ending explanation consulted", "The simulation and physical condition revealed outside it.",
           "Independent fan publication, not Netflix itself. No universal welfare population is inferred from one traveler's experience."),
    source("src-zima-episode-reference", "List of Love, Death & Robots episodes: Zima Blue", "Wikipedia contributors",
           "https://en.wikipedia.org/wiki/List_of_Love%2C_Death_%26_Robots_episodes", "secondary_episode_synopsis",
           "Public indexed Zima Blue synopsis read", "The artist's origin, upgrades and return to pool-cleaning.",
           "One android's life and artistic resources do not establish society-wide production or access. The short story remains a separate version."),
    source("src-galactic-north-reference", "Galactic North", "Wikipedia contributors",
           "https://en.wikipedia.org/wiki/Galactic_North", "secondary_plot_reference",
           "Public indexed late Greenfly plot account read", "Machine expansion, human flight, preserved scans and the surviving Conjoiner group.",
           "Machine-tended biospheres do not establish a supported human leisure society. The story and collection sharing a title are distinguished.")
]
D = [
    decision("c0189", "needs_evidence", "The holoship reference establishes a generation society but does not settle labor-independent basic access.", ["src-steel-breeze-wertzone"], analysis="A life-support system, a large passenger population and advanced propulsion do not alone establish who controls production or whether necessities depend on work.", follow_up="Skip deeper reading under the pace instruction."),
    decision("c0190", "boundary_case", "The quick sources describe a working salvage/trade economy, without a verified automatic support or unnecessary-employment mechanism.", ["src-revenger-bonesilence-starburst"], analysis="Quoins and ancient artifacts are not proof of post-work distribution. Later currency disruption does not retroactively supply a welfare economy.", follow_up="Preserve as a far-future trade comparison; skip a trilogy investigation."),
    decision("c0191", "needs_evidence", "The discovery label Mechanism-dominated Earth is unverified for Troika.", ["src-troika-york-description"], analysis="The identified Troika description concerns the Matryoshka and cosmonauts. The same archive also contains other Reynolds books; nearby Mechanism wording cannot be imported across works.", follow_up="Skip deeper reading; correct the lead only if a clear Troika-specific economic source appears."),
    decision("c0192", "boundary_case", "The simulated sanctuary does not establish a durable material-support society for a defined living human population.", ["src-aquila-ldr-reference", "src-aquila-netflix-review"], analysis="Thom's comfort is not proof of bodily security, the other crew members are not automatically living leisure residents, and the alien caretaker is not proven AI. Original-story and animated continuity details cannot be merged.", follow_up="Keep as a care/illusion comparison; no full-story or episode reconstruction in this pass."),
    decision("c0193", "boundary_case", "Zima's artistic life and robot origins do not establish an entire robot-served human economy.", ["src-zima-episode-reference"], analysis="The episode focuses on one android's chosen work and transformation, not general household allocation or a human nonworking population.", follow_up="Skip the broad society lead; do not infer general guarantees from an exceptional artist."),
    decision("c0194", "boundary_case", "Greenfly expansion displaces human civilization rather than documenting a human population maintained in post-work security.", ["src-galactic-north-reference"], analysis="Vegetated machine biospheres, passive colonist scans and fugitives are different things. Neither lost humans nor unoccupied habitats create a 100% nonworking denominator.", follow_up="Preserve as an autonomous machine-ecology comparison and skip further investigation.")
]
write_batch(36, [f"c{i:04}" for i in range(189, 195)], S, [], D, [
    "Reference-led fast dispositions without full-text recovery. Six unsupported/boundary leads do not inflate the retained count.",
    "The Troika discovery label is not verified by a mixed-work review archive. Mechanism facts from another novel are not borrowed.",
    "Aquila Rift versions are kept distinct; an alien caregiver is not automatically AI, and simulated comfort is not equivalent to reliable bodily support.",
    "Zima's exceptional resources and Greenfly's machine-tended vegetation do not establish human leisure societies."
])
