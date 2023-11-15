"""Track performance score example (beginner).

This example shows how to use the most basic features of the scoretree module,
which is the generation of a score list (not actually a tree, due to its
simplicity) from a list of Score instances.

Author:
    Paulo Sanchez (@erlete)
"""

from scoretree import Score, ScoreTree

st = ScoreTree([
    # Top speed score that weights 60% of the total score, can have any value
    #   between 0 and 100, and has a current value of 48.12. The higher the
    #   top speed, the better the score.
    Score(
        name="Top speed (m/s)",
        weight=0.5,
        score_range=(0, 100),
        value=48.12
    ),
    # Elapsed time score. This time, the score is inverted, since the lower
    #   the time, the better the score.
    Score(
        name="Elapsed time (s)",
        weight=0.3,
        score_range=(20, 60),
        value=31.2,
        inverse=True
    ),
    Score(
        name="Traveled distance (m)",
        weight=0.2,
        score_range=(250, 785),
        value=327.12,
        inverse=True
    )
], colorized=True)

print(f"{' Score list ':=^80}\n{st}")
print(f"{f' Total track score: {st.score * 100:.2f} ':=^80}")
