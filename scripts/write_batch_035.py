from research_helpers import source, decision, write_batch

S = [
    source("src-house-suns-reference", "House of Suns", "Wikipedia contributors",
           "https://en.wikipedia.org/wiki/House_of_Suns", "secondary_plot_and_setting_reference",
           "Public indexed setting account read", "Gentian shatterlings, independent machine civilization and the Line's history.",
           "Wealth, extreme longevity and powerful ships do not alone establish an unconditional support system; no primary novel read attempted."),
    source("src-house-suns-reader-reviews", "House of Suns: reader reviews", "Reader reviews displayed by Everand",
           "https://www.everand.com/audiobook/635877127/House-of-Suns", "secondary_reader_reviews_indexed",
           "Public indexed Gentian/Vigilance discussion consulted", "Long-lived wealthy travelers, occasional engineering/trade and Vigilance archives.",
           "User-generated reviews, not publisher verification; multiple reviewers share a page. Used as discovery/context only, not economic admission proof."),
    source("src-pushing-ice-reference", "Pushing Ice", "Wikipedia contributors",
           "https://en.wikipedia.org/wiki/Pushing_Ice", "secondary_plot_reference",
           "Public indexed colony and Structure summary read", "Multiple human settlement periods, alien technological trade and a later colony.",
           "The framing future, Janus settlement and later colony must not inherit one another's institutions; no household access constitution established."),
    source("src-blue-earth-wertzone", "Blue Remembered Earth by Alastair Reynolds", "The Wertzone, January 2012",
           "https://thewertzone.blogspot.com/2012/01/blue-remembered-earth-by-alastair.html?amp=1&m=0", "secondary_literary_review_indexed",
           "Public indexed prosperity and surveillance discussion read", "Economic development, AI crime intervention and differing coverage off Earth.",
           "Prosperity and automated policing do not establish that wages cease to be the main route to necessities or that AI owns production.")
]
D = [
    decision("c0184", "needs_evidence", "Gentian wealth, longevity and advanced ships are clear, but the quick references do not establish a common labor-independent support arrangement.", ["src-house-suns-reference", "src-house-suns-reader-reviews"], analysis="The group also performs engineering and trade. An affluent clonal cohort cannot be admitted solely from the absence of visible subsistence labor.", follow_up="Skip deeper reading under the pace instruction; require a concrete automatic production/access reference before admission."),
    decision("c0185", "boundary_case", "The Machine People are an independent robot civilization, without an established human support population or justified post-work person-level economy.", ["src-house-suns-reference"], analysis="Artificial personhood is not denied, but a robot civilization alone supplies neither an applicable human work fraction nor evidence that its people are free of necessary labor.", follow_up="Preserve as a machine-civilization comparison; skip further investigation."),
    decision("c0186", "needs_evidence", "The Vigilance's unusual archivists and information exchange do not establish general production or labor-independent material access.", ["src-house-suns-reader-reviews"], analysis="Archival work, immense bodies and longevity are capabilities and occupations rather than a verified post-work distribution mechanism.", follow_up="Skip a primary novel investigation."),
    decision("c0187", "needs_evidence", "The broad far-future settlement lead combines distinct periods without clear general access rules in the short references.", ["src-pushing-ice-reference"], analysis="Alien technology gifts, bargaining and a later human colony do not by themselves establish who receives necessities independently of work. The early mining crew and the framing Congress are separate scopes.", follow_up="Skip deeper reading; reopen only on a short, specific material-economy reference."),
    decision("c0188", "needs_evidence", "The short sources establish a prosperous surveilled Earth, but not labor-independent household access or ownership of automated production.", ["src-blue-earth-wertzone"], analysis="AI intervention against crime is not sovereign AI control of the economy. A wealthy protagonist's family and eliminated poverty cannot alone establish the requested automation-distribution link across Earth and the United Aquatic Nations.", follow_up="Skip further reading in this pass; preserve the distinction between security automation and material provision.")
]
write_batch(35, [f"c{i:04}" for i in range(184, 189)], S, [], D, [
    "The user explicitly permits obscure economic leads to be skipped; no novel reading was used to rescue these five cases.",
    "Long life, wealthy travelers, robot citizens, alien gifts and AI policing are not substituted for actual production/allocation arrangements.",
    "Reader-review aggregation is identified as such and used for context only; no unsupported source is promoted into an admitted society record."
])
