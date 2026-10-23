from research_helpers import source, assessment, record, scope, evidence, decision, write_batch

S = [
    source("src-reynolds-sfe", "Reynolds, Mack", "The Encyclopedia of Science Fiction",
           "https://sf-encyclopedia.com/entry/reynolds_mack", "secondary_reference",
           "Entry opened; pertinent narrative and bibliography passages read", "Tomorrow Might Be Different's expansion; separate Julian West, Bat Hardin and Lagrange sequences; After Utopia bibliography.",
           "Bibliographic grouping does not establish a common economy across different series. It identifies The Towns Must Roll as an If serial, despite a reader review calling it Galaxy."),
    source("src-tomorrow-different-publisher", "Tomorrow Might Be Different", "Hachette Australia / Gateway",
           "https://www.hachette.com.au/mack-reynolds/tomorrow-might-be-different", "official_publisher_synopsis",
           "Product page opened; synopsis read", "Cheap Soviet exports, declining Western industry and the proposed religious countermeasure.",
           "The synopsis establishes a trade satire, not the productive technology, entitlement rules or human participation needed for admission."),
    source("src-after-utopia-publisher", "After Utopia", "Hachette Australia / Gateway",
           "https://www.hachette.com.au/mack-reynolds/after-utopia", "official_publisher_synopsis",
           "Product page opened; synopsis read", "United Earth without poverty or shortages, stagnation and programmed-dream addiction.",
           "Publisher framing is not an employment census or a description of effective voting institutions."),
    source("src-after-utopia-athans", "What We Can Learn from a Random Science Fiction Novel: After Utopia", "Philip Athans; Fantasy Author's Handbook, 25 June 2024",
           "https://fantasyhandbook.wordpress.com/2024/06/25/what-we-can-learn-from-a-random-science-fiction-novel-after-utopia/", "secondary_literary_analysis_with_primary_excerpts",
           "Article opened; economic explanation, quoted transceiver scene and ending discussion read", "No-money automated provision, free requests, education, dream machines and Cogswell's later fabricated threat.",
           "Full novel not read. Separate the reviewer's dislike of the storytelling from its quoted or summarized arrangements. The ending does not establish a fully described new distribution system."),
    source("src-after-utopia-hanley", "After Utopia by Mack Reynolds", "Terence E. Hanley; Tellers of Weird Tales, 16 October 2022",
           "https://tellersofweirdtales.blogspot.com/2022/10/after-utopia-by-mack-reynolds.html", "secondary_literary_analysis_with_primary_excerpt",
           "Article opened; Stein's quoted explanation and its page locator read", "Pages 54-55 as quoted: democratic self-description, abundance and the dissidents' concern about stagnation.",
           "The primary quotation is mediated by a strongly opinionated review and was not checked against a complete edition. Reviews disagree on the exact future year, so no exact year is assigned."),
    source("src-rolltown-publisher", "Rolltown", "Hachette Australia / Gateway",
           "https://www.hachette.com.au/mack-reynolds/rolltown", "official_publisher_synopsis",
           "Product page opened; synopsis read", "Mobile American communities containing hundreds or thousands of people.",
           "The local caravan premise does not explain the national income and voting rules."),
    source("src-rolltown-boaz", "Book Review: Rolltown, Mark Reynolds (1976)", "Joachim Boaz; Science Fiction and Other Suspect Ruminations, 29 April 2011",
           "https://sciencefictionruminations.com/2011/04/29/book-review-rolltown-mark-reynolds-1976/", "secondary_reader_review",
           "Whole short review opened and read", "Mechanized production and services, NIT, restricted employment and New Woodstock's volunteer police and arts.",
           "The heading misspells Mack as Mark; the text identifies Mack correctly. Its shorthand about intelligence and voting is refined by the more specific earned-income rule in other evidence."),
    source("src-rolltown-goodreads", "Rolltown: Rafeeq O. review", "Rafeeq O.; Goodreads, 15 February 2025",
           "https://www.goodreads.com/book/show/8034789", "secondary_reader_review_with_primary_excerpts",
           "Substantial indexed review read; direct page retrieval returned 403", "1976 Ace pages 23-25 on automation and GAI; pages 31-32 on earned-income voting; arts and voluntary policing.",
           "Quoted novel passages were available in the search index, not a directly opened full novel. The serial's magazine is incorrectly called Galaxy here; SFE identifies If. No inflation conversion or average-income figure is used as a minimum benefit."),
    source("src-rolltown-marzaat", "Rolltown; or, Adventures in Reviewer Parallax", "MarzAat, 23 August 2026",
           "https://marzaat.com/2026/08/23/rolltown-or-adventurers-in-reviewer-parallax/", "secondary_reader_review",
           "Whole short review opened and read", "Novel versus serial; NIT-only population and earned-income franchise.",
           "Its 90% and 3% figures remain secondary reports. NIT income status does not measure useful artistic or volunteer work. No uniform Latin American welfare scheme is implied."),
    source("src-lagrange-five-publisher", "Lagrange Five", "Hachette Australia / Gateway",
           "https://www.hachette.com.au/mack-reynolds/lagrange-five", "official_publisher_synopsis",
           "Product page opened; synopsis read", "Artificial space-colony environment and Wide syndrome.",
           "Pleasant surroundings and recycling establish neither unmanned production nor unconditional access."),
    source("src-lagrange-five-marzaat", "Lagrange Five", "MarzAat, 7 November 2025",
           "https://marzaat.com/2025/11/07/lagrange-five/comment-page-1/", "secondary_reader_review",
           "Review opened; resident institutions and labor passages read", "Island Three's syndicalist elections, request distribution, thirty-hour workweek, residential screening and Casey's informal influence.",
           "No complete primary text was read. Automation described in a later sequel cannot silently establish the first novel's arrangement. Thirty hours is a schedule, not a percentage of people employed.")
]

after = ["src-after-utopia-publisher", "src-after-utopia-athans", "src-after-utopia-hanley"]
roll = ["src-rolltown-publisher", "src-rolltown-boaz", "src-rolltown-goodreads", "src-rolltown-marzaat", "src-reynolds-sfe"]
R = [record(
    "after-utopia-earth", "c0057", "After Utopia (Earth before Cogswell's intervention)", "After Utopia", "Earth's automated common provision", ["book"],
    scope("The 1977 novel", "The established future encountered by Cogswell, before his fabricated alien threat", "Human residents of the united Earth", ["An assumed new economic constitution after the ending", "The claim that every enjoyable activity is nonwork", "An exact future date inferred from conflicting reviews"]),
    "Automated production and recycling let people request goods without earning money first. Together with the stated absence of poverty and shortages, that places material guarantees near the strong end. The problem driving the story is what people do with this freedom: immersive dream entertainment and declining initiative worry a small group of dissidents. Their alarm does not turn reliable provision into an absence of provision.\n\nThe human-control point is cautiously positive. A quoted explanation calls the order democratic, and people appear able to choose their activities, but the gathered passages do not map effective control over the production system. Computers providing services are insufficient evidence of an AI sovereign. The high nonworking estimate reflects widespread inactivity, with a broad allowance for research and other useful voluntary work. It is an editorial judgment, not a canonical headcount. This snapshot ends before Cogswell tries to supply a new collective purpose through a false external threat.",
    {"guarantees": -0.9, "control": 0.65, "nonworking": 0.85},
    {"guarantees": assessment(-0.9, [-1, -0.7], "medium", "On-request automated provision is corroborated by the publisher's description of no poverty or shortages.", after),
     "control": assessment(0.65, [0.1, 0.95], "low", "Character testimony claims democracy, but effective ownership and override rights need primary follow-up.", ["src-after-utopia-hanley", "src-after-utopia-athans"]),
     "nonworking": assessment(0.85, [0.6, 0.98], "low", "Qualitative inactivity and dream absorption support a high share; productive dissidents, researchers and other voluntary activity prevent equating optional work with total idleness.", after)},
    2, after,
    [evidence("Material access is independent of paid employment through automated provision.", ["src-after-utopia-athans", "src-after-utopia-publisher"], "Athans: discussion following transceiver scene; publisher synopsis", "secondary_summary"),
     evidence("Democracy is a character's description requiring an institutional check.", ["src-after-utopia-hanley"], "Stein's explanation, quoted as pages 54-55", "primary_excerpt_via_secondary")],
    ["Read the novel's allocation and decision passages before treating the control point as secure.", "There is no verified participation census.", "A later motivation campaign is not automatically a separate economic order."], alternatives=[1])]

R.append(record(
    "rolltown-us-meritocracy", "c0058", "Rolltown (United States Meritocracy)", "Rolltown", "The national automated economy supporting the rolltowns", ["book"],
    scope("The expanded 1976 Bat Hardin novel", "The established Meritocracy during New Woodstock's journey", "US human residents supported by the national economy, including citizens traveling in rolltowns", ["Mexican or South American residents as beneficiaries of the same guarantee", "New Woodstock as an economically self-sufficient nation", "An unverified economy shared with Reynolds's unrelated novels"]),
    "Automation has displaced most ordinary production and service jobs. A guaranteed annual income, delivered as a negative income tax, allows people to live and travel without finding scarce paid work. That gives the society a fairly strong provision point, although the gathered evidence does not define an enforceable minimum covering every need. The mobile towns depend on this larger arrangement; their prosperity should not be projected onto the countries they visit.\n\nEffective political control is sharply concentrated. Votes depend on earned income, so people supported by the guarantee lose influence even though the economy no longer needs their employment. Basic security therefore coexists with exclusion from power. A high nonworking estimate is plausible, but recipients are not all inactive: artists and volunteer peace officers do useful work. The broad range allows for that activity. The national system is the unit here, rather than a claim that every caravan has the same local government or that its members own the automated factories.",
    {"guarantees": -0.6, "control": 0.05, "nonworking": 0.8},
    {"guarantees": assessment(-0.6, [-0.85, -0.2], "medium", "The NIT supports the displaced majority and mobile life; exact floor, residence conditions and full coverage remain unverified.", ["src-rolltown-boaz", "src-rolltown-goodreads"]),
     "control": assessment(0.05, [0, 0.2], "medium", "Earned-income voting excludes the supported majority; a computer dossier is not autonomous machine sovereignty.", ["src-rolltown-goodreads", "src-rolltown-marzaat"]),
     "nonworking": assessment(0.8, [0.5, 0.95], "low", "A coarse majority-nonworking estimate from extensive displacement, adjusted downward from the secondary NIT-only share to allow for productive arts, service and volunteering. No all-age census of useful work is available.", ["src-rolltown-boaz", "src-rolltown-marzaat"])},
    1, roll,
    [evidence("Automation and GAI coexist with an earned-income franchise.", ["src-rolltown-goodreads"], "Review's excerpts identified as Ace 1976, pages 23-25 and 31-32", "primary_excerpt_via_secondary"),
     evidence("New Woodstock contains useful volunteer work despite NIT support.", ["src-rolltown-boaz"], "Plot summary: Bat Hardin and the arts community", "secondary_summary")],
    ["Primary edition confirmation of income and franchise rules is still needed.", "The NIT-only income share does not count unpaid productive activity.", "Check Commune 2000 A.D. and The Towers of Utopia for overlap before admitting another national-system record.", "The first serial appeared in If; no short_story tag is added without reviewing that version."]))
R[-1]["reported_labor_statistics"] = [{"value": 0.9, "measure": "Population reported as living only on NIT, not a measured nonworking fraction", "denominator": "The national populace as described by the secondary reviewer; exact age coverage not verified", "source_id": "src-rolltown-marzaat", "locator": "Paragraph beginning Most significantly"}]

D = [
    decision("c0056", "needs_evidence", "Economic outperformance and cheap exports do not yet establish the proposed automated consumer society.", ["src-tomorrow-different-publisher", "src-reynolds-sfe"],
             "The novel is an expansion of Russkies Go Home!, a satire of Soviet commercial success and Western decline. The consulted synopsis does not say how Soviet residents obtain necessities, which labor is automated or whether employment is deliberately retained despite that capacity. It would be circular to import GAI from the author's other futures.",
             "Read the expanded novel's Soviet production and household-consumption explanations. Keep the original story and expansion distinct where their rules differ; retain no coordinates until the automation connection is evidenced."),
    decision("c0057", "included", "Automated on-request provision removes wage dependence; effective democratic control remains provisional.", after, society_id="after-utopia-earth"),
    decision("c0058", "included", "National automation and guaranteed income support the mobile communities while political power follows earned income.", roll, society_id="rolltown-us-meritocracy", scope_correction="The candidate's mobile communities are situated within their sustaining national economy; they are not assumed to manufacture everything themselves."),
    decision("c0059", "needs_evidence", "A short workweek and generous resident consumption are documented secondarily, but the technology and entitlement conditions still need checking.", ["src-lagrange-five-publisher", "src-lagrange-five-marzaat", "src-reynolds-sfe"],
             "Island Three combines technical-profession elections, free requested goods and wages saved for Earth, while residents still have a thirty-hour workweek. Screening can expel children who fail the residence criteria, so abundant consumption cannot become an unconditional guarantee for all humans. A later sequel's automation and unemployment cannot be backdated silently. The current evidence neither establishes post-work admission nor proves a zero variant.",
             "Check the first novel's economy passages, especially the distribution and employment relationship and actual automated production. If admitted, scope the resident enclave including its children and qualifications; assess Casey's informal power alongside elections. Investigate the later Chaos in Lagrangia period separately if it adds a materially different labor order.")
]

write_batch(8, [f"c{i:04}" for i in range(56, 60)], S, R, D, [
    "Four contiguous candidates receive dispositions; two supported post-work records are retained and two admission questions stay open.",
    "Second pass distinguished cheap exports from post-work distribution, local caravans from their funding economy, stated democracy from verified control, and income status from productive participation.",
    "Both new participation points are explicitly coarse editorial estimates with broad intervals. They are not canonical censuses, and numeric completeness does not finish quality review.",
    "The available book-specific source mixture is weaker than a complete primary reading. Direct retrieval failures and mediated excerpts are labeled; no full-novel read is claimed.",
    "No website, deployment, poster collection or invented later settlement was produced. The 500-1000-record objective remains active."
])
