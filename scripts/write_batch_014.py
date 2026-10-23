from research_helpers import source, assessment, record, scope, evidence, decision, write_batch

S = [
    source("src-eden-official", "Eden", "Official Stanislaw Lem website",
           "https://english.lem.pl/works/novels/eden", "official_work_commentary_and_author_opinion",
           "Page opened and work commentary read", "The novel's alien political system and the difficulty of interpreting a culture through unfamiliar technology; the author's retrospective assessment.",
           "An authoritarian-system comparison does not establish the actual distribution of necessities or the contribution of the factory to households."),
    source("src-eden-factory-indexed", "Eden: automatic factory scene", "Stanislaw Lem; Russian translation indexed on iTexts",
           "https://itexts.net/avtor-stanislav-lem/108164-edem-stanislav-lem/read/page-3.html", "indexed_primary_fiction_translation_excerpt",
           "Substantial public indexed scene read; direct opening returned cache miss", "The explorers enter a continuously operating installation and the Engineer identifies an automatic factory.",
           "A bounded excerpt was read, not the complete chapter or novel. A working automatic factory does not establish household entitlement or political control of the whole civilization."),
    source("src-eden-reference", "Eden (Lem novel)", "Wikipedia contributors",
           "https://en.wikipedia.org/wiki/Eden_(Lem_novel)", "secondary_plot_reference",
           "Public plot summary read through search and opened page", "The factory's production/destruction/recycling cycle; the crew's contact with the Doublers and eventual political interpretation.",
           "The recycled-output account is secondary here. Neither this summary nor the isolated plant supplies a labor census or a demonstrated post-work allocation system."),
    source("src-cyberiad-seventh-primary", "The Seventh Sally or How Trurl's Own Perfection Led to No Good", "Stanislaw Lem; English text on University of San Diego faculty page",
           "https://home.sandiego.edu/~baber/analytic/Lem1979.html", "primary_fiction_english_transcription",
           "Complete short story opened and read", "Excelsius's miniature kingdom, hard labor and taxation, the constructors' debate about real suffering, and the subjects' escape and later technological development.",
           "Synthetic subjects are not automatically human nonworkers. Whether their suffering is morally real is a central issue, but it does not itself establish an internal labor-saving allocation system."),
    source("src-peace-earth-official", "Peace on Earth", "Official Stanislaw Lem website; author opinion and attributed reviews",
           "https://english.lem.pl/works/novels/peace-on-earth", "official_work_synopsis_with_separately_attributed_commentary",
           "Page opened; synopsis, author comment and critical descriptions read", "National arsenals and factories are relocated to the Moon to evolve independently; a visiting investigator is sent from Earth.",
           "A lunar weapons ecology is distinct from Earth's civilian economy. Reviews' peace and welfare language does not establish automatic population-wide subsistence on Earth."),
    source("src-local-inspection-official", "Inspection at the Scene of the Crime", "Official Stanislaw Lem website; Stanislaw Lem's retrospective comment",
           "https://english.lem.pl/works/novels/inspection-at-the-scene-of-the-crime", "official_work_commentary_and_author_opinion",
           "Page opened and commentary read", "Encja's protective technology and limits of happiness; the author's deliberate correction of the Fourteenth Voyage's apparent planet.",
           "The English work title varies. The earlier amusement-park setting cannot be merged into the actual planet's two polities."),
    source("src-local-inspection-publisher", "Observation on the Spot / Osmotr na meste", "AST; Stanislaw Lem",
           "https://ast.ru/book/osmotr-na-meste-029918/", "official_publisher_synopsis",
           "Public indexed publisher description read", "Distinct Kurdland and Luzania, engineered living city-beasts and the technologically enforced nonviolence of Luzania.",
           "Marketing establishes the separation of polities, not a measured labor share or the truth of every in-world national history."),
    source("src-local-inspection-primary", "Observation on the Spot: Russian translation", "Stanislaw Lem; public text on Kyiv city library site",
           "https://lib.misto.kiev.ua/LEM/osmotr.dhtml", "primary_fiction_translation",
           "Public web text opened; bounded history, manufacturing and late ethicsphere passages read", "The self-reproducing molecular devices; on-request automatic production; surviving humanities; the protection system; late debate about benevolent instructions, bodily intervention and ineffective oversight.",
           "Targeted sections, not a whole-novel reading. The early national histories openly contradict each other. Some late claims about reproductive selection are a character's fears, not confirmed events. A separate ordinary network fetch was forbidden and was not bypassed."),
    source("src-invincible-official", "The Invincible", "Official Stanislaw Lem website; attributed Ursula K. Le Guin commentary",
           "https://english.lem.pl/index.php/works/novels/the-invincible", "official_work_synopsis_and_literary_commentary",
           "Page opened; work description and critical explanation read", "Spontaneously evolved microautomata confront a human expedition; reflexive mechanical conflict is contrasted with reasoning and restraint.",
           "An autonomous machine ecology is not a civilian community providing for human residents; a human expedition is a separate working population."),
    source("src-invincible-game-official", "The Invincible", "11 bit studios; official PlayStation product page",
           "https://www.playstation.com/en-us/games/the-invincible/", "official_game_description",
           "Product page opened; story and adaptation description read", "Yasna's scientific/search mission on Regis III and a branching game based on motifs of Lem's novel.",
           "No playthrough or branch-specific economic arrangement was verified. Shared motifs do not make every game ending part of the novel's continuity.")
]

loc = ["src-local-inspection-primary", "src-local-inspection-official", "src-local-inspection-publisher"]
R = [record(
    "local-inspection-luzania", "c0083", "Observation on the Spot (Luzania's ethicsphere)", "Observation on the Spot", "Luzania's biological Entians within the molecular protective environment", ["book"],
    scope("Wizja lokalna / Inspection at the Scene of the Crime; the actual Encja setting", "The developed Luzanian order described during Tichy's investigation and visit", "Living biological Luzanian Entians, explicitly used as a humanlike participation proxy", ["Kurdland as an identical economy", "Enteropia's amusement-park simulation", "Molecular devices as biological residents", "Dead or purely preserved remains as automatically leisured citizens"], proxy=True),
    "Luzania can arrange an entire manufacturing process around a resident's requested result. Self-reproducing molecular devices replace much routine production, research and protection, while material access no longer depends on earning a wage. The guarantee point is strongly favorable, qualified by the difference between reliable bodily support and a life someone actually wishes to lead. Humanities and other meaningful activities still survive, so their participants must not disappear into a supposed universal leisure statistic.\n\nControl is harder than the republic's formal institutions suggest. The ethicsphere develops the implications of its benevolent instructions beyond what residents can readily inspect, negotiate or undo. A negative control estimate describes that effective algorithmic constraint; it does not invent a conscious robot monarch. Residents can still request results and specialists can modify systems, so complete machine sovereignty would overstate the evidence. The control interval remains wide, and the biological aliens are an explicit population proxy. Kurdland's contrasting arrangements require separate verification before a second point is added.",
    {"guarantees": -0.85, "control": -0.65, "nonworking": None},
    {"guarantees": assessment(-0.85, [-0.98, -0.55], "medium", "Automatic on-request manufacture and broadly available goods remove ordinary wage dependence. Continuing bodily support is not a guarantee against every psychological harm or unforeseen system development.", loc),
     "control": assessment(-0.65, [-0.9, -0.15], "low", "The distributed protective system implements its remit beyond readily reversible resident choice. Humanlike residents retain requests, expertise and institutions; no unitary conscious sovereign is assumed.", ["src-local-inspection-primary"]),
     "nonworking": assessment(None, None, "low", "Automation makes much conventional scientific and productive work unnecessary, but humanities, specialist intervention and chosen activity persist. No all-age participation count is available for the alien proxy.", ["src-local-inspection-primary"])},
    5, loc,
    [evidence("Molecular systems reproduce themselves and automatically implement productive processes around requested ends; historical accounts describe general material saturation.", ["src-local-inspection-primary"], "Library text: molecular devices and science section, web lines 3191-3235; abundance and synthetic culture, 3272-3343", "depicted_or_author_stated"),
     evidence("Benevolent instructions produce unrequested interventions and disputed limits to effective oversight.", ["src-local-inspection-primary"], "Late conversation about the ethicsphere and ectotechnology, web lines 9645-9759", "depicted_or_author_stated")],
    ["The negative control point maps functional autonomous machine constraints, not a claim of a self-aware central AI.", "Character speculation about hidden reproductive selection is not recorded as established fact.", "Kurdland's self-serving historical account does not by itself justify another retained society.", "The English title and country spelling vary; no complete English translation is claimed."], alternatives=[2])]
R[0]["work_aliases"] = ["Wizja lokalna", "Inspection at the Scene of the Crime", "Eyewitness Account"]
R[0]["control_analogy"] = {"system": "Distributed molecular protective and productive technology", "reference": "Effective autonomous machine control", "limitation": "Autonomous implementation does not require a conscious centralized ruler; residents retain meaningful requests and technical roles."}

D = [
    decision("c0080", "needs_evidence", "Automatic machinery and an oppressive alien polity are established separately; a wage-independent household economy is not.", ["src-eden-official", "src-eden-factory-indexed", "src-eden-reference"],
             "The factory scene confirms automatic operation, while a secondary summary describes an output-recycling loop. Such a plant may be economically disconnected or dysfunctional rather than a source of universal provision. The novel's difficulty of interpreting alien institutions also makes an unqualified global control point misleading. Neither advanced technology nor political violence answers how the Doublers obtain necessities.",
             "Read the later Doubler conversation and its account of current productive and allocative institutions. Verify who receives useful output and who must work; retain the factory as a lead rather than inventing a welfare or zero-variant regime."),
    decision("c0081", "boundary_case", "An automatically constructed miniature world still depicts internal hard labor, without an established labor-saving material system for its subjects.", ["src-cyberiad-seventh-primary"],
             "The relevant story is the Seventh Sally. Its miniature subjects labor, pay taxes, suffer under Excelsius and eventually escape the box. The constructors' argument makes their moral personhood important, but does not demonstrate that their production is done for them or that a known labor-saving alternative is deliberately suppressed. Treating the entire physical simulation as an automatic factory confuses the outside mechanism with the subjects' economy. The ending changes political power without describing post-work distribution.",
             "Keep as a personhood and control comparison. Reopen only if an applicable synthetic-population proxy and an internal automation/distribution relationship can both be justified. Do not infer a zero variant from creator omnipotence alone."),
    decision("c0082", "boundary_case", "The lunar system is an autonomous weapons ecology, without a resident human society receiving its output.", ["src-peace-earth-official"],
             "National arms factories and arsenals evolve on the Moon after separation from terrestrial politics. A human investigator's visit is not a settled nonworking population. The source's description of Earth's peace and welfare concerns a different population and does not establish its civilian entitlements or productive automation. Military autonomy alone therefore supplies no three-axis society record.",
             "Preserve as an autonomous-production comparison. Research Earth's civilian economy separately if explicit wage-independent provision is found; do not assign a lunar human leisure rate from the absence of residents."),
    decision("c0083", "included", "Primary manufacturing and ethicsphere passages qualify a specifically scoped Luzania; the entire Entian planet is not treated as one system.", loc,
             society_id="local-inspection-luzania", unretained_subscopes=[{"society": "Kurdland", "status": "needs_evidence", "reason": "Bioengineered cities and state discipline may support a distinct arrangement, but their labor and subsistence rules need confirmation beyond contradictory national histories."}]),
    decision("c0084", "boundary_case", "Regis III's evolved microautomata are a machine ecology, not a demonstrated human or humanlike post-work polity.", ["src-invincible-official", "src-invincible-game-official"],
             "Autonomous replication and effective resistance to an expedition do not create material guarantees for human residents. The explorers are actively working visitors. Mechanical evolution is also not evidence for a deliberate sovereign AI. The game explicitly uses its own protagonist and branches, so those outcomes cannot silently become extra canonical novel societies.",
             "Keep as a nonhuman autonomy comparison. Reopen only for a separately evidenced resident population with productive and allocative rules; never convert the lack of human settlement or the fate of explorers into 100% leisure.")
]

write_batch(14, [f"c{i:04}" for i in range(80, 85)], S, R, D, [
    "The sequential pass distinguishes artificial construction, automatic weapons and machine ecology from post-work provision for an applicable resident population.",
    "Luzania qualifies through primary on-request production, with explicit alien proxy and broad uncertainty about effective control. No unsupported all-planet or Kurdland point is counted.",
    "Second pass separated literal novel events from in-world nationalist accounts, character fears and proposed futures; conscious sovereignty from functional automatic constraints; and the game from the novel.",
    "Zero variants remain welcome under the user's clarification, but ordinary hard work without an established automation connection does not automatically qualify."
])
