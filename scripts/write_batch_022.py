from research_helpers import source, decision, write_batch

S = [
    source("src-veldt-primary", "The Veldt", "Ray Bradbury; Northern Virginia Community College ENG 236 teaching text",
           "https://pressbooks.nvcc.edu/eng236/chapter/the-veldt/", "primary_fiction_educational_transcription",
           "Public English HTML opened; house purchase/provision, family dependence, psychologist's advice and ending read",
           "Purchased Happylife Home displaces domestic tasks; Lydia's loss of purpose; George's switches, children's resistance and final trap.",
           "The teaching transcription has visible typographical defects. Domestic task replacement does not establish where food stocks, utilities or purchasing income come from. No general public material rights are inferred from one family's house."),
    source("src-soft-rains-primary", "There Will Come Soft Rains", "Ray Bradbury; English teaching transcription at shortsonline/XpressEnglish",
           "https://xpressenglish.com/our-stories/soft-rains/", "primary_fiction_educational_transcription",
           "Public HTML read from the opening routine through the final surviving wall",
           "Automatic cooking and cleaning, work and school reminders, payable insurance/utilities, the destroyed human family and eventual failure of water and fire defenses.",
           "The consulted version dates the day to August 2026; other editions vary. Its operating house is a post-destruction remnant, while the queued candidate specifically concerns the earlier living city. The old family's bills and reminders are evidence about that earlier period, not a full economic census."),
    source("src-pedestrian-primary", "The Pedestrian", "Ray Bradbury; English teaching transcription at Longfield Learning, NSW education Google Sites",
           "https://sites.google.com/education.nsw.gov.au/longfieldlearning/english-texts/short-story-prose-fiction/the-pedestrian", "primary_fiction_educational_transcription",
           "Public HTML opened; evening/daytime contrast, occupational interrogation and complete arrest/ending sequence read",
           "Crowded daytime highways, nighttime television viewing, the reduced police fleet, Mead's unsaleable writing and the empty automatic police car.",
           "The teaching text contains typos and a 2052/2053 setting; exact dates differ across editions. Crime reduction and automatic enforcement do not establish automatic general production, universal income or an all-day absence of work."),
    source("src-martian-settlers-primary", "The Martian Chronicles: The Settlers and adjacent passages", "Ray Bradbury; unofficial English transcription on ThePhilosopher",
           "https://thephilosopher.net/bredberi/tvorchestvo/the-martian-chronicles/pagen/16/", "primary_fiction_unofficial_transcription",
           "Public HTML opened; The Settlers and the opening of The Green Morning read",
           "Government work recruitment, varied settler motives and Driscoll's continuing physical tree-planting labor.",
           "Only these sections and adjacent context were read, not the complete collection. Dates and story selection vary by edition. Early frontier employment does not resolve the institutions of every later settlement."),
    source("src-martian-chronicles-reference", "The Martian Chronicles", "Encyclopedia.com literary reference entry",
           "https://www.encyclopedia.com/arts/culture-magazines/martian-chronicles", "literary_reference",
           "Public indexed discussion of automated-house episodes read",
           "There Will Come Soft Rains places the automatic house in the collection, and discusses its resource failure rather than a self-sustaining welfare system.",
           "Indexed secondary access only; the full entry was not read. Its Earth house cannot be silently moved to Mars or used to characterize all human colonies."),
    source("src-fahrenheit-primary-text", "Fahrenheit 451", "Ray Bradbury; unofficial English PDF transcription hosted by Westminster International University in Tashkent's learning resource center",
           "https://lrc.wiut.uz/Content/Uploads/Ckeditor/8a2e0514-2d96-4592-80e6-e888320e26c3Ray-Bradbury-Fahrenheit-451.pdf", "primary_fiction_unofficial_pdf_transcription",
           "Public 77-page PDF normally fetched in memory; selected text extracted; three complete pages rendered and visually read",
           "Wall-screen cost versus Montag's annual pay; Beatty's account of job-centered life and after-work entertainment; robot bank tellers, unemployed intellectuals and continued human mobilization.",
           "One-based PDF pages 9, 27 and 43 were visually checked. This is a reflowed transcription with errors, not a verified facsimile; the whole novel and its film adaptations were not read/viewed. Robot banking is not general automatic production."),
    source("src-fahrenheit-publisher", "Fahrenheit 451: official publisher page and reading guide", "Simon & Schuster",
           "https://www.simonandschuster.com/books/Fahrenheit-451/Ray-Bradbury/9781451673319", "official_publisher_synopsis_and_guide",
           "Public synopsis and relevant reading-guide discussion opened and read",
           "Montag's occupation, Mildred's television-centered life and the novel's censorship conflict.",
           "Synopsis/guide, not a primary economic constitution. No film-specific allocation or labor rules were established from this page, and its retail price is not a fictional-world price.")
]

D = [
    decision("c0118", "boundary_case", "Domestic task replacement is explicit, but the purchased house is not a verified work-independent material economy.", ["src-veldt-primary"],
             "The house cooks, dresses, cleans and performs care, and the parents explicitly feel unnecessary (web lines 163-166 and 227-259). This matters as domestic automation, but the story does not establish how the household acquires food stocks, energy, repairs or purchasing income. A substantial purchase and a professional psychologist coexist with the family's leisure. The children oppose deactivation and trap the parents; this does not by itself establish autonomous AI ownership of a whole economy. Restoring some household tasks is a personal therapeutic proposal, not a demonstrated society-wide preservation of employment.",
             "Keep as a domestic-automation comparison. Reopen for a specifically verified material-access system, rather than converting one comfortable home into universal guarantees or a zero variant."),
    decision("c0119", "needs_evidence", "The queued living Allendale economy is not recoverable from its automatic house's surviving routines alone.", ["src-soft-rains-primary"],
             "The complete consulted story makes cooking and cleaning automatic, but its old routines also demand payment of insurance and utility bills and tell residents to leave for work (web lines 27-38). Those traces complicate an effortless prewar society without proving a deliberate policy of preserving replaceable employment. During the narrated day the human residents are dead, and the house eventually exhausts water and burns. Neither their absence nor remaining mechanical activity supplies a living human nonworking fraction or a current AI-governed welfare society.",
             "Seek evidence of the pre-destruction city's broader production and access rules; retain the queued before-destruction scope. Do not classify the dead family or an empty house as 100% leisure, and do not move this California setting to Mars."),
    decision("c0120", "boundary_case", "Automatic policing and evening television do not establish a post-work material order.", ["src-pedestrian-primary"],
             "Mead's writer occupation has lost its market, and an unoccupied police car arrests him. Yet the text contrasts empty nighttime roads with heavy daytime traffic and open gas stations (web lines 33-34). The fleet reduction follows falling crime, not an explicit all-sector labor replacement. Air conditioning and viewing screens say little about wages, necessities or control of production. The episode establishes oppressive automated enforcement; that political mechanism is not enough to place the whole economy under autonomous AI.",
             "Preserve as an automated-surveillance and consumption comparison. Reopen only for material-economy evidence; do not infer a nonworking rate from evening viewing, professional displacement or the number of police cars."),
    decision("c0121", "needs_evidence", "The collection's different worlds and periods cannot yet be retained as one automated human settlement economy.", ["src-martian-settlers-primary", "src-martian-chronicles-reference", "src-soft-rains-primary"],
             "The Settlers explicitly recruits people to work on Mars; the following section shows Driscoll's physical cultivation (primary web lines 672-690). That does not exclude every later supported enclave, but it prevents treating all colonization as a single leisure regime. The much-cited automated house in There Will Come Soft Rains is in Allendale, California, and cannot verify Mars's human household rights. A collection or franchise is not one uniform material constitution.",
             "Identify exact Martian communities and periods with automatic material provision, then check ownership, access and distinctness individually. Read later relevant primary episodes before adding points; do not borrow Earth's house or infer welfare from private robotic entertainment."),
    decision("c0122", "needs_evidence", "The novel depicts wage-funded consumption and some automated services, but general labor replacement or deliberate zero-variant preservation remains unverified.", ["src-fahrenheit-primary-text", "src-fahrenheit-publisher"],
             "The visually checked primary page ties another wall-screen to one-third of Montag's yearly pay and current sacrifices for the previous screen (PDF page 9). Beatty's account still centers jobs and pleasure after work (page 27), while a later passage explicitly has robot bank tellers (page 43). Thus automation is real, but banking, censorship tools and entertainment do not establish automatic production sufficient to replace society's employment. The book's political repression alone is not the zero-variant criterion. Its film versions have not been checked for equivalent material rules.",
             "Find primary evidence for production, ordinary necessities access and any deliberate preservation of technologically replaceable jobs. Analyze each film continuity separately if its arrangements differ; do not inherit economic coordinates from the discovery media tags.")
]

write_batch(22, [f"c{i:04}" for i in range(118, 123)], S, [], D, [
    "Read material-access implications separately from domestic convenience, censorship and automatic policing. No whole-society welfare was inferred from a well-equipped private house.",
    "Allendale's earlier living period is kept distinct from the empty post-destruction house; the Earth's episode is not evidence of Mars-wide provision.",
    "Three complete Fahrenheit PDF pages were visually compared with extraction. Beatty's account is character speech, and no evidence of a deliberate full-automation rollback was established.",
    "Same-researcher second pass only. Five more consecutive dispositions are durable; goal remains active and no unsupported record was added."
])
