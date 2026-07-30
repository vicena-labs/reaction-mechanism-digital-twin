# Getting started
Part of the [Vicena Research Twins collection](https://vicena.ai).

```bash
python -m venv .venv
. .venv/bin/activate
pip install -e .[dev,chem]
pytest -q
python scripts/validate_reaction.py reactions/example/reaction.json
python scripts/analyze_archived.py
```
This is an analysis and validation starter. The barrier, frequency, and IRC example is synthetic and archived. It does not compute a new mechanism. Add uploads in a new reaction folder and validate every unit and condition before comparison.


Continue with the eight-stage guide in [GUIDED_WORKFLOW.md](GUIDED_WORKFLOW.md).
