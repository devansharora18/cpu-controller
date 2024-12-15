# CPU Cores Controller

This is a PyQt6 application to control the state of CPU cores on a Linux system. The application allows you to enable or disable individual CPU cores or a range of CPU cores.

## Features

- **Enable/Disable Individual Cores**: Click on the CPU core buttons to toggle their state.
- **Enable/Disable Range of Cores**: Use the "Disable Range" and "Enable Range" buttons to specify a range of cores to disable or enable.
- **Dynamic Core Detection**: Automatically detects the number of CPU cores on your system.

## Requirements

- Python 3.x
- PyQt6
- Root privileges (sudo access)

## Installation

1. Clone the repository:
	```sh
	git clone https://github.com/devansharora18/cpu-controller.git
	cd cpu-controller
	```

2. Install the required Python packages:
	```sh
	pip install -r requirements.txt
	```

3. Run the application:
	```sh
	sudo python3 main.py
	```

## Usage

- **Toggle Individual Cores**: Click on the CPU core buttons to enable or disable them.
- **Disable Range**: Click on the "Disable Range" button and enter the start and end core indices to disable.
- **Enable Range**: Click on the "Enable Range" button and enter the start and end core indices to enable.

## Screenshots

![CPU Cores Controller](image.png)

## License

This project is licensed under the MIT License.