import pytest
from src.core.hash_utils import detect_algorithm, get_algorithm_instance

def test_detect_algorithm():
    assert detect_algorithm("5f4dcc3b5aa765d61d8327deb882cf99") == "md5"
    assert detect_algorithm("9f86d081884c7d659a2feaa0c55ad015a3bf4f1b2b0b822cd15d6c15b0f00a08") == "sha256"
    assert detect_algorithm("invalid") is None

def test_algorithm_hashing():
    md5 = get_algorithm_instance("md5")
    assert md5.hash("password") == "5f4dcc3b5aa765d61d8327deb882cf99"
    assert md5.verify("password", "5f4dcc3b5aa765d61d8327deb882cf99")

    sha256 = get_algorithm_instance("sha256")
    assert sha256.hash("password") == "5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8"
