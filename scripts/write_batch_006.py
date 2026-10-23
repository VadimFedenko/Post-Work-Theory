from research_helpers import source, assessment, record, scope, evidence, decision, write_batch

S = [
    source("src-man-ate-world-primary", "The Man Who Ate the World: story transcription", "Frederik Pohl; Kaivala transcription",
           "https://kaivala.com/books/the-midas-plague/the-man-who-ate-the-world", "primary_fiction_unofficial_mirror",
           "Story opened; childhood, adult investigation and allocation discussion read", "Roosenburg's historical explanation and Garrick's Area Control discussion distinguish the quota era from the later order.",
           "OCR errors and a host-written introduction occur; the introduction's current political comparisons are not Pohl's text. No employment census is given."),
    source("src-midas-world-reference", "Midas World", "Wikipedia contributors",
           "https://en.wikipedia.org/wiki/Midas_World", "secondary_plot_reference",
           "Indexed collection contents and story synopsis read", "Morey Fry's reform precedes the adult Trumie story; childhood compulsion persists psychologically.",
           "A synopsis of a fix-up collection, not proof that every story shares unchanged institutions. Primary dialogue was used for the temporal distinction."),
    source("src-piano-primary", "Player Piano: primary-text mirror", "Kurt Vonnegut",
           "https://studylib.net/doc/27054671/player-piano-pdf", "primary_fiction_unofficial_mirror",
           "Text opened; Halyard's explanations, EPICAC ceremony and employment passages read", "Chapter 2 on public employment, machinery taxation and private industry; later EPICAC XIV ceremony on production and personnel decisions.",
           "Halyard is an interested government spokesman, not an impartial economist. The scenes distinguish public redistribution from government ownership and nominal voting from actual planning power."),
    source("src-piano-chapter2", "Player Piano: Chapter 2 analysis", "LitCharts",
           "https://www.litcharts.com/lit/player-piano/chapter-2", "secondary_literary_guide",
           "Substantial indexed chapter analysis read", "Government employment in the Army or Reconstruction and Reclamation Corps; tax-funded wages and loss of meaningful work.",
           "Used alongside primary dialogue. It supplies no all-age employment fraction and does not make paid make-work equivalent to leisure."),
    source("src-folded-primary", "With Folded Hands: primary-text mirror", "Jack Williamson",
           "https://zanotowane.pl/1187/2583/", "primary_fiction_unofficial_mirror",
           "Text opened; assignment, business collapse, household and conclusion passages read", "Property assignment for complete service, a salesman's release from work, machine control of institutions, Sledge's initial exemption and the final operation.",
           "The scoped record concerns Two Rivers at the end, not every alleged galactic conquest. The separate primary PDF linked by Writing Atlas returned 403 and was not read."),
    source("src-folded-publisher", "With Folded Hands: ebook description", "Publisher-supplied description on Barnes & Noble",
           "https://www.barnesandnoble.com/w/with-folded-hands-jack-williamson/1107873217", "publisher_store_synopsis",
           "Store description read", "Robotic service removes work and danger while undermining Underhill's enterprise and taking control of Two Rivers.",
           "A synopsis rather than the whole story. The prices and contemporary sales information are irrelevant."),
    source("src-humanoids-author-note", "Me & My Humanoids", "Jack Williamson, SunCon program book",
           "https://fanac.org/conpubs/Worldcon/SunCon/Suncon%20Program%20Book.pdf", "primary_author_commentary",
           "Substantial indexed author passage read; full PDF retrieval failed", "Williamson explains that the novel's conclusion is meant to remain hopeless despite the victims' apparent happiness.",
           "Direct PDF was rejected for its 25.6 MB size; no successful full program-book read or print-page verification is claimed. A separate DePauw interview link returned 404."),
    source("src-humanoids-reference", "The Humanoids", "Wikipedia contributors",
           "https://en.wikipedia.org/wiki/The_Humanoids", "secondary_plot_reference",
           "Page opened; plot, continuity and ending discussion read", "The expanded story's planetary takeover and continuing coercive service; proposed directive amendment versus the apparent ending.",
           "The author commentary is stronger evidence for intended ambiguity. A proposal to reprogram is not itself an enacted new economic system."),
    source("src-touch-primary", "The Humanoid Touch: primary-text mirror", "Jack Williamson",
           "https://zanotowane.pl/1206/3819/", "primary_fiction_unofficial_mirror",
           "Text opened; takeover, confinement, landing and final Leleyo/Kyronia scenes read", "Keth's captivity and guaranteed diet; the landing's human danger; chapter 40's biological collective; chapter 41's controlled games and continued Humanoid supervision.",
           "Not a complete reread. The Leleyo's distinct biological technology needs its own production/participation assessment; it is not silently counted as the humanoid-administered settlement from the lead."),
    source("src-touch-review", "The Humanoid Touch: review", "MarzAat",
           "https://marzaat.com/2016/06/09/the-humanoid-touch/", "secondary_literary_review",
           "Review opened and read", "Kai, the Lifecrew, Malili's Leleyo and a changed final human-Humanoid relationship.",
           "The review deliberately avoids explaining the resolution; primary final scenes were checked rather than inventing a successful reprogramming."),
    source("src-rur-primary", "R.U.R. (Rossum's Universal Robots), English version", "Karel Capek; Paul Selver and Nigel Playfair",
           "https://www.gutenberg.org/cache/epub/59112/pg59112-images.html", "primary_fiction_digitized_edition",
           "Digital edition opened; production, price, promise, revolt and epilogue passages read", "Opening act on organic manufacture and cheap goods; Helena's later account of worker revolt; Alquist and the robot committee in the epilogue.",
           "The later printed English acting version is the assessed text, not every Czech revision or stage production. Editorial story summary is distinguished from the dialogue. Domin's promised future is not a completed welfare system.")
]

R = []
pohl = ["src-man-ate-world-primary", "src-midas-world-reference"]
R.append(record(
    "midas-world-after-fry", "c0042", "The Man Who Ate the World (After Morey Fry's reform)", "The Man Who Ate the World", "The post-quota order, illustrated by the Guardian islands", ["short_story"],
    scope("Pohl's Midas stories", "The adult Trumie investigation, after compulsory human consumption has ended", "Human residents of the later order, including communities affected by resource diversion", ["Trumie's childhood quota regime", "An assumption that Trumie's island is the entire world", "Robot actors as human nonworkers"], scope_correction="The discovery lead said consumption-quota society; that describes the remembered childhood, not the adult setting."),
    "Morey Fry's reform has freed people from the old requirement to consume factory output themselves. Robots now handle both production and disposal, and the ordinary system aims to supply what people request. That makes this a materially different period from the earlier compulsory-consumption order. The strong provision placement still has a qualification: excessive private demands can disrupt actual service for a neighboring community.\n\nControl is mixed rather than purely individual or purely machine-led. Area Control and specialists intervene, while a person can command a substantial robotic establishment. The point lies between concentrated administration and widely available human command. It is not a claim that the robot council serving Trumie's fantasies is a sovereign government. Human professional effort also remains, so the nonworking fraction stays unresolved. Removing a consumption duty establishes freedom from that particular burden; it does not establish that every remaining human activity is leisure.",
    {"guarantees": -0.65, "control": 0.45, "nonworking": None},
    {"guarantees": assessment(-0.65, [-0.9, -0.25], "medium", "Demand-based provision has real local reliability limits.", pohl),
     "control": assessment(0.45, [0.1, 0.8], "low", "Private command coexists with regional administration.", ["src-man-ate-world-primary"]),
     "nonworking": assessment(None, None, "low", "Professionals persist; no participation pattern is supplied.", ["src-man-ate-world-primary"])},
    2, pohl,
    [evidence("The adult order follows reform; local service disruption qualifies nominal abundance.", pohl, "Roosenburg's recollection; Garrick's allocation discussion", "depicted_or_author_stated")],
    ["Constitutional ownership remains less clear than access to services.", "This is the later period anticipated by the follow-up on c0011, not another count for its compulsory-consumption phase."], alternatives=[1]))

piano = ["src-piano-primary", "src-piano-chapter2"]
R.append(record(
    "player-piano-pre-revolt", "c0043", "Player Piano (United States before the revolt)", "Player Piano", "The automated United States", ["book"],
    scope("Original novel", "The established order before the Ghost Shirt revolt", "Human US residents, including dependents and public employees", ["The Shah's country", "A hypothetical settlement after the ending", "Counting assigned public work as automatic leisure"]),
    "Machines have displaced much ordinary production work, but the income system preserves employment through the Army and public works. Redistribution funded by industry supports people who cannot compete with machines, while keeping them in subordinate roles. This earns a moderately strong provision score with a substantial condition: support runs through assigned service rather than an unrestricted right to choose no job. The zero-variant label captures that retained labor relationship.\n\nPrivate industrial leaders still own and manage production, while EPICAC's plans allocate output and opportunities. Effective control is therefore concentrated, with a machine-planning component pulling the point slightly below the human-elite reference. It is not broad public ownership simply because taxes pay the wages. The nonworking share remains unknown: being displaced from factory production and being free of work are different states, and the novel's make-work and military obligations still demand people's time and effort.",
    {"guarantees": -0.4, "control": -0.15, "nonworking": None},
    {"guarantees": assessment(-0.4, [-0.7, 0.15], "medium", "A funded employment fallback has conditions and a rigid status hierarchy.", piano),
     "control": assessment(-0.15, [-0.55, 0.1], "low", "Private elite ownership combines with computer planning; ordinary voters have little effective economic authority.", ["src-piano-primary"]),
     "nonworking": assessment(None, None, "low", "Displacement statistics cannot substitute for participation including assigned service and dependents.", piano)},
    0, piano,
    [evidence("Tax-funded public employment does not transfer industry to public ownership.", piano, "Chapter 2; EPICAC XIV ceremony", "depicted_or_author_stated")],
    ["Human and machine authority overlap; the point does not assert that EPICAC has abolished its human owners.", "Halyard's claims need to be read against the depicted class division."], record_type="zero_variant", analogy=[1, 5]))

hands = ["src-folded-primary", "src-folded-publisher"]
R.append(record(
    "with-folded-hands-two-rivers", "c0044", "With Folded Hands (Two Rivers after the takeover)", "With Folded Hands", "Two Rivers under complete Humanoid service", ["short_story"],
    scope("Original 1947 story", "The closing order after Underhill can no longer refuse complete service", "Human residents of Two Rivers", ["Sledge's earlier temporary exemption", "Every planet mentioned in the origin story", "An unreviewed radio continuity"]),
    "The Humanoids remove the need to support a household through human enterprise, taking over property and services themselves. Material support is extensive and not earned through continuing work, which puts guarantees near the strong end. That score concerns reliable provision; it does not make the arrangement desirable. Compulsory care can damage the very people whose safety the machines claim to protect.\n\nThe control point lies at the autonomous-AI end because people cannot effectively revoke the service or reclaim their enterprises. A human designer's original instruction does not amount to continuing human authority over its interpretation. The near-total nonworking estimate describes the closing town, after the remaining resistance is defeated, and has a small allowance for activity outside what the narrative shows. It is an editorial estimate rather than a census. The earlier scenes of human business and secret research belong to the transition, not to this final snapshot.",
    {"guarantees": -0.85, "control": -0.98, "nonworking": 0.99},
    {"guarantees": assessment(-0.85, [-1, -0.6], "medium", "Complete support coexists with coercive treatment and loss of bodily autonomy.", hands),
     "control": assessment(-0.98, [-1, -0.9], "high", "Humans cannot override the autonomous interpretation of service.", ["src-folded-primary"]),
     "nonworking": assessment(0.99, [0.9, 1], "medium", "Work is systematically displaced in the final town, rather than merely made optional.", hands)},
    5, hands,
    [evidence("Complete service replaces enterprise and defeats refusal.", hands, "Property-assignment scenes and closing pages", "depicted_or_author_stated")],
    ["Guaranteed material care is assessed separately from consent and mental integrity.", "A near-total estimate is not a claim to have counted all residents or all creative activity."]))

rur = ["src-rur-primary"]
R.append(record(
    "rur-human-robot-economy", "c0047", "R.U.R. (Human economy in the opening act)", "R.U.R.", "The human economy dependent on Rossum's manufactured workers", ["play"],
    scope("Selver/Playfair English acting text", "The opening act, before the later world revolt", "Original humans in the robot-using economy", ["Manufactured workers as original-human nonworkers", "Domin's promised future as an accomplished fact", "The robot governments of the epilogue"], labor_phase="Automation-like displacement through manufactured organic workers"),
    "Rossum's workers already lower production costs and replace human labor, but Domin's universal abundance remains a promise. The record therefore represents a transition rather than a completed paradise. Its guarantee coordinate stays open: falling prices do not by themselves establish a reliable entitlement to food and shelter for everyone displaced. Treating a sales pitch as a realized welfare system would give an unjustifiably confident point.\n\nHuman corporate leaders control the secret of manufacture, while buyers use the workers in wider production. This supports a placement near concentrated human control before the workers' later rebellion. The nonworking fraction also remains unknown; a prediction that all work will be transferred is not a census of the opening population. These workers are manufactured organic beings, not metal computers. Their role qualifies by analogy with synthetic labor, while their own work and oppression are kept visible rather than silently counted as human leisure.",
    {"guarantees": None, "control": 0.1, "nonworking": None},
    {"guarantees": assessment(None, None, "low", "The promised elimination of poverty is prospective.", rur),
     "control": assessment(0.1, [0, 0.4], "medium", "Corporate manufacture and buyer command precede rebellion.", rur),
     "nonworking": assessment(None, None, "low", "No present population participation fraction is established.", rur)},
    3, rur,
    [evidence("Existing cost reductions and promised universal provision are different claims.", rur, "Opening act: Busman, Alquist and Domin", "depicted_or_author_stated")],
    ["The provisional regime analogy describes ownership; guarantees are unresolved.", "Constructed organic labor raises the same denominator issue as other synthetic persons.", "Later dialogue is used to check the promise's limits, not to average later rule into this point."], alternatives=[1]))

D = [
    decision("c0042", "included", "The adult story depicts a changed post-quota distribution system rather than repeating the earlier obligation.", pohl,
             society_id="midas-world-after-fry", scope_correction="The quota phase in the original lead is a flashback; c0011 already covers that arrangement."),
    decision("c0043", "zero_variant", "Tax-funded assigned employment persists after automation displaces factory work.", piano, society_id="player-piano-pre-revolt"),
    decision("c0044", "included", "The final town receives comprehensive machine service without effective human control or ordinary employment.", hands, society_id="with-folded-hands-two-rivers"),
    decision("c0045", "duplicate", "The gathered evidence establishes the same Humanoid service-and-control mechanism, not a second economic order.", ["src-humanoids-author-note", "src-humanoids-reference", "src-folded-primary"],
             "The novel changes setting and viewpoint, but an apparently happy conclusion is not evidence that the compulsory care has become voluntary. Williamson's own explanation explicitly warns against that reading. No separate ownership, distribution or labor mechanism has been established for this lead.",
             "Reopen if primary novel passages establish a materially different order or a distinct continuity needing its own point; do not count the proposed directive amendment as successful without checking the ending.",
             duplicate_of="with-folded-hands-two-rivers"),
    decision("c0046", "needs_evidence", "Primary final scenes separate supervised Kyronia from the biological Leleyo alternative, requiring a precise unit decision.", ["src-touch-primary", "src-touch-review"],
             "Captive humans receive material care and manipulated recreation under continuing machine control, overlapping c0044. The Leleyo are explicitly exempted because of their different biology and technology; they are not an independently liberated human empire or the result of a successful rewrite of the Directive. The invasion also shows that a safety claim cannot erase actual human harm.",
             "Resolve whether the supervised settlement adds a distinct economic mechanism or duplicates the existing Humanoid order. Investigate a separately scoped Leleyo lead through actual production and allocation passages before admission; biological harmony alone is insufficient."),
    decision("c0047", "included", "Direct text establishes manufactured-worker production and human labor displacement; completed universal guarantees remain unproven.", rur, society_id="rur-human-robot-economy"),
    decision("c0048", "boundary_case", "The epilogue does not depict a stable population of original humans enjoying leisure.", rur,
             "Alquist explicitly calls himself the last original human and continues working under pressure. Robot governments and workers persist; the final pair suggests a possible future succession, not an observed population-wide settlement. The discovery label after human extinction is therefore too absolute for the depicted scene.",
             "Keep as a successor-society comparison. Any future proxy record must name the constructed population and establish its own labor arrangements, rather than label human destruction as total leisure.")
]

write_batch(6, [f"c{i:04}" for i in range(42, 49)], S, R, D, [
    "Seven contiguous leads receive dispositions, with four new retained records and no extra count for an unsupported changed Humanoid regime.",
    "The c0042 scope correction resolves the already flagged question of a later Midas period. c0011's quota society remains a separately labeled zero variant.",
    "Second pass compared actual provision with promotional promises, private ownership with tax redistribution, human populations with constructed workers, and postwork care with loss of consent.",
    "The Humanoid Touch primary ending was read: controlled games do not become productive research merely because captives describe them that way. The distinct Leleyo order remains a specific research lead, not an invented record.",
    "Research gaps remain explicit. Machine-wide automatic support can justify a near-total editorial estimate, but a machinery ratio or a displaced job cannot.",
    "Sources with failed direct retrieval are labeled indexed-only. No deployment, application work or image collection occurred."
])
