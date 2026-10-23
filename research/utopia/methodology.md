# Utopian / dystopian assessment

This is an additional editorial parameter requested by the user on 2026-10-21.
It rates each retained society/period/continuity/ending, rather than an entire
franchise. Research revision 056 subsequently aligned all economic classifications
and four records' axes with article.txt. Wellbeing review 002 explicitly reaffirmed
all numerical ratings against those changes; their scale is independent of regime.

## Scale

`utopia_score` ranges from **-1 (strong dystopia)** through **0 (mixed or
unclear)** to **+1 (strong utopia)**. Ratings use coarse 0.05 steps; decimal
values are judgments for comparison, not measurements or canonical statistics.
The centre is deliberately used when conditions are ambiguous or poorly
specified, as requested. A zero is still an explicit reviewed assessment.

Assess material security, health and continuity of life together with agency,
freedom of exit, coercion, violence, exclusion and exploitation. Consider
cooperation and meaningful chosen activity positively. Continued useful work
does not itself reduce a rating; unemployment or leisure does not increase it.
Machine rule, public ownership and private ownership receive no automatic moral
sign. Material comfort can coexist with dystopia.

The unit is the existing record's scoped population and period. Systemic harm
to other sentient workers or excluded populations described by that record
qualifies an enclave's apparent comfort. Do not treat robot persons as mere
equipment or dead populations as satisfied citizens. Distinguish a functioning
baseline, a catastrophic phase, a reform and a projected ending. This rating
concerns living conditions and institutions, not whether the fiction is dark,
whether its protagonist is happy, or whether a future catastrophe occurs.

## Evidence and uncertainty

This pass reuses the supplied research corpus: descriptions, scope, evidence,
canonical-fact lists, assumptions and registered sources. It does not claim a
new reading of every work or a fresh independent verification of its lore.
Two bounded checks supplement the saved economic descriptions: the
[Scythe publisher synopsis and excerpt](https://www.simonandschuster.com/books/Scythe/Neal-Shusterman/Arc-of-a-Scythe/9781442472433)
describe the coexistence of material safety and population-control killing;
the [SFE Silverberg entry](https://sf-encyclopedia.com/entry/silverberg_robert)
characterizes The World Inside as a dystopian high-density society. Their
scope and limits are recorded separately in the annotation overlay.
The rationale expresses
the main considerations behind an individually selected number. Where the
corpus provides little about freedom, everyday life or distribution, use a
central estimate rather than infer utopia from technology alone.

Every assessment is explicitly `low` confidence: evidence varies and the
normative weighting is inherently contestable. This is not a population poll,
a universal moral ranking, or an inference from the existing numeric axes.
The same franchise may legitimately have positive and negative entries.

## Persistence and review

The original `review-index.json` remains historical. The current overlay selects
`review-index-v2.json`, which freezes the reviewed article-aligned research and
assets after the explicit re-review. `manual-ratings.txt` contains an
explicit score and rationale code for each index. The writer refuses missing,
duplicate or reordered identities and changes to the reviewed research input.
`data/society-utopia.json` is the durable annotation overlay. Explicit changes
to a saved annotation are retained under `revisions/`; the normal merger
adds `utopia_score` and `utopia_assessment` to `data/societies.json`. It must not
derive scores from guarantees, control, participation or regime numbers.

`scripts/validate_utopia.py` checks coverage, range, source links, fingerprint,
overlay equivalence and preservation of the active reviewed research/asset values.
It also reports central scores and distinct franchise-period examples.
An ordinary research rebuild retains the overlay and rejects stale ratings
if the underlying reviewed research changes.
