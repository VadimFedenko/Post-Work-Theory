from research_helpers import source, assessment, record, scope, evidence, decision, write_batch

S = [
    source("src-female-man-hicks", "Automating Feminism: The Case of Joanna Russ's The Female Man", "Heather Hicks, Postmodern Culture 9.3, May 1999",
           "https://www.pomoculture.org/2013/09/19/automating-feminism-the-case-of-joanna-russs-the-female-man/", "secondary_scholarly_literary_analysis",
           "Public web text's Whileaway/Jael sections read", "Induction helmets, labor's conflicting descriptions, work enforcement and Jael's world.",
           "Interpretive criticism, not a new primary read. It explicitly recognizes incompatible readings of Whileaway's work. An ordinary separate fetch returned 406; no recovery was pursued."),
    source("src-female-man-reference", "The Female Man", "Wikipedia contributors",
           "https://en.wikipedia.org/wiki/The_Female_Man", "secondary_plot_and_setting_reference",
           "Public setting and plot sections read", "Whileaway and Jael's separate continuities and the distinction between robot partners and whole economies.",
           "General reference with uneven citation quality; used for scope, not exact guarantees or a labor census."),
    source("src-fifth-sacred-reference", "The Fifth Sacred Thing", "Wikipedia contributors",
           "https://en.wikipedia.org/wiki/The_Fifth_Sacred_Thing", "secondary_plot_and_setting_reference",
           "Public indexed summary read", "San Francisco's sustainable local agriculture and collective provision.",
           "Reference-only short check. No autonomous general production was established; no novel or sequel read is claimed."),
    source("src-accelerando-author-crib", "Crib sheet: Accelerando", "Charles Stross, Charlie's Diary, 28 May 2013",
           "https://www.antipope.org/charlie/blog-static/2013/05/crib-sheet-accelerando.html", "official_author_commentary",
           "Public indexed author post read; direct web open later errored", "The early/late distinction, human destruction and arbitrary mutilated resurrection by the Vile Offspring.",
           "Author commentary, not a complete novel read. Death and passive records do not count as leisure persons. The author does not present the outcome as a straightforward utopia."),
    source("src-accelerando-reference", "Accelerando", "Wikipedia contributors",
           "https://en.wikipedia.org/wiki/Accelerando", "secondary_plot_reference",
           "Public chapter synopsis read", "Early venture altruism and self-replicating factories; Curator/Elector bankruptcy, enforcement and separate Saturnian politics.",
           "Used for broad chronological scope; no participation percentages. A secondary chapter synopsis is not a complete primary read."),
    source("src-accelerando-gebhart", "Book Review: Accelerando Will Make Your Brain Hurt - In a Good Way", "Tim Gebhart, Blogcritics",
           "https://blogcritics.org/book-review-accelerando-will-make-your/", "secondary_literary_review",
           "Public paragraphs on planetary conversion and late human communities read", "Vile Offspring, automated financial entities, converted planets and the human-derived remnant.",
           "Review interpretation; its loose biological/posthuman terminology is not a count of distinct persons or evidence of universal provision."),
    source("src-accelerando-svec", "Book Review: Accelerando", "Chris Svec, 29 November 2009",
           "https://chrissvec.com/book-review-accelerando/", "secondary_literary_review_with_primary_excerpt",
           "Public review's economic discussion read", "Obsolescence of human skills and inability to compete in Economics 2.0.",
           "A short review and selected quotations, not an independently read novel. Its favorable evaluation is not treated as an economic guarantee.")
]
h = ["src-female-man-hicks"]
ac = ["src-accelerando-author-crib", "src-accelerando-gebhart", "src-accelerando-svec"]
R = [
    record("female-man-whileaway", "c0143", "The Female Man (Whileaway)", "The Female Man", "Whileaway's highly mechanized society with enforced work", ["book"],
           scope("Russ's novel, Janet's Whileaway continuum", "The society described during Janet's visit, after induction helmets enter industry", "Living Whileawayans of all ages", ["Jael's Womanland and Manland", "Other Janet stories silently merged into the novel", "An exterminated population counted as nonworking"]),
           "Whileaway is retained provisionally as a zero variant. Its induction technology lets a single worker direct machinery on a scale formerly requiring thousands. Yet work remains a defining social obligation, with severe enforcement against refusal. The scholarly account treats this as a deliberate tension between productive abundance and a culture organized around work. It also flags conflicting descriptions of incessant toil and a short formal week. The classification preserves that ambiguity rather than declaring every remaining task technically pointless.\n\nMaterial security is therefore conditional enough to prevent a strong universal-guarantee score. Direct participation by workers suggests dispersed human agency, but the consulted sources do not settle ownership or effective political control, so that coordinate remains open. Useful care and other activity still count as work. A short week cannot supply the nonworking share, and the record excludes Jael's different future. The alternative reading is a partially automated society that still needs its remaining labor.",
           {"guarantees": 0.2, "control": None, "nonworking": None},
           {"guarantees": assessment(0.2, [-0.45, 0.65], "low", "Provision is qualified by severe compulsory-participation enforcement. This assesses conditional security, not a claim that ordinary compliant residents lack goods.", h),
            "control": assessment(None, None, "low", "Worker-directed cybernetic machinery does not settle ownership or the distribution of binding authority.", h),
            "nonworking": assessment(None, None, "low", "Conflicting work descriptions and a formal short week do not measure all-resident participation; caregiving is useful work.", h)},
           0, h + ["src-female-man-reference"],
           [evidence("The criticism identifies high productive leverage alongside a work imperative whose economic necessity is disputed.", h, "Whileaway discussion, especially web text lines 153-155 and 192-204", "secondary_interpretation")],
           ["Zero-variant admission is explicitly interpretive: the criticism offers incompatible readings and does not prove every current job redundant.", "Both control and participation remain unresolved. A partial post-work reading is an alternative classification."], record_type="zero_variant", analogy=[2, 4]),
    record("accelerando-economics-two-human-remnant", "c0147", "Accelerando (Economics 2.0 and the human remnant)", "Accelerando", "Humans and human-derived persons exposed to the autonomous inner-system economic takeover", ["book", "short_story"],
           scope("Stross's Accelerando arc", "The late singularity around Curator and Elector, during inner-system conversion and its impact on human survivors", "Active human and human-derived persons subject to the machine economic order; restored persons count only when active", ["Autonomous financial agents counted as ordinary humans", "Dead people and passive backups counted as leisure residents", "Saturn's local refugee government conflated with the inner-system economy", "Early Manfred's patrons treated as a universal welfare system"], proxy=True, proxy_basis="Recognized active human-derived persons are included; an agent or stored copy is not automatically another human."),
           "The late inner system runs through superhuman intelligences and autonomous economic entities, with planetary matter absorbed into computational infrastructure. Ordinary human skill no longer secures a viable place in that economy. This is a destructive post-work case: productive power expands while protection for the human remnant collapses. Stross's own commentary stresses that people are destroyed and arbitrarily restored in damaged form. Such restoration supplies no dependable right to a safe life or continued resources.\n\nThe strongly negative control score describes effective autonomy from the affected humans. The Vile Offspring include human-derived successors, so this is a functional use of the AI end of the axis, not a claim that ancestry alone determines control. Human politics in Saturn's refuges is a separate local system. Economic obsolescence does not establish that every survivor stops researching, caring or organizing; participation remains unresolved. Death, dormant backups and automated financial agents never inflate a human leisure estimate.",
           {"guarantees": 0.9, "control": -0.95, "nonworking": None},
           {"guarantees": assessment(0.9, [0.7, 1], "high", "The author describes destruction and arbitrary damaged resurrection; the late economy offers the human remnant no reliable security of access.", ["src-accelerando-author-crib"]),
            "control": assessment(-0.95, [-1, -0.8], "medium", "Successor intelligences and autonomous economic entities operate beyond ordinary human control. The negative coordinate is relative to the affected human remnant, including an explicit functional analogy for human-derived successors.", ["src-accelerando-gebhart", "src-accelerando-svec"]),
            "nonworking": assessment(None, None, "low", "Obsolete market skills and loss of assets do not count all useful activity among surviving active persons.", ["src-accelerando-svec"])},
           6, ac + ["src-accelerando-reference"],
           [evidence("Human economic obsolescence accompanies autonomous productive expansion rather than guaranteed material security.", ac, "Author's 2013 retrospective; reviews' late-system and Economics 2.0 discussions", "author_commentary_and_secondary_lore")],
           ["A reference-led broad assessment; local Saturnian institutions and later extrasolar settlements are distinct.", "The active-person proxy and functional AI-control analogy must remain visible in any later presentation.", "No full-novel read or human nonworking census is claimed."])
]
D = [
    decision("c0143", "zero_variant", "A clear scholarly account supports a provisional automation/work-obligation contradiction, with alternative readings retained.", h + ["src-female-man-reference"], society_id="female-man-whileaway"),
    decision("c0144", "boundary_case", "Jael's robot companion and inter-society labor trade do not establish general automatic material provision.", h + ["src-female-man-reference"], analysis="Womanland/Manland are separate from Whileaway. Robot intimacy and outsourced human labor cannot supply a society-wide post-work mechanism.", follow_up="Skip deeper reading under the faster-pass instruction; reopen only on an explicit economic reference."),
    decision("c0145", "boundary_case", "The quick reference describes ecological and collective provision without establishing automatic replacement of necessary human production.", ["src-fifth-sacred-reference"], analysis="Shared resources and local agriculture alone do not meet the automation criterion.", follow_up="Skip deeper reading; preserve as an ecological-utopia comparison."),
    decision("c0146", "boundary_case", "Early venture altruism and machine projects do not establish labor-independent necessities for the general human population.", ["src-accelerando-reference"], analysis="Manfred's useful inventions and patronage remain a narrow individual arrangement within a changing working economy. Later successor institutions are a separate period.", follow_up="No primary-text rescue in this pass; the late economy is assessed separately at c0147."),
    decision("c0147", "included", "The autonomous successor economy removes human economic power while denying reliable material security to its human remnant.", ac + ["src-accelerando-reference"], society_id="accelerando-economics-two-human-remnant")
]
write_batch(27, [f"c{i:04}" for i in range(143, 148)], S, R, D, [
    "Continues the user's reference-led faster pass; no full primary read or complex format recovery was attempted.",
    "Whileaway's zero classification remains interpretive and openly disputed, with unresolved coordinates. Its short workweek is never converted into a nonworking percentage.",
    "Accelerando's successor economy is scored relative to the affected human remnant with an active-person proxy and explicit functional AI-control analogy. Human extinction or dormant copies never create leisure citizens.",
    "Second pass checked these scope distinctions against consulted references; it is not independent peer review."
])
