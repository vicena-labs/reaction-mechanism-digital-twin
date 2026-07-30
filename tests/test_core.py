from pathlib import Path
import sys
import pytest
ROOT = Path(__file__).parents[1]
sys.path.insert(0, str(ROOT / 'src'))
from reaction_mechanism_twin import *
EXCLUDED_TREES = {'.git', '.venv', 'venv', '.pytest_cache', '__pycache__', 'build', 'dist'}
TEXT_SUFFIXES = {'.md', '.py', '.json', '.toml', '.csv', '.cff', '.yml', '.yaml', '.html', '.xml'}
def repository_files():
    for path in ROOT.rglob('*'):
        if path.is_file() and not any(part in EXCLUDED_TREES for part in path.parts): yield path
def m(): return load(ROOT / 'reactions/example/reaction.json')
def r(): return load(ROOT / 'results/example/archived_result.json')
def test_conservation(): assert validate(m())['atoms'] == 16
def test_charge_spin(): assert validate(m())['charge'] == 0 and validate(m())['multiplicity'] == 1
def test_bad_mapping():
    x = m(); x['atom_mapping'][0] = 2
    with pytest.raises(ValueError): validate(x)
def test_units(): assert abs(EH - 627.509474) < 1e-8
def test_eyring(): assert 1e-8 < eyring(27, 298.15) < 1e-6
def test_arrhenius(): assert arrhenius(1e13, 27, 298.15) > 0
def test_ts_gate(): assert accept_ts(r())['accepted']
def test_irc_gate():
    x = r(); x['irc']['forward_endpoint'] = 'wrong'; assert not accept_ts(x)['accepted']
def test_rowan_uuid(): assert parse_rowan(ROOT / 'results/example/rowan_archived.json')['workflow_uuid'] == 'ARCHIVED-NOT-LIVE'
def test_uuid_reuse(): assert task_key({'x': 1}) == task_key({'x': 1})
def test_no_submit_notebooks():
    suffix = '.' + ''.join(['i','p','y','n','b'])
    for path in (ROOT / 'notebooks').glob('*' + suffix): assert 'rowan.' + 'submit_' not in path.read_text(errors='ignore')
def test_no_em_dash():
    for path in repository_files():
        if path.suffix in TEXT_SUFFIXES: assert chr(8212) not in path.read_text(errors='ignore'), path
