from research_helpers import source, assessment, record, scope, evidence, decision, write_batch

S = [
    source("src-singularity-sky-reference", "Singularity Sky", "Wikipedia contributors",
           "https://en.wikipedia.org/wiki/Singularity_Sky", "secondary_plot_and_setting_reference",
           "Public indexed plot and setting account read", "Rochard's World, the Festival's information exchange and proliferating cornucopias; the Republic's prior restrictions.",
           "General reference; no guarantees constitution or nonworking census. The Festival's own uploaded population is distinct from its human hosts."),
    source("src-singularity-sky-stoddard", "You Will Know—Singularity! Singularity Sky by Charles Stross", "William H. Stoddard, Black Gate, 12 January 2025",
           "https://www.blackgate.com/2025/01/12/you-will-know-singularity-singularity-sky-by-charles-stross/", "secondary_literary_review",
           "Public setting and cornucopia discussion read", "Widespread cornucopia distribution, material abundance and disruptive consequences.",
           "Secondary interpretation; the page mistakenly groups Accelerando as a sequel, which is not adopted. Earth political remarks do not establish every planet's economy."),
    source("src-singularity-sky-kennedy", "Singularity Sky - Charles Stross", "D. Kennedy, literary review",
           "https://www.dkennedy.org/C2025243227/E958048421/", "secondary_literary_review_indexed",
           "Public indexed review read; direct opening returned 502", "Suppressed technology, exploited workers/peasants and self-replicating production given to the colony.",
           "Indexed access only. The revolutionary leader's theory is distinguished from the depicted technology distribution."),
    source("src-singularity-sky-twodudes", "Singularity Sky", "Two Dudes in an Attic, 28 February 2012 archive",
           "https://twodudesff.wordpress.com/2012/02/28/", "secondary_literary_review_indexed",
           "Public indexed review read; direct opening had a cache miss", "Deliberate suppression of innovation to preserve the New Republic elite.",
           "Short reference check, not a novel read. The economic effects of the intervention do not apply retroactively to the pre-contact order."),
    source("src-iron-sunrise-walker", "Reading List: Iron Sunrise", "John Walker, Fourmilab, December 2018",
           "https://www.fourmilab.ch/fourmilog/archives/2018-12/001804.html", "secondary_literary_review",
           "Public review's setting and political-conflict account consulted", "Eschaton causality constraints, independent worlds, arms control and the ReMastered conflict.",
           "The opening incorrectly attributes the Eschaton backstory to Accelerando; that conflation and its Earth economic claims are not adopted. Used only for the separately corroborated arms-control/faction conflict, not household provision."),
    source("src-iron-sunrise-author-unwritten", "Books I will not write #4: Space Pirates of KPMG", "Charles Stross, Charlie's Diary, September 2010",
           "https://www.antipope.org/charlie/blog-static/2010/09/books-i-will-not-write-4-escha.html", "official_author_commentary_indexed",
           "Public indexed author discussion read; direct opening timed out", "Conflict with the Eschaton and the planned third book's proposed mechanisms.",
           "Explicitly unwritten continuation. Its proposed outcomes and future god are not treated as enacted institutions in Iron Sunrise."),
    source("src-rapture-author-about", "About The Rapture of the Nerds", "Cory Doctorow, official website",
           "https://craphound.com/rotn/about/", "official_author_book_description",
           "Public book description consulted", "Remaining terrestrial humans, the smartcloud and Huw's technology-jury service.",
           "Synopsis only; upload capacity and technology gifts do not specify each polity's material entitlements or governance."),
    source("src-rapture-pw", "The Rapture of the Nerds", "Publishers Weekly",
           "https://www.publishersweekly.com/9780765329103", "secondary_trade_review",
           "Public indexed review read", "The distinction between ascended posthumans and Huw's terrestrial world.",
           "Short reference account; no complete novel read or general household allocation rules established.")
]
f = ["src-singularity-sky-reference", "src-singularity-sky-stoddard"]
n = ["src-singularity-sky-kennedy", "src-singularity-sky-twodudes"]
R = [
    record("singularity-sky-rochard-cornucopias", "c0153", "Singularity Sky (Rochard's World after the Festival's gifts)", "Singularity Sky", "The human colony after cornucopia production spreads", ["book"],
           scope("Stross's Eschaton novels, Singularity Sky", "The enacted transition after cornucopia machines proliferate during the Festival's visit", "Living human and human-derived inhabitants of the visited colony", ["The Festival's own uploaded members treated as the same population", "The pre-contact Republic", "An already stable galaxy-wide welfare constitution"], proxy=True, proxy_basis="The colony's living transformed people remain persons; uploaded visitors and automatic devices are not automatically added to the human denominator."),
           "The Festival initially exchanges powerful technology for new stories and information. The decisive change comes when cornucopia machines spread among the colony's inhabitants: ordinary productive capacity no longer rests with the old employers and nobility. This record concerns that implemented local transition, rather than guessing the internal economy of the Festival's uploaded citizens. Broad access to material production supports a substantial guarantee estimate, qualified by disorder and the absence of a settled entitlement system.\n\nControl moves toward recipients who possess replicating productive machines. The Festival initiates the transformation, but the account is more than a continuing queue for gifts from one remote provider. The positive control estimate captures that dispersion, while allowing uncertainty about dependence on the visiting system. The transformation also brings danger and unintended outcomes. Telling stories, organizing and caring can remain useful work, so rapid abundance does not justify a precise nonworking share. The New Republic before the intervention is assessed separately.",
           {"guarantees": -0.6, "control": 0.75, "nonworking": None},
           {"guarantees": assessment(-0.6, [-0.9, -0.15], "medium", "Widespread cornucopias establish material access beyond ordinary wages. Political disorder and no stated universal legal entitlement limit the estimate.", f),
            "control": assessment(0.75, [0.25, 0.95], "medium", "The machines proliferate among local recipients, undermining elite control. The estimate concerns the dispersed-production stage, not only the initial Festival exchange.", f + ["src-singularity-sky-kennedy"]),
            "nonworking": assessment(None, None, "low", "The transition removes much necessary production, but provides no all-resident census of useful activity.", f)},
           2, f + ["src-singularity-sky-kennedy"],
           [evidence("Cornucopia production spreads and destroys the old production hierarchy.", f, "Plot account and Black Gate's cornucopia discussion", "secondary_lore_report")],
           ["The record narrows the discovery Festival label to the documented human host society.", "Coordinates describe a turbulent transition; a stable final constitution is not asserted.", "Ongoing technical dependence on the Festival would move control lower; exact ownership rules remain incomplete."] ),
    record("singularity-sky-new-republic", "c0154", "Singularity Sky (The New Republic before contact)", "Singularity Sky", "The New Republic's deliberately restricted colonial order", ["book"],
           scope("Stross's Eschaton novels, Singularity Sky", "Before the Festival breaks the technological restrictions on Rochard's World", "The colonial population subject to New Republic restrictions, including workers and peasants", ["The post-cornucopia transition", "Earth's separate institutions", "All Eschaton-era societies assigned one economy"]),
           "The New Republic deliberately suppresses productive and information technologies available in its wider civilization. Its ruling order maintains a dependent workforce and a rigid hierarchy, rather than allowing broad access to self-replicating production. This makes it a zero variant: the restriction is a political choice to preserve the existing order despite the availability of labor-replacing technology. The Festival's intervention later exposes how vulnerable that arrangement is.\n\nControl is concentrated in human elites, placing the society near zero on that axis. The ordinary population's position depends on work, status and obedience, rather than a reliable universal right to the fruits of advanced production. The guarantee score is consequently weak. This does not claim that every possible job would disappear or that every resident currently works. Children, care and other activity remain relevant, and no population-wide participation rate was established. The record ends before cornucopias proliferate and redistribute productive power.",
           {"guarantees": 0.8, "control": 0.05, "nonworking": None},
           {"guarantees": assessment(0.8, [0.55, 1], "medium", "The dependent colonial population lacks broad access to the available productive technology; the references describe exploitation and maintained hierarchy.", n),
            "control": assessment(0.05, [0, 0.15], "high", "Human elites deliberately regulate technology to preserve their power.", n),
            "nonworking": assessment(None, None, "low", "A work-dependent hierarchy does not establish the all-age participation fraction.", n)},
           0, n + ["src-singularity-sky-reference"],
           [evidence("Innovation and productive access are deliberately restricted to sustain the elite order.", n, "Reviews' pre-Festival New Republic setting accounts", "secondary_lore_report")],
           ["This is the implemented restriction period, not a claim that the entire post-singularity galaxy has the same institutions.", "No census or exact basic-income policy was established in the quick pass."], record_type="zero_variant", analogy=3)
]
D = [
    decision("c0153", "included", "The Festival lead is narrowed to the documented human colony's cornucopia transition.", f + ["src-singularity-sky-kennedy"], society_id="singularity-sky-rochard-cornucopias", analysis="No separate point is added for the Festival's own members without their allocation rules."),
    decision("c0154", "zero_variant", "The Republic deliberately withholds modern productive technology to preserve a labor-dependent hierarchy.", n, society_id="singularity-sky-new-republic"),
    decision("c0155", "boundary_case", "Eschaton constraints do not make all independent human worlds one uniformly provisioned economy.", ["src-stross-sfe", "src-singularity-sky-reference"], analysis="Causality enforcement and arms-control protection are not a universal household allocation system; materially different polities already exist within this setting.", follow_up="Skip the broad aggregate; retain narrower polities only when their production/access arrangements are clear."),
    decision("c0156", "needs_evidence", "The quick sources establish an ideological and military faction, not its general automatic material economy.", ["src-iron-sunrise-walker", "src-iron-sunrise-author-unwritten"], analysis="A proposed future god in an unwritten continuation cannot establish current AI rule or welfare in the published novel.", follow_up="Skip deeper reading under the user's faster-pass instruction."),
    decision("c0157", "needs_evidence", "Earth and the Cloud are distinct populations, and the available short descriptions do not settle a single material-access regime.", ["src-rapture-author-about", "src-rapture-pw"], analysis="Uploading, gifts and technology jury service establish capability and conflict but do not supply each society's guarantees and effective control.", follow_up="Skip a full-novel investigation; the next separate non-uploaded-community lead also requires a short, scoped reference check.")
]
write_batch(29, [f"c{i:04}" for i in range(153, 158)], S, R, D, [
    "Continues the reference-led faster pass. Published sources are used for broad, transparent estimates; obscure admission gaps are skipped without novel reconstruction.",
    "The Festival label is narrowed to the actual host colony's material transition. Its original information exchange and later dispersed cornucopia access are distinguished.",
    "The New Republic's suppression is a separate zero variant. Eschaton-wide aggregates and unwritten sequel mechanisms do not generate extra economic points.",
    "Second pass checked periods, source scope and estimates; no full primary novel read or independent peer review is claimed."
])
