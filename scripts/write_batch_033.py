from research_helpers import source, assessment, record, scope, evidence, decision, write_batch

S = [
    source("src-incandescence-big-idea", "Incandescence: The Big Idea", "Greg Egan, official website",
           "https://www.gregegan.net/INCANDESCENCE/Idea/Idea.html", "official_author_commentary",
           "Public premise paragraphs read", "The Splinter's deliberately pre-industrial scientific-discovery premise.",
           "The astrophysical explanation is not an automatic-production or allocation system; no further technical reading was needed."),
    source("src-learning-me-reference", "Learning to Be Me", "Wikipedia contributors",
           "https://en.wikipedia.org/wiki/Learning_to_Be_Me", "secondary_plot_reference",
           "Public indexed plot account read", "The jewel, identity transfer and its relationship to the biological brain.",
           "Biomedical/mind-transfer capability alone does not establish a whole society's economic arrangements."),
    source("src-border-guards-author", "Border Guards", "Greg Egan, official website",
           "https://www.gregegan.net/BORDER/Border.html", "official_author_synopsis",
           "Public synopsis read", "Noether, Jamil, quantum soccer and postmortal life.",
           "The synopsis does not describe necessities production or general access rights; no full story read was attempted."),
    source("src-crystal-nights-primary-indexed", "Crystal Nights", "Greg Egan, official story text",
           "https://www.gregegan.net/MISC/CRYSTAL/Crystal.html", "primary_fiction_indexed_excerpt",
           "Public indexed passages on the simulated population read", "Creator intervention, scarcity tests, Phite labor and later scientific development.",
           "Targeted indexed passages only. The population is nonhuman and the resource/work rules change over time; no single post-work point is inferred."),
    source("src-chasm-city-identity-thesis", "Restoration of identity from space in Alastair Reynolds's Chasm City", "Tampere University repository thesis",
           "https://trepo.tuni.fi/bitstream/10024/94688/1/GRADU-1386072830.pdf", "secondary_scholarly_analysis_indexed_excerpt",
           "Public indexed page 39 discussion consulted", "Automated city maintenance, service work, the Canopy/Mulch divide and the pre-plague post-scarcity order.",
           "Indexed excerpt, not a full PDF read or visual check. Its inference from the absence of unemployment discussion is not adopted as a labor census."),
    source("src-demarchy-linguistic-thesis", "Analysis of faction terminology in Revelation Space", "University of Oulu repository thesis, 2015",
           "https://oulurepo.oulu.fi/bitstream/10024/40695/1/nbnfioulu-201505261664.pdf", "secondary_scholarly_analysis_indexed_excerpt",
           "Public indexed Demarchist entry read", "Ubiquitous voting implants and participatory political decisions.",
           "The near-automatic voting interface is distinct from automatic production; original Greek lottery demarchy is not substituted for the novel's system."),
    source("src-yellowstone-grubstreet", "Chasm City discussion", "Grub Street literary review archive",
           "https://grubstreethack.wordpress.com/page/4/", "secondary_literary_review_indexed",
           "Public indexed pre-plague setting paragraph read", "Yellowstone's earlier near-post-scarcity prosperity and the later disruption.",
           "Archive page may contain unrelated reviews; only the identified Chasm City paragraph supports this record."),
    source("src-glitterband-sfandf", "Elysium Fire - Alastair Reynolds", "Sci-Fi and Fantasy Reviews, 13 December 2017",
           "https://sfandfreviews.blogspot.com/2017/12/?m=0", "secondary_literary_review_indexed",
           "Public indexed setting paragraphs read", "Glitter Band abundance, citizen votes, local habitat autonomy and different lifestyles.",
           "No uniform work census across all habitats. Comatose bodies do not automatically count as active leisure people; virtual minds require explicit treatment.")
]
q = ["src-chasm-city-identity-thesis", "src-yellowstone-grubstreet", "src-glitterband-sfandf"]
c = ["src-demarchy-linguistic-thesis", "src-glitterband-sfandf"]
R = [record("yellowstone-demarchy-preplague", "c0178", "Revelation Space (The Yellowstone Demarchy before the Melding Plague)", "Revelation Space", "The pre-plague Yellowstone system's demarchic post-scarcity order", ["book"],
    scope("Reynolds's Revelation Space continuity, including its prequel depictions", "The established high-technology order before the Melding Plague; the Prefect-era Band supplies same-period institutional context", "Living residents of the Yellowstone demarchic system and its participating habitats", ["Post-plague Chasm City", "All habitats assumed to have identical internal institutions", "The Conjoiners or Ultras assigned demarchic rules", "Stored bodies or passive files counted as active people"]),
    "Before the Melding Plague, Yellowstone's demarchic civilization combines extensive automatic infrastructure with broad material abundance. Sources describe the earlier city and orbital communities as near or effectively post-scarcity, rather than societies whose basic output requires a large conventional workforce. This supports substantial guarantees for residents, qualified by the lack of a single documented universal entitlement charter. The later destruction of the system belongs to a different period.\n\nCitizen implants allow continuous participation in public decisions, and habitats retain considerable autonomy. These arrangements favor distributed human control rather than a single owner or an autonomous machine government. They also permit diverse local choices, so the system-wide coordinate is an approximate common reference point, not a claim that every habitat is identical. Police, artists and other useful workers remain. Neither abundance nor elaborate voting automation supplies an all-resident nonworking percentage. The orbital setting alone is not a reason to add another equivalent economic point when the Glitter Band lead is reached.",
    {"guarantees": -0.7, "control": 0.85, "nonworking": None},
    {"guarantees": assessment(-0.7, [-0.9, -0.35], "medium", "Independent setting accounts describe broad abundance with automatic infrastructure; a universal formal guarantee is not established for every habitat.", q),
     "control": assessment(0.85, [0.6, 1], "medium", "Continuous citizen voting and local habitat autonomy support dispersed effective human control, with local differences retained.", c),
     "nonworking": assessment(None, None, "low", "Useful professions and varied habitat lifestyles remain; no all-resident participation estimate is supported.", ["src-glitterband-sfandf"])},
    2, q + ["src-demarchy-linguistic-thesis"],
    [evidence("The pre-plague system has broad abundance; demarchic public control coexists with diverse local communities.", q + c, "Indexed pre-plague city, voting and Glitter Band setting accounts", "secondary_lore_report")],
    ["Reference-led umbrella record; materially different local economies would need their own evidence before a split.", "The catastrophe is not silently included in an earlier guarantee score.", "No complete primary novel read or work census is claimed."])]
D = [
    decision("c0174", "boundary_case", "The Splinter is explicitly a pre-industrial discovery society, not a verified automatic-support economy.", ["src-incandescence-author", "src-incandescence-big-idea"], analysis="An unusual habitat and advanced scientific insight do not confer the Amalgam's productive technology or guarantees.", follow_up="Preserve as a separate low-technology comparison; skip deeper reading."),
    decision("c0175", "boundary_case", "The jewel establishes mind replacement and longevity, not general automatic material provision.", ["src-learning-me-reference"], analysis="A biomedical identity technology cannot establish population-wide work independence, ownership or guarantees.", follow_up="Skip further investigation in this pass."),
    decision("c0176", "needs_evidence", "The short official account identifies a postmortal community but leaves its material production and allocation unstated.", ["src-border-guards-author"], analysis="Immortality and leisure in a featured scene do not establish a complete economic regime.", follow_up="Skip the full story under the user's faster-pass instruction."),
    decision("c0177", "needs_evidence", "The indexed passages show changing creator-imposed rules for a nonhuman simulated population, without a stable scoped post-work arrangement.", ["src-crystal-nights-primary-indexed"], analysis="Substrate support, manipulated famines and later scientific labor must not be merged into one universal leisure society; the population proxy also needs justification.", follow_up="Skip a full-story reconstruction in the faster pass."),
    decision("c0178", "included", "Clear references establish the pre-plague demarchic order's automatic support, abundance and distributed public control.", q + ["src-demarchy-linguistic-thesis"], society_id="yellowstone-demarchy-preplague")
]
write_batch(33, [f"c{i:04}" for i in range(174, 179)], S, R, D, [
    "Continues the user's faster reference pass without full-story reading, downloaded novels or technical reconstruction.",
    "The Splinter, jewel technology and a postmortal sporting scene do not inherit another Egan society's economic arrangements.",
    "The Yellowstone record deliberately covers the pre-plague demarchic system. The later Glitter Band lead must be checked for economic duplication, not counted again for location alone.",
    "Second pass checked scope and sources; universal charters and participation rates remain unstated where not supported."
])
