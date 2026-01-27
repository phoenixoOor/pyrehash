import pytest
import os
from src.attacks.dictionary_attack import DictionaryAttack
from src.attacks.brute_force_attack import BruteForceAttack

def test_dictionary_attack(tmp_path):
    dict_file = tmp_path / "dict.txt"
    dict_file.write_text("admin\npassword\n123456")
    
    target = "5f4dcc3b5aa765d61d8327deb882cf99" # md5 for 'password'
    engine = DictionaryAttack(target, "md5")
    result = engine.run(str(dict_file))
    
    assert result == "password"

def test_brute_force_attack():
    target = "5f4dcc3b5aa765d61d8327deb882cf99" # md5 for 'password'
    # 'password' is too long for a quick test, let's use 'abc'
    target_abc = "900150983cd24fb0d6963f7d28e17f72" # md5 for 'abc'
    engine = BruteForceAttack(target_abc, "md5")
    result = engine.run("abc", 1, 3)
    
    assert result == "abc"
