import pytest
import os
from ContactApp.project import Project
from ContactApp.project_manager import ProjectManager
from ContactApp.contact_model import Contact
from ContactApp.phone_number import PhoneNumber
import datetime

TEST_FILE = "./test_contacts.notes"

def test_project_manager_save_and_load():
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

    # Сохранение
    ProjectManager.FILE_PATH = TEST_FILE
    ProjectManager.save_to_file(project)

    # Загрузка
    loaded_project = ProjectManager.load_from_file()

    assert len(loaded_project.contacts) == 1
    assert loaded_project.contacts[0].last_name == "Иванов"

    # Удаление тестового файла
    os.remove(TEST_FILE)