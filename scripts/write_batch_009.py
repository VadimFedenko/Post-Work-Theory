from research_helpers import source, assessment, record, scope, evidence, decision, write_batch

S = [
    source("src-roads-primary", "The Roads Must Roll in The Man Who Sold the Moon", "Robert A. Heinlein; converted text on Zanotowane",
           "https://zanotowane.pl/1188/8408/", "primary_fiction_unofficial_transcription",
           "Collection opened; story opening and Gaines's machinery explanation read", "Story starts at The Roads Must Roll heading; workers' demands, competing trades and the road-service bottleneck.",
           "Unofficial conversion with pagination artifacts. Sampling this story does not establish a uniform economy for Heinlein's entire Future History."),
    source("src-horizon-preview", "Beyond This Horizon: HTML preview", "Robert A. Heinlein; unofficial Robert A Heinlein blog",
           "https://raheinlein.wordpress.com/novels/beyond-this-horizon/", "primary_fiction_unofficial_excerpt",
           "Preview opened; economic opening and synthesist discussion read", "Chapter One's mixed economy, free food, allowance and accounting computer; Hamilton's discussion of the leadership hierarchy.",
           "The page's introductory publication statement conflicts with its heading; it is not used for dating. The excerpt does not specify the entire electorate or ownership structure."),
    source("src-horizon-scan", "Beyond This Horizon", "Robert A. Heinlein; scanned edition hosted by Luminist",
           "https://s3.us-west-1.wasabisys.com/luminist/EB/H/Heinlein%20-%20Beyond%20This%20Horizon.pdf", "primary_fiction_scanned_edition",
           "PDF opened and dividend find passages read; later targeted retrievals timed out", "Printed pages 71-73 on surplus, work and research; Smith's discussion of living on the dividend; page 174 on servants and automaton furniture.",
           "Not a complete read. PDF page indices differ from printed numbers. A human calls himself a computer in the work; that word alone does not denote an AI ruler."),
    source("src-living-primary", "For Us, the Living: A Comedy of Customs", "Robert A. Heinlein; converted text on Zanotowane",
           "https://www.zanotowane.pl/1210/6477/", "primary_fiction_unofficial_transcription",
           "Text opened; Chapters IX-X and XII's economic and franchise passages read", "Machines, optional work, dividend, free medicine, private industry, public banking and voting conditions.",
           "The discussion advocates a fictional economic system, not a verified real-world theorem. Its statement about the urge to work is not an actual employment census."),
    source("src-living-publisher", "For Us, The Living: A Comedy of Customs", "Simon & Schuster / Scribner",
           "https://www.simonandschuster.com/books/For-Us-The-Living/Robert-James/9780743261579", "official_publisher_page",
           "Indexed product page read", "Novel identity, Perry Nelson's starting period, posthumous edition and synopsis.",
           "The publisher's Future History marketing does not erase differences between this manuscript's future and later stories."),
    source("src-moon-primary", "The Moon Is a Harsh Mistress", "Robert A. Heinlein; transcription on The Ted K Archive",
           "https://www.thetedkarchive.com/library/robert-a-heinlein-the-moon-is-a-harsh-mistress", "primary_fiction_unofficial_transcription",
           "Text opened; find passages read; opening machine scope also available in indexed text", "Mike's services in May 2075; Wyoh's early meeting on water, power, wheat and labor shortage; later account of air lending and food.",
           "Some follow-up opens timed out. An insurgent's promises are not an already realized post-revolution welfare settlement. Mike does not run Hong Kong's separate air and water system."),
    source("src-friday-primary", "Friday", "Robert A. Heinlein; converted text on Zanotowane",
           "https://zanotowane.pl/1200/5839/", "primary_fiction_unofficial_transcription",
           "Text opened; travel bureau and Shipstone research passages read", "Chapter 1's automated booking with a human attendant; converted pages 125-128 on storage technology, corporate ownership and Friday's uncertainty.",
           "Friday's investigation distinguishes demonstrated interlocking ownership from potential systemwide government. No complete population-wide distribution or labor account was established by these samples.")
]

horizon = ["src-horizon-preview", "src-horizon-scan"]
living = ["src-living-primary", "src-living-publisher"]
R = [record(
    "beyond-horizon-americas", "c0061", "Beyond This Horizon (American civilization)", "Beyond This Horizon", "The hemisphere's dividend-supported economy", ["book"],
    scope("The original novel's future", "The established civilization defended against the attempted coup", "Human residents of the depicted American hemisphere", ["All Earth societies as a uniform economic unit", "The conspirators' proposed replacement order", "An accounting machine as the creator of physical goods"]),
    "Productivity supports a regular citizen dividend and free ordinary food, while paid businesses and luxury purchases continue. People can refuse badly paid service because they have another means of living; automated household equipment is an alternative to servants. That supports strong guarantees without making every desirable service free. The text also distinguishes its accounting computer from the machinery that actually produces wealth.\n\nHuman specialists and the Policy Board guide this mixed economy. Leadership is strongly associated with a small class of synthesists, so elections do not automatically establish broadly shared control. The control estimate stays near the human-elite region with a wide range. The moderate nonworking estimate reflects continuing occupations and invention alongside freedom from wage necessity. It is deliberately much lower than a total-leisure reading: people working on new devices or research still count as working. No population census settles their actual share.",
    {"guarantees": -0.85, "control": 0.2, "nonworking": 0.3},
    {"guarantees": assessment(-0.85, [-0.95, -0.55], "medium", "Dividend-backed subsistence; costly personal services remain.", horizon),
     "control": assessment(0.2, [0, 0.55], "low", "Human Board and private enterprise; leadership hierarchy clearer than electorate.", ["src-horizon-preview"]),
     "nonworking": assessment(0.3, [0.1, 0.6], "low", "Coarse minority estimate: voluntary invention and occupations continue. Optional employment is not inactivity.", ["src-horizon-scan"])},
    1, horizon,
    [evidence("The dividend reduces wage dependence while productive work continues.", ["src-horizon-scan"], "Printed pages 71-73 and 174", "depicted_or_author_stated"),
     evidence("Accountants and synthesists remain human decision-makers.", ["src-horizon-preview"], "Chapter One; Hamilton and Mordan discussion", "depicted_or_author_stated")],
    ["Verify the electorate and ownership concentration.", "No all-age labor census; long-lived adults complicate demographic assumptions.", "Genetic status and dueling complicate the claimed ideal of freedom."], alternatives=[2])]

R.append(record(
    "for-us-living-us2086", "c0062", "For Us, the Living (United States, 2086)", "For Us, the Living", "The federal social-credit settlement", ["book"],
    scope("The posthumously published manuscript's distinct future", "2086, during Perry Nelson's visit", "Human US residents under the federal settlement", ["A uniform world economy", "Coventry's seceding communities", "Wisconsin's extra cooperative arrangements as a national rule", "Later Future History stories without comparison"]),
    "Machines make essential production possible with comparatively few operators. A public dividend gives people purchasing power whether they take a job or not, and medical service is free. Guarantees are consequently strong, with a qualification: the political explanation ties drawing the dividend to voting. This is freedom from wage dependence with a civic condition, rather than an entirely unconditional material right.\n\nElections, public banking and room for different state policies give citizens meaningful influence, while much industry remains privately owned. That combination supports a moderately positive human-control estimate. Computers do not appear to replace the electorate. The nonworking point is a rough minority estimate because the dialogue emphasizes continuing creative activity and scarce drudgery. Its statement about a widespread urge to work mixes useful activity with recreation; it cannot be read as an employment census. The wide range leaves that distinction open.",
    {"guarantees": -0.75, "control": 0.55, "nonworking": 0.3},
    {"guarantees": assessment(-0.75, [-0.95, -0.4], "medium", "Non-wage dividend and medicine, qualified by voting eligibility.", ["src-living-primary"]),
     "control": assessment(0.55, [0.25, 0.8], "medium", "Public monetary control and elections coexist with private industry.", ["src-living-primary"]),
     "nonworking": assessment(0.3, [0.1, 0.65], "low", "Editorial estimate from continuing voluntary activity; no conversion of motivation into a headcount.", ["src-living-primary"])},
    2, living,
    [evidence("Machines and shared technical inheritance justify non-wage access.", ["src-living-primary"], "Chapter X: Davis and Perry", "depicted_or_author_stated"),
     evidence("Dividend voting condition requires instruction, without a pass/fail examination.", ["src-living-primary"], "End of Chapter XII", "depicted_or_author_stated")],
    ["Check dividend eligibility for dependents and nonvoters more closely.", "State variation remains inside a federal scope, not an assertion of identical ownership everywhere.", "The participation estimate is not a canonical statistic."]))

D = [
    decision("c0060", "boundary_case", "Advanced road machinery creates an essential human-maintenance bottleneck, not a demonstrated post-work distribution system.", ["src-roads-primary"],
             "The opening explicitly retains wages, guilds, insurance and retirement; other farmers and industrial workers remain necessary. Gaines argues for disciplined service because a small transport workforce can paralyze production. The story does not establish general wage-independent access or deliberately retained employment after machines could remove its material necessity. Automatic transport alone is too broad an admission rule, including for the zero variant.",
             "Keep as a comparison about concentrated technical power. Reopen only with broader production/distribution evidence, and do not borrow another Future History period's arrangements."),
    decision("c0061", "included", "Direct passages establish dividend-supported subsistence and labor-saving technology alongside substantial voluntary work.", horizon, society_id="beyond-horizon-americas", scope_correction="The economic account depicts a hemisphere; it is not silently generalized to every human society."),
    decision("c0062", "included", "The primary dialogue directly connects machine productivity, the shared dividend and freedom to decline employment.", living, society_id="for-us-living-us2086"),
    decision("c0063", "boundary_case", "Mike's autonomous intelligence and extensive services do not make this work-dependent Lunar economy post-work.", ["src-moon-primary"],
             "Mike runs important transport, communications and life-support services, but not every settlement's infrastructure. The early meeting describes producers squeezed by the Authority's prices and monopoly, and Hong Kong's chronic labor shortage. A later explanation explicitly leaves food dependent on work or other means. There is no verified automatic material share for the population, or deliberate job preservation after human labor became dispensable. Revolutionary coordination must also be separated from the later government's economy.",
             "Retain as an AI-control and scarce-resource comparison. Research a separately realized later arrangement if proposed; neither Mike's presence nor his alliance with Mannie supplies an automatic admission or a pure-AI control score."),
    decision("c0064", "needs_evidence", "Primary samples establish sophisticated services and concentrated corporate ownership, but not the candidate's claimed post-work economy.", ["src-friday-primary"],
             "The automated travel bureau still has an attendant. Shipstones are energy-storage technology; cheap energy and an industrial secret do not establish automatic goods for nonworkers. Friday discovers interlocking ownership and distinguishes potential systemwide government from proof that it acts as such. The queue's broad date and uniform economic label remain unverified, and artificial persons cannot be assumed to replace all necessary labor.",
             "Locate actual manufacturing, income and household-access passages for a defined polity and period. Decide post-work, zero variant or comparison from that relationship, rather than mapping the entire fragmented setting from one protagonist's corporate investigation.")
]

write_batch(9, [f"c{i:04}" for i in range(60, 65)], S, R, D, [
    "Five contiguous leads receive decisions; two primary-supported societies are retained. Roads and Luna remain comparisons, and Friday's broad discovery label needs further evidence.",
    "Second pass checked machines versus accounting, voluntary useful activity versus nonwork, expert leadership versus public ownership, and a basic dividend versus an unconditional right.",
    "The two new participation points are qualitative editorial estimates with broad ranges, not employment statistics inferred from the freedom to refuse a wage job.",
    "For Us, the Living's explicit voting condition is included in guarantees. Its stated urge to work is not entered as a measured participation rate.",
    "The scan's successful find passages and later retrieval failures are both recorded. No source is described as a full-novel read, and unofficial transcription status remains visible."
])
