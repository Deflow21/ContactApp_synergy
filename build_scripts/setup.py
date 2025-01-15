from cx_Freeze import setup, Executable

setup(
    name="ContactApp",
    version="1.0",
    description="Contact Management Application",
    executables=[Executable("ContactApp/contacts_app.py")]
)