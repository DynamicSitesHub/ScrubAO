from qgis.PyQt.QtWidgets import QDialog, QVBoxLayout, QLabel, QLineEdit, QPushButton, QFileDialog, QMessageBox, QComboBox

from .ao_scrub_logic import run_ao_scrub

class AOScrubDialog(QDialog):
    def __init__(self, iface, parent=None):
        super().__init__(parent)
        self.iface = iface
        self.setWindowTitle("AO Scrub Tool")
        self.setMinimumWidth(400)

        layout = QVBoxLayout()

        # Input folder
        self.input_folder_edit = QLineEdit()
        input_btn = QPushButton("Select Input Folder")
        input_btn.clicked.connect(self.select_input_folder)
        layout.addWidget(QLabel("Input folder:"))
        layout.addWidget(self.input_folder_edit)
        layout.addWidget(input_btn)

        # Output folder
        self.output_folder_edit = QLineEdit()
        output_btn = QPushButton("Select Output Folder")
        output_btn.clicked.connect(self.select_output_folder)
        layout.addWidget(QLabel("Output folder:"))
        layout.addWidget(self.output_folder_edit)
        layout.addWidget(output_btn)

        # Keyword
        self.keyword_edit = QLineEdit()
        layout.addWidget(QLabel("Keyword in filename (e.g., Export):"))
        layout.addWidget(self.keyword_edit)

        # Other parameters
        self.group_edit = QLineEdit()
        self.tier_edit = QLineEdit()
        self.utility_edit = QLineEdit()
        self.market_edit = QLineEdit()
        self.status_edit = QLineEdit()
        for label, widget in [("Group:", self.group_edit),
                              ("Tier:", self.tier_edit),
                              ("Utility:", self.utility_edit),
                              ("Market:", self.market_edit),
                              ("Lead Status:", self.status_edit)]:
            layout.addWidget(QLabel(label))
            layout.addWidget(widget)

        # Star rating combo boxes
        self.star1_combo = QComboBox()
        self.star1_combo.setEditable(True)
        self.star1_combo.addItems(['GIS Team identified 15-20 contiguous buildable acres'])
        self.star1_combo.addItems(['GIS Team identified 10-15 contiguous buildable acres'])
        self.star2_combo = QComboBox()
        self.star2_combo.setEditable(True)
        self.star2_combo.addItems(['GIS Team identified 20-25 contiguous buildable acres'])
        self.star2_combo.addItems(['GIS Team identified 15-20 contiguous buildable acres'])
        self.star3_combo = QComboBox()
        self.star3_combo.setEditable(True)
        self.star3_combo.addItems(['GIS Team identified 25+ contiguous buildable acres'])
        self.star3_combo.addItems(['GIS Team identified 20+ contiguous buildable acres'])
        for label, combo in [("Star 1:", self.star1_combo),
                             ("Star 2:", self.star2_combo),
                             ("Star 3:", self.star3_combo)]:
            layout.addWidget(QLabel(label))
            layout.addWidget(combo)

        # Run button
        run_btn = QPushButton("Run")
        run_btn.clicked.connect(self.run_tool)
        layout.addWidget(run_btn)

        self.setLayout(layout)

    def select_input_folder(self):
        folder = QFileDialog.getExistingDirectory(self, "Select Input Folder")
        if folder:
            self.input_folder_edit.setText(folder)

    def select_output_folder(self):
        folder = QFileDialog.getExistingDirectory(self, "Select Output Folder")
        if folder:
            self.output_folder_edit.setText(folder)

    def run_tool(self):
        input_folder = self.input_folder_edit.text()
        output_folder = self.output_folder_edit.text()
        keyword = self.keyword_edit.text()
        group = self.group_edit.text()
        tier = self.tier_edit.text()
        utility = self.utility_edit.text()
        market = self.market_edit.text()
        status = self.status_edit.text()
        star1 = self.star1_combo.currentText()
        star2 = self.star2_combo.currentText()
        star3 = self.star3_combo.currentText()

        if not all([input_folder, output_folder, keyword, group, tier, utility, market, status]):
            QMessageBox.warning(self, "Missing parameters", "Please fill in all fields.")
            return

        try:
            output_file = run_ao_scrub(input_folder, keyword, group, tier, utility, market, status, output_folder, star1, star2, star3)
            QMessageBox.information(self, "Success", f"CSV generated successfully:\n{output_file}")
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))
