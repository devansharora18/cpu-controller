import sys
from PyQt6.QtWidgets import QApplication, QWidget, QMessageBox, QGridLayout, QPushButton, QLabel, QVBoxLayout, QInputDialog, QHBoxLayout
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QIcon, QFont
import subprocess
import pkg_resources
import os

os.environ["XDG_SESSION_TYPE"] = "xcb"


class CPUCoresController(QWidget):
    def __init__(self):
        super().__init__()

        self.init_ui()

    def init_ui(self):
        icon_path = pkg_resources.resource_filename(__name__, 'cpu.png')
        self.setWindowTitle('CPU Cores Controller')
        self.setMinimumSize(600, 600)

        # Dynamically determine the number of CPU cores from the filesystem
        self.num_cores = self.detect_cores()

        self.layout = QVBoxLayout()

        # Create the range control buttons (Disable and Enable Range)
        self.range_control_layout = QHBoxLayout()
        self.disable_range_button = QPushButton("Disable Range")
        self.disable_range_button.setFont(QFont('Arial', 12, QFont.Weight.Bold))
        self.disable_range_button.clicked.connect(self.disable_range)
        
        self.enable_range_button = QPushButton("Enable Range")
        self.enable_range_button.setFont(QFont('Arial', 12, QFont.Weight.Bold))
        self.enable_range_button.clicked.connect(self.enable_range)

        self.range_control_layout.addWidget(self.disable_range_button)
        self.range_control_layout.addWidget(self.enable_range_button)
        
        self.layout.addLayout(self.range_control_layout)

        # Create the grid layout for CPU core buttons
        self.grid_layout = QGridLayout()

        self.core_buttons = []
        for core in range(self.num_cores):
            button = QPushButton()
            button.setCheckable(True)
            button.setIcon(QIcon(icon_path))  # Replace with the path to your icon
            button.setIconSize(QSize(64, 64))  # Adjust the icon size
            button.clicked.connect(lambda _, core=core: self.toggle_core(core))

            # Add label to display core number below the icon
            label = QLabel(f'CPU {core}')
            label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            label.setFont(QFont('Arial', 10, QFont.Weight.Bold))  # Adjust font for a more luxurious look

            # Create a container widget to hold the button and label vertically
            container = QWidget()
            container_layout = QVBoxLayout(container)
            container_layout.addWidget(button)
            container_layout.addWidget(label)
            container_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

            self.grid_layout.addWidget(container, core // 4, core % 4)
            self.core_buttons.append(button)

        self.layout.addLayout(self.grid_layout)
        self.setLayout(self.layout)

        # Set initial core states
        self.update_core_states()

    def detect_cores(self):
        cores = 0
        while os.path.exists(f'/sys/devices/system/cpu/cpu{cores}'):
            cores += 1
        return cores

    def toggle_core(self, core):
        file_path = f'/sys/devices/system/cpu/cpu{core}/online'

        try:
            current_state = int(open(file_path).read().strip())
            new_state = 1 - current_state
            subprocess.run(['sudo', 'su', '-c', f'echo {new_state} > {file_path}'])
            self.update_core_states()
        except FileNotFoundError:
            print(f'File not found: {file_path}. Assuming core is online.')
        except Exception as e:
            print(f'An error occurred: {str(e)}')

    def update_core_states(self):
        for core, button in enumerate(self.core_buttons):
            if core == 0:
                button.setChecked(True)
                button.setStyleSheet("background-color: #4CAF50; color: white;")
                continue
            file_path = f'/sys/devices/system/cpu/cpu{core}/online'

            try:
                current_state = int(open(file_path).read().strip())
                if current_state == 1:
                    button.setChecked(True)
                    button.setStyleSheet("background-color: #4CAF50; color: white;")
                else:
                    button.setChecked(False)
                    button.setStyleSheet("background-color: #D32F2F; color: white;")
            except FileNotFoundError:
                button.setChecked(False)
                button.setStyleSheet("background-color: #D32F2F; color: white;")

    def disable_range(self):
        try:
            # Get the range of cores to disable
            start_core, ok1 = QInputDialog.getInt(self, "Disable Range", "Enter start core index:", 0, 0, self.num_cores - 1)
            if not ok1:
                return

            end_core, ok2 = QInputDialog.getInt(self, "Disable Range", "Enter end core index:", start_core, start_core, self.num_cores - 1)
            if not ok2:
                return

            # Disable the specified range
            for core in range(start_core, end_core + 1):
                file_path = f'/sys/devices/system/cpu/cpu{core}/online'
                try:
                    subprocess.run(['sudo', 'su', '-c', f'echo 0 > {file_path}'])
                except Exception as e:
                    print(f'An error occurred while disabling CPU {core}: {str(e)}')

            self.update_core_states()

        except Exception as e:
            print(f'An error occurred: {str(e)}')

    def enable_range(self):
        try:
            # Get the range of cores to enable
            start_core, ok1 = QInputDialog.getInt(self, "Enable Range", "Enter start core index:", 0, 0, self.num_cores - 1)
            if not ok1:
                return

            end_core, ok2 = QInputDialog.getInt(self, "Enable Range", "Enter end core index:", start_core, start_core, self.num_cores - 1)
            if not ok2:
                return

            # Enable the specified range
            for core in range(start_core, end_core + 1):
                file_path = f'/sys/devices/system/cpu/cpu{core}/online'
                try:
                    subprocess.run(['sudo', 'su', '-c', f'echo 1 > {file_path}'])
                except Exception as e:
                    print(f'An error occurred while enabling CPU {core}: {str(e)}')

            self.update_core_states()

        except Exception as e:
            print(f'An error occurred: {str(e)}')

    def show_all_cpus_enabled_popup(self):
        msg_box = QMessageBox()
        msg_box.setWindowTitle("All CPUs Enabled")
        msg_box.setText("All CPU cores have been enabled.")
        msg_box.setIcon(QMessageBox.Icon.Information)
        msg_box.exec()


def main():
    app = QApplication(sys.argv)

    if subprocess.run(['sudo', '-v']).returncode != 0:
        print("Please run this script as root.")
        sys.exit(1)

    cpu_cores_controller = CPUCoresController()
    cpu_cores_controller.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
