
from app import LOGO_HEIGHT, LOGO_HEIGHT_MAX

def test_no_prof_changes_logo_above_max():
    assert LOGO_HEIGHT <= LOGO_HEIGHT_MAX
    