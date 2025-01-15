import json
from .project import Project
from .contact_model import Contact

class ProjectManager:
    FILE_PATH = "./ContactsApp.notes"

    @staticmethod
    def save_to_file(project: Project):
        with open(ProjectManager.FILE_PATH, "w", encoding="utf-8") as file:
            json.dump([contact.to_dict() for contact in project.contacts], file, ensure_ascii=False)

    @staticmethod
    def load_from_file():
        project = Project()
        try:
            with open(ProjectManager.FILE_PATH, "r", encoding="utf-8") as file:
                data = json.load(file)
                for contact_data in data:
                    contact = Contact.from_dict(contact_data)
                    project.add_contact(contact)
        except FileNotFoundError:
            pass  # Файл ещё не создан
        return project