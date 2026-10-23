from research_helpers import source, assessment, record, scope, evidence, decision, write_batch

S = [
    source("src-sirens-titan-primary", "The Sirens of Titan", "Kurt Vonnegut; unofficial English transcription on Manuals.plus",
           "https://manuals.plus/m/741a32b64293cf3c83240ce86217f398960f4c5dc2feb881548bb968b480a791", "primary_fiction_unofficial_transcription",
           "Public HTML opened; late Titan account and Tralfamadorian origin legend read",
           "Salo as a machine among machine Tralfamadorians; their manufacture of each other; the explicitly labeled legend of organic creators delegating purposes and then their destruction.",
           "Targeted reading, not the whole novel. The origin account is a legend within the fiction, not a directly depicted constitution. Different Vonnegut books' Tralfamadores are not silently combined."),
    source("src-silver-eggheads-sfe", "Arts: The Silver Eggheads", "The Encyclopedia of Science Fiction contributors",
           "https://sf-encyclopedia.com/entry/arts", "literary_reference",
           "Public entry opened and indexed Leiber paragraph read",
           "Wordmills produce human commercial fiction; robot authors write authored fiction for robots; original shorter work and expanded novel are distinguished.",
           "Secondary summary of the literary sector, not evidence that all necessities are produced automatically or universally available."),
    source("src-silver-eggheads-opening-index", "The Silver Eggheads: opening quotation and edition blurb", "Fritz Leiber, quoted by the independent Trash Fiction site",
           "https://trashfiction.co.uk/silver_eggheads.html", "primary_excerpt_with_secondary_commentary",
           "Public indexed quotation and quoted book blurb read; direct web opening failed",
           "Gaspard's wordmill tending and publisher-assigned public persona; the robot Zane Gort described as a self-employed writer for robots.",
           "Only the indexed opening quotation/blurb was consulted, not the complete review or novel. Another public text mirror returned 403 and was not bypassed. No inference about society-wide provisioning is taken from its search presence."),
    source("src-wanderer-primary", "The Wanderer: Russian translation", "Fritz Leiber; public Lib.Ru transcription",
           "https://www.lib.ru/INOFANT/LEJBER/wanderer.txt", "primary_fiction_translation",
           "Public text opened; ordinary HTTPS decoded with its declared charset; selected guest-accommodation and chapter 36 passages read",
           "Artificial inhabited planet, comfortable guest accommodation, Tigerishka's account of the wider civilization's democratic but restrictive elders, and the Wanderer's dissident aims.",
           "Translation provenance was not independently checked. Guest comfort and planet-building are not universal household rights. The fugitives' aspirations and wider civilization are different scopes; thought-to-object devices are still a stated ambition."),
    source("src-green-millennium-primary", "The Green Millennium", "Fritz Leiber; Project Gutenberg transcription of the Ace edition",
           "https://www.gutenberg.org/cache/epub/65482/pg65482-images.html", "primary_fiction_transcription",
           "Public HTML opened; opening employment/housing, Fun Incorporated sales robots and full ending sequence read",
           "Phil's repeated job displacement, small rented living space, commercial robot sales and cash collection, and the green-cat resolution.",
           "Targeted passages, not a whole-novel read. No generalized material entitlement or society-wide unemployment rate was established. The ending's emotional harmony is not itself automated food or housing provision."),
    source("src-grammatizator-primary", "The Great Automatic Grammatizator", "Roald Dahl; unofficial English document transcription hosted by Gumer",
           "https://detective.gumer.info/txt/dal_2.pdf", "primary_fiction_unofficial_pdf_transcription",
           "Public 11-page PDF opened; final three complete PDF pages rendered and visually read, with text-layer comparison",
           "Human operation of the novel machine; lifetime paid nonwriting contracts and name licensing; about seventy percent of the selected list signing; half of English-language fiction production; excluded narrator's hungry children.",
           "Reflowed document transcription, not a verified original-edition facsimile; spellings/OCR vary. Visual pages are one-based PDF pages 9-11. The whole story was not read from this PDF. No full novel/story file was retained or delivered."),
    source("src-grammatizator-education-text", "The great automatic grammatizator", "Roald Dahl; English teaching transcription on Lengish",
           "https://lengish.com/texts/text-89.html", "primary_fiction_educational_transcription",
           "Public HTML opened; construction and business-plan sections read, with the indexed ending compared against the longer PDF",
           "Commercially directed automatic story generation and the agency's human owners; corroborating lifetime-contract premise.",
           "This educational version omits or compresses passages found in the longer PDF, including details of manual novel controls. It is not called an unabridged original. The PDF supplies the controlling final-contract evidence.")
]
g = ["src-grammatizator-primary", "src-grammatizator-education-text"]
R = [
    record("grammatizator-contracted-authors", "c0117", "The Great Automatic Grammatizator (The contracted authors)", "The Great Automatic Grammatizator", "Authors receiving lifetime payments from Knipe's agency in exchange for ceasing to write", ["short_story"],
           scope("Dahl's original short-story setting", "After the machine's first full commercial year and the initial contract campaign", "Only the human authors who have signed the paid lifetime nonwriting contracts", ["The entire contemporary country", "All English-language writers", "Unsigned authors and their dependents", "Agency operators automatically counted as nonworkers"], unit_type="contract-defined economic cohort"),
           "Knipe's agency offers writers a continuing income for life in return for stopping their own writing and lending their names to machine-made books. Many actually sign. Within this small contractual group, automation has therefore replaced the work that previously earned the income. The guarantee estimate is moderately favorable and uncertain: a company promises payment, but the amount, purchasing power and protection against default are unspecified. The starving narrator's family remains outside this arrangement.\n\nKnipe and Bohlen control the productive machine, admission and payments. The authors surrender part of their independence without receiving shared control, so the control estimate stays near concentrated human ownership. Machine operation, marketing and management still require people; this is not sovereign AI. Nor does the contract prove that its recipients perform no other useful activity. The reported signing rate concerns a selected list of writers, and the machine's publication share concerns output. Neither measures the nonworking population.",
           {"guarantees": -0.3, "control": 0.05, "nonworking": None},
           {"guarantees": assessment(-0.3, [-0.65, 0.25], "low", "Actual signatories obtain a contractual annual payment for life, independent of further writing. Amount, necessities coverage, enforcement and default protection remain unspecified; this is neither a universal entitlement nor assured comprehensive care.", g),
            "control": assessment(0.05, [0, 0.15], "high", "The two human business organizers retain access to the machine and direct the agency; signatories license their names and relinquish writing without acquiring collective production control.", g),
            "nonworking": assessment(None, None, "low", "A nonwriting obligation is not a prohibition of every useful activity. Seventy percent applies only to the solicited list, and half applies to published fiction output; neither supplies an all-person participation census.", g)},
           1, g, [evidence("The business buys out authors with annual lifetime payments, forbids further writing and uses their names for machine production; many contracts are signed.", ["src-grammatizator-primary"], "One-based PDF pages 10-11", "depicted_or_author_stated"),
                  evidence("The novel machine still needs a practiced human operator using controls and pedals.", ["src-grammatizator-primary"], "One-based PDF page 9", "depicted_or_author_stated")],
           ["A deliberately narrow contractual cohort, not a claim that the whole surrounding country is post-work.", "Material coverage and corporate payment reliability are unresolved; the guarantee interval crosses into weak support.", "Voluntary useful activity counts as work. Signed contracts do not establish total idleness.", "The machine's human operators and displaced unsigned writers are different economic positions, not hidden inside this cohort."], alternatives=[3])
]
D = [
    decision("c0113", "boundary_case", "The current Tralfamadorian population consists of machines; its creators' fate is an internal origin legend.", ["src-sirens-titan-primary"],
             "The late Titan chapter explicitly identifies Salo and his fellows as machines which manufacture each other (web lines 1501-1510). The organic population's delegation of ever-higher purposes ends in extermination in the legend. The machine civilization has no established resident human denominator, and the legend supplies no dependable access or control constitution for a living biological society. Salo also undertakes an assigned mission and makes art; machine identity is not automatic idleness.",
             "Preserve as an autonomous-machine and purpose comparison. Reopen the pre-extinction legendary period only as a separately labeled proxy if its production/access structure can be substantiated; never score extermination as human leisure or import Slaughterhouse-Five's aliens."),
    decision("c0114", "needs_evidence", "Automatic commercial fiction is verified; society-wide material provision or a deliberate zero-variant employment order is not.", ["src-silver-eggheads-sfe", "src-silver-eggheads-opening-index"],
             "The reference and indexed primary opening establish wordmills, human tending/persona roles and robot authors working for robot readers. That is a real literary-automation lead, but maintaining equipment is still useful work and a marketing role alone does not establish an economy-wide work-preservation policy. Broad secondary claims that robots do everything need primary confirmation of ordinary access to goods, ownership and household livelihood. Preserved living brains would also require their own active-person scope rather than automatic nonworker status.",
             "Read primary material on non-literary production, household income and the writers' union before deciding post-work versus zero variant. The consulted text mirror's 403 was respected; indexed fragments are not a completed novel read."),
    decision("c0115", "needs_evidence", "The artificial world has immense productive capacity, but durable ordinary provisioning rights remain unverified.", ["src-wanderer-primary"],
             "Don's comfortable accommodation is guest or captive treatment, not an entitlement census. Chapter 36 distinguishes the wider civilization's democratic, security-focused elders from the Wanderer's dissidents and ambitions (ordinary-fetch lines 9550-9688). Constructed planets, immortality and malleable bodies are not proof of work-independent necessities or AI government. Tigerishka even presents thought-realizing devices as a problem still to solve. Human visitors are not silently substituted for all alien residents.",
             "Locate actual production and household-allocation passages for the Wanderer's population. If a point is retained, name an alien-person proxy and keep it distinct from the parent civilization; useful exploration, engineering and art still count as work."),
    decision("c0116", "needs_evidence", "Repeated robot displacement is direct, but the current evidence does not establish a qualifying general distribution system.", ["src-green-millennium-primary"],
             "The opening shows Phil losing successive jobs to faster robots and living in subdivided housing; the Fun Incorporated scene shows robots selling commodities for money. Neither one displaced man nor automated retail establishes how most residents obtain necessities. No primary rule deliberately preserving replaceable employment was established either. The ending introduces mood-mediating alien symbionts and political acceptance, rather than a completed new material constitution; emotional peace is not automatic production.",
             "Check broader production ownership, unemployment support and access conditions before choosing a post-work or zero-variant classification. Keep the before-contact economy separate from the still-unfolding green-cat settlement."),
    decision("c0117", "included", "A realized contract-defined author cohort has a durable automation-funded income independent of further writing.", g, society_id="grammatizator-contracted-authors",
             analysis="The broad publishing-economy lead is narrowed explicitly to actual lifetime-contract signatories. The final PDF pages were visually checked. The record does not extend their payments to unsigned writers, the country's residents or the narrator's hungry dependents; it leaves participation unresolved and discloses the small occupational scope.")
]
write_batch(21, [f"c{i:04}" for i in range(113, 118)], S, R, D, [
    "Second pass checked the Sirens origin legend and separate Vonnegut versions, Leiber's uncertain household institutions, and the difference between automation-funded buyouts and preserved employment.",
    "The Dahl record is a narrow contract-defined population with actual continuing payment arrangements, not an entire civilization inferred from automated publishing. Its output/signature statistics are never used as participation percentages.",
    "Primary PDF visual checks corrected the educational abridgment's omission of skilled manual novel controls. Useful human operation persists alongside the buyout cohort.",
    "No new zero variant was asserted without evidence of deliberate replaceable work. Same-researcher evidence review only; goal remains active and images remain deferred."
])
