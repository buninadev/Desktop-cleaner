

from cx_Freeze import setup, Executable

# On appelle la fonction setup
setup(
    name = "Desktop Cleaner",
    version = "0.1",
    description = "This helps you clean your desktop from PDF/DOCX  files",
    executables = [Executable("arrange.py")],
)