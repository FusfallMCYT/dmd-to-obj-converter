import sys

from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QLabel,
    QPushButton,
    QFileDialog,
    QTextEdit,
    QVBoxLayout,
    QHBoxLayout,
    QLineEdit,
    QProgressBar
)

from converter import DMDConverter


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        self.converter = DMDConverter()

        self.setWindowTitle("ZDSimulator DMD Converter")
        self.resize(800, 650)

        self.dmd_file = ""
        self.output_folder = ""
        self.texture_file = ""

        self.build_ui()

    def build_ui(self):

        central = QWidget()
        self.setCentralWidget(central)

        layout = QVBoxLayout()

        # ---------- DMD ----------
        layout.addWidget(QLabel("DMD файл"))
        row = QHBoxLayout()
        self.dmd_edit = QLineEdit()
        btn = QPushButton("Обзор")
        btn.clicked.connect(self.select_dmd)
        row.addWidget(self.dmd_edit)
        row.addWidget(btn)
        layout.addLayout(row)

        # ---------- Output ----------
        layout.addWidget(QLabel("Папка сохранения"))
        row2 = QHBoxLayout()
        self.out_edit = QLineEdit()
        btn2 = QPushButton("Обзор")
        btn2.clicked.connect(self.select_output)
        row2.addWidget(self.out_edit)
        row2.addWidget(btn2)
        layout.addLayout(row2)

        # ---------- Custom Texture (Задел на будущее) ----------
        layout.addWidget(QLabel("Кастомная текстура PNG (Необязательно)"))
        row_tex = QHBoxLayout()
        self.tex_edit = QLineEdit()
        self.tex_edit.setPlaceholderText("По умолчанию используется <имя_модели>.png")
        btn_tex = QPushButton("Обзор")
        btn_tex.clicked.connect(self.select_texture)
        row_tex.addWidget(self.tex_edit)
        row_tex.addWidget(btn_tex)
        layout.addLayout(row_tex)

        # ---------- New File Name ----------
        layout.addWidget(QLabel("Новое имя файла (без расширения, необязательно)"))
        self.name_edit = QLineEdit()
        self.name_edit.setPlaceholderText("Оставьте пустым для сохранения оригинального имени")
        layout.addWidget(self.name_edit)

        # ---------- Progress ----------
        self.progress = QProgressBar()
        layout.addWidget(self.progress)

        # ---------- Action Buttons ----------
        row_btns = QHBoxLayout()

        self.analyze_btn = QPushButton("🔍 Анализ DMD")
        self.analyze_btn.clicked.connect(self.analyze)
        row_btns.addWidget(self.analyze_btn)

        self.convert_btn = QPushButton("⚙️ Конвертировать")
        self.convert_btn.clicked.connect(self.convert)
        row_btns.addWidget(self.convert_btn)

        layout.addLayout(row_btns)

        # ---------- Log ----------
        self.log = QTextEdit()
        self.log.setReadOnly(True)
        layout.addWidget(self.log)

        central.setLayout(layout)

    def write(self, text):
        self.log.append(text)

    def select_dmd(self):
        filename, _ = QFileDialog.getOpenFileName(
            self, "Выберите DMD", "", "DMD (*.dmd)"
        )
        if filename:
            self.dmd_file = filename
            self.dmd_edit.setText(filename)

    def select_output(self):
        folder = QFileDialog.getExistingDirectory(
            self, "Папка сохранения"
        )
        if folder:
            self.output_folder = folder
            self.out_edit.setText(folder)

    def select_texture(self):
        filename, _ = QFileDialog.getOpenFileName(
            self, "Выберите текстуру PNG", "", "PNG Image (*.png)"
        )
        if filename:
            self.texture_file = filename
            self.tex_edit.setText(filename)

    def analyze(self):
        if not self.dmd_file:
            self.write("❌ Ошибка: Не выбран DMD файл.")
            return

        self.write("--- 🔍 ДИАГНОСТИКА DMD ---")
        info = self.converter.analyze(self.dmd_file)
        self.write(f"Found Vertices: {info['vertices']}")
        self.write(f"Found UVs: {info['uvs']}")
        self.write(f"Found Faces: {info['faces']}")
        self.write(f"Invalid Faces Removed: {info['invalid_faces']}")
        self.write(f"Max Index: {info['max_index']}")
        self.write("---------------------------\n")

    def convert(self):
        if not self.dmd_file:
            self.write("❌ Ошибка: Не выбран DMD файл.")
            return

        if not self.output_folder:
            self.write("❌ Ошибка: Не выбрана папка сохранения.")
            return

        self.progress.setValue(20)

        new_filename = self.name_edit.text().strip()
        custom_tex = self.tex_edit.text().strip()

        info = self.converter.convert(
            self.dmd_file,
            self.output_folder,
            new_name=new_filename,
            custom_texture=custom_tex
        )

        self.progress.setValue(100)

        self.write("=== ✅ УСПЕШНО КОНВЕРТИРОВАНО ===")
        self.write(f"Found Vertices: {info['vertices']}")
        self.write(f"Found UVs: {info['uvs']}")
        self.write(f"Found Faces: {info['faces']}")
        self.write(f"Invalid Faces Removed: {info['invalid_faces']}")
        self.write(f"Max Index: {info['max_index']}")
        self.write(f"OBJ File: {info['obj']}")
        self.write(f"MTL File: {info['mtl']}")
        self.write("=================================\n")


app = QApplication(sys.argv)
window = MainWindow()
window.show()
sys.exit(app.exec())
