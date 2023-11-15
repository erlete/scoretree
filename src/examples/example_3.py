"""Track performance score example (intermediate).

This example explores the nesting capabilities of the ScoreArea class in
combination with the Score class, allowing complex score trees to be created.

Author:
    Paulo Sanchez (@erlete)
"""

from scoretree import Score, ScoreArea, ScoreTree

st = ScoreTree([
    ScoreArea("Track 1", 1, [
        ScoreArea("Dynamics", 0.6, [
            Score("Top speed (m/s)", 0.5, (0, 100), 88.2),
            Score("Elapsed time (s)", 0.3, (20, 60), 31.2, True),
            Score("Traveled distance (m)", 0.2, (250, 785), 327.12, True)
        ]),
        ScoreArea("Efficiency", 0.4, [
            Score("Fuel consumption (l)", 0.72, (39.13, 69.32), 58.12, True),
            ScoreArea("Energy consumption", 0.28, [
                Score("Battery consumption (kWh)", 0.65, (0, 43.74), 6, True),
                Score("Regenerative braking (kWh)", 0.35, (0, 16.1), 8.16)
            ])
        ])
    ])
], colorized=True)

print(f"{' Score tree ':=^80}\n{st}")
print(f"{f' Total track score: {st.score * 100:.2f} ':=^80}")
