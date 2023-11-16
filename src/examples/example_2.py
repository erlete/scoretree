"""Track performance score example (beginner).

This example introduces the ScoreArea class, which allows for the creation of
nested score areas, which in turn can contain other score areas and/or scores.

Author:
    Paulo Sanchez (@erlete)
"""

from scoretree import Score, ScoreArea, ScoreTree

st = ScoreTree([
    ScoreArea(name="Track 1", weight=0.4, items=[
        Score("Top speed (m/s)", 0.5, (0, 100), 48.12),
        Score("Elapsed time (s)", 0.3, (20, 60), 31.2, True),
        Score("Traveled distance (m)", 0.2, (250, 785), 327.12, True)
    ]),
    ScoreArea(name="Track 2", weight=.6, items=[
        Score("Top speed (m/s)", 0.5, (0, 100), 72.32),
        Score("Elapsed time (s)", 0.3, (20, 60), 26.2, True),
        Score("Traveled distance (m)", 0.2, (250, 785), 295.12, True)
    ])
], colorized=True)

print(f"{' Score tree ':=^80}\n{st}")
print(f"{f' Total simulation score: {st.score * 100:.2f} ':=^80}")
