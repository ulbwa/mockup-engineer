# MockupEngineer

`mockup_engineer` is a Python-based project designed to facilitate the creation and management of device mockups. 

This tool allows users to import, manage, and render templates for various devices, such as smartphones, tablets, and computers. 

With a focus on flexibility and ease of use, mockup_engineer supports the handling of device specifications, rendering templates 
with screenshots, and saving rendered images.

## Features

- File Repository Management: Import and store templates and device information.
- Device Management: Define and manage device specifications including manufacturer, name, type, resolution, and rotation capability.
- Template Rendering: Render templates with screenshots and custom frame images using the PilRenderer.
- Flexible Design: Support for different device types and customizable template properties.

## Getting Started

Prerequisites
Ensure you have the following installed:

- Python 3.10 or later
- Poetry (for dependency management)

## Installation
Clone the repository and install the necessary dependencies using Poetry:


```sh 
poetry add git+https://github.com/ulbwa/mockup-engineer.git
```

## Usage

```python
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
```

### Manage your templates

```python
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
```

### Create your own repository with templates

```python
from pathlib import Path
from uuid import uuid4

from mockup_engineer import (
    FileRepository,
    Device,
    Template,
    DeviceType,
    Size2D,
    Point2D,
    FileReader,
    Color,
)

repository_path = Path("./my_new_repository")
repository_path.mkdir(exist_ok=True)
repository_path.joinpath("config.json").touch(exist_ok=True)

# Initialize a FileRepository object
repository = FileRepository(repository_path)

# Create a Device object
device = Device(
    id=uuid4(),
    manufacturer="Google",
    name="Pixel 6",
    type=DeviceType.SMARTPHONE,
    resolution=Size2D(1080, 2400),
    can_rotate=True,
)

# Create a Template object for the device
template = Template(
    id=uuid4(),
    color=Color("Black"),
    device=device,
    screenshot_size=Size2D(1080, 2400),
    screenshot_start_point=Point2D(200, 200),
    frame=FileReader(Path("./my_new_repository/pixel_6_black_frame.png")),
)

# Save the device information to the repository
repository.save(device)
```