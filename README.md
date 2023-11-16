# ScoreTree

[![PyPI Release](https://github.com/erlete/scoretree/actions/workflows/python-publish.yml/badge.svg)](https://github.com/erlete/scoretree/actions/workflows/python-publish.yml) [![Package Build and Test](https://github.com/erlete/scoretree/actions/workflows/python-tests.yml/badge.svg)](https://github.com/erlete/scoretree/actions/workflows/python-tests.yml) [![Coverage Status](https://coveralls.io/repos/github/erlete/scoretree/badge.svg?branch=stable)](https://coveralls.io/github/erlete/scoretree?branch=stable) ![Python Version](https://img.shields.io/badge/Python%20Version-3.10-blue)

**ScoreTree is an *easy to use*, *multi-level* grade weighting system that serves as excellent tool for cascade grading methods.**

## Installation

This package [has been released through PyPI](https://pypi.org/project/scoretree/), so it can be installed using Python's `pip` module:

```shell
python -m pip install scoretree
```

> [!NOTE]
> The command above asumes that your Python interpreter is aliased to `python` and references a version equal to or greater than 3.10

Alternatively, it is also possible to clone this repository and install the package via `pip` and/or `build`.

## Usage

Here is an usage example. Feel free to take a look at [other examples](src/examples/) in the corresponding section of the repository.

```python
from scoretree import Score, ScoreArea, ScoreTree

# Define a score tree:
st = ScoreTree([
    # Add a list of areas to be evaluated:
    ScoreArea(name=f"Simulation", weight=1, items=[
        # Each area can contain other areas and/or scores:
        ScoreArea("Stop maneuver", .2, [
            # Scores are the minimal grading unit:
            Score(
                name="Distance to end",
                weight=.8,
                score_range=(0, 10),
                value=9.8848,
                inverse=True
            ),
            Score("Deceleration intensity", .2, (0, 20), value=185555)
        ]),
        # Different instance creation syntax:
        ScoreArea("Track performance", .8, [
            Score("Speed", .3, (0, 20), 5),
            ScoreArea("Efficiency", .7, [
                Score("Track time", .5, (0, 40), 30),
                Score("Track distance", .5, (0, 200), value=10, inverse=True)
            ])
        ])
    ])
], colorized=True)  # Enable or disable colorized output.

print(f"Total simulation score: {st.score}")
```

This would be the colorized output for the code snippet above:

![sample_output](https://github.com/erlete/scoretree/assets/76848729/260d4e88-160a-4b4f-bcc4-568691c0bbca)

## Contributing

Since this is a very small project that can be easily improved and can expand its functionality way further down the development process, any contributions, suggestions or bug reports are more than welcome!
