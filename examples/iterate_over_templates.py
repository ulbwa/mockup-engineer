from pathlib import Path

from mockup_engineer import TemplateStorage, FileRepository

# Initialize a TemplateStorage object to manage templates
storage = TemplateStorage()

# Import templates from a file repository located at "./file_repository"
storage.import_from_repository(FileRepository(Path("./file_repository")))

for device in storage:
    print(device)
    for template in device:
        print("\t", template)
