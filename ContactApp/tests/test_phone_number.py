import pytest
from ContactApp.phone_number import PhoneNumber

def test_phone_number_valid():
    number = PhoneNumber("79991234567")
    assert number.number == "79991234567"

def test_phone_number_invalid_length():
    with pytest.raises(ValueError):
        PhoneNumber("123456")

def test_phone_number_invalid_prefix():
    with pytest.raises(ValueError):
        PhoneNumber("89991234567")