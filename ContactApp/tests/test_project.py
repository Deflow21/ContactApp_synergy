import pytest
from ContactApp.project import Project
from ContactApp.contact_model import Contact
from ContactApp.phone_number import PhoneNumber
import datetime


def test_project_add_contact():
    project = Project()
    contact = Contact(
        last_name="Иванов",
        first_name="Иван",
        phone_number=PhoneNumber("79991234567"),
        birth_date=datetime.date(1990, 1, 1),
        email="ivan@example.com",
        vk_id="ivan_vk"
    )
    project.add_contact(contact)
    assert len(project.contacts) == 1
    assert project.contacts[0].last_name == "Иванов"


def test_project_remove_contact():
    project = Project()
    contact = Contact(
        last_name="Иванов",
        first_name="Иван",
        phone_number=PhoneNumber("79991234567"),
        birth_date=datetime.date(1990, 1, 1),
        email="ivan@example.com",
        vk_id="ivan_vk"
    )
    project.add_contact(contact)
    assert len(project.contacts) == 1

    # Удаление контакта
    project.contacts.remove(contact)
    assert len(project.contacts) == 0


def test_project_search_contacts():
    project = Project()
    contact1 = Contact(
        last_name="Петров",
        first_name="Петр",
        phone_number=PhoneNumber("79991112233"),
        birth_date=datetime.date(1995, 5, 10),
        email="petr@example.com",
        vk_id="petr_vk"
    )
    contact2 = Contact(
        last_name="Иванов",
        first_name="Иван",
        phone_number=PhoneNumber("79991234567"),
        birth_date=datetime.date(1990, 1, 1),
        email="ivan@example.com",
        vk_id="ivan_vk"
    )
    project.add_contact(contact1)
    project.add_contact(contact2)

    # Поиск по подстроке
    result = project.search_contacts("Иван")
    assert len(result) == 1
    assert result[0].last_name == "Иванов"