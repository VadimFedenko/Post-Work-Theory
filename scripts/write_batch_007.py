from research_helpers import source, assessment, record, scope, evidence, decision, write_batch

S = [
    source("src-sleeper-primary", "When the Sleeper Wakes", "H. G. Wells; Project Gutenberg eBook 775",
           "https://www.gutenberg.org/files/775/775-h/775-h.htm", "primary_fiction_digitized_edition",
           "Text opened; ownership, Labour Company and workshop passages read", "Ostrog's explanation of the Trustees; Helen's account of the Company; Chapter XXI's machine-minders and supervision.",
           "Assessed under the title supplied by this digital text, not silently combined with the later revision The Sleeper Awakes. A Labour Company membership share is not the total employed share."),
    source("src-men-gods-economy", "Men Like Gods: A Loiterer in a Living World", "H. G. Wells; American Literature transcription",
           "https://americanliterature.com/author/hg-wells/book/men-like-gods/2-a-loiterer-in-a-living-world", "primary_fiction_transcription",
           "Chapter opened; sections 4-5 read closely", "Crystal explains the birth endowment, accounts, expected occupation and dispersed specialist authority.",
           "Moneyless daily transactions do not mean that work and accounts have disappeared. Crystal is a character explaining his society, not a statistical survey."),
    source("src-men-gods-primary", "Men Like Gods", "H. G. Wells; Project Gutenberg Australia",
           "https://gutenberg.net.au/ebooks02/0200221h.html", "primary_fiction_digitized_edition",
           "Text opened; government, activity and engineering passages read", "Book I's account of active citizens and absence of central government; engineering works and worker camps; the visitor's partial understanding.",
           "The narrative endorses selective population practices; an account of comfortable present residents does not establish inclusive treatment of every possible human being. It contains no employment census."),
    source("src-shape-council", "The Shape of Things to Come: The Tyranny of the Second Council", "H. G. Wells; Telelib",
           "https://www.telelib.com/authors/W/WellsHerbertGeorge/prose/thingstocome/thingstocome41.html", "primary_fiction_transcription",
           "Chapter opened; Council rule and work ethic passages read", "Book IV.5: concentrated leadership, austerity, resistance to succession and continued projects after reconstruction.",
           "Part of a fictional retrospective history, not a neutral real-world policy account. Its period is kept separate from the post-Council world."),
    source("src-shape-keying", "The Shape of Things to Come: Keying Up the Planet", "H. G. Wells; Telelib",
           "https://www.telelib.com/authors/W/WellsHerbertGeorge/prose/thingstocome/thingstocome45.html", "primary_fiction_transcription",
           "Chapter opened; machinery, employment and withheld discovery passages read", "Book V.2 retrospectively explains the Second Council's universal-employment objective and the later growth of biological invention.",
           "Historical figures and publications within the forecast are fictional where appropriate; they are not outside evidence. The chapter gives no all-age nonworking rate."),
    source("src-shape-megeve", "The Shape of Things to Come: The Declaration of Megeve", "H. G. Wells; Telelib",
           "https://www.telelib.com/authors/W/WellsHerbertGeorge/prose/thingstocome/thingstocome43.html", "primary_fiction_transcription",
           "Whole short chapter read", "Book IV.7: independent cooperation among Controls, retirement of the supreme Council, universal security and the remaining modicum of work.",
           "A political declaration does not prove equal direct decision power for every person. Remaining public duties must not disappear from a post-work description."),
    source("src-shape-plenty", "The Shape of Things to Come: Organization of Plenty", "H. G. Wells; Telelib",
           "https://www.telelib.com/authors/W/WellsHerbertGeorge/prose/thingstocome/thingstocome48.html", "primary_fiction_transcription",
           "Chapter opened and material-distribution passages read", "Book V.5: ordinary access to food, housing and clothes; mechanical production, replacement systems, portable homes, money accounts and socialized property.",
           "A surviving money account is explicit. The chapter does not support a simplistic claim that every transaction is free or that people have no work duties."),
    source("src-shape-interest", "The Shape of Things to Come: Sublimation of Interest", "H. G. Wells; Telelib",
           "https://www.telelib.com/authors/W/WellsHerbertGeorge/prose/thingstocome/thingstocome51.html", "primary_fiction_transcription",
           "Chapter opened; first section on work and necessities read", "Book V.8: few specialists sustain primary provision; congenial work and scientific or artistic activity remain.",
           "The numerical percentages near the beginning concern the old world around 1930, not the 2106 population. They are not imported as a modern employment statistic."),
    source("src-modern-utopia-primary", "A Modern Utopia", "H. G. Wells; Project Gutenberg eBook 6424",
           "https://www.gutenberg.org/files/6424/6424-h/6424-h.htm", "primary_fiction_digitized_edition",
           "Text opened; Chapters III, V, VII and IX sampled for specific arrangements", "Machinery's potential, reserve employment and minimum wages, insurance and pensions, toy-factory bargaining, and Samurai control.",
           "Philosophical proposals and the imagined encounter coexist in the work. Reduced toil does not abolish wage dependence; reproductive restrictions and seclusion qualify its universalist language."),
    source("src-bellamy-service", "Looking Backward: Chapter 6", "Edward Bellamy; Marxists Internet Archive",
           "https://www.marxists.org/reference/archive/bellamy-ed/works/backward/ch06.htm", "primary_fiction_transcription",
           "Chapter opened; service and retirement account read", "Compulsory national service, ages 21-45 and exceptional emergency recall until 55.",
           "A service age band is not a population pyramid. It does not count other useful activity or imply that every person over 45 is inactive."),
    source("src-bellamy-credit", "Looking Backward: Chapter 9", "Edward Bellamy; Marxists Internet Archive",
           "https://www.marxists.org/reference/archive/bellamy-ed/works/backward/ch09.htm", "primary_fiction_transcription",
           "Chapter opened; distribution and equal shares read", "Personal credit on the public books, equal material claim, effort versus output and continued service duties.",
           "Equality of shares is distinct from having no work obligation. Dr. Leete's claims describe the intended order rather than independently audited outcomes."),
    source("src-bellamy-control", "Looking Backward: Chapter 17", "Edward Bellamy; Marxists Internet Archive",
           "https://www.marxists.org/reference/archive/bellamy-ed/works/backward/ch17.htm", "primary_fiction_transcription",
           "Chapter opened; production and the full election explanation read", "Administrative hierarchy, retired guild members electing leaders, disenfranchisement of active industrial workers for those elections, and professional exceptions.",
           "National ownership must not be equated with direct worker control. Public office and professional activity can continue beyond ordinary service."),
    source("src-bellamy-inventions", "Looking Backward: labor-saving inventions and household service", "Edward Bellamy; Project Gutenberg eBook 624",
           "https://www.gutenberg.org/files/624/624-h/624-h.htm", "primary_fiction_digitized_edition",
           "Targeted household and invention passages read", "Public kitchens and laundries, electric service, and incentives to develop labor-saving inventions.",
           "Moving work out of the private home does not prove it is unmanned. Labor-saving technology and public organization are both present."),
    source("src-equality-preface", "Equality: Preface", "Edward Bellamy; Project Gutenberg eBook 7303",
           "https://www.gutenberg.org/files/7303/7303-h/7303-h.htm", "primary_author_preface_and_fiction",
           "Preface and recap opened and read", "Bellamy explicitly retains the date and framework of Looking Backward and expands the same national cooperative system.",
           "An elaboration is not automatically a new phase. Later policy differences can be reopened if primary evidence shows a changed arrangement."),
    source("src-reynolds-author-recap", "Equality: In the Year 2000: Introduction recapping Looking Backward", "Mack Reynolds; publisher ebook preview on Everand",
           "https://www.everand.com/book/484777968/Equality-In-the-Year-2000", "primary_author_commentary_in_publisher_preview",
           "Public preview opened; author's Introduction read", "Reynolds summarizes the previous novel, its automation, GAI and limited productive workforce, and distinguishes his rewrite from Bellamy.",
           "This is the author's retrospective recap, not a full read of the first novel. The claimed GAI share does not rule out productive voluntary activity outside essential employment."),
    source("src-reynolds-looking-publisher", "Looking Backward From the Year 2000", "Hachette Australia / Gateway",
           "https://www.hachette.com.au/mack-reynolds/looking-backward-from-the-year-2000", "official_publisher_catalogue",
           "Official catalogue page opened", "Title, author, current edition identity and sleeper premise.",
           "The short synopsis does not establish the constitution or a labor rate. Edition dates and the synopsis's rounded sleep duration are not used to settle the novel's exact chronology."),
    source("src-reynolds-looking-review", "1973: Looking Backward, from the Year 2000", "2theD, Potpourri of Science Fiction Literature",
           "https://sfpotpourri.blogspot.com/2015/01/1973-looking-backward-from-year-2000.html", "secondary_literary_review_with_primary_quotation",
           "Review opened; quoted social-system discussion and its context read", "Reported page 168 combines collective, syndicalist, technocratic and meritocratic elements rather than one simple political label.",
           "A reader review's pagination is not a verified edition locator. Its quotations support a provisional interpretation but not a detailed franchise or ownership map."),
    source("src-sfe-automation", "Automation", "The Encyclopedia of Science Fiction",
           "https://sf-encyclopedia.com/entry/automation", "secondary_specialist_reference",
           "Indexed opening discussion read", "Bellamy's Looking Backward and Reynolds's modern counterpart in the history of automation utopias.",
           "A genre overview supports relevance, not work-specific numerical coordinates or an inference that their labor systems are identical.")
]

R = []
sleeper = ["src-sleeper-primary"]
R.append(record(
    "sleeper-graham-trustees", "c0049", "When the Sleeper Wakes (The Trustees' corporate order)", "When the Sleeper Wakes", "The inherited corporate order centered on Graham's estate", ["book"],
    scope("Text titled When the Sleeper Wakes, Gutenberg 775", "The mature Trustees' order whose labor institutions persist into the opening power struggle", "Human residents, including Labour Company workers and their children", ["A new settlement after Graham's resistance", "Graham's personal ownership as proof of his effective command", "The later revised novel without an edition comparison"]),
    "Advanced machinery has replaced much heavy effort, while people remain machine attendants, servants and directed workers. The poorest obtain food and shelter through a company that demands labor in exchange. This is a zero variant: mechanization has not made access independent of work for those at the bottom. The weak guarantee point reflects the condition attached to support, rather than denying that the company provides any food at all.\n\nEffective control lies with a small governing and financial circle. Graham's immense nominal ownership does not make the ordinary population owners, and does not initially let even him direct the system freely. The nonworking fraction remains open because workers outside the Company also exist. A reported Company membership share would miss managers, skilled occupations and other activity. The snapshot concerns inherited economic institutions, not an assumed improved society after the struggle over the Council.",
    {"guarantees": 0.65, "control": 0.02, "nonworking": None},
    {"guarantees": assessment(0.65, [0.3, 0.9], "medium", "The fallback trades subsistence for labor and entrenches dependency.", sleeper),
     "control": assessment(0.02, [0, 0.15], "high", "Ownership and practical authority are highly concentrated.", sleeper),
     "nonworking": assessment(None, None, "low", "Company membership omits other working groups.", sleeper)},
    0, sleeper,
    [evidence("Mechanization coexists with work-conditioned subsistence and concentrated authority.", sleeper, "Ostrog's explanation; Helen's Labour Company account; Chapter XXI", "depicted_or_author_stated")],
    ["The novel's hierarchy and its narration contain racial and eugenic assumptions; physical description is not used as an employment statistic.", "The final struggle supplies no verified later economic settlement."], record_type="zero_variant", analogy=[3]))

men = ["src-men-gods-economy", "src-men-gods-primary"]
R.append(record(
    "men-like-gods-utopia", "c0050", "Men Like Gods (Utopia)", "Men Like Gods", "The parallel Utopian Earth", ["book"],
    scope("Original novel", "The established Utopian order encountered by Barnstaple", "Present Utopian human residents, including children", ["Earth visitors as representative residents", "An assumption of equal inclusion in its historical population-selection policies", "Equating the absence of coins with the absence of accounts"]),
    "Utopia uses its command of natural resources as a shared inheritance, including support for children. Adults are still expected to take an occupation and replenish their accounts; the disappearance of small cash payments has not removed the work relationship. That is why this is marked as a zero variant. Material security is strong for present residents, but the point is qualified by the gap between generous social language and the account-based explanation.\n\nAuthority is dispersed among people with relevant knowledge and exposed to criticism, rather than concentrated in a supreme ruler or delegated to an autonomous AI. That supports a high positive control placement without assuming every specialist decision is a referendum. The low nonworking estimate is an editorial judgment from the repeated picture of active occupations and the expectation that adults contribute. It includes room for children and leisure, and counts useful research or creative work even when it is enjoyable.",
    {"guarantees": -0.65, "control": 0.8, "nonworking": 0.25},
    {"guarantees": assessment(-0.65, [-0.9, -0.25], "medium", "Shared inheritance and sufficiency coexist with accounts expected to be replenished through work.", men),
     "control": assessment(0.8, [0.5, 0.95], "medium", "Dispersed specialist authority is subject to criticism, without a supreme sovereign.", ["src-men-gods-economy"]),
     "nonworking": assessment(0.25, [0.05, 0.55], "low", "Coarse minority-nonworking estimate from widespread purposeful occupations; no census is supplied.", men)},
    0, men,
    [evidence("The account explanation and present occupations qualify the moneyless ideal.", men, "A Loiterer in a Living World, sections 4-5; Book I account of active Utopians", "depicted_or_author_stated")],
    ["The work expectation's enforcement and the treatment of a persistent nonworker are not fully specified.", "Historical exclusion is not erased by present comfort.", "The participation estimate is qualitative and includes broad uncertainty."], record_type="zero_variant", analogy=[2]))

old = ["src-shape-council", "src-shape-keying", "src-shape-plenty"]
R.append(record(
    "shape-second-council", "c0051", "The Shape of Things to Come (Second Council)", "The Shape of Things to Come", "The mature Air Dictatorship under the Second Council", ["book"],
    scope("Wells's 1933 prose forecast", "The mature Second Council before its retirement", "Human world population under the Council", ["Earlier collapse and reconstruction emergencies", "The later autonomous cooperation among Controls", "The 1936 film continuity"]),
    "The Second Council has the productive capacity to support the world comfortably, yet makes universal employment and purchasing power an explicit goal. Its rulers respond to rising efficiency with further organized activity and hold back some discoveries. This supports a zero-variant placement: retaining work is part of the governing design, rather than evidence that machinery has failed to become powerful. The material score remains strong because provision has improved greatly.\n\nControl stays close to concentrated human command. The Council's expertise and public purpose do not give ordinary people its overriding authority. This period must also be distinguished from the later world, when the supreme body retires and the functional Controls cooperate directly. No defensible population-wide nonworking fraction is established here. An employment objective is not a census of children, retirees or researchers, and it does not tell us how much useful activity occurs outside formal assignments.",
    {"guarantees": -0.8, "control": 0.03, "nonworking": None},
    {"guarantees": assessment(-0.8, [-0.95, -0.5], "medium", "The mature regime supports the population easily, though disciplines remain extensive.", ["src-shape-keying", "src-shape-plenty"]),
     "control": assessment(0.03, [0, 0.15], "high", "A central human Council retains overriding authority.", ["src-shape-council"]),
     "nonworking": assessment(None, None, "low", "The employment policy supplies neither all-age participation nor a reliable denominator.", ["src-shape-keying"])},
    0, old,
    [evidence("Abundance coexists with an explicit universal-employment policy.", ["src-shape-keying"], "Book V.2, retrospective Second Council discussion", "depicted_or_author_stated")],
    ["This is a mature-regime point, not an average of the novel's entire history.", "No unverified two-year labor-conscription statistic is used."], record_type="zero_variant", analogy=[1]))

late = ["src-shape-megeve", "src-shape-plenty", "src-shape-interest"]
R.append(record(
    "shape-after-megeve", "c0051", "The Shape of Things to Come (After the Declaration of Megeve)", "The Shape of Things to Come", "The world after the supreme Council's retirement", ["book"],
    scope("Wells's 1933 prose forecast", "The post-Council order described by the historian of 2106", "The human world population", ["The Second Council's employment-building phase", "An assertion that money accounts have disappeared", "The 1936 film continuity"]),
    "The later world treats access to food, housing and clothing as ordinary security, sustained by highly efficient production and common service systems. The material point is therefore near strong provision. Personal accumulation has lost much of its former role, though money accounts remain. This is not a claim that every desired item is unlimited or that every transaction has vanished.\n\nControl has changed materially: functional services cooperate without an overriding Council. That moves the point toward distributed human authority, while leaving uncertainty about how much influence a non-specialist has within each service. A small public contribution remains a duty, and creative, scientific and administrative work continues. The record consequently represents release from the struggle to earn basic existence, not universal inactivity. The nonworking fraction stays unresolved: a small essential-production workforce cannot tell us how many others perform useful research or other work. The later order is kept separate from its more centralized predecessor.",
    {"guarantees": -0.9, "control": 0.65, "nonworking": None},
    {"guarantees": assessment(-0.9, [-1, -0.7], "medium", "Ordinary needs and protection from destitution are generalized.", ["src-shape-megeve", "src-shape-plenty"]),
     "control": assessment(0.65, [0.35, 0.9], "medium", "Controls cooperate directly after the supreme Council retires; specialist authority remains.", ["src-shape-megeve"]),
     "nonworking": assessment(None, None, "low", "A remaining civic work duty and extensive knowledge work prevent inferring leisure from essential-production staffing.", ["src-shape-megeve", "src-shape-interest"])},
    2, late,
    [evidence("The declaration ends supreme Council control while retaining limited common duties.", ["src-shape-megeve"], "Book IV.7, declaration and preceding explanation", "depicted_or_author_stated"),
     evidence("General provision is distinct from the amount of useful activity citizens pursue.", ["src-shape-plenty", "src-shape-interest"], "Book V.5 and V.8")],
    ["Membership rights and the surviving account system need further detailed review.", "The six-regime interpretation is provisional where a small civic labor obligation remains.", "Old-world percentages in Book V.8 do not describe the late society."], alternatives=[1]))

modern = ["src-modern-utopia-primary"]
R.append(record(
    "modern-utopia-world-state", "c0052", "A Modern Utopia (The Samurai world state)", "A Modern Utopia", "The parallel Earth's world state", ["book"],
    scope("Original philosophical novel", "The proposed and visited mature world state", "The whole human population, including people assigned restrictions or seclusion", ["Only comfortable Samurai members as the denominator", "Taking a claim of reduced toil as abolition of all employment"]),
    "Machinery reduces toil, yet ordinary people still use earnings to obtain goods. The state guarantees a reserve route to paid work at a decent minimum, alongside insurance and pensions. This is a meaningful fallback, but it is conditional support rather than a general release from employment. Reproductive restrictions on people at the minimum and the treatment of excluded groups also keep the guarantee point well short of an unqualified ideal.\n\nThe Samurai control the state and its much larger wealth. Their order is open to qualified volunteers, which prevents treating it as a hereditary owner, but important authority is still reserved to a selected group. Workers also have bargaining institutions, so the human-control point allows some distribution of influence. The zero-variant label reflects the surviving wage-and-service system despite technological abundance. The nonworking fraction remains open: the existence of pensions and machinery does not supply an age structure or a count of useful voluntary work.",
    {"guarantees": -0.3, "control": 0.2, "nonworking": None},
    {"guarantees": assessment(-0.3, [-0.65, 0.2], "medium", "A right to minimum paid employment and pensions coexists with restrictive conditions.", modern),
     "control": assessment(0.2, [0, 0.5], "medium", "Selected Samurai command state wealth, with open qualification and organized worker bargaining.", modern),
     "nonworking": assessment(None, None, "low", "No defensible population participation estimate follows from the provisions alone.", modern)},
    0, modern,
    [evidence("Labor-saving ambition coexists with wage dependence, public employment and selected rule.", modern, "Chapters III, V, VII and IX", "depicted_or_author_stated")],
    ["The narrator proposes and evaluates a system as well as describing it; evidentiary layers remain explicit.", "Welfare coverage is assessed across the whole population, not only its eligible governing order."], record_type="zero_variant", analogy=[1, 2]))

bellamy = ["src-bellamy-service", "src-bellamy-credit", "src-bellamy-control", "src-bellamy-inventions", "src-equality-preface", "src-sfe-automation"]
R.append(record(
    "bellamy-industrial-commonwealth", "c0053", "Looking Backward (The industrial commonwealth of 2000)", "Looking Backward", "The US industrial commonwealth, illustrated by Boston", ["book"],
    scope("Bellamy's Looking Backward and its elaboration in Equality", "The established order of the year 2000", "Human residents across ages, including disabled people and retired citizens", ["Mack Reynolds's separate rewrite", "Calling the service-age band a measured age distribution", "Excluding useful work after formal retirement"]),
    "The commonwealth distributes equal personal shares and uses labor-saving inventions to make collective provision efficient. It nevertheless requires a period of national service. The zero-variant label captures this retained duty rather than implying unchanged private wages. Guarantees are strong across the life cycle, with a qualification for the compulsory demands made on those expected to serve.\n\nPublic ownership also does not mean direct control by active workers. A command hierarchy organizes production, while retired guild members elect leaders and ordinary industrial workers lack that vote. The control point is therefore between elite administration and broad social ownership. The nonworking estimate uses an explicitly illustrative age scenario, not a canonical census: the service-age band supplies an anchor, while assumptions about lifespan and activity outside formal service supply the rest. Retirement does not make research or public office nonwork. Equality expands this same society and receives no additional count merely for being a second book.",
    {"guarantees": -0.75, "control": 0.35, "nonworking": 0.6},
    {"guarantees": assessment(-0.75, [-0.95, -0.45], "medium", "Equal shares and life-cycle support are strong, though service is obligatory.", ["src-bellamy-credit", "src-bellamy-service"]),
     "control": assessment(0.35, [0.1, 0.65], "medium", "National ownership coexists with a hierarchy and restricted industrial suffrage.", ["src-bellamy-control"]),
     "nonworking": assessment(0.6, [0.3, 0.8], "low", "Illustrative demographic estimate anchored in the 24-year service rule, with an allowance for productive activity outside it.", ["src-bellamy-service", "src-bellamy-control"])},
    0, bellamy,
    [evidence("Equal provision, obligatory service and limited worker voting coexist.", ["src-bellamy-service", "src-bellamy-credit", "src-bellamy-control"], "Chapters 6, 9 and 17", "depicted_or_author_stated"),
     evidence("Labor-saving technology supports relevance to the automation question.", ["src-bellamy-inventions", "src-sfe-automation"], "Household/invention discussion; SFE opening")],
    ["The participation point is a scenario estimate; its demographic assumptions are not Bellamy's statistics.", "The service band alone would undercount work in liberal professions and after retirement.", "Women's service arrangements and actual age distribution require a fuller final pass."], record_type="zero_variant", analogy=[1, 2]))
R[-1]["axis_assessment"]["nonworking"]["estimate_model"] = {
    "method": "Illustrative stationary-age scenario, not a reconstructed census",
    "canonical_anchor": "Ordinary formal service lasts 24 years, from age 21 to age 45",
    "noncanonical_assumptions": {"illustrative_lifespan_years": 80, "additional_productive_participation_outside_service": 0.1},
    "calculation": "1 - 24 / 80 - 0.10 = 0.60",
    "limitations": "Actual population shape, professional exceptions, women's service and useful activity outside formal service are unknown; the wide interval is editorial."
}

reynolds = ["src-reynolds-author-recap", "src-reynolds-looking-publisher", "src-reynolds-looking-review", "src-sfe-automation"]
R.append(record(
    "reynolds-looking-backward", "c0055", "Looking Backward from the Year 2000 (Reynolds's future America)", "Looking Backward from the Year 2000", "Mack Reynolds's automated future America", ["book"],
    scope("Reynolds's Julian West novels, distinct from Bellamy", "The future order encountered in the first novel, as recapped by the author", "The country's human population, not an assumed uniform world population", ["Bellamy's compulsory industrial army", "Later sequel reforms not established in the first novel", "Equating GAI receipt with no useful activity"]),
    "Reynolds's future has a small productive core and broad guaranteed income, making the automation link explicit. It is materially different from Bellamy's compulsory industrial army even though the two stories share names and a sleeper premise. Provision therefore sits near the strong end. The author's retrospective figures are retained separately from the coordinate, because receiving income does not by itself reveal every useful activity a person performs.\n\nThe provisional positive control point reflects the described mixture of collective and syndicalist arrangements, qualified by technocratic and meritocratic elements. Its broad interval acknowledges that the consulted evidence does not map the constitution in detail. Computers alone are not proof of independent AI sovereignty. The high nonworking estimate follows the small essential workforce, with an allowance for voluntary production and creative work. It remains a low-confidence editorial interpretation, not a declaration that all income recipients are idle or that the society has solved every problem.",
    {"guarantees": -0.9, "control": 0.55, "nonworking": 0.95},
    {"guarantees": assessment(-0.9, [-1, -0.7], "medium", "The author explicitly describes generalized GAI under automation.", ["src-reynolds-author-recap"]),
     "control": assessment(0.55, [0.05, 0.9], "low", "Collective and syndicalist elements coexist with expertise-based authority; the institutional map is incomplete.", ["src-reynolds-looking-review"]),
     "nonworking": assessment(0.95, [0.75, 0.99], "low", "Estimate anchored in the reported small productive core, reduced to allow useful voluntary activity among income recipients.", ["src-reynolds-author-recap"])},
    2, reynolds,
    [evidence("The author's recap establishes automation and GAI; it does not quantify all voluntary activity.", ["src-reynolds-author-recap"], "Equality: In the Year 2000, Introduction", "depicted_or_author_stated"),
     evidence("The quoted political self-description combines several arrangements.", ["src-reynolds-looking-review"], "Review quotation attributed to first-novel page 168")],
    ["Review the first novel's primary government and ownership passages before treating the control point as settled.", "The exact calendar year is not inferred from the title or rounded publisher synopsis.", "An official edition identity and an author recap do not constitute a complete reread."], alternatives=[1]))
R[-1]["reported_labor_statistics"] = [
    {"value": 0.02, "measure": "Population needed to produce the country's consumption", "denominator": "The country's population in the author's recap", "source_id": "src-reynolds-author-recap", "locator": "Introduction, recap of Looking Backward"},
    {"value": 0.98, "measure": "Population on Guaranteed Annual Income", "denominator": "The country's population in the author's recap", "source_id": "src-reynolds-author-recap", "locator": "Same recap paragraph; not treated as a literal nonworking fraction"}
]

D = [
    decision("c0049", "zero_variant", "Mechanized production coexists with labor-conditioned subsistence under concentrated corporate authority.", sleeper, society_id="sleeper-graham-trustees"),
    decision("c0050", "zero_variant", "The direct account explanation retains an occupation-and-earnings relationship despite advanced collective provision.", men, society_id="men-like-gods-utopia"),
    decision("c0051", "included", "Primary chapters establish a material change from the Second Council to the post-Megeve order.", old + [sid for sid in late if sid not in old],
             society_id="shape-second-council", society_ids=["shape-second-council", "shape-after-megeve"],
             split_rationale="The earlier Council explicitly pursues universal employment and retains supreme authority. The later declaration retires it, establishes direct cooperation among functional Controls, and describes generalized freedom from the subsistence struggle while retaining a small civic duty. These are separate realized periods, not two names for one snapshot.",
             follow_up="Review the 1936 film separately before adding its media tag or a distinct film record; verify membership/account details and participation in the late prose order."),
    decision("c0052", "zero_variant", "Reduced toil coexists with wages, reserve public employment and selected Samurai authority.", modern, society_id="modern-utopia-world-state"),
    decision("c0053", "zero_variant", "National service remains obligatory despite equal shares and labor-saving technology.", bellamy, society_id="bellamy-industrial-commonwealth"),
    decision("c0054", "duplicate", "Bellamy explicitly keeps the date and framework of Looking Backward and elaborates the same commonwealth.", ["src-equality-preface", "src-bellamy-credit"],
             "The preface and recap identify the same social arrangement rather than a newly realized post-2000 regime. A new title alone would double-count its population and mechanism.",
             "Reopen only if later primary passages establish materially changed guarantees, control or work rules; keep Reynolds's similarly titled sequel separate.", duplicate_of="bellamy-industrial-commonwealth"),
    decision("c0055", "included", "The author's own recap establishes automation, a small productive core and broad guaranteed income in a separate rewrite.", reynolds, society_id="reynolds-looking-backward")
]

write_batch(7, [f"c{i:04}" for i in range(49, 56)], S, R, D, [
    "Previous goal turn was progress: batches 005-006 and their source-backed records changed authoritative state. This batch continues the queue without gaps.",
    "Seven candidates yield seven new records because c0051 has two evidenced periods while c0054 is a duplicate. The discovery queue and IDs remain unchanged.",
    "The validator now supports one-to-many retained decisions and requires a split rationale, matching candidate identities, distinct scopes and valid duplicate targets.",
    "Bellamy's participation point is a disclosed illustrative model, not a fabricated census. Reynolds's reported GAI share is preserved separately from the editorial participation point.",
    "No two-year conscription claim from secondary summaries was verified in the sampled Wells passages, so it was not imported. The small civic-duty statement was read directly instead.",
    "Second pass checked moneyless transactions against account replenishment, public title against actual control, material provision against service conditions and old-world percentages against the correct period.",
    "Numeric readiness remains distinct from final evidentiary completeness. No full reread or independent review is claimed. Images and all application work remain deferred."
])
