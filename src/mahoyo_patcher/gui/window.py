from pathlib import Path

from PySide6.QtCore import Qt
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import (
    QCheckBox,
    QFileDialog,
    QLabel,
    QMessageBox,
    QProgressBar,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from mahoyo_patcher import __version__
from mahoyo_patcher.constants import (
    HFA_FILE,
    ICON_FILE,
)
from mahoyo_patcher.gui.worker import Worker
from mahoyo_patcher.utils import (
    autodetect_game_path,
    get_resource_path,
)


class Window(QWidget):
    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle(f"Mahoyo Patcher v{__version__}")
        self.setMinimumWidth(480)
        self.build_ui()
        self.set_icon()
        self.connect_signals()

        self.game_path: Path | None = None
        self.hfa_path: Path | None = None
        self.worker: Worker | None = None
        self.try_autodetect()

    def build_ui(self) -> None:
        layout = QVBoxLayout(self)

        # Path display
        self.folder_label: QLabel = QLabel("No game folder selected")
        self.folder_label.setWordWrap(True)
        self.folder_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.folder_label.setStyleSheet(
            "border: 1px solid #aaa; "
            "padding: 5px; "
            "background: #f0f0f0; "
            "border-radius: 4px;"
        )
        layout.addWidget(self.folder_label)

        # Select button
        self.select_folder_btn: QPushButton = QPushButton("Select game folder")
        layout.addWidget(self.select_folder_btn)

        # Separator line
        line: QLabel = QLabel("Options")
        line.setStyleSheet("font-weight: bold; margin-top: 15px;")
        layout.addWidget(line)

        # Checkboxes
        self.metric_cb: QCheckBox = QCheckBox("Metric System")
        self.romanization_cb: QCheckBox = QCheckBox("Fix Romanization")
        self.name_order_cb: QCheckBox = QCheckBox("Fix Name Order")
        self.honorifics_cb: QCheckBox = QCheckBox("Restore Honorifics")
        self.name_order_cb.setEnabled(False)
        self.honorifics_cb.setEnabled(False)
        layout.addWidget(self.metric_cb)
        layout.addWidget(self.romanization_cb)
        layout.addWidget(self.name_order_cb)
        layout.addWidget(self.honorifics_cb)

        # Progress label and bar
        self.progress_label: QLabel = QLabel("")
        self.progress_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.progress_label.setStyleSheet("margin-top: 10px;")
        self.progress_bar: QProgressBar = QProgressBar()
        self.progress_bar.setRange(0, 100)
        self.progress_bar.setValue(0)
        self.progress_bar.setVisible(False)
        layout.addWidget(self.progress_label)
        layout.addWidget(self.progress_bar)

        # Patch button
        self.patch_btn: QPushButton = QPushButton("Patch!")
        self.patch_btn.setEnabled(False)
        self.patch_btn.setMinimumHeight(40)
        layout.addWidget(self.patch_btn)

    def set_icon(self) -> None:
        try:
            icon_path: Path | None = get_resource_path(
                "mahoyo_patcher.resources", ICON_FILE
            )
            if icon_path and icon_path.is_file():
                self.setWindowIcon(QIcon(str(icon_path)))
        except (OSError, RuntimeError):
            pass

    def connect_signals(self) -> None:
        self.select_folder_btn.clicked.connect(self.select_folder)
        self.romanization_cb.toggled.connect(self.on_romanization_toggled)
        self.name_order_cb.toggled.connect(self.on_name_order_toggled)
        self.patch_btn.clicked.connect(self.start_worker)

    def try_autodetect(self) -> None:
        game_path: Path | None = autodetect_game_path()
        if game_path:
            self.validate_and_set_path(game_path)

    def select_folder(self) -> None:
        game_path_str: str | None = QFileDialog.getExistingDirectory(
            parent=self, caption="Select main game folder"
        )
        game_path: Path | None = Path(game_path_str) if game_path_str else None
        if game_path:
            self.validate_and_set_path(game_path)

    def validate_and_set_path(self, game_path: Path) -> None:
        self.folder_label.setText(str(game_path))
        hfa_path: Path = game_path / HFA_FILE
        if not hfa_path.is_file():
            self.game_path = None
            self.hfa_path = None
            self.patch_btn.setEnabled(False)
            if self.sender() == self.select_folder_btn:
                QMessageBox.critical(
                    self, "File not found", f"Could not find:\n{HFA_FILE}"
                )
            return
        self.game_path = game_path
        self.hfa_path = hfa_path
        self.patch_btn.setEnabled(True)

    def start_worker(self) -> None:
        options: dict[str, bool] = {
            "metric": self.metric_cb.isChecked(),
            "romanization": self.romanization_cb.isChecked(),
            "name_order": self.name_order_cb.isChecked(),
            "honorifics": self.honorifics_cb.isChecked(),
        }
        self.patch_btn.setEnabled(False)
        self.select_folder_btn.setEnabled(False)
        self.progress_bar.setVisible(True)
        self.progress_bar.setValue(0)
        self.progress_label.setText("Starting...")
        if self.game_path is None or self.hfa_path is None:
            QMessageBox.critical(self, "Error", "Invalid game or HFA path.")
            self.patch_btn.setEnabled(True)
            self.select_folder_btn.setEnabled(True)
            return
        self.worker = Worker(self.game_path, self.hfa_path, options)
        self.worker.progress_signal.connect(self.update_progress)
        self.worker.status_signal.connect(self.update_status)
        self.worker.finished_signal.connect(self.on_patch_finished)
        self.worker.start()

    def update_progress(self, val: int) -> None:
        self.progress_bar.setValue(val)

    def update_status(self, text: str) -> None:
        self.progress_label.setText(text)

    def on_romanization_toggled(self, checked: bool) -> None:
        self.name_order_cb.setEnabled(checked)
        if not checked:
            self.name_order_cb.setChecked(False)

    def on_name_order_toggled(self, checked: bool) -> None:
        self.honorifics_cb.setEnabled(checked)
        if not checked:
            self.honorifics_cb.setChecked(False)

    def on_patch_finished(self, success: bool, message: str) -> None:
        self.patch_btn.setEnabled(True)
        self.select_folder_btn.setEnabled(True)
        self.progress_label.setText("Done" if success else "Error")

        if success:
            QMessageBox.information(self, "Success", message)
            self.progress_bar.setVisible(False)
            self.progress_label.setText("")
        else:
            QMessageBox.critical(self, "Patch Failed", message)
