"""Track performance score example (advanced).

This example shows how to iteratively generate a score tree from a original
data source (i.e. a dictionary containing track results).

Author:
    Paulo Sanchez (@erlete)
"""

from scoretree import Score, ScoreArea, ScoreTree

data = {
    "track 1": {
        "top_speed": 88.2,
        "elapsed_time": 31.2,
        "traveled_distance": 327.12,
        "fuel_consumption": 58.12,
        "battery_consumption": 6,
        "regenerative_braking": 8.16
    },
    "track 2": {
        "top_speed": 72.32,
        "elapsed_time": 26.2,
        "traveled_distance": 295.12,
        "fuel_consumption": 48.12,
        "battery_consumption": 4.5,
        "regenerative_braking": 6.12
    },
    "track 3": {
        "top_speed": 92.12,
        "elapsed_time": 28.2,
        "traveled_distance": 315.12,
        "fuel_consumption": 52.12,
        "battery_consumption": 5.5,
        "regenerative_braking": 7.12
    }
}

track_weights = {
    "track 1": 0.3,
    "track 2": 0.5,
    "track 3": 0.2
}

st = ScoreTree([
    ScoreArea(track, weight, [
        ScoreArea("Dynamics", 0.6, [
            Score("Top speed (m/s)", 0.5, (0, 100), results["top_speed"]),
            Score("Elapsed time (s)", 0.3, (20, 60),
                  results["elapsed_time"], True),
            Score("Traveled distance (m)", 0.2, (250, 785),
                  results["traveled_distance"], True)
        ]),
        ScoreArea("Efficiency", 0.4, [
            Score("Fuel consumption (l)", 0.72, (39.13, 69.32),
                  results["fuel_consumption"], True),
            ScoreArea("Energy consumption", 0.28, [
                Score("Battery consumption (kWh)", 0.65, (0, 43.74),
                      results["battery_consumption"], True),
                Score("Regenerative braking (kWh)", 0.35, (0, 16.1),
                      results["regenerative_braking"])
            ])
        ])
    ])
    for (track, results), weight in zip(data.items(), track_weights.values())
], colorized=True)

print(f"{' Score tree ':=^80}\n{st}")
print(f"{f' Total simulation score: {st.score * 100:.2f} ':=^80}")
