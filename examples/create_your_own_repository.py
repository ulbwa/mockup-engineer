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
