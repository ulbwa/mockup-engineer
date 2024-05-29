from pathlib import Path
from uuid import UUID

from mockup_engineer import TemplateStorage, FileRepository, PilRenderer

# Initialize a TemplateStorage object to manage templates
storage = TemplateStorage()

# Import templates from a file repository located at "./file_repository"
storage.import_from_repository(FileRepository(Path("./file_repository")))

# Retrieve a specific template using its UUID
template = storage.get_template_by_id(UUID("50cf93e1-9ab8-4754-9a15-0aa44237e9f8"))

# Path to the image file that will be used for rendering the template
screenshot_path = Path("./funny_cat.jpg")

# Render the template with the provided image using PilRenderer
rendered_template = PilRenderer.render(template, screenshot_path)

# Save the rendered template to a file named "destination.png"
with Path("./destination.png").open("wb") as destination_file:
    destination_file.write(rendered_template.to_bytes())
