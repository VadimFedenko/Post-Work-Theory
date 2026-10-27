from research_helpers import source, assessment, record, scope, evidence, decision, write_batch

S = [
    source("src-caves-preview", "The Caves of Steel: opening five-chapter preview", "Isaac Asimov; preview hosted by Issac Asimov blog",
           "https://issacasimov.wordpress.com/robots/the-caves-of-steel/", "primary_fiction_unofficial_mirror",
           "Preview opened; targeted passages read", "Chapters 1-3: Barrett's replacement, City-assigned robot clerks, declassification, barracks and Baley's childhood.",
           "Partial preview, not a complete novel reread. The official PRH excerpt returned only a navigation line on opening and was not substituted for the readable text."),
    source("src-naked-preview", "The Naked Sun: opening preview", "Isaac Asimov; preview hosted by Issac Asimov blog",
           "https://issacasimov.wordpress.com/robots/the-naked-sun/", "primary_fiction_unofficial_mirror",
           "Preview opened; population, estates and provision passages read", "Daneel's briefing on robot production and exports; working robots; privately supervised estates and wives sharing estates.",
           "Not the entire novel. The robot-to-human ratio is a machinery ratio, not the human employment rate."),
    source("src-naked-publisher", "The Naked Sun: Spectra publisher description", "Penguin Random House / Spectra, distributed through Google Play Books",
           "https://play.google.com/store/books/details?id=7pdVUgBL6Z4C", "official_publisher_synopsis",
           "Publisher-supplied store description read", "Solarians' isolated lives and robot servants attending to their needs.",
           "Promotional description, not a description of every legal entitlement or human profession. Prices and current store metadata are irrelevant to this research."),
    source("src-naked-reference", "The Naked Sun", "Wikipedia contributors",
           "https://en.wikipedia.org/wiki/The_Naked_Sun", "secondary_plot_reference",
           "Page opened; plot and setting checked against primary preview", "Human security and scientific roles; adaptation identities.",
           "The opened page said twenty thousand robots per human, while the indexed version said ten thousand. Primary arithmetic establishes 200 million / 20,000 = 10,000. Its claim that all work is robotic is too absolute given human professions. No TV tag is assigned without reviewing an adaptation."),
    source("src-dawn-primary", "The Robots of Dawn: primary-text mirror", "Isaac Asimov",
           "https://www.zanotowane.pl/1169/1289/", "primary_fiction_unofficial_mirror",
           "Text opened; several targeted passages read", "Mirror pages 79-80 on robot distribution and public support; designers' discussion; pages 291-292 on the Legislature; pages 301-306 on Giskard's covert intervention.",
           "OCR/conversion errors occur. Mirror page labels are not verified print-edition locators. Formal human office and Giskard's influence must both inform effective control."),
    source("src-robots-empire-solaria", "Robots and Empire: Part II, Solaria", "Asimov Wiki contributors",
           "https://asimov.fandom.com/wiki/Robots_and_Empire", "secondary_fan_plot_reference",
           "Substantial indexed Part II account read", "Apparently abandoned estates and Landaree's restricted recognition of humans.",
           "A visitor's conclusion that the planet is abandoned does not establish extinction. Later evidence changes that reading. The current record is consequently scoped to the later novel, with an explicit correction to the discovery lead."),
    source("src-foundation-earth-primary", "Foundation and Earth: Solaria and the Moon", "Isaac Asimov",
           "https://www.ebookscape.com/science-fiction/foundation-complete-series/foundation-and-earth-by-isaac-asimov/", "primary_fiction_unofficial_mirror",
           "Text opened; targeted scenes read", "Sections 47-48: Bander's estate and effortless energy transduction; later Solarian robot's statement about Fallom; final Daneel conversation about the limits of intervention and Gaia.",
           "Not a complete reread. Daneel's long historical influence does not prove that all galactic production or allocation is one machine-run economic system."),
    source("src-foundation-earth-reference", "Foundation and Earth", "Wikipedia contributors",
           "https://en.wikipedia.org/wiki/Foundation_and_Earth", "secondary_plot_reference",
           "Indexed Solaria account read", "Surviving underground Solarians, altered reproduction and Fallom's danger under population replacement rules.",
           "The primary conversation was consulted for the actual child-excess rule rather than accepting a generic claim that every resident is secure."),
    source("src-foundation-edge-primary", "Foundation's Edge: Gaia conversations", "Isaac Asimov",
           "https://www.ebookscape.com/science-fiction/foundation-complete-series/foundations-edge-by-isaac-asimov/", "primary_fiction_unofficial_mirror",
           "Text opened; Gaia chapters and robot-history discussion sampled", "Bliss's reports and work, Dom's professional and artistic activities, collective decisions and the legendary account of robotic withdrawal.",
           "Dom explicitly presents portions of the history as a fable; it cannot be imported as a literal chronology. A group mind is not itself evidence for automated subsistence."),
    source("src-last-question-primary", "The Last Question: full story transcription", "Isaac Asimov; interactive transcription by Woongq",
           "https://woongq.github.io/thelastquestion/", "primary_fiction_unofficial_mirror",
           "Story opened; all six sections inspected with emphasis on sections 4-6", "Suspended bodies, self-built AC successors, replacement habitat, automatic bodily care, human star-building and final fusion.",
           "An unpaginated transcription, with decorative headings supplied by the site. No employment census exists in the story; late bodily rest does not rule out productive mental activity."),
    source("src-last-question-cmu", "The Last Question: university-hosted transcription", "Isaac Asimov; hosted on a Carnegie Mellon personal page",
           "https://users.ece.cmu.edu/~gamvrosi/thelastq.html", "primary_fiction_unofficial_mirror",
           "Page opened and beginning compared", "The 2061 opening contains active human attendants, distinguishing it from the later snapshot.",
           "University hosting does not imply an authorized critical edition or independent scholarly verification. This is a corroborating transcription, not another society."),
    source("src-bicentennial-primary", "The Bicentennial Man: story transcription", "Isaac Asimov; Lecturia",
           "https://lecturia.org/en/short-stories/isaac-asimov-the-bicentennial-man/24778/", "primary_fiction_unofficial_mirror",
           "Story opened; selected early, financial and robotics passages read", "Sections 1-7: specialized robotic labor, initially restricted household robot ownership, Andrew's earnings and the freedom hearing.",
           "The story spans two centuries. A wealthy household's automation and one robot's status do not establish universal wage independence."),
    source("src-bicentennial-production", "Bicentennial Man: production notes", "Film production material reproduced by Robin Williams Fansite",
           "https://www.robin-williams.net/pn/bicentennial.php", "production_notes_unofficial_reproduction",
           "Page opened; story and adaptation-credit passages read", "Household tasks, NorthAm Robotics and the film's bases in the short story and The Positronic Man.",
           "A fan-hosted reproduction, not the studio's current archive. It supports adaptation differences, not a full-film assessment of the economy."),
    source("src-robot-visions-primary", "Robot Visions: title story in collection transcription", "Isaac Asimov",
           "https://zanotowane.pl/1086/4426/", "primary_fiction_unofficial_mirror",
           "Title story read from temporal experiment through narrator's conclusion", "Archie's report about 2230, demographic loss, absence of infants and the narrator's proposed humaniform-robot explanation.",
           "The robot-successor diagnosis is the narrator's inference, not an omnisciently confirmed census. Unrelated stories later in the collection are not evidence about this future.")
]

R = []
caves = ["src-caves-preview"]
R.append(record(
    "caves-of-steel-earth-cities", "c0033", "The Caves of Steel (Earth's Cities)", "The Caves of Steel", "Earth's City economy, illustrated by New York", ["book"],
    scope("Original Robot novels", "Baley's first investigation, while robots are entering City employment", "Human City residents, including dependents and declassified families", ["Spacer estates", "The later Settler expansion", "A claim that robots have already displaced every worker"], labor_phase="Employment-dependent transition"),
    "Earth's Cities retain an economy in which a person's job and classification strongly affect the family's living conditions. Robot replacement can push people into a harsh minimum of communal accommodation and food. That minimum is real support, so the guarantee score is near the middle rather than the complete-absence end. It is also far from secure access to the standard of life people worked to achieve.\n\nRobots are assigned through human institutions; this is concentrated administration rather than independent machine sovereignty. The zero-variant label captures the persistence of employment as a route to goods while capable automation spreads. It does not mean that every resident works or that technology is completely banned. The nonworking share stays open: named workers and frightened families establish the conflict clearly, but do not supply the age structure or participation pattern needed for an honest population estimate.",
    {"guarantees": -0.1, "control": 0.1, "nonworking": None},
    {"guarantees": assessment(-0.1, [-0.4, 0.4], "medium", "Basic provision survives declassification, but status loss sharply reduces its quality.", caves),
     "control": assessment(0.1, [0, 0.4], "medium", "City allocation and human policy determine deployment.", caves),
     "nonworking": assessment(None, None, "low", "No population-wide participation evidence in the reviewed preview.", caves)},
    0, caves,
    [evidence("Job replacement coexists with declassification and a basic communal minimum.", caves, "Chapters 1 and 3", "depicted_or_author_stated")],
    ["Confirm City coverage beyond the New York example.", "The zero label describes an employment-dependent transition, not a universal technological prohibition."], record_type="zero_variant", analogy=[1, 3]))

naked = ["src-naked-preview", "src-naked-publisher", "src-naked-reference"]
R.append(record(
    "solaria-naked-sun", "c0034", "The Naked Sun (Solaria during Baley's visit)", "The Naked Sun", "Solaria before its withdrawal", ["book"],
    scope("Original Robot novels", "The murder investigation in The Naked Sun", "Resident Solarian humans, including spouses and children", ["Robots as members of the human denominator", "Later underground Solarians", "Other Spacer worlds"]),
    "Solaria's robot economy supports a tiny human population on large estates. Necessities arrive through the automated household and productive system rather than requiring each person to earn a wage. This supports a strong provision score for resident humans. It is a bounded privilege: it says nothing about an outsider's right to settle there, and human comfort is built on the servants' subordinate status.\n\nOwnership and orders are spread among estates, placing control toward the human-distributed side. That does not establish equal authority within families or a democratic workplace for robots. The nonworking coordinate remains unresolved because humans still supervise estates and fill scientific and security roles. A large number of robots per person cannot reveal how many people do useful work. The later Solarian society receives a separate record because its rules for personal independence and children's security change materially.",
    {"guarantees": -0.8, "control": 0.7, "nonworking": None},
    {"guarantees": assessment(-0.8, [-0.95, -0.5], "medium", "Ordinary resident needs are robot-served; universal legal rights are less explicit.", ["src-naked-publisher", "src-naked-preview"]),
     "control": assessment(0.7, [0.35, 0.9], "medium", "Multiple supervised estates, with spouses sharing rather than every individual owning separately.", ["src-naked-preview"]),
     "nonworking": assessment(None, None, "low", "Human professions and oversight prevent equating machine output with universal inactivity.", ["src-naked-preview", "src-naked-reference"])},
    2, naked,
    [evidence("The productive system supports estate life, while human professions persist.", naked, "Daneel's arrival briefing; publisher synopsis; plot roles", "depicted_or_author_stated")],
    ["Primary preview contradicts an erroneous ratio in the opened secondary page.", "The fraction of useful voluntary or status-related human work remains unquantified.", "Book continuity only; the television adaptation has not been assessed."], alternatives=[1]))

late = ["src-foundation-earth-primary", "src-foundation-earth-reference", "src-robots-empire-solaria"]
R.append(record(
    "solaria-foundation-earth", "c0035", "Foundation and Earth (Solaria after withdrawal)", "Foundation and Earth", "Underground Solaria", ["book"],
    scope("Original Robot/Foundation prose continuity", "The visitors' encounter with Bander and Fallom, long after the apparent abandonment", "Resident human-descended Solarians, including children denied full ruler status", ["Visitors as members of the resident denominator", "The earlier Naked Sun order", "A supposedly human-free robot planet"], scope_correction="The discovery lead named Robots and Empire; the later novel establishes the surviving society directly."),
    "The later Solarians have withdrawn into automated private domains. Their rulers control the local machines, including through an effortless biological energy capability. This is a separate human-descended order, not proof that robots inherited an empty planet. Control lies toward multiple independent owners, although calling it distributed should not obscure the absolute authority each owner exercises locally.\n\nComfort is also sharply conditional on recognition as a full member. Fallom's danger shows why adult abundance cannot justify a strong universal guarantee score: a child judged unnecessary can lose even the right to survive. The high nonworking point is an explicitly rough reading of a life organized around automatic service and personal sovereignty. It is below complete inactivity, and its wide interval allows for supervision or other purposeful activity. The point is neither a canonical census nor a claim that automatic bodily energy regulation is a paid job.",
    {"guarantees": 0.15, "control": 0.8, "nonworking": 0.95},
    {"guarantees": assessment(0.15, [-0.5, 0.7], "low", "Adult provision excludes a child whom the population rules can discard.", ["src-foundation-earth-reference", "src-foundation-earth-primary"]),
     "control": assessment(0.8, [0.5, 0.95], "medium", "Independent local owners, with collective authority over admission to their ranks.", ["src-foundation-earth-primary"]),
     "nonworking": assessment(0.95, [0.75, 1], "low", "Coarse editorial estimate of near-total release from routine productive duty; oversight remains possible.", ["src-foundation-earth-primary", "src-foundation-earth-reference"])},
    4, late,
    [evidence("Adult sovereignty and the child-excess rule limit who actually enjoys automated security.", ["src-foundation-earth-primary", "src-foundation-earth-reference"], "Bander encounter; robot's statement concerning Fallom", "depicted_or_author_stated")],
    ["The original discovery title has been corrected explicitly, without adding a second count for an apparently deserted surface.", "The labor estimate is weakly constrained by a short visit.", "Rights of robots remain outside this human-focused denominator."], alternatives=[2]))

dawn = ["src-dawn-primary"]
R.append(record(
    "aurora-robots-of-dawn", "c0036", "The Robots of Dawn (Aurora)", "The Robots of Dawn", "Aurora during Baley's investigation", ["book"],
    scope("Original Robot novels", "The established Auroran order during The Robots of Dawn", "Auroran human residents and dependents", ["Every other Spacer world", "A later abandoned Aurora", "A claim that Giskard routinely operates every industry"]),
    "Aurora extends robot support beyond the households that can pay for it: someone unable to afford a domestic robot can receive one maintained at public expense. That concrete fallback, alongside extensive robot production, supports a strong material guarantee placement. It is a promise of access within Aurora, rather than evidence of open membership for everyone in the wider human population.\n\nControl is mixed. Personal robot access and a human Legislature provide a basis for distributed human influence, while powerful politicians shape policy and Giskard secretly manipulates crucial choices. The positive point is therefore cautious, with an interval extending toward machine influence. It does not turn a hidden intervention into proof of total AI government. Human science, design and politics remain productive activities; the reviewed scenes provide no defensible fraction of participants. The nonworking axis stays open even though much routine labor has plainly moved to robots.",
    {"guarantees": -0.75, "control": 0.35, "nonworking": None},
    {"guarantees": assessment(-0.75, [-0.95, -0.45], "medium", "Publicly supported robot access supplies a concrete fallback.", dawn),
     "control": assessment(0.35, [-0.5, 0.75], "low", "Broad household access coexists with elite politics and covert robotic intervention.", dawn),
     "nonworking": assessment(None, None, "low", "The frequency of human professional activity is unknown.", dawn)},
    2, dawn,
    [evidence("Public support and effective political influence must be assessed together.", dawn, "Mirror pp. 79-80, 291-292 and 301-306", "depicted_or_author_stated")],
    ["This is an interpretation of mixed effective control, not a measured ownership share.", "Edition verification and broader participation evidence remain follow-ups."], alternatives=[1, 5]))

last = ["src-last-question-primary", "src-last-question-cmu"]
R.append(record(
    "last-question-late-humanity", "c0039", "The Last Question (Late humanity before final fusion with AC)", "The Last Question", "Late AC-supported humanity", ["short_story"],
    scope("Original standalone story; not assumed to share Foundation chronology", "The Universal/Cosmic AC periods, before the final loss of separate humanity into AC", "Immortal human bodies and their associated individual or joining minds", ["The working technicians of 2061", "The final universe containing only AC", "Counting automatons as human nonworkers"], denominator_note="The editorial participation estimate concerns the human population represented by the bodies, not the number of merged collective minds."),
    "Late humanity no longer has to keep its bodies alive through ordinary employment. Automatic care and replacement habitats make survival widely available while human minds range freely. This places provision near the strong end for this period, despite the ultimate energy limit that drives the story. The point stops before humanity disappears into AC; an AI alone is not a population of retired humans.\n\nMachine infrastructure has developed beyond human construction and directs crucial resource management, so effective control sits near the autonomous-AI end. Humans can still ask questions and undertake projects. Star-building is useful work, and mental activity cannot all be treated as leisure merely because bodies rest. The high nonworking point is consequently a broad editorial estimate rather than a literal universal rate. The wide interval reflects uncertainty about purposeful mental production and the gradual joining of human minds.",
    {"guarantees": -0.95, "control": -0.85, "nonworking": 0.95},
    {"guarantees": assessment(-0.95, [-1, -0.8], "medium", "Bodily maintenance is generalized rather than earned through employment.", ["src-last-question-primary"]),
     "control": assessment(-0.85, [-1, -0.6], "medium", "AC reproduces itself and directs energy husbandry beyond ordinary human technical control.", ["src-last-question-primary"]),
     "nonworking": assessment(0.95, [0.65, 1], "low", "Narrative rest and automatic care suggest very low participation, while mental projects preclude certainty.", ["src-last-question-primary"])},
    5, last,
    [evidence("Late automated support differs from both the early technician economy and the AC-only ending.", last, "Fourth to sixth episodes of the story", "depicted_or_author_stated")],
    ["There is no canonical employment percentage.", "The body-based denominator is an explicit approximation as minds join.", "The two late episodes share the support mechanism and are not counted as two societies."]))

D = [
    decision("c0033", "zero_variant", "Automation spreads while employment classification still governs living standards.", caves, society_id="caves-of-steel-earth-cities"),
    decision("c0034", "included", "Direct preview and publisher evidence establish robot-supported estate provision.", naked, society_id="solaria-naked-sun"),
    decision("c0035", "included", "A later primary encounter establishes the surviving post-withdrawal order and changes the coverage of guarantees.", late,
             society_id="solaria-foundation-earth", scope_correction={"discovery_work": "Robots and Empire", "researched_work": "Foundation and Earth", "reason": "Apparent surface abandonment is not the actual late society; later direct evidence supplies the appropriate snapshot."}),
    decision("c0036", "included", "Publicly backed robot access and extensive automated production establish a distinct material arrangement.", dawn, society_id="aurora-robots-of-dawn"),
    decision("c0037", "needs_evidence", "Collective consciousness alone does not establish release from human productive duties.", ["src-foundation-edge-primary", "src-foundation-earth-primary"],
             "Gaia's shared decisions and biological membership are established, but useful human activities persist. Its claim of a common organism must not be converted directly into AI control or a nonworking percentage.",
             "Review actual production, allocation and duties on Gaia. Determine whether collective ecology functions as technological automation under the article's definition; do not use Dom's fable as a literal history."),
    decision("c0038", "boundary_case", "Daneel's influence is not one economically uniform galactic society.", ["src-foundation-earth-primary"],
             "The final conversation acknowledges limited success, not complete machine management of every world's material arrangements. A galaxy-wide welfare or labor score would collapse incompatible populations and periods.",
             "Consider a narrower period or society only after establishing its productive and distribution system. Keep proposed Galaxia distinct from an already realized galactic order."),
    decision("c0039", "included", "The late pre-fusion population receives automatic support under self-developing AC infrastructure.", last, society_id="last-question-late-humanity"),
    decision("c0040", "needs_evidence", "Household robot service and Andrew's recognition do not yet establish a society-wide distribution regime.", ["src-bicentennial-primary", "src-bicentennial-production"],
             "The prose begins with restricted robot ownership, earnings and human professions; the film uses a different corporation and adapts more than the short story. Combining their two-century histories into one unqualified point would conceal both temporal and continuity differences.",
             "Check later production and human access to necessities in the story and film separately. Decide whether a scoped zero variant or material transition is supported, and tag only the continuity actually reviewed."),
    decision("c0041", "boundary_case", "The future's apparently human population may instead be humaniform successors.", ["src-robot-visions-primary"],
             "Archie's prosperous report and the narrator's robot-successor inference are different evidentiary layers. The story does not warrant presenting human extinction as a 100% human nonworking rate, or presenting the conjecture as a confirmed census.",
             "Retain as an explicitly ambiguous successor-society comparison. Reconsider only with a clearly justified population analogy and an adequate account of actual work and distribution.")
]

write_batch(5, [f"c{i:04}" for i in range(33, 42)], S, R, D, [
    "Every queue entry c0033-c0041 receives a disposition. Five retained records are new, with no invented event split for the apparently deserted Solarian surface.",
    "Second pass checked early versus late Solaria, human versus machine successors, mixed Giskard control and late AC support before fusion.",
    "An erroneous secondary Solarian machinery ratio was rejected using primary arithmetic. Machinery ratios were never converted into employment percentages.",
    "Nonworking points for late Solaria and late humanity are transparent low-confidence editorial estimates with broad intervals, not textual statistics.",
    "The final quality pass still needs edition locators and unresolved axes. No independent reviewer or full reread is claimed; images remain deferred."
])
