from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, QWidget,
    QPushButton, QListWidget, QLabel, QDialog, QFormLayout, QLineEdit, QMessageBox, QFileDialog
)
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
from ContactApp.project import Project
from ContactApp.contact_model import Contact
from ContactApp.phone_number import PhoneNumber
import datetime
import sys


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("ContactsApp")
        self.setMinimumSize(800, 600)

        # Экземпляр Project
        self.project = Project()

        # Главный контейнер
        main_widget = QWidget()
        main_layout = QHBoxLayout()

        # Список контактов
        self.contacts_list = QListWidget()
        self.contacts_list.itemSelectionChanged.connect(self.display_contact_details)
        main_layout.addWidget(self.contacts_list, stretch=2)

        # Правая панель
        right_panel = QVBoxLayout()

        # Виджет для отображения аватара
        self.avatar_label = QLabel()
        self.avatar_label.setFixedSize(100, 100)
        self.avatar_label.setStyleSheet("border: 1px solid black;")  # Рамка вокруг аватара
        self.avatar_label.setAlignment(Qt.AlignCenter)
        self.avatar_label.hide()
        right_panel.addWidget(self.avatar_label, stretch=0)

        # Виджет для деталей контакта
        self.contact_details = QLabel("Выберите контакт для просмотра деталей")
        self.contact_details.setAlignment(Qt.AlignTop)
        self.contact_details.setWordWrap(True)
        right_panel.addWidget(self.contact_details, stretch=1)

        # Кнопки
        buttons_layout = QHBoxLayout()
        self.add_contact_button = QPushButton("Добавить контакт")
        self.edit_contact_button = QPushButton("Редактировать контакт")
        self.remove_contact_button = QPushButton("Удалить контакт")

        buttons_layout.addWidget(self.add_contact_button)
        buttons_layout.addWidget(self.edit_contact_button)
        buttons_layout.addWidget(self.remove_contact_button)

        right_panel.addLayout(buttons_layout)
        main_layout.addLayout(right_panel, stretch=3)

        main_widget.setLayout(main_layout)
        self.setCentralWidget(main_widget)

        # Сигналы
        self.add_contact_button.clicked.connect(self.add_contact)
        self.edit_contact_button.clicked.connect(self.edit_contact)
        self.remove_contact_button.clicked.connect(self.remove_contact)

    def add_contact(self):
        dialog = ContactForm(self)
        if dialog.exec_() == QDialog.Accepted:
            contact_data = dialog.get_contact_data()
            if contact_data:
                contact = Contact(**contact_data)
                self.project.add_contact(contact)
                self.update_contacts_list()

    def edit_contact(self):
        current_row = self.contacts_list.currentRow()
        if current_row == -1:
            return  # Ничего не выбрано

        contact = self.project.contacts[current_row]
        dialog = ContactForm(self, contact)
        if dialog.exec_() == QDialog.Accepted:
            updated_data = dialog.get_contact_data()
            if updated_data:
                contact.last_name = updated_data["last_name"]
                contact.first_name = updated_data["first_name"]
                contact.phone_number = updated_data["phone_number"]
                contact.birth_date = updated_data["birth_date"]
                contact.email = updated_data["email"]
                contact.vk_id = updated_data["vk_id"]
                contact.avatar = updated_data.get("avatar", contact.avatar)
                self.update_contacts_list()

    def remove_contact(self):
        current_row = self.contacts_list.currentRow()
        if current_row != -1:
            self.project.contacts.pop(current_row)
            self.update_contacts_list()
            if not self.project.contacts:
                self.clear_contact_details()

    def display_contact_details(self):
        current_row = self.contacts_list.currentRow()
        if current_row != -1 and current_row < len(self.project.contacts):
            contact = self.project.contacts[current_row]
            details = "\n".join(
                [
                    f"Фамилия: {contact.last_name}" if contact.last_name else "",
                    f"Имя: {contact.first_name}" if contact.first_name else "",
                    f"Телефон: {contact.phone_number.number}" if contact.phone_number else "",
                    f"Дата рождения: {contact.birth_date}" if contact.birth_date else "",
                    f"Email: {contact.email}" if contact.email else "",
                    f"ID ВКонтакте: {contact.vk_id}" if contact.vk_id else "",
                ]
            )
            self.contact_details.setText(details)

            # Отображение аватара
            if contact.avatar:
                pixmap = QPixmap(contact.avatar).scaled(
                    self.avatar_label.width(),
                    self.avatar_label.height(),
                    Qt.KeepAspectRatio,
                    Qt.SmoothTransformation
                )
                self.avatar_label.setPixmap(pixmap)
            else:
                self.avatar_label.clear()
                self.avatar_label.setText("Нет фото")
            self.avatar_label.show()
        else:
            self.clear_contact_details()
        self.avatar_label.setStyleSheet("border: none;") 

    def clear_contact_details(self):
        self.contact_details.setText("Выберите контакт для просмотра деталей")
        self.avatar_label.clear()
        self.avatar_label.hide() 

    def update_contacts_list(self):
        self.contacts_list.clear()
        for contact in self.project.contacts:
            display_name = f"{contact.first_name or ''} {contact.last_name or ''}".strip()
            self.contacts_list.addItem(display_name)

class ContactForm(QDialog):
    def __init__(self, parent=None, contact=None):
        super().__init__(parent)
        self.setWindowTitle("Добавить/Редактировать контакт")
        self.setMinimumSize(400, 300)

        # Основной контейнер
        layout = QVBoxLayout()

        # Поля ввода
        form_layout = QFormLayout()
        self.first_name_input = QLineEdit()
        self.last_name_input = QLineEdit()
        self.phone_input = QLineEdit()
        self.email_input = QLineEdit()
        self.birth_date_input = QLineEdit()
        self.vk_id_input = QLineEdit()

        # Поле для выбора аватара
        self.avatar_path = None
        self.avatar_button = QPushButton("Выбрать аватар")
        self.avatar_button.clicked.connect(self.choose_avatar)

        form_layout.addRow("Имя:", self.first_name_input)
        form_layout.addRow("Фамилия:", self.last_name_input)
        form_layout.addRow("Телефон:", self.phone_input)
        form_layout.addRow("Email:", self.email_input)
        form_layout.addRow("Дата рождения (YYYY-MM-DD):", self.birth_date_input)
        form_layout.addRow("ID ВКонтакте:", self.vk_id_input)
        form_layout.addRow("Аватар:", self.avatar_button)

        layout.addLayout(form_layout)

        # Заполнение формы, если редактируется контакт
        if contact:
            self.first_name_input.setText(contact.first_name or "")
            self.last_name_input.setText(contact.last_name or "")
            self.phone_input.setText(contact.phone_number.number or "")
            self.email_input.setText(contact.email or "")
            self.birth_date_input.setText(contact.birth_date.isoformat() if contact.birth_date else "")
            self.vk_id_input.setText(contact.vk_id or "")
            if contact.avatar:
                self.avatar_path = contact.avatar
                self.avatar_button.setText("Изменить аватар")

        # Кнопки
        buttons_layout = QHBoxLayout()
        self.save_button = QPushButton("Сохранить")
        self.cancel_button = QPushButton("Отмена")

        buttons_layout.addWidget(self.save_button)
        buttons_layout.addWidget(self.cancel_button)
        layout.addLayout(buttons_layout)

        self.setLayout(layout)

        # Сигналы
        self.save_button.clicked.connect(self.accept)
        self.cancel_button.clicked.connect(self.reject)

    def choose_avatar(self):
        """Открывает диалог выбора файла для аватара."""
        avatar_path, _ = QFileDialog.getOpenFileName(self, "Выберите аватар", "", "Images (*.png *.jpg *.jpeg)")
        if avatar_path:
            self.avatar_path = avatar_path
            self.avatar_button.setText("Аватар выбран")

    def get_contact_data(self):
        # Проверяем, заполнены ли обязательные поля: имя и телефон
        if not self.first_name_input.text() or not self.phone_input.text():
            QMessageBox.warning(self, "Ошибка", "Поля 'Имя' и 'Телефон' обязательны для заполнения!")
            return None

        # Обрабатываем данные
        try:
            birth_date = None
            if self.birth_date_input.text().strip():  # Проверяем, что дата не пустая
                try:
                    birth_date = datetime.date.fromisoformat(self.birth_date_input.text().strip())
                except ValueError:
                    QMessageBox.warning(self, "Ошибка", "Дата рождения должна быть в формате YYYY-MM-DD!")
                    return None

            return {
                "first_name": self.first_name_input.text().strip(),
                "last_name": self.last_name_input.text().strip() or None,
                "phone_number": PhoneNumber(self.phone_input.text().strip()),
                "birth_date": birth_date,  # datetime.date или None
                "email": self.email_input.text().strip() or None,
                "vk_id": self.vk_id_input.text().strip() or None,
                "avatar": self.avatar_path,  # Путь к аватару
            }
        except Exception as e:
            QMessageBox.warning(self, "Ошибка", f"Ошибка ввода данных: {e}")
            return None

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())