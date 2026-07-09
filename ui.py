"""
PyQt5 GUI for the Data Format Converter.
Task 8: UI implementation (PyQt5 with graphical interface).
"""

import sys
import os
from pathlib import Path
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QLineEdit, QPushButton, QComboBox, QFileDialog,
    QTextEdit, QGroupBox, QMessageBox, QProgressBar
)
from PyQt5.QtCore import Qt, QThread, pyqtSignal
from PyQt5.QtGui import QFont, QColor, QTextCursor

from data_reader import read_file, DataReaderError
from data_writer import (
    write_file, DataWriterError, validate_json_syntax,
    validate_yaml_syntax, validate_xml_syntax
)


class ConversionWorker(QThread):
    """Worker thread for file conversion."""
    finished = pyqtSignal()
    error = pyqtSignal(str)
    success = pyqtSignal(str)
    progress = pyqtSignal(int)
    
    def __init__(self, input_file, output_file, input_format, output_format):
        super().__init__()
        self.input_file = input_file
        self.output_file = output_file
        self.input_format = input_format
        self.output_format = output_format
    
    def run(self):
        """Execute the conversion."""
        try:
            self.progress.emit(25)
            
            # Read input file
            data = read_file(self.input_file, self.input_format)
            self.progress.emit(50)
            
            # Write output file
            write_file(self.output_file, data, self.output_format)
            self.progress.emit(75)
            
            # Validate output
            if self.output_format == 'json':
                validate_json_syntax(self.output_file)
            elif self.output_format in ('yaml', 'yml'):
                validate_yaml_syntax(self.output_file)
            elif self.output_format == 'xml':
                validate_xml_syntax(self.output_file)
            
            self.progress.emit(100)
            self.success.emit(
                f"Conversion successful!\n"
                f"✓ Read {self.input_format.upper()} file\n"
                f"✓ Wrote {self.output_format.upper()} file\n"
                f"✓ Verified syntax"
            )
            self.finished.emit()
        except (DataReaderError, DataWriterError) as e:
            self.error.emit(f"Conversion error:\n{str(e)}")
            self.finished.emit()
        except Exception as e:
            self.error.emit(f"Unexpected error:\n{str(e)}")
            self.finished.emit()


class DataConverterUI(QMainWindow):
    """Main PyQt5 window for the Data Format Converter."""
    
    SUPPORTED_FORMATS = ['json', 'xml', 'yaml', 'yml']
    
    def __init__(self):
        super().__init__()
        self.worker = None
        self.init_ui()
    
    def init_ui(self):
        """Initialize the UI."""
        self.setWindowTitle("Data Format Converter")
        self.setGeometry(100, 100, 800, 600)
        
        # Central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Main layout
        main_layout = QVBoxLayout()
        central_widget.setLayout(main_layout)
        
        # Title
        title = QLabel("Data Format Converter")
        title.setFont(QFont("Arial", 16, QFont.Bold))
        main_layout.addWidget(title)
        
        # Input file section
        input_group = QGroupBox("Input File")
        input_layout = QHBoxLayout()
        
        input_layout.addWidget(QLabel("File:"))
        self.input_file_edit = QLineEdit()
        self.input_file_edit.setReadOnly(True)
        input_layout.addWidget(self.input_file_edit)
        
        browse_input_btn = QPushButton("Browse...")
        browse_input_btn.clicked.connect(self.browse_input_file)
        input_layout.addWidget(browse_input_btn)
        
        input_layout.addWidget(QLabel("Format:"))
        self.input_format_combo = QComboBox()
        self.input_format_combo.addItems(self.SUPPORTED_FORMATS)
        input_layout.addWidget(self.input_format_combo)
        
        input_group.setLayout(input_layout)
        main_layout.addWidget(input_group)
        
        # Output file section
        output_group = QGroupBox("Output File")
        output_layout = QHBoxLayout()
        
        output_layout.addWidget(QLabel("File:"))
        self.output_file_edit = QLineEdit()
        self.output_file_edit.setReadOnly(True)
        output_layout.addWidget(self.output_file_edit)
        
        browse_output_btn = QPushButton("Browse...")
        browse_output_btn.clicked.connect(self.browse_output_file)
        output_layout.addWidget(browse_output_btn)
        
        output_layout.addWidget(QLabel("Format:"))
        self.output_format_combo = QComboBox()
        self.output_format_combo.addItems(self.SUPPORTED_FORMATS)
        self.output_format_combo.setCurrentIndex(1)  # Default to XML
        output_layout.addWidget(self.output_format_combo)
        
        output_group.setLayout(output_layout)
        main_layout.addWidget(output_group)
        
        # Progress bar
        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        main_layout.addWidget(self.progress_bar)
        
        # Convert button
        button_layout = QHBoxLayout()
        convert_btn = QPushButton("Convert")
        convert_btn.setFont(QFont("Arial", 12, QFont.Bold))
        convert_btn.clicked.connect(self.convert_files)
        button_layout.addStretch()
        button_layout.addWidget(convert_btn)
        button_layout.addStretch()
        main_layout.addLayout(button_layout)
        
        # Output log
        log_group = QGroupBox("Conversion Log")
        log_layout = QVBoxLayout()
        
        self.log_text = QTextEdit()
        self.log_text.setReadOnly(True)
        log_layout.addWidget(self.log_text)
        
        log_group.setLayout(log_layout)
        main_layout.addWidget(log_group)
    
    def browse_input_file(self):
        """Browse for input file."""
        file_dialog = QFileDialog()
        file_path, _ = file_dialog.getOpenFileName(
            self,
            "Select Input File",
            "",
            "All Files (*.*)"
        )
        
        if file_path:
            self.input_file_edit.setText(file_path)
            # Auto-detect format from extension
            ext = Path(file_path).suffix.lstrip('.').lower()
            if ext in self.SUPPORTED_FORMATS:
                self.input_format_combo.setCurrentText(ext)
    
    def browse_output_file(self):
        """Browse for output file."""
        file_dialog = QFileDialog()
        file_path, _ = file_dialog.getSaveFileName(
            self,
            "Select Output File",
            "",
            "All Files (*.*)"
        )
        
        if file_path:
            self.output_file_edit.setText(file_path)
            # Auto-detect format from extension
            ext = Path(file_path).suffix.lstrip('.').lower()
            if ext in self.SUPPORTED_FORMATS:
                self.output_format_combo.setCurrentText(ext)
    
    def convert_files(self):
        """Start file conversion."""
        input_file = self.input_file_edit.text()
        output_file = self.output_file_edit.text()
        input_format = self.input_format_combo.currentText()
        output_format = self.output_format_combo.currentText()
        
        # Validate inputs
        if not input_file:
            QMessageBox.warning(self, "Input Error", "Please select an input file")
            return
        
        if not os.path.exists(input_file):
            QMessageBox.warning(self, "Input Error", "Input file does not exist")
            return
        
        if not output_file:
            QMessageBox.warning(self, "Output Error", "Please select an output file")
            return
        
        if input_format == output_format:
            QMessageBox.warning(
                self, "Format Error",
                "Input and output formats must be different"
            )
            return
        
        # Clear log and show progress
        self.log_text.clear()
        self.log_text.append(f"Starting conversion...\n")
        self.log_text.append(f"Input:  {input_file} ({input_format.upper()})")
        self.log_text.append(f"Output: {output_file} ({output_format.upper()})\n")
        
        self.progress_bar.setVisible(True)
        self.progress_bar.setValue(0)
        
        # Start worker thread
        self.worker = ConversionWorker(
            input_file, output_file, input_format, output_format
        )
        self.worker.progress.connect(self.update_progress)
        self.worker.success.connect(self.show_success)
        self.worker.error.connect(self.show_error)
        self.worker.finished.connect(self.conversion_finished)
        self.worker.start()
    
    def update_progress(self, value):
        """Update progress bar."""
        self.progress_bar.setValue(value)
    
    def show_success(self, message):
        """Display success message."""
        self.log_text.append(f"\n{message}")
        
        # Style success text
        cursor = self.log_text.textCursor()
        cursor.movePosition(QTextCursor.End)
        self.log_text.setTextCursor(cursor)
    
    def show_error(self, message):
        """Display error message."""
        self.log_text.append(f"\n❌ ERROR\n{message}")
        QMessageBox.critical(self, "Conversion Error", message)
    
    def conversion_finished(self):
        """Handle conversion completion."""
        self.progress_bar.setVisible(False)


def run_ui():
    """Run the PyQt5 UI."""
    app = QApplication(sys.argv)
    window = DataConverterUI()
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    run_ui()
