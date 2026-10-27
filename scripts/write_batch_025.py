from research_helpers import source, assessment, record, scope, evidence, decision, write_batch

S = [
    source("src-little-black-bag-primary", "The Little Black Bag", "C. M. Kornbluth; Project Gutenberg Canada transcription",
           "https://gutenberg.ca/ebooks/kornbluth-littleblack/kornbluth-littleblack-00-h.html", "primary_fiction_transcription",
           "Public HTML opening and selected ending passages read through the web reader",
           "Future social hierarchy, medical practice, Mike's actual role and the circuit-builder; selected medical-bag ending context.",
           "Targeted reading, not the complete story. The hereditary hierarchy is a fictional premise, not accepted science. Similar motifs do not establish continuity with The Marching Morons."),
    source("src-skills-xanadu-primary", "The Skills of Xanadu", "Theodore Sturgeon; unofficial Binwiped transcription, 2004 PDF conversion",
           "https://fennetic.net/irc/Theodore_Sturgeon_-_The_Skills_of_Xanadu.pdf", "primary_fiction_unofficial_pdf_transcription",
           "Public 13-page PDF normally fetched; selected text read and four complete pages rendered and visually checked",
           "Shared skills, houses and public decisions; material production, alternation between tasks, and the belt's effect on Kit Carson. One-based PDF pages 9, 10, 12 and 13 visually checked.",
           "Reflowed unofficial transcription with conversion headers, not the original magazine. The whole story was not read. An indexed alternative returned reader errors and was not treated as a completed read."),
    source("src-venus-plus-x-primary-es", "Venus más X / Venus Plus X", "Theodore Sturgeon; Domingo Santos translation, Orbis 1985 edition transcription",
           "https://maestrosdelsaber.com/wp-content/uploads/ftp-files/Novela%2C%20Cuentos%20y%20Teatro/Nov%20Ciencia%20Ficcion%20y%20Fantas%C3%ADa/Sturgeon%20Theodore/Nov%20Sturgeon%2C%20Theodore%20-%20Venus%20m%C3%A1s%20X.pdf", "primary_fiction_translation_unofficial_pdf",
           "Public 118-page PDF normally fetched into memory; selected technological and ending passages read; six complete pages visually checked",
           "A-field explanation and material abundance, preserved practical knowledge, founding history, and the identity/research revelations. Visually checked one-based PDF pages 55, 56, 59 and 113-115; ending text also read on pages 112 and 116-117.",
           "Spanish translation in an unofficial reflow, not compared with the English edition or original printing. Targeted reading, not a whole-novel read. The visitor's assumptions about future chronology and a time machine are overturned within the novel. No source novel was saved or delivered."),
    source("src-venus-plus-x-publisher", "Venus Plus X", "Penguin Random House / Vintage",
           "https://www.penguinrandomhouse.com/books/175023/venus-plus-x-by-theodore-sturgeon/", "official_publisher_description",
           "Public publisher description and bibliographic details read",
           "English title, author, novel format and the premise of technological relief from hunger in Ledom.",
           "The spoiler-light future-world and transport framing is not used to override the primary ending. Marketing praise does not establish ownership or a participation percentage."),
    source("src-dispossessed-primary", "The Dispossessed: An Ambiguous Utopia", "Ursula K. Le Guin; public 404-page PDF text",
           "https://files.libcom.org/files/Le%20Guin%20-%20The%20Dispossessed.pdf", "primary_fiction_pdf_cached_text",
           "Ordinary direct fetch returned 403 and was respected; a later normal web-reader open exposed the cached text, from which selected passages were read",
           "PDF pages labelled 147-149 in the reader: depositories, rotating work, voluntary postings and social sanctions; page 260: Divlab's human/computer matching and famine-prevention staffing; page 86: the separate Urrasti steel mill.",
           "Targeted web text reading only, not a whole-novel or visually verified PDF read. Screenshot requests returned cache misses. An independently indexed primary mirror corroborated the Divlab passage; no blocked download was bypassed. The Urrasti factory is not Anarresti evidence."),
    source("src-dispossessed-author", "The Dispossessed", "Ursula K. Le Guin official website",
           "https://www.ursulakleguin.com/dispossessed", "official_author_synopsis_and_bibliography",
           "Public official synopsis and publication context read",
           "Anarres/Urras distinction, Shevek and the 1974 novel.",
           "The utopian-anarchist synopsis alone does not establish automation or eliminate necessary labor."),
    source("src-telling-primary-indexed", "The Telling", "Ursula K. Le Guin; unofficial primary transcription indexed at Zanotowane",
           "https://www.zanotowane.pl/1064/4565/", "primary_fiction_indexed_excerpt",
           "Public search-index passages read; no complete direct text read claimed",
           "Sutty's ZIL checks, food purchase, human food-counter worker and ferry crew; the distinction between urban Corporation checks and the rural inn.",
           "Indexed excerpts only. Automatic identity checking and robocabs do not establish automatic food production. Sutty is an honored visitor, not evidence of universal resident entitlements."),
    source("src-telling-author", "The Telling", "Ursula K. Le Guin official website",
           "https://www.ursulakleguin.com/the-telling", "official_author_synopsis_and_bibliography",
           "Public official synopsis, original publication and scope notes read",
           "Aka's Corporation, imported technology, required producer-consumer identity and suppressed local culture; 2000 novel.",
           "The synopsis does not say all human labor could already be replaced. Its authoritarian state must not be mistaken for an AI government or the entire Ekumen.")
]

v = ["src-venus-plus-x-primary-es"]
R = [
    record("venus-plus-x-ledom", "c0135", "Venus Plus X (Ledom)", "Venus Plus X", "The existing A-field-supported Ledom enclave", ["book"],
           scope("Sturgeon's novel; Spanish translation consulted", "The established enclave during the Charlie-persona visit, before and at the final protective closure", "Living Ledom residents of all ages, biologically modified human descendants treated as persons", ["All Homo sapiens outside the enclave", "A real time-travel journey inferred by Charlie", "Quesbu's research confinement treated as a separate society", "An already completed future reconstruction of humanity"], proxy=True, proxy_basis="The living human-derived Ledom population is an explicit person proxy; no machine, stored recording or repeated persona is counted as an extra resident."),
           "Ledom's A-field moves material, processes food, makes fabric and forms buildings and everyday objects. Together with the cerebrostyle it removes the ordinary energy and instruction bottlenecks. The explanation explicitly says that food, housing and clothing are no longer scarce and that people are free for other activities. There is no wage-payment vocabulary in the language being used. These are concrete material arrangements, supporting strong provision for the resident enclave. Teaching, research, care and creative activity still matter, so freedom from subsistence work supplies no reliable nonworking percentage.\n\nThe technology is directed by people, without evidence of an autonomous AI sovereign. Personal use and widely available knowledge favor dispersed control, but specialists retain substantial power. The ending exposes secret medical confinement and manipulation of Quesbu's identity, with some leaders themselves uninformed. The control estimate therefore remains broad and provisional. Ledom is a community of living human descendants, not a city of robots. Charlie's assumed time machine is also disproved; neither the outside world nor a promised later restoration of humanity inherits this enclave's guarantees.",
           {"guarantees": -0.8, "control": 0.4, "nonworking": None},
           {"guarantees": assessment(-0.8, [-0.95, -0.55], "medium", "The primary explanation directly removes scarcity of food, housing and clothing for Ledom residents. This is an observed provision system rather than a specified constitutional entitlement; bounded membership and secret medical power qualify the estimate.", v),
            "control": assessment(0.4, [0, 0.85], "low", "People program and operate the A-field; usable knowledge is shared, while Seace and medical leaders possess exceptional infrastructural and personal power. The record uses a broad mixed-human-control estimate, not proven equal ownership or AI sovereignty.", v),
            "nonworking": assessment(None, None, "low", "The text frees residents for other activities but shows education, science and care. Neither no wages nor very low necessary energy measures all-age useful participation; no census or defensible demographic rate was established.", v)},
           2, v + ["src-venus-plus-x-publisher"],
           [evidence("Programmable A-fields perform construction, material handling, food processing and fabric production; residents lack ordinary material scarcity.", v, "Spanish PDF pages 55-56 and 59, Seace's technological explanation", "depicted_or_author_stated"),
            evidence("The final explanation overturns time travel and reveals Quesbu's confinement and the hidden manipulation of identity by human medical specialists.", v, "Spanish PDF pages 112-116, Mielwis and Seace's revelations", "depicted_or_author_stated")],
           ["The control score is provisional; concentrated specialist control is a serious alternative to the dispersed-use interpretation.", "The exact English terminology and the complete novel require a further pass against an English edition.", "Biological alteration and the novel's sexual politics do not themselves establish economic guarantees or erase personhood.", "A recorded Charlie persona is not an additional biological leisure citizen, and useful chosen work still counts."], alternatives=[1])
]

D = [
    decision("c0133", "needs_evidence", "Automatic medical tools and socially wasteful pseudo-research do not establish the future population's general material economy.", ["src-little-black-bag-primary"],
             "The future doctor still performs useful treatment with protected instruments, while a highly capable human minority supplies development and supervision. Mike's role supports a make-work lead, but there is no verified general food, housing or income system. The present-day bag's effects cannot supply missing future institutions.",
             "Find a concrete population-wide production/access passage before admission or zero-variant classification; keep this future separate from The Marching Morons unless continuity is established."),
    decision("c0134", "boundary_case", "The network distributes skills and coordination, while the depicted necessities are still made by human participants.", ["src-skills-xanadu-primary"],
             "Residents alternate work, play and rest; they gather materials, operate vats and presses, build houses and take over one another's useful tasks. Belts transmit skill rather than performing the work independently. A sharing economy with powerful tools is not sufficient proof that automation removes labor as the basis of material support. Kit Carson's ending transformation is not a second verified post-work economy.",
             "Retain as a comparison for distributed capability and access. Reopen if labor-independent basic provision is explicitly established; do not equate enjoyable activity or shared expertise with nonwork."),
    decision("c0135", "included", "The existing enclave has explicit programmable material production and non-scarce necessities, with qualified human control and an unresolved participation rate.", v + ["src-venus-plus-x-publisher"], society_id="venus-plus-x-ledom"),
    decision("c0136", "boundary_case", "Anarres shares resources without wages, but the read primary scenes depend on real human production and famine-prevention labor.", ["src-dispossessed-primary", "src-dispossessed-author"],
             "Shevek describes rotating unpleasant work, voluntary postings and powerful social pressure. Divlab is a human/computer job-matching network. The visited automated steel mill belongs to Urras, not Anarres. Neither moneylessness nor advanced physics verifies an available general labor replacement deliberately withheld on Anarres.",
             "Keep as a labor-based anarchist comparison. Reopen on a concrete automatic provision passage; do not label it a zero variant merely because other worlds have more machinery."),
    decision("c0137", "needs_evidence", "Aka's required producer-consumer role and automated identity gates do not establish general labor replacement.", ["src-telling-author", "src-telling-primary-indexed"],
             "The official synopsis verifies coercive modernization. Indexed primary scenes show paid food, human service and transport workers, and uneven identity enforcement between city and countryside. Robocabs and ZIL checks establish sectoral automation, not a fully automatic material economy or sovereign AI control.",
             "Find actual food/manufacturing and resident access rules before admission. A zero variant requires evidence that necessary employment is deliberately preserved despite existing replacement capacity; do not infer that from the producer-consumer slogan alone.")
]

write_batch(25, [f"c{i:04}" for i in range(133, 138)], S, R, D, [
    "Ledom is retained on direct technological and household-provision evidence, not on a utopia label or assumptions about gender. Useful creative/care work prevents an invented participation rate.",
    "The primary ending corrects the visitor's time-machine assumption and exposes human specialist control. Quesbu's recording is not counted as a second person or separate society.",
    "Xanadu's distributed useful work and Anarres's coordinated necessary labor remain comparisons. A pleasant, moneyless or egalitarian economy does not automatically meet the automation admission criterion.",
    "Source reads are targeted; no complete novel or original magazine comparison is claimed. Translation, cached-text and indexed-only limits remain explicit. No blocked fetch was bypassed.",
    "Second pass checked descriptions against the recorded passages and challenged automatic admission of all five discovery leads. This is not an independent review."
])
