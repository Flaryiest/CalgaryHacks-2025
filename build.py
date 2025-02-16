import os
import PyInstaller.__main__

script_path = os.path.join(os.getcwd(), "main.py")
output_dir = os.path.join(os.getcwd(), "dist")

PyInstaller.__main__.run(
    [
        script_path,
        "--onefile",
        "--windowed",
        "--distpath",
        output_dir,
        "--name",
        "SaveTheAnimals",
    ]
)
