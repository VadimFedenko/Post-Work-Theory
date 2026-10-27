from research_helpers import source, decision, write_batch

S = [
    source("src-fountains-preview", "The Fountains of Paradise", "Arthur C. Clarke; Open Road Integrated Media on Everand",
           "https://www.everand.com/book/399436244/The-Fountains-of-Paradise", "official_synopsis_and_indexed_primary_preview",
           "Public indexed product text and limited excerpt read", "Morgan's elevator project, technical and economic obstacles, and a clearly separate ancient-palace scene.",
           "The ancient slave-work excerpt is not evidence for the late twenty-second-century candidate. A cheap route to orbit does not establish automatic household provision."),
    source("src-fountains-pip", "Arthur C Clarke and Web 2.0", "Sarah Maddox; ffeathers, 20 June 2008",
           "https://ffeathers.wordpress.com/2008/06/20/arthur-c-clarke-and-web-20/", "secondary_reader_commentary_with_primary_excerpt",
           "Substantial indexed article read; direct retrieval returned cache miss", "Chapter 34, Vertigo: automated information tasks and the new burden of Personal Interest Profiles.",
           "An information-management passage does not establish the whole material economy or a universal right to subsistence."),
    source("src-imperial-preview", "Imperial Earth: opening chapters", "Arthur C. Clarke; Open Road Integrated Media on Everand",
           "https://www.everand.com/book/399436227/Imperial-Earth", "primary_fiction_in_publisher_preview",
           "Page opened; Chapters 1-3's hydrogen, dynasty and administration passages read", "Orbital hydrogen collection, financing, Malcolm's rise, limited personal fortunes, family decisions and Assembly scrutiny.",
           "A publisher synopsis gives an inconsistent five-hundred-year ancestry; the actual chapters put Malcolm's project in the 2180s and the present in 2276. Restricted wealth does not itself prove universal material rights or an end to work."),
    source("src-time-firstborn-publisher", "Firstborn", "Penguin Random House / Del Rey; Arthur C. Clarke and Stephen Baxter",
           "https://www.penguinrandomhouse.com/books/28164/firstborn-by-arthur-c-clarke-and-stephen-baxter/", "official_publisher_synopsis",
           "Product page opened; plot description read", "Mir's patchwork creation, destructive interventions against Earth and the later renewed threat.",
           "The marketing links the Firstborn with Space Odyssey imagery, but that is not permission to import a single shared economic continuity. Destructive power is not a civilian allocation system."),
    source("src-time-series-publisher", "A Time Odyssey", "Penguin Random House / Del Rey",
           "https://www.penguinrandomhouse.com/series/1TO/a-time-odyssey/", "official_series_synopses",
           "Series page opened; Firstborn and Sunstorm descriptions read", "Mir combines people and lands from different eras; Bisesa returns to another Earth; later threats affect both settings.",
           "This establishes distinct worlds and periods, not a homogeneous post-work society. Individual settlements still require their own productive evidence."),
    source("src-last-theorem-publisher", "The Last Theorem", "Penguin Random House / Del Rey; Arthur C. Clarke and Frederik Pohl",
           "https://www.penguinrandomhouse.com/books/28199/the-last-theorem-by-arthur-c-clarke-----frederik-pohl/", "official_publisher_synopsis",
           "Indexed product description read", "Ranjit's proof, fame, the NSA and Pax per Fidem; coauthor and edition identity.",
           "The synopsis concerns the main human plot rather than the later alien exchange or its economic effects."),
    source("src-last-theorem-reference", "The Last Theorem", "Wikipedia contributors",
           "https://en.wikipedia.org/wiki/The_Last_Theorem", "secondary_plot_reference",
           "Page opened; alien arrival and late ending summary read", "The One Point Fives and Machine Stored act while the Grand Galactics are absent; power technology and uploads; a return thirteen millennia later.",
           "Needs primary confirmation. Power and mind uploading alone do not establish goods for nonworkers. The ending should not be treated as one unchanged contemporary Earth under continuous alien government.")
]

D = [
    decision("c0072", "needs_evidence", "The consulted passages establish advanced transport and information systems, not the candidate's post-work material arrangements.", ["src-fountains-preview", "src-fountains-pip"],
             "Morgan's project lowers the cost of reaching orbit and encounters financial, technical and institutional constraints. A Chapter 34 excerpt describes information automation creating successor tasks, which cannot substitute for an account of necessities, employment or ownership. The preview's ancient palace and slave labor belong to another period entirely. Neither period nor the remote ending can be averaged into a generic automated Earth.",
             "Read the late twenty-second-century production and household-access passages, and date any epilogue society separately. Admit a post-work or zero-variant unit only if its automation/distribution relationship is actually established."),
    decision("c0073", "needs_evidence", "Titan's concentrated family administration is directly supported; wage-independent material provision is not.", ["src-imperial-preview"],
             "The opening describes a financed hydrogen-export project and a family that combines engineering and political leadership. An Assembly can criticize privileges, and there are no great private fortunes, but those facts do not make all residents collective owners or guarantee nonworkers an income. Orbital scoops establish technology, not the total human labor requirement. The tempting dynastic-control coordinate is withheld until the society's admission is supported.",
             "Find Titan's actual operating workforce, household benefits, industrial ownership and Assembly powers. Keep Earth practices, including any lottery government, separate from Titan; use the primary chronology rather than the inconsistent publisher ancestry."),
    decision("c0074", "boundary_case", "Species management and extermination are not a demonstrated post-work human economy.", ["src-time-firstborn-publisher", "src-time-series-publisher"],
             "The Firstborn manipulate worlds and threaten human survival. That establishes coercive technological power, but not a resident human society whose productive assets, material access and work participation can be mapped. A species-wide extinction policy cannot supply a human leisure fraction or automatically establish autonomous AI ownership. The broad lead combines many potentially different populations.",
             "Keep as an external-control comparison. Reopen for a precisely named protected or administered population only after its daily production and allocation are evidenced; do not treat a cosmic power's entire domain as one economy."),
    decision("c0075", "boundary_case", "Mir is a patchwork of historical populations, not a verified homogeneous administered post-work society.", ["src-time-series-publisher", "src-time-firstborn-publisher"],
             "The publisher explicitly distinguishes Mir from the Earth to which Bisesa returns. Its inhabitants include ancient armies and people from other eras. Their assembly into an artificial world does not show that labor, supplies and ownership have become one shared system. A single world coordinate would erase the differences that make this setting distinctive.",
             "If a particular Mir settlement or later order has automatic provision, name and research it individually. Preserve the broad lead's correction and do not conflate alien construction with an already functioning welfare economy."),
    decision("c0076", "needs_evidence", "The lead's continuous alien-rule label obscures distinct periods, while the material effect of the later technology remains unverified.", ["src-last-theorem-publisher", "src-last-theorem-reference"],
             "The secondary ending describes client aliens acting independently while the Grand Galactics are absent, followed by new power technology, mind uploading and a much later transfer of guardianship. Those changes may produce a suitable society, but neither cheap power nor digital existence alone proves automated subsistence or a nonworking share. The scientific protagonist's initial wealth is also not population-wide provision.",
             "Read the actual exchange and late-epilogue passages. Separate contemporary humans, any uploaded community and the distant successor order; qualify a record only after its productive and allocative rules are established.")
]

write_batch(12, [f"c{i:04}" for i in range(72, 77)], S, [], D, [
    "Five contiguous broad leads receive reasoned dispositions without unsupported retained points.",
    "Primary Titan chapters sharpen the governance evidence and correct a publisher chronology, while leaving the admission question open.",
    "Mir's heterogeneous populations and the Firstborn's external intervention remain comparisons rather than a single invented automated society.",
    "Second pass checked resource wealth against entitlements, machine existence against the human labor requirement, external threats against domestic government, and remote epilogues against main-story periods.",
    "No discovery lead is promoted merely to maintain a numerical acceptance rate. The full target still requires 500-1000 researched, reviewed records."
])
