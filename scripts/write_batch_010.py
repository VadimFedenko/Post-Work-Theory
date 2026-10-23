from research_helpers import source, assessment, record, scope, evidence, decision, write_batch

S = [
    source("src-childhood-revenant", "Utopian Wasteland: Abundance, Futurity, and the Golden Age in Arthur C. Clarke's Childhood's End", "Jerome Cox-Strong; Revenant, Post-Apocalyptic Waste, pages 224-242",
           "https://www.revenantjournal.com/contents/utopian-wasteland-abundance-futurity-and-the-golden-age-in-arthur-c-clarkes-childhoods-end/", "secondary_academic_analysis_with_primary_excerpts",
           "Open-access article opened; Golden Age, labor and power passages read", "Quoted novel pages 68-75 and 93; free necessities, paid luxuries, Overlord power and eventual destruction.",
           "The article's stricter full-unemployment test differs from this project's wage-independence test. Its judgment that the ending undermines utopia does not erase earlier material provision."),
    source("src-childhood-abrash", "Utopia Subverted: Unstated Messages in Childhood's End", "Merritt Abrash; Extrapolation 30.4 (1989), pages 372-379; eNotes reproduction",
           "https://www.enotes.com/topics/arthur-c-clarke/criticism/clarke-arthur/merritt-abrash-essay-date-winter-1989", "secondary_academic_analysis_with_primary_excerpts",
           "Page opened; relevant quoted passages also read in indexed text", "Robot production and free community necessities, cited as novel pages 71-72 and 112; externally imposed political order.",
           "A subscription notice appears on the page. No account or restricted download was used. Novel excerpts are mediated by scholarship, not a complete primary reading."),
    source("src-city-stars-primary", "The City and the Stars", "Arthur C. Clarke; Signet text PDF hosted by Cjayarts",
           "https://cjayarts.com/pages/library/The%20City%20And%20The%20Stars-ArthurC.Clarke.pdf", "primary_fiction_unofficial_pdf",
           "Web opens timed out; public PDF fetched successfully and targeted text extracted in memory with pypdf", "PDF pages 5, 7-10, 30, 47-53, 58 and 72: synthesis, art voting, computer veto, Lys's technology and ambiguous leadership.",
           "Locators are one-based PDF pages, not printed pages. The full file was parsed to locate passages, not read in its entirety. OCR/conversion errors remain. No full novel file or text is redistributed in the research outputs."),
    source("src-city-stars-preview", "The City and the Stars: publisher ebook preview", "Arthur C. Clarke; Open Road Integrated Media on Everand",
           "https://www.everand.com/book/387516558/The-City-and-the-Stars", "official_ebook_synopsis_and_primary_preview",
           "Product page opened; prologue and early chapter extracts read in indexed preview", "Publisher identity, designed enclosed city and Alvin's visual art.",
           "The title is marked unavailable locally; only the openly returned synopsis and indexed preview were used. No later chapter access is claimed."),
    source("src-city-stars-review", "The City and the Stars", "divinenanny; Worlds Without End, 5 February 2012",
           "https://www.worldswithoutend.com/novel_review.asp?ID=1825", "secondary_reader_review",
           "Whole short review opened and read", "Food and furniture materialization and recurrent embodied lives.",
           "The review repeats the Invader story before resolving the novel's historical deception. That in-world legend is not adopted as objective history."),
    source("src-fall-night-primary", "Against the Fall of Night, in The Lion of Comarre and Against the Fall of Night", "Arthur C. Clarke; scanned collection hosted by Luminist",
           "https://s3.us-west-1.wasabisys.com/luminist/EB/C/Clarke%20-%20Comarre.pdf", "primary_fiction_scan_with_indexed_excerpts",
           "Initially indexed-only; follow-up rendered and visually read the relevant image-only pages", "Printed pages 148-160: synthesis, interpreting human instructions, duplication, Council orders and Alvin's view of the machines as the real rulers.",
           "PDF pages are printed pages plus 14 in this portion. This is a targeted visual reading, not the whole novel. Alvin's view of the real rulers is character interpretation; neither non-sentience nor absolute human command is inferred."),
    source("src-fall-night-comparison", "The Highway Men: discussion comparing Clarke's two novels", "Swords & Stitchery, 25 October 2012",
           "https://swordsandstitchery.blogspot.com/2012/10/the-highway-men-stars-without-numbers_25.html", "tertiary_reproduction_and_reader_commentary",
           "Page opened; comparative section read", "Different life cycles, Rorden versus Khedron and the changed computational role.",
           "Much is attributed to Wikipedia and is not independent corroboration. Its assertion that the earlier machines lack self-awareness is too strong beside the primary excerpt and is not adopted.")
]

child = ["src-childhood-revenant", "src-childhood-abrash"]
city = ["src-city-stars-primary", "src-city-stars-preview", "src-city-stars-review"]
R = [record(
    "childhood-end-golden-age", "c0065", "Childhood's End (Earth's Golden Age)", "Childhood's End", "Human Earth under Overlord supervision", ["book"],
    scope("The original novel", "The mature Golden Age before the children's transformation", "Human residents of Earth during ordinary social life", ["The final loss of humanity as a leisure statistic", "The Overmind as a human population", "New Athens as proof of a uniform local culture", "The unreviewed television adaptation"]),
    "Robot factories make ordinary necessities available without requiring people to earn a wage. Paid work still buys luxuries, so this is strong basic provision rather than the disappearance of every market or status distinction. The guarantee point describes the mature Golden Age. It does not average that period together with humanity's eventual transformation and the destruction of Earth.\n\nThe ultimate rulers are the biological Overlords, whose decisions humans cannot effectively overturn. The point near zero uses an explicit analogy with concentrated non-AI authority; these aliens are neither human elected representatives nor autonomous production robots. Local human institutions and everyday choices continue underneath their supervision. The nonworking fraction remains unresolved because work being optional does not reveal how many people take it. Technologists, researchers and people earning luxuries still exist, and the source passages offer no population-wide count of their activity.",
    {"guarantees": -0.9, "control": 0.0, "nonworking": None},
    {"guarantees": assessment(-0.9, [-1, -0.7], "medium", "Automated basic provision; luxuries and status remain.", child),
     "control": assessment(0.0, [0, 0.15], "medium", "Concentrated biological alien supremacy, explicitly mapped by analogy to the non-AI elite reference.", child),
     "nonworking": assessment(None, None, "low", "Optional luxury employment and technological work have no verified participation denominator.", child)},
    1, child,
    [evidence("Basic goods cease to depend on wages, while luxuries can still require work.", ["src-childhood-revenant"], "Golden Age analysis quoting novel page 71", "primary_excerpt_via_secondary"),
     evidence("Human institutions operate under decisive alien supervision.", child, "Overlord power and the UN; discussion of externally imposed utopia", "secondary_academic_analysis")],
    ["The control axis requires an explicit biological-alien analogy.", "The two academic essays do not replace a full primary read.", "New Athens may warrant a later split only after its actual economic differences are verified.", "No TV media tag until its continuity is reviewed."])]
R[-1]["control_analogy"] = {"actor": "Biological alien Overlords", "reference": "Concentrated non-AI authority at 0", "limitation": "The axis's literal human-elite label does not describe their species. Lack of a human veto is not itself proof of autonomous AI rule."}

R.append(record(
    "city-stars-diaspar", "c0066", "The City and the Stars (Diaspar)", "The City and the Stars", "Diaspar's sustained city and recurrent human lives", ["book"],
    scope("The City and the Stars, revised novel", "The stable city before public reopening to Lys", "Currently embodied human residents of Diaspar", ["Stored identity patterns as people enjoying leisure", "Lys", "A completely specified later reconstruction", "The earlier novel's different machine architecture"]),
    "Residents can summon food and furnishings through the city's synthesizers without taking production jobs. Physical maintenance and even the reconstruction of human bodies are built into the system, giving strong material guarantees. The protected population here is the embodied city: identities waiting in storage are not added to the leisure count. Artistic creation continues, and residents help decide which works deserve permanent preservation.\n\nThat cultural vote does not give them unrestricted control of the machinery. Changing the city requires both its Council and the Central Computer's approval, giving the machine an effective veto. The negative control point reflects that continuing authority, qualified by human choice and the computer's inherited purposes. It is not simply inferred from the presence of robots. The nonworking fraction stays open because effortless subsistence does not count the artists, mentors and other useful activity that still occupies human lives.",
    {"guarantees": -0.95, "control": -0.65, "nonworking": None},
    {"guarantees": assessment(-0.95, [-1, -0.8], "high", "On-request synthesis and enduring maintenance support the resident population.", city),
     "control": assessment(-0.65, [-0.9, -0.3], "medium", "Explicit computer veto over Council-approved changes; human choices still matter.", ["src-city-stars-primary"]),
     "nonworking": assessment(None, None, "low", "Art, mentoring and special roles continue without a quantified participation rate.", city)},
    5, city,
    [evidence("The Council cannot alter the city without computer approval.", ["src-city-stars-primary"], "PDF page 30: Khedron explains the monitors", "depicted_or_author_stated"),
     evidence("Human creative activity remains alongside synthesized subsistence.", ["src-city-stars-primary"], "PDF pages 5-10: food, furnishings, memory and artistic voting", "depicted_or_author_stated")],
    ["A full comparison of original design constraints and present override rights would refine the control interval.", "Stored and embodied persons require separate denominators.", "This is not a score for all distant-future humanity."], alternatives=[1]))

lys = ["src-city-stars-primary"]
R.append(record(
    "city-stars-lys", "c0067", "The City and the Stars (Lys)", "The City and the Stars", "The communities of Lys, observed principally at Airlee", ["book"],
    scope("The City and the Stars, revised novel", "Alvin's visit before the two cultures reopen their relationship", "Human residents of Lys, including children and older people", ["Diaspar's stored identities", "Assuming all villages have identical institutions", "Freedom from toil as proof of political democracy"]),
    "Lys retains the tools for effortless provision but often chooses living processes instead. Its people grow fruit for the pleasure of cultivation and experimentation; Hilvar can also produce a meal with a portable matter-converter. This supports a post-work reading despite the visible gardening. The moderately strong guarantee estimate is qualified because routine access is clearer than a formal universal entitlement.\n\nControl remains unresolved. Alvin cannot tell whether Seranis has commanding authority or very little power, and the villages deliberately differ. Telepathic communication alone does not establish equal ownership or an accountable political system. The provisional distributed-regime label therefore still needs checking. A low nonworking estimate reflects the repeated picture of busy residents, while allowing for children and the very old. Their voluntary cultivation and useful experiments count as work. The estimate is broad and editorial; it does not count all self-chosen activity as either a job or mere leisure.",
    {"guarantees": -0.65, "control": None, "nonworking": 0.25},
    {"guarantees": assessment(-0.65, [-0.9, -0.2], "low", "Synthesis remains available alongside chosen cultivation; universal legal coverage is not specified.", lys),
     "control": assessment(None, None, "low", "Narration explicitly leaves Seranis's authority and diverse village institutions unclear.", lys),
     "nonworking": assessment(0.25, [0.05, 0.6], "low", "Coarse minority estimate from busy useful pursuits, with children and older residents included; no census.", lys)},
    2, lys,
    [evidence("Retaining cultivation does not mean lacking synthesizers.", lys, "PDF pages 52-53 and 58: Airlee and Hilvar's camp", "depicted_or_author_stated"),
     evidence("The observer cannot resolve the local leadership structure.", lys, "PDF page 52: Seranis and the differing villages; page 72: coercive memory proposal", "depicted_or_author_stated")],
    ["Control and the provisional regime require further institutional evidence.", "The ability to alter an outsider's memory qualifies an uncomplicated picture of freedom.", "Useful gardening counts as work even when its products are replaceable by synthesis."], alternatives=[1]))

fall = ["src-fall-night-primary", "src-fall-night-comparison", "src-city-stars-primary"]
D = [
    decision("c0065", "included", "Robot-made necessities are available outside employment during the defined Golden Age.", child, society_id="childhood-end-golden-age"),
    decision("c0066", "included", "Direct text establishes automatic provision and the computer's veto over city alterations.", city, society_id="city-stars-diaspar"),
    decision("c0067", "included", "Direct text confirms synthesis despite optional cultivation; political control stays explicitly unresolved.", lys, society_id="city-stars-lys"),
    decision("c0068", "duplicate", "Direct visual follow-up confirms the same core automatic-provision mechanism without a sufficiently distinct allocation or labor regime to count another Diaspar.", fall,
             "Printed pages 148-160 show synthesis at human request, an intelligent interpreter, a Council issuing restrictive orders and Alvin explicitly regarding the underlying machines as the city's real rulers. That last claim is his interpretation, not an audited constitution. It nevertheless defeats the easy claim that this is a simple human-run alternative to the later novel. Different life cycles and a revised computer architecture remain version differences, but the evidence does not establish a second material distribution or labor order under the project's economic-unit rule.",
             "Reopen if a specific difference in ownership, access, work obligation or present override rights is established. Keep original and revised life cycles separate in quotations; this disposition does not merge their literal continuities or transfer the later record's precise coordinate to the earlier text.",
             duplicate_of="city-stars-diaspar", duplication_basis="Economic comparison across alternate versions, not identical literal continuity", follow_up_completed="The image-only scan's relevant pages were rendered and read after the initial indexed-only pass.")
]

write_batch(10, [f"c{i:04}" for i in range(65, 69)], S, R, D, [
    "Four contiguous leads yield three retained societies; a later direct visual follow-up resolves the fourth as an economic duplicate across versions.",
    "Second pass distinguishes guaranteed basic goods from free luxuries, biological alien rulers from AI, shared artistic voting from control of production, and optional cultivation from wage dependence.",
    "The full City and the Stars PDF was fetched only after web retrieval timed out; selected extracted passages, not a complete novel reading, support the two records.",
    "Lys's control coordinate is intentionally unresolved because the narrator expressly lacks that knowledge. Its positive regime label is provisional, with a concentrated alternative retained.",
    "The original Diaspar's machines are not called non-sentient merely because a secondary comparison does so. Follow-up visual reading covers printed pages 148-160 and confirms the caution about treating its Council as simply sovereign over passive tools.",
    "No human extinction, stored-person interval, or absence of compulsory jobs is converted into a 100% leisure statistic. Assets remain deferred and the overall goal is unfinished."
])
