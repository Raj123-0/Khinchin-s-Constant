import importlib.util
import os
import pytest

def test_khinchin_computation(tmp_path):
    orig_dir = os.getcwd()
    os.chdir(tmp_path)
    try:
        # Use double quotes to avoid syntax errors if the path contains single quotes
        spec = importlib.util.spec_from_file_location("khinchin", "MODULE_FILENAME")
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        
        # Test with 10 digits
        digits = module.compute_khinchin_hpc(10)
        
        # Khinchin's constant is 2.685452001...
        assert digits == "2685452001"
        
        # Check files
        raw_file = tmp_path / "Khinchin_10_digits.txt"
        b_file = tmp_path / "b_file_Khinchin_10.txt"
        
        assert raw_file.exists()
        assert b_file.exists()
        
        assert raw_file.read_text(encoding="utf-8") == "2685452001"
        
        b_content = b_file.read_text(encoding="utf-8").splitlines()
        assert len(b_content) == 10
        assert b_content[0] == "1 2"
        assert b_content[1] == "2 6"
        assert b_content[9] == "10 1"
    finally:
        os.chdir(orig_dir)
