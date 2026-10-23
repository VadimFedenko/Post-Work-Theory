from research_helpers import source, assessment, record, scope, evidence, decision, write_batch

S = [
    source("src-haldeman-author-books", "Joe Haldeman: Books", "Joe Haldeman; author's website",
           "https://sites.google.com/site/joehaldemansf/books", "author_work_descriptions",
           "Public page opened; relevant Forever Free and Forever Peace descriptions read", "Man's benevolent dictatorship in the direct sequel; Forever Peace as a different continuity; human remote operators and Julian's continuing physics work.",
           "The sequel blurb does not describe the clone civilization's household economy in The Forever War. Remotely operated soldierboys are not autonomous military minds; the author gives 2043, while some secondary summaries give another year."),
    source("src-forever-war-man-reference", "The Forever War", "Wikipedia contributors",
           "https://en.wikipedia.org/wiki/The_Forever_War", "secondary_plot_reference",
           "Substantial publicly indexed ending account read", "Cloning and Man's collective species, peace with the Taurans and separate colonies for old-style humans.",
           "Collective biological consciousness is not by itself sovereign AI or proof of post-work production. Different Earth periods and old-human colonies must not be merged; comic adaptation institutions were not verified."),
    source("src-forever-peace-publisher", "Forever Peace", "Ace / Penguin Random House; Joe Haldeman",
           "https://www.penguinrandomhouse.com/books/341965/forever-peace-by-joe-haldeman/", "official_publisher_synopsis",
           "Public indexed description and attributed review excerpts read", "Ngumi War, human soldierboy operators and the physics project; explicit distinction from a direct Forever War sequel.",
           "The short synopsis does not supply nanoforge ownership or stipend conditions. Mental linking of people must not automatically be coded as nonhuman AI rule."),
    source("src-forever-peace-reilly", "John J. Reilly on Joe Haldeman's Forever Peace", "John J. Reilly's 1998 review excerpt, republished by Benjamin Espen in 2020",
           "https://www.benespen.com/2020-12-18-john-j-reilly-on-joe-haldemans-forever-peace/", "contemporary_critical_review_republication",
           "Page opened; quoted review and its economic argument read", "Almost nobody working in advanced countries, government stipends, a guarded nanoforge monopoly, and output allocations used to control client states.",
           "This is a secondary review, not a canonical census. Its professors/waiters shorthand is not an exhaustive occupation list, as the author independently depicts soldiers and physicists. The reviewer's real-world economic argument is not imported as fictional fact."),
    source("src-software-objects-publisher", "The Lifecycle of Software Objects", "Subterranean Press; Ted Chiang, with attributed Charles Stross review",
           "https://subterraneanpress.com/lifecycle-of-software-objects/", "official_publisher_description_and_attributed_review",
           "Public product page opened and description read", "Artificial minds raised through interaction in a world of software companies, gaming and open source; the human and software life cycles remain connected.",
           "An artificial community is not automatically an economy that frees humans from labor. Publisher and review text are distinguished from the novella itself."),
    source("src-software-objects-primary", "The Lifecycle of Software Objects: first-edition scan", "Ted Chiang; Subterranean Press 2010, scan on University of Chicago course site",
           "https://cpb-us-w2.wpmucdn.com/voices.uchicago.edu/dist/8/644/files/2017/08/Chiang-Lifecycle-of-Software-Objects-q3tsuw.pdf", "primary_fiction_scanned_edition",
           "Public PDF opened, target passages located; complete selected spreads rendered and visually read", "Printed pages 96-97 and 140-141: financing the platform port, continuing professional care, Ana's major expense and prospective job sacrifice.",
           "The PDF has 78 two-page spreads; zero-based PDF pages 50 and 72 contain these selected printed pages. The complete novella was not read. No full source copy is retained as a deliverable."),
    source("src-oryx-crake-publisher-author", "Oryx and Crake", "Vintage / Penguin Random House; Margaret Atwood author interview",
           "https://www.penguinrandomhouse.com/books/6113/oryx-and-crake-by-margaret-atwood/", "official_publisher_synopsis_and_author_interview",
           "Page opened; synopsis and author interview read", "Corporate genetic engineering, Snowman's post-plague struggle, and the author's distinction between scientific tools and human choices.",
           "Powerful biotechnology and a corporate enclave are not proof of labor-saving universal access. Before-plague compounds and after-plague populations require different scopes."),
    source("src-oryx-crake-reference", "Oryx and Crake", "Wikipedia contributors",
           "https://en.wikipedia.org/wiki/Oryx_and_Crake", "secondary_plot_reference",
           "Public plot account read through search and opened page", "Walled employee/family compounds, Jimmy's paid advertising work, Crake's bioengineering position and corporate products.",
           "This confirms work-linked enclave access in the summary, but not a demonstrated policy of preserving jobs despite an available complete replacement. Genetic products are not necessarily automated household production."),
    source("src-maddaddam-primary-preview", "MaddAddam: publisher excerpt", "Margaret Atwood; Penguin Random House Higher Education",
           "https://penguinrandomhousehighereducation.com/book/?isbn=9780739384008", "official_synopsis_and_primary_fiction_excerpt",
           "Page opened; synopsis and displayed Egg and Rope scenes read", "Crakers and human survivors together, plants the Crakers eat, catching fish for Snowman, material craft skills and continuing danger.",
           "Toby's origin account is an in-world story for the Crakers, not a literal technical manual. The displayed scenes do not establish a machine-provisioned economy or an all-population work rate."),
    source("src-maddaddam-author-event", "Margaret Atwood is #Internet", "The Link; report of Margaret Atwood in conversation with Sheila Heti",
           "https://thelinknewspaper.ca/article/margaret-atwood-is-internet", "reported_author_event_with_direct_comments",
           "Substantial publicly indexed event report read", "Atwood explains that the engineered grass-and-leaf diet removes the need for agriculture; the report also discusses surviving community and storytelling.",
           "Reported author comments establish a reduced biological requirement, not automatic external productive machinery or unconditional material rights. No direct attendance or complete event recording is claimed.")
]

f = ["src-haldeman-author-books", "src-forever-peace-publisher", "src-forever-peace-reilly"]
R = [record(
    "forever-peace-welfare-states", "c0096", "Forever Peace (The developed welfare states)", "Forever Peace", "The United Welfare States' resident society during the Ngumi War", ["book"],
    scope("The separate Forever Peace continuity", "The existing nanoforge order during the main war, before the proposed worldwide neural reform is treated as accomplished", "Resident humans of the United Welfare States, within the developed-country provision described by the consulted account", ["Third World client and enemy populations as equal welfare recipients", "Teleoperated soldierboys as autonomous residents", "The clone society Man from The Forever War", "A fully enacted universal postwar reform without ending verification"]),
    "Nanoforges provide an automated productive base, and the consulted economic account describes most residents of the developed countries living on government stipends. This weakens the connection between paid work and ordinary subsistence. The guarantee estimate is favorable within the selected resident population, qualified by the need to verify the precise benefit conditions. It does not extend that security to client states whose supply allocations are instruments of pressure.\n\nThe productive technology is a guarded government monopoly, so public branding alone is insufficient to place control at the fully distributed end. A low positive estimate allows for human institutions while keeping the concentration visible; political accountability needs closer primary examination. The soldierboys are operated by humans, and scientists, service workers and soldiers continue to work. A broad high-nonworking estimate follows the review's explicit near-universal nonemployment description, with a wide interval allowing for those occupations and other useful activity. It is an editorial all-resident approximation, not a canonical percentage or an automatic conversion of stipend receipt into idleness.",
    {"guarantees": -0.65, "control": 0.15, "nonworking": 0.85},
    {"guarantees": assessment(-0.65, [-0.9, -0.35], "medium", "Automatic output and widespread government stipends support the scoped residents. Exact benefit adequacy, eligibility and housing rules remain primary-source gaps; foreign clients are excluded.", f),
     "control": assessment(0.15, [0, 0.45], "low", "A guarded state nanoforge monopoly is established in the review. No effective citizen ownership/override procedure was verified; government ownership alone does not establish distributed control.", ["src-forever-peace-reilly"]),
     "nonworking": assessment(0.85, [0.6, 0.97], "low", "The review explicitly describes almost nobody working, beyond merely receiving stipends. This broad all-resident editorial estimate allows substantial uncertainty for the continuing military, services, research and useful voluntary work; no labor-force denominator is silently converted.", f)},
    1, f,
    [evidence("Government stipends coexist with a restricted nanoforge monopoly and extensive nonemployment in developed countries.", ["src-forever-peace-reilly"], "Republished review's economics-of-abundance paragraph", "secondary_report"),
     evidence("Humans operate soldierboys and Julian continues productive scientific work outside his military service.", ["src-haldeman-author-books", "src-forever-peace-publisher"], "Author's Forever Peace description and publisher synopsis", "author_or_publisher_commentary")],
    ["Direct nanoforge and benefit scenes are still needed; this retained assessment relies substantially on a contemporary secondary account.", "The nonworking point is a coarse interpretive estimate with a wide interval, not an author-reported statistic.", "Restricted client-state supplies and the proposed global reform are separate scopes.", "The author's 2043 date is preferred over conflicting secondary dating, but no exact date is needed for this snapshot."], alternatives=[2])]

D = [
    decision("c0095", "needs_evidence", "Man's biological collective and peace settlement are clear; the final clone society's productive and distributive rules are not.", ["src-haldeman-author-books", "src-forever-war-man-reference", "src-forever-peace-reilly"],
             "The ending introduces a clone collective and separate old-human colonies; the author's sequel blurb calls Man's rule a benevolent dictatorship. Neither establishes the final period's household rights or labor participation. A review's general recollection of automation in The Forever War is not dated precisely enough to transfer earlier consumer arrangements to Man. A shared biological mind also cannot be silently scored as autonomous nonhuman AI.",
             "Read the final Man conversation and, if needed, the direct sequel's material arrangements, keeping periods separate. Verify the comic's depicted institutions before adding its media tag; do not use Forever Peace's nanoforges as evidence for this continuity."),
    decision("c0096", "included", "Nanoforge output, broad stipend support and restricted productive control qualify a scoped developed-country order.", f, society_id="forever-peace-welfare-states"),
    decision("c0097", "boundary_case", "Digital community life depends on ongoing paid infrastructure and human care; virtual existence does not itself establish post-work provision.", ["src-software-objects-publisher", "src-software-objects-primary"],
             "The selected primary spreads show funding sought for a costly platform port and Ana considering professional work and personal sacrifice to secure her digient's future. Digients are developing persons, not a costless automatic supply system for humans. Their growth requires continuing care, and apparent freedom inside a virtual world depends on material and institutional support outside it. No justified human participation rate or automated livelihood system follows from being software.",
             "Preserve as a digital-dependency and care comparison. Reopen for a particular later community only if its productive access rules actually change; distinguish young dependent persons from adults freed from work and active digients from paused files."),
    decision("c0098", "needs_evidence", "Corporate employee compounds and advanced genetic products do not yet establish a qualifying automation/distribution relationship.", ["src-oryx-crake-publisher-author", "src-oryx-crake-reference"],
             "Compound protection in the consulted account is tied to employment and family membership, while Jimmy, Crake and other specialists do paid work. This could support a deliberately work-preserving zero variant only if an available labor-saving alternative and its restriction are actually shown. An organ-producing animal or biomedical breakthrough alone does not establish that the whole enclave could, or does, operate without its human workforce.",
             "Read the actual compound productive and access arrangements, including bioengineered production, to determine whether labor dependence is weakened or explicitly preserved despite replacement capacity. Keep pre-plague employees, outside residents and post-plague survivors separate."),
    decision("c0099", "boundary_case", "The Crakers' engineered reduction of subsistence needs is not yet a demonstrated automatic productive and allocative economy.", ["src-maddaddam-primary-preview", "src-maddaddam-author-event"],
             "The author explains that a grass-and-leaf diet removes agriculture, while primary scenes retain gathering food, catching fish for another person, craft skills, care and danger. Biological redesign is relevant to a reduced need for work, but not automatically equivalent to a continuously operating material system that guarantees access. The broader mixed survivor community cannot be called uniformly nonworking, and the loss of most humans cannot inflate a leisure percentage.",
             "Keep as a needs-reduction comparison. Reopen if further primary evidence establishes a qualifying technologically maintained productive mechanism for a named living population; explicitly justify any biological-function analogy rather than silently treating grazing or extinction as automation.")
]

write_batch(17, [f"c{i:04}" for i in range(95, 100)], S, R, D, [
    "The three similarly titled Haldeman novels remain distinct continuities, and a human group mind is not labeled a nonhuman AI.",
    "The welfare-state nonworking estimate has a source-supported qualitative participation basis and an explicit wide interval; stipend receipt alone is not the calculation.",
    "Selected Chiang PDF spreads were visually checked as complete pages, correcting the late scene's locator to printed pages 140-141.",
    "The Crakers remain a comparison until the proposed biological-production analogy is justified; engineered needs reduction, ordinary foraging and automated external provision are not silently conflated.",
    "Second pass checked population boundaries, human teleoperation, primary versus secondary economics, platform costs, useful care work and the difference between extinct people and living nonworkers."
])
