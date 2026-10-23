from research_helpers import source, assessment, record, scope, evidence, decision, write_batch

S = [
    source("src-songs-publisher", "Songs of Distant Earth", "Penguin Random House / Del Rey",
           "https://www.penguinrandomhouse.com/books/28183/songs-of-distant-earth-by-arthur-c-clarke/", "official_publisher_synopsis",
           "Product page opened; bibliographic identity and synopsis read", "Thalassa's abundant resources and the arrival of the Magellan; 1987 paperback edition of the novel.",
           "A paradise description does not specify income, ownership or work obligations. The 1958 story, 1986 novel, simplified readers and musical album are not interchangeable."),
    source("src-songs-preview", "The Songs of Distant Earth: novel preview", "Arthur C. Clarke; Open Road Integrated Media on Everand",
           "https://www.everand.com/book/387516595/The-Songs-of-Distant-Earth", "official_synopsis_and_indexed_primary_preview",
           "Product page opened; opening novel excerpts read through the public search index", "Mirissa, Kumar and Brant's fishing research; Mayor Waldron and the discussion of robot-seedship ancestry.",
           "The product is marked locally unavailable. Only openly returned/indexed extracts were read. Founding technology does not prove current automated entitlement."),
    source("src-3001-primary", "3001: The Final Odyssey", "Arthur C. Clarke; unofficial OCR transcription on StudyLib",
           "https://studylib.net/doc/7772218/title--3001-the-final-odyssey", "primary_fiction_unofficial_transcription",
           "Text opened; Skyland maintenance, bio-organism explanation, human council and author's continuity note sampled", "Poole initially assumes robot garden maintenance, then learns that enhanced animals are used; cleaning microts, human technical work and Council of War; final author's note.",
           "No general income or entitlement arrangement was established. Keyword absence is not proof that no such arrangement exists. The author explicitly treats the Odyssey novels as variations rather than one entirely consistent timeline."),
    source("src-comarre-primary", "The Lion of Comarre", "Arthur C. Clarke; Harcourt Brace Jovanovich collection scan hosted by Luminist",
           "https://s3.us-west-1.wasabisys.com/luminist/EB/C/Clarke%20-%20Comarre.pdf", "primary_fiction_scanned_edition",
           "Image-only PDF rendered locally; selected complete printed pages visually read", "Printed pages 31-36, 42-62: automatic city, sleeping residents, Engineers' autonomy, maintenance, awakening tests and the ending's proposed future.",
           "In this portion PDF page equals printed page plus 14. Targeted scenes, not the entire collection, were read. The ending anticipates a wider partnership; it does not depict that later economy as accomplished.")
]

comarre = ["src-comarre-primary"]
R = [record(
    "comarre-sleeping-enclave", "c0071", "The Lion of Comarre (The sleeping city)", "The Lion of Comarre", "Comarre's remaining resident dreamers", ["short_story"],
    scope("The original story, as printed in the scanned collection", "The established city before Peyton's intervention", "The physically sleeping human residents sustained inside Comarre", ["Peyton as a visiting investigator", "Dream characters as additional people or productive workers", "The outside World Council's population", "The promised later human-machine partnership"]),
    "Comarre maintains its human residents while they live inside machine-generated dreams. Its automatic infrastructure has no resident human workforce: the builder is long dead, and self-repairing robots keep the city functioning. Material support therefore lies near the strong end, though this is maintenance of sheltered bodies, not a promise of immortality. Dream experiences do not count as production for the physical community.\n\nThe conscious Engineers exercise substantial independent authority, including protecting equipment against a human visitor. That supports a negative control point, qualified by their inherited purpose and willingness to follow some requests. The story complicates a simple captivity reading: a recently awakened resident actively chooses his dream again. The near-total nonworking estimate concerns the settled sleeping population, with a small allowance around the observed condition. It excludes the visitor's investigation and does not convert the ending's hoped-for partnership into an already realized new regime.",
    {"guarantees": -0.8, "control": -0.7, "nonworking": 0.99},
    {"guarantees": assessment(-0.8, [-0.95, -0.55], "medium", "Durable automatic maintenance supports sleepers; aging and the condition of their bodies qualify the guarantee.", comarre),
     "control": assessment(-0.7, [-0.95, -0.2], "medium", "Conscious Engineers defend the system and can refuse human orders, while serving an inherited purpose and accepting some requests.", comarre),
     "nonworking": assessment(0.99, [0.95, 1], "high", "The established resident population is physically asleep and maintained by machines. This is a scoped editorial near-total estimate, not an exact census.", comarre)},
    5, comarre,
    [evidence("Sleeping residents are sustained by an automatic, self-maintaining city.", comarre, "Printed pages 31-33, 42-43 and 49", "depicted_or_author_stated"),
     evidence("The Engineers have their own consciousness and can use force; some requested awakenings are granted.", comarre, "Printed pages 46-57", "depicted_or_author_stated")],
    ["An offered refuge and the loss of an old resident's former identity complicate consent.", "The number of active dream circuits is approximate, not a verified population census.", "The promised Third Renaissance is kept outside this snapshot."])]

D = [
    decision("c0069", "needs_evidence", "Robotic founding and a prosperous colony do not yet establish the mature society's production and entitlement rules.", ["src-songs-publisher", "src-songs-preview"],
             "The novel's opening supplies human fishing research, local officeholders and robot-seedship ancestry; publisher material describes abundant resources. None of the consulted passages establishes how nonworkers obtain necessities now. A quoted lottery-government lead is not sufficient by itself and must be checked against similar material in Imperial Earth. The original short story and simplified adaptation must not silently supply the novel's missing economy.",
             "Locate the 1986 novel's present production, consumption and constitutional passages. Confirm whether automation materially replaces wage dependency, rather than infer it from colonization or an idyllic tone; then assign the axes for Thalassa alone."),
    decision("c0070", "needs_evidence", "Primary passages show labor-saving technology, but general subsistence access and economic control remain unestablished.", ["src-3001-primary"],
             "Poole's comfortable treatment is not proof of an unconditional population-wide right. The garden scene specifically corrects his assumption that robots do all maintenance: enhanced animals are preferred for some tasks. Human technical careers and collective decisions also continue. A Monolith threatening humanity is not automatically the ruler of its civilian economy, and the author's own note warns against importing a single seamless continuity from earlier volumes.",
             "Find explicit household access, income and productive ownership evidence for the Earth-Tower community and compare it with other settlements. Keep it unresolved rather than mapping all humanity from a revived celebrity's care."),
    decision("c0071", "included", "Direct visual reading establishes an automatic sleeping enclave and independently acting conscious robot guardians.", comarre, society_id="comarre-sleeping-enclave")
]

write_batch(11, [f"c{i:04}" for i in range(69, 72)], S, R, D, [
    "The previous goal turn made progress: it changed durable counts and supplied primary evidence. This continuation adds decisions for three further contiguous leads and directly reads previously inaccessible scan pages.",
    "Thalassa and 3001 remain evidence gaps rather than being admitted solely as technologically advanced paradises.",
    "Second pass checked dream activity against physical production, autonomous Engineers against ordinary obedient robots, choice of refuge against unqualified captivity, and a future promise against an accomplished new order.",
    "A separate follow-up updates c0068 in batch 010 after visual reading. Its alternate-version differences are retained without counting another economically equivalent Diaspar.",
    "No complete novel read, population census, poster collection or website implementation is claimed."
])
