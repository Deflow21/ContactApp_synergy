class Project:
    def __init__(self):
        self.contacts = []

    def add_contact(self, contact):
        self.contacts.append(contact)

    def remove_contact(self, contact):
        self.contacts.remove(contact)

    def get_contacts_sorted(self):
        return sorted(self.contacts, key=lambda c: c.last_name)

    def search_contacts(self, query):
        """Возвращает список контактов, чьи фамилии или имена содержат подстроку query."""
        query = query.lower()
        return [
            contact for contact in self.contacts
            if query in contact.last_name.lower() or query in contact.first_name.lower()
        ]

    def __str__(self):
        return "\n".join(str(contact) for contact in self.contacts)