import datetime
from copy import deepcopy

class Contact:
    def __init__(self, last_name, first_name, phone_number, birth_date=None, email=None, vk_id=None, avatar=None):
        self.last_name = last_name
        self.first_name = first_name
        self.phone_number = phone_number
        self.birth_date = birth_date
        self.email = email
        self.vk_id = vk_id
        self.avatar = avatar

    @property
    def last_name(self):
        return self._last_name

    @last_name.setter
    def last_name(self, value):
        if value is not None and len(value) > 50:
            raise ValueError("Фамилия не должна превышать 50 символов.")
        self._last_name = value.capitalize() if value else None

    @property
    def first_name(self):
        return self._first_name

    @first_name.setter
    def first_name(self, value):
        if len(value) > 50:
            raise ValueError("Имя не должно превышать 50 символов.")
        self._first_name = value.capitalize()

    @property
    def birth_date(self):
        return self._birth_date

    @birth_date.setter
    def birth_date(self, value):
        if value is None:
            self._birth_date = None
        elif isinstance(value, str):
            try:
                parsed_date = datetime.date.fromisoformat(value)
                if parsed_date.year < 1900 or parsed_date > datetime.date.today():
                    raise ValueError("Дата рождения должна быть между 1900 годом и сегодняшним днём.")
                self._birth_date = parsed_date
            except ValueError:
                raise ValueError("Дата рождения должна быть строкой в формате YYYY-MM-DD.")
        elif isinstance(value, datetime.date):
            if value.year < 1900 or value > datetime.date.today():
                raise ValueError("Дата рождения должна быть между 1900 годом и сегодняшним днём.")
            self._birth_date = value
        else:
            raise ValueError("Дата рождения должна быть объектом datetime.date или строкой в формате YYYY-MM-DD.")

    @property
    def email(self):
        return self._email

    @email.setter
    def email(self, value):
        if value is not None and len(value) > 50:
            raise ValueError("Email не должен превышать 50 символов.")
        self._email = value

    @property
    def vk_id(self):
        return self._vk_id

    @vk_id.setter
    def vk_id(self, value):
        if value is not None and len(value) > 15:
            raise ValueError("ID ВКонтакте не должен превышать 15 символов.")
        self._vk_id = value

    def clone(self):
        return deepcopy(self)

    def to_dict(self):
        return {
            "last_name": self.last_name,
            "first_name": self.first_name,
            "phone_number": self.phone_number.to_dict(),
            "birth_date": self.birth_date.isoformat() if self.birth_date else None,
            "email": self.email,
            "vk_id": self.vk_id,
            "avatar": self.avatar,
        }

    @classmethod
    def from_dict(cls, data):
        from .phone_number import PhoneNumber
        return cls(
            last_name=data["last_name"],
            first_name=data["first_name"],
            phone_number=PhoneNumber.from_dict(data["phone_number"]),
            birth_date=datetime.date.fromisoformat(data["birth_date"]) if data["birth_date"] else None,
            email=data.get("email"),
            vk_id=data.get("vk_id"),
            avatar=data.get("avatar")
        )
    
    def export_to_vcard(self):
        vcard = f"""BEGIN:VCARD
    VERSION:3.0
    FN:{self.first_name} {self.last_name}
    TEL:{self.phone_number.number}
    EMAIL:{self.email}
    END:VCARD
    """
        with open(f"{self.last_name}_{self.first_name}.vcf", "w") as file:
            file.write(vcard)

    def __str__(self):
        return f"{self.last_name} {self.first_name} ({self.phone_number})"