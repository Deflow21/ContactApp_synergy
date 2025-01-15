import pytest
from ContactApp.contact_model import Contact
from ContactApp.phone_number import PhoneNumber
import datetime

def test_contact_creation_valid():
    contact = Contact(
        last_name="Иванов",
        first_name="Иван",
        phone_number=PhoneNumber("79991234567"),
        birth_date=datetime.date(1990, 1, 1),
        email="ivan@example.com",
        vk_id="ivan_vk"
    )
    assert contact.last_name == "Иванов"
    assert contact.first_name == "Иван"
    assert str(contact.phone_number) == "79991234567"

def test_contact_invalid_last_name():
    with pytest.raises(ValueError):
        Contact(
            last_name="ИвановИвановИвановИвановИвановИвановИвановИвановИвановИвановИванов",
            first_name="Иван",
            phone_number=PhoneNumber("79991234567"),
            birth_date=datetime.date(1990, 1, 1),
            email="ivan@example.com",
            vk_id="ivan_vk"
        )