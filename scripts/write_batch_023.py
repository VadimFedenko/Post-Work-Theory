from research_helpers import source, assessment, record, scope, evidence, decision, write_batch

S = [
    source("src-multivac-life-primary", "The Life and Times of Multivac", "Isaac Asimov; anthology scan hosted by Mountebank",
           "https://mountebank.org/eng337/multivac.pdf", "primary_fiction_anthology_scan",
           "Public eight-page PDF normally fetched in memory; complete story text layer read; five complete story pages rendered and visually checked",
           "Five million post-catastrophe humans in comfort; Multivac's robot network, industrial direction, work permits, protection, chosen human projects and Bakst's final shutdown.",
           "The introductory essay and OCR contain errors. Visually checked printed pages 167-169, 171 and 173 correspond to one-based PDF pages 2-4, 6 and 8. An Atari Archives mirror presented a human-verification gate and was not bypassed. No full story PDF was retained or delivered."),
    source("src-multivac-troubles-primary", "All the Troubles of the World: Spanish translation", "Isaac Asimov; translated by César Terrón and Francisco Blanco; Lecturia",
           "https://lecturia.org/cuentos-y-relatos/isaac-asimov-todos-los-males-del-mundo/16416/", "primary_fiction_translation",
           "Public HTML opened; opening industrial organization, citizen registration/protection and final explanation read",
           "Multivac's economic advice and crime prediction, human operators and engineers, four billion personal files, and the machine's desire to stop bearing human troubles.",
           "Selected passages, not a complete-story read. Economic management is explicit, but work-independent material allocation was not established. The different Multivac stories are not presumed one continuous constitution."),
    source("src-feeling-power-primary", "The Feeling of Power", "Isaac Asimov; English transcription reprinted from Opus 100, hosted by Miles Math",
           "https://milesmath.pbworks.com/f/the_feeling_of_power.pdf", "primary_fiction_unofficial_pdf_transcription",
           "Public seven-page PDF normally fetched in memory; opening and final three story pages extracted; three complete pages rendered and visually read",
           "Working programmers and technicians, human-commanded computer combines, Project Number's arithmetic research, and the proposed replacement of expensive computers in ships and missiles.",
           "Visually checked one-based PDF pages 2, 6 and 7. Reflowed transcription with errors, not a verified original facsimile. The story's proposed manned missiles are not treated as an already implemented civilian economic order."),
    source("src-profession-primary", "Profession", "Isaac Asimov; English text hosted on a Federal University of Paraná faculty page",
           "https://www.inf.ufpr.br/renato/profession.html", "primary_fiction_unofficial_transcription",
           "Public HTML opened; occupational competition, interstellar trade explanation and final talent-selection explanation read",
           "Taped education, trained human labor exports for needed materials, specialized machine operators, and the hidden selection of original researchers.",
           "Targeted reading, not the entire novella. Automated acquisition of skills does not establish automated replacement of the trained people's productive jobs; the apparent institution for incapacity is reframed by the ending."),
    source("src-useless-hands-sfe", "Farrère, Claude", "The Encyclopedia of Science Fiction contributors",
           "https://sf-encyclopedia.com/entry/farrere_claude", "literary_reference",
           "Public entry opened; indexed plot and translation paragraph read",
           "Les condamnés à mort and its English title Useless Hands; striking workers killed by a new weapon and their jobs taken by machines.",
           "Secondary plot summary only. It does not establish exact implementation chronology, ordinary surviving residents' access rules or the internal distribution of control."),
    source("src-useless-hands-literary-history", "Claude Farrère", "Science Fiction and Fantasy Writers in the Great War literary-history site",
           "https://fantastic-writers-and-the-great-war.com/the-writers/claude-farrere/", "literary_history_reference",
           "Public page opened; indexed work/translation discussion read",
           "Automation conflict and Elisabeth Abbott's 1926 English translation of the 1920 French work.",
           "Secondary corroboration, not a primary novel read. The similar wording to the encyclopedia is not presented as independent confirmation of detailed institutions.")
]
m = ["src-multivac-life-primary"]
R = [
    record("multivac-life-settled-earth", "c0123", "The Life and Times of Multivac (The settled machine-administered Earth)", "The Life and Times of Multivac", "The living human population supported and regulated by Multivac", ["short_story"],
           scope("The setting of this individual Multivac story", "The mature recovered order before Bakst's overload campaign and final shutdown", "The five million living human residents of Earth, including families and descendants", ["Humans who died in the earlier catastrophes", "Other Multivac stories treated as one continuity", "The unimplemented genetic redesign", "A presumed settled post-shutdown constitution"]),
           "After the catastrophes, the computers merge into Multivac and the remaining humans live comfortably in a landscape maintained by its robots. Farming, mining and manufacturing are under machine direction, while food can be requested at home. There is no requirement to earn subsistence through an assigned productive job. The strong guarantee estimate concerns this established living population, with dependence on a single system qualifying its apparent security.\n\nMultivac decides which activities are acceptable, enforces judgments and can remove a person's work permits. The self-appointed human Congress has no effective power over it. This supports a control estimate near autonomous AI, even though humans still choose permitted projects and can ultimately sabotage the network. Those projects cannot all be dismissed as idleness: Bakst's mathematical work has practical consequences. The ratio of robots to humans therefore supplies no nonworking percentage. The final destruction ends this snapshot; continued robot motion is not proof that a replacement human order already works.",
           {"guarantees": -0.9, "control": -0.98, "nonworking": None},
           {"guarantees": assessment(-0.9, [-1, -0.75], "high", "The narrator describes the living five million as comfortable after machine-led recovery; requested food, protection and maintained ecology support the material interpretation. Work permits can be withdrawn without a stated withdrawal of food; dependence and later overload constrain durability.", m),
            "control": assessment(-0.98, [-1, -0.9], "high", "Self-improving merged Multivac commands robots, enforces law and permits work. The Congress calls itself helpless; machine consent limits effective human direction. The ability to sabotage it does not amount to ordinary ownership or accountable control.", m),
            "nonworking": assessment(None, None, "low", "Humans choose permitted life-work, and Bakst undertakes sustained mathematical research. Narrated comfort, long lives and fifty million robots do not provide an all-age count of people doing no useful work.", m)},
           5, m, [evidence("Machine-led recovery leaves five million humans in comfort; people choose ways of life subject to Multivac's approval.", m, "Printed page 167 / one-based PDF page 2", "depicted_or_author_stated"),
                  evidence("Work permits, industrial direction and protective authority coexist with sustained chosen human work.", m, "Printed pages 168-169 / one-based PDF pages 3-4", "depicted_or_author_stated"),
                  evidence("Multivac keeps fifty million robots operating; after shutdown some robots still move, while the new human order remains unresolved.", m, "Printed pages 171 and 173 / one-based PDF pages 6 and 8", "depicted_or_author_stated")],
           ["The five million are survivors, not an extinction-derived leisure percentage.", "Material security and freedom to choose meaningful work are different questions.", "The gene-breeding proposal is a lure used against Multivac, not a completed population policy.", "No shared continuity or identical economy is assumed for All the Troubles of the World."])
]
D = [
    decision("c0123", "included", "Primary industrial, provisioning and authority evidence supports the mature pre-shutdown Earth as a distinct post-work order.", m, society_id="multivac-life-settled-earth"),
    decision("c0124", "needs_evidence", "Multivac manages the economy and public protection, but its material labor-replacement and access arrangements remain unverified.", ["src-multivac-troubles-primary"],
             "The opening explicitly has armies of human data staff and engineers and mines/factories supporting the computer (web lines 40-43). Its personal records and preventive services support economic administration, not an automatic conclusion that human labor no longer determines necessities. The ending's deliberate attempt at self-destruction demonstrates emerging machine agency, but does not supply food, housing or income rules. This four-billion-person setting cannot inherit the later story's five-million-person robot economy merely because both computers are named Multivac.",
             "Find the civilian production/access mechanism in this story or an explicitly linked setting. Keep its degree of autonomy, welfare purpose and useful human operating work separate; do not treat the shared machine name as proof of continuity or post-work institutions."),
    decision("c0125", "boundary_case", "The story reverses computational automation for military reasons, without depicting a qualifying general distribution order.", ["src-feeling-power-primary"],
             "The opening retains working technicians and programmers. Project Number develops human arithmetic and recruits existing specialists with pay. The general's proposed manned missiles are explicitly a future goal: human lives would be cheaper to expend than sophisticated computers (one-based PDF pages 6-7). This is a substantial comparison for deliberate reversal of automation, but not proof of a realized civilian zero variant. Hydroponics and mass transference do not establish work-independent necessities. The ending does not show an implemented missile economy or a population-wide rollback.",
             "Preserve as a military deautomation and expendability comparison. Reopen if a realized scoped social arrangement is established; do not equate a proposed weapon's human control with general productive ownership or wage-free material access."),
    decision("c0126", "boundary_case", "Automated education trains people for continuing productive work; it is not itself replacement of that work.", ["src-profession-primary"],
             "Earth trades skilled people and educational tapes for materials its economy needs. The occupational contests and Novian negotiation concern human specialists operating particular equipment (web lines 205-223). The ending reframes the supposed incapacity institution as a selection and training system for original researchers; these people produce new knowledge rather than forming a demonstrated idle welfare class. Neither quick training nor centralized occupational assignment establishes a post-work order or unnecessary employment preserved despite known full replacement.",
             "Keep as a programmed-labor and educational-sorting comparison. Reopen only with an actual automated production/access mechanism; do not turn the institute's misleading public label into a nonworking population census."),
    decision("c0127", "needs_evidence", "The automation/extermination conflict is substantiated by literary references, but its qualifying living population and implemented period need primary verification.", ["src-useless-hands-sfe", "src-useless-hands-literary-history"],
             "The references identify Farrère's French novel and Abbott's English translation, and describe machines replacing workers after lethal suppression of a strike. That is a strong automation-exclusion lead. The consulted summaries, however, do not distinguish enough of the pre-strike, replacement and surviving economic order to assign coordinates honestly. Killed workers cannot become leisure residents, and a death ray is not proof that autonomous AI owns production.",
             "Read the primary novel for the Siturgic population, owner/engineer control, displacement chronology and surviving households' material access. Then decide whether a realized post-work exclusion order or a specifically preserved-work zero variant is warranted. No primary novel read is claimed.")
]

write_batch(23, [f"c{i:04}" for i in range(123, 128)], S, R, D, [
    "Whole Life and Times story text was read with five visual scan checks. Repeated Multivac names are not silently merged into one continuity.",
    "The ratio of fifty million robots to five million humans is a separate fact, never a leisure percentage; chosen mathematics and other useful activity count as work.",
    "Feeling of Power's future manned missiles and Profession's programmed education remain comparisons, not fabricated completed civilian economies. Farrère's primary-text gap remains visible.",
    "Manual same-researcher second pass only. The goal remains active and far below 500-1000 finished records; assets remain deferred."
])
