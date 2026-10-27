from research_helpers import source, decision, write_batch

S = [
    source("src-conjoiner-evacuation-reference", "Conjoiner Evacuation Fleet", "Revelation Space Wiki contributors",
           "https://revelationspace.fandom.com/wiki/Conjoiner_Evacuation_Fleet", "secondary_fan_lore_reference_indexed",
           "Public indexed production account read", "Secret fleet built with servitors under the Master of Works and intermittent human oversight.",
           "This is a particular military-industrial project, not a verified general civilian access arrangement for all Conjoiners."),
    source("src-reynolds-ultras-context", "Technology and Society 2: Revelation Space", "Atomic Rockets; quotations and literary setting context",
           "https://www.projectrho.com/public_html/rocket/scisociety2.php", "secondary_setting_reference_with_primary_quotations",
           "Public indexed faction discussion consulted", "Distinction between interstellar crews and Conjoiner settlements.",
           "A broad mixed-source page; only the identified fictional faction context is used, not real engineering claims or a full primary read."),
    source("src-glitterband-political-review", "Speculations on Speculative Fiction: Is This Alastair Reynolds's Most Political Novel?", "Illusory Promise, 26 September 2018",
           "https://illusorypromise.wordpress.com/2018/09/26/speculations-on-speculative-fiction-is-this-alastair-reynoldss-most-political-novel/", "secondary_literary_analysis_indexed",
           "Public indexed setting account read", "Glitter Band abundance, diverse local settings and political disputes following the Aurora crisis.",
           "Later pre-plague setting context, not proof that every habitat has identical internal institutions or a second distinct economic regime.")
]
D = [
    decision("c0179", "needs_evidence", "Automatic city maintenance survives, but the post-plague population's general access to necessities is not established in the short sources.", ["src-chasm-city-identity-thesis"], analysis="The account describes service/criminal livelihoods and inequality between Canopy and Mulch. Surviving automatic machines do not justify carrying over the earlier demarchy's guarantees.", follow_up="Skip deeper reading; do not manufacture a post-work or zero-variant point from the pre-plague system alone."),
    decision("c0180", "needs_evidence", "A genuinely automated Conjoiner fleet factory is documented, but whole-population civilian access remains unclear.", ["src-conjoiner-evacuation-reference"], analysis="Master of Works control of one secret project does not establish sovereign AI rule, general guarantees or a civilian nonworking fraction.", follow_up="Skip a deeper novel investigation in the faster pass."),
    decision("c0181", "boundary_case", "The Ultras are working interstellar crews and traders, not a verified common post-work welfare society.", ["src-reynolds-ultras-context"], analysis="Ship automation and long hibernation do not erase crew labor or establish labor-independent access for every Ultra.", follow_up="Preserve as a spacer-work comparison and skip deeper reading."),
    decision("c0182", "duplicate", "The established pre-plague Glitter Band is already represented within the Yellowstone demarchy record.", ["src-glitterband-sfandf", "src-glitterband-political-review"], analysis="The earlier record explicitly includes the participating habitats and their abundance/voting institutions. Orbital location and another novel do not create another materially different economic point.", follow_up="Link further same-regime evidence to the existing record. Split a specific habitat only if its production or access rules materially differ and are clearly documented.", duplicate_of="yellowstone-demarchy-preplague"),
    decision("c0183", "needs_evidence", "The broad Pattern-Juggler-associated lead lacks one identified community with clear automatic material provision.", ["src-reynolds-ultras-context"], analysis="A technology/ecology for storing or transmitting mental patterns does not itself establish a shared economic constitution. The quick check did not identify a qualifying allocation system.", follow_up="Skip deeper reading and require a named community plus a direct economic reference before reopening.")
]
write_batch(34, [f"c{i:04}" for i in range(179, 184)], S, [], D, [
    "Reference-led pass with explicit non-inclusions; no primary-text recovery undertaken.",
    "Automatic military production, surviving city maintenance, hibernating crews and mental-pattern storage do not automatically establish civilian work-independent guarantees.",
    "Glitter Band is an economic duplicate of the already encompassing pre-plague Yellowstone demarchy record; the duplicate is linked rather than counted again.",
    "The Tampere thesis's direct open returned an Anubis access-denied page, which was respected. Its public indexed passage remains labeled indexed-only."
])
