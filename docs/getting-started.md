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
The example is synthetic and archived. Add uploads in a new reaction folder and validate every unit and condition before comparison.
