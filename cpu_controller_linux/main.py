import sys
from PyQt6.QtWidgets import QApplication, QWidget, QMessageBox, QGridLayout, QPushButton, QLabel, QVBoxLayout
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
        self.setMinimumSize(500, 500)  # Adjusted minimum size for a more spacious design

        # Dynamically determine the number of CPU cores
        num_cores = os.cpu_count() or 1

        self.layout = QGridLayout()

        self.core_buttons = []
        for core in range(num_cores):
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

            self.layout.addWidget(container, core // 4, core % 4)
            self.core_buttons.append(button)

        self.setLayout(self.layout)

        # Set initial core states
        self.update_core_states()

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
            file_path = f'/sys/devices/system/cpu/cpu{core}/online'

            try:
                current_state = int(open(file_path).read().strip())
                if current_state == 1:
                    button.setStyleSheet("background-color: #4CAF50; color: white;")
                else:
                    button.setStyleSheet("background-color: #D32F2F; color: white;")
            except FileNotFoundError:
                button.setStyleSheet("background-color: #4CAF50; color: white;")

    def closeEvent(self, event):
        all_cpus_enabled = True

        for core in range(len(self.core_buttons)):
            file_path = f'/sys/devices/system/cpu/cpu{core}/online'
            try:
                subprocess.run(['sudo', 'su', '-c', f'echo 1 > {file_path}'])
            except Exception as e:
                print(f'An error occurred: {str(e)}')
                all_cpus_enabled = False

        if all_cpus_enabled:
            self.show_all_cpus_enabled_popup()

        event.accept()

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
