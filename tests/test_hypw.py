# tests/test_hypw.py
import numpy as np
import pytest
from hypw.hypw import filename

# Test cases for the filename function
def test_filename_checkboard():
    assert filename((2, 3, 7), style="checkboard") == "237-checkboard.png"
    assert filename((2, 3, np.inf), style="checkboard") == "23i-checkboard.png"

def test_filename_edged():
    assert filename((4, 5, 6), style="edged") == "456-edged.png"
    assert filename((np.inf, 5, 6), style="edged") == "i56-edged.png"

def test_filename_patterned():
    assert filename((2, 3, 7), style="patterned", form_idx=0, pat_id=5) == "237-patterned-form0-pat005.png"
    assert filename((2, 3, 7), style="patterned", form_idx=1, pat_id=127) == "237-patterned-form1-pat127.png"
    assert filename((np.inf, 3, np.inf), style="patterned", form_idx=2, pat_id=0) == "i3i-patterned-form2-pat000.png"

def test_filename_invalid_style():
    with pytest.raises(ValueError, match="Unknown style for filename: invalid"):
        filename((2,3,7), style="invalid")

def test_filename_patterned_missing_params():
    with pytest.raises(ValueError, match="form_idx and pat_id are required for patterned style filenames."):
        filename((2,3,7), style="patterned", form_idx=0) # Missing pat_id
    with pytest.raises(ValueError, match="form_idx and pat_id are required for patterned style filenames."):
        filename((2,3,7), style="patterned", pat_id=0) # Missing form_idx
    with pytest.raises(ValueError, match="form_idx and pat_id are required for patterned style filenames."):
        filename((2,3,7), style="patterned") # Missing both
