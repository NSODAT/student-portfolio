#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Portfolio Manager App - Updated Version for Student Portfolio
Supports management of education modules, thesis, courseworks, and practical works
"""

import json
import os
import sys
import subprocess
import threading
import webbrowser
from datetime import datetime
from typing import List, Dict, Any

# PyQt6 import (required for this UI)
try:
    from PyQt6.QtWidgets import (
        QApplication, QMainWindow, QWidget, QHBoxLayout, QVBoxLayout, QLabel, QPushButton,
        QTableWidget, QTableWidgetItem, QStackedWidget, QDialog, QLineEdit, QTextEdit, QFormLayout,
        QComboBox, QDialogButtonBox, QMessageBox, QProgressBar, QTabWidget, QListWidget, QListWidgetItem,
        QSplitter, QInputDialog
    )
    from PyQt6.QtCore import Qt, pyqtSignal, QObject, QThread, pyqtSlot
    from PyQt6.QtGui import QCursor
except Exception as e:
    sys.exit("PyQt6 is required: {}".format(e))

class PortfolioManager:
    def __init__(self, repo_path: str = "."):
        self.repo_path = os.path.abspath(repo_path)
        # Ensure data directory exists
        self.data_dir = os.path.join(self.repo_path, "public", "data")
        os.makedirs(self.data_dir, exist_ok=True)

        # File paths for new content types
        self.education_modules_file = os.path.join(self.data_dir, "education_modules.json")
        self.thesis_file = os.path.join(self.data_dir, "thesis.json")
        self.courseworks_file = os.path.join(self.data_dir, "courseworks.json")
        self.practical_works_file = os.path.join(self.data_dir, "practical_works.json")

        # Initialize default data files if they don't exist
        self._initialize_default_files()

    def _initialize_default_files(self):
        """Initialize default JSON files if they don't exist"""
        default_files = {
            self.education_modules_file: [
                {
                    "id": 1,
                    "title": "Модуль 1: Основы программирования",
                    "semesters": [
                        {
                            "id": 1,
                            "title": "Семестр 1",
                            "labs": [
                                {"id": 1, "title": "ЛР1: Введение в алгоритмы", "link": "#"},
                                {"id": 2, "title": "ЛР2: Основы Python", "link": "#"},
                                {"id": 3, "title": "ЛР3: Структуры данных", "link": "#"}
                            ]
                        }
                    ]
                }
            ],
            self.thesis_file: {
                "title": "Дипломная работа",
                "topic": "Разработка веб-приложения для управления учебными проектами",
                "description": "Моя дипломная работа посвящена созданию современного веб-приложения для управления учебными проектами студентов.",
                "previewImage": "/thesis-preview.jpg",
                "link": "#",
                "keyFeatures": [
                    "Анализ требований",
                    "Проектирование архитектуры",
                    "Реализация основных модулей",
                    "Тестирование и оптимизация"
                ]
            },
            self.courseworks_file: [
                {
                    "id": 1,
                    "title": "Курсовая работа по базам данных",
                    "semester": "Семестр 3",
                    "description": "Разработка системы управления учебными проектами с использованием реляционных баз данных.",
                    "link": "#",
                    "technologies": ["PostgreSQL", "SQL", "Python"]
                }
            ],
            self.practical_works_file: [
                {
                    "id": 1,
                    "title": "Практические работы по программированию",
                    "semester": "Семестр 1-2",
                    "description": "Коллекция практических работ по основам программирования.",
                    "link": "#",
                    "items": [
                        "Практика 1: Основы Python",
                        "Практика 2: Работа с файлами",
                        "Практика 3: Алгоритмы сортировки"
                    ]
                }
            ]
        }

        for file_path, default_data in default_files.items():
            if not os.path.exists(file_path):
                with open(file_path, 'w', encoding='utf-8') as f:
                    json.dump(default_data, f, ensure_ascii=False, indent=2)

    def log(self, message: str, level: str = "INFO"):
        colors = {
            "INFO": "\033[94m",
            "SUCCESS": "\033[92m",
            "WARNING": "\033[93m",
            "ERROR": "\033[91m",
            "RESET": "\033[0m",
        }
        timestamp = datetime.now().strftime("%H:%M:%S")
        print(f"{colors[level]}[{timestamp}] {message}{colors['RESET']}")

    # Education Modules Management
    def read_education_modules(self) -> List[Dict[str, Any]]:
        try:
            with open(self.education_modules_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            self.log(f"Ошибка чтения учебных модулей: {e}", "ERROR")
            return []

    def write_education_modules(self, modules: List[Dict[str, Any]]) -> bool:
        try:
            with open(self.education_modules_file, 'w', encoding='utf-8') as f:
                json.dump(modules, f, ensure_ascii=False, indent=2)
            return True
        except Exception as e:
            self.log(f"Ошибка записи учебных модулей: {e}", "ERROR")
            return False

    # Thesis Management
    def read_thesis(self) -> Dict[str, Any]:
        try:
            with open(self.thesis_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            self.log(f"Ошибка чтения дипломной работы: {e}", "ERROR")
            return {}

    def write_thesis(self, thesis_data: Dict[str, Any]) -> bool:
        try:
            with open(self.thesis_file, 'w', encoding='utf-8') as f:
                json.dump(thesis_data, f, ensure_ascii=False, indent=2)
            return True
        except Exception as e:
            self.log(f"Ошибка записи дипломной работы: {e}", "ERROR")
            return False

    # Courseworks Management
    def read_courseworks(self) -> List[Dict[str, Any]]:
        try:
            with open(self.courseworks_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            self.log(f"Ошибка чтения курсовых работ: {e}", "ERROR")
            return []

    def write_courseworks(self, courseworks: List[Dict[str, Any]]) -> bool:
        try:
            with open(self.courseworks_file, 'w', encoding='utf-8') as f:
                json.dump(courseworks, f, ensure_ascii=False, indent=2)
            return True
        except Exception as e:
            self.log(f"Ошибка записи курсовых работ: {e}", "ERROR")
            return False

    # Practical Works Management
    def read_practical_works(self) -> List[Dict[str, Any]]:
        try:
            with open(self.practical_works_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            self.log(f"Ошибка чтения практических работ: {e}", "ERROR")
            return []

    def write_practical_works(self, practical_works: List[Dict[str, Any]]) -> bool:
        try:
            with open(self.practical_works_file, 'w', encoding='utf-8') as f:
                json.dump(practical_works, f, ensure_ascii=False, indent=2)
            return True
        except Exception as e:
            self.log(f"Ошибка записи практических работ: {e}", "ERROR")
            return False

    def deploy_to_github(self, commit_message: str = "Update portfolio content") -> bool:
        try:
            os.chdir(self.repo_path)
            
            # Проверяем, инициализирован ли git
            if not os.path.exists('.git'):
                self.log("Git репозиторий не инициализирован. Инициализируем...", "WARNING")
                subprocess.run(["git", "init"], capture_output=True)
                
                # Добавляем remote origin
                remote_url = "https://github.com/NSODAT/developer-portfolio.git"
                subprocess.run(["git", "remote", "add", "origin", remote_url], capture_output=True)
                
                # Создаем ветку main
                subprocess.run(["git", "branch", "-M", "main"], capture_output=True)
            
            # Проверяем наличие remote origin
            result = subprocess.run(["git", "remote", "get-url", "origin"], capture_output=True, text=True)
            if result.returncode != 0:
                self.log("Remote origin не настроен. Добавляем...", "WARNING")
                remote_url = "https://github.com/NSODAT/developer-portfolio.git"
                subprocess.run(["git", "remote", "add", "origin", remote_url], capture_output=True)
            
            # Выполняем команды git
            commands = [
                ["git", "add", "."],
                ["git", "commit", "-m", commit_message],
                ["git", "push", "-u", "origin", "main"]  # Добавлен флаг -u для первого push
            ]
            
            for cmd in commands:
                self.log(f"Выполняем: {' '.join(cmd)}", "INFO")
                result = subprocess.run(cmd, capture_output=True, text=True, encoding='utf-8')
                
                if result.returncode != 0:
                    # Если это ошибка "nothing to commit", это не критично
                    if "nothing to commit" in result.stdout or "nothing to commit" in result.stderr:
                        self.log("Нет изменений для коммита", "WARNING")
                        continue
                    # Если ошибка с веткой, пробуем создать и push
                    elif "error: src refspec main does not match any" in result.stderr:
                        self.log("Создаем ветку main...", "WARNING")
                        subprocess.run(["git", "checkout", "-b", "main"], capture_output=True)
                        continue
                    else:
                        self.log(f"Ошибка выполнения {cmd[0]}: {result.stderr}", "ERROR")
                        return False
                        
            self.log("Изменения успешно загружены в GitHub!", "SUCCESS")
            return True
        
        except Exception as e:
            self.log(f"Ошибка деплоя: {e}", "ERROR")
            return False

class EducationModuleDialog(QDialog):
    def __init__(self, parent=None, title: str = "", module_data: Dict[str, Any] | None = None):
        super().__init__(parent)
        self.setWindowTitle(title)
        self.setModal(True)
        self.resize(1000, 700)
        self.setMinimumSize(800, 600)

        # Main layout
        main_layout = QVBoxLayout(self)
        main_layout.setSpacing(15)
        main_layout.setContentsMargins(20, 20, 20, 20)

        # Header
        header_layout = QHBoxLayout()
        header_layout.addWidget(QLabel("📚"), alignment=Qt.AlignmentFlag.AlignTop)
        self.title_input = QLineEdit()
        self.title_input.setPlaceholderText("Введите название модуля...")
        self.title_input.setStyleSheet("""
            QLineEdit {
                font-size: 18px;
                font-weight: bold;
                padding: 12px;
                border: 2px solid #334155;
                border-radius: 8px;
                background: #0b1220;
                color: #e2e8f0;
            }
            QLineEdit:focus {
                border-color: #60a5fa;
            }
        """)
        self.title_input.setText(module_data.get("title", "") if module_data else "")
        header_layout.addWidget(self.title_input, 1)
        main_layout.addLayout(header_layout)

        # Content area with splitter
        splitter = QSplitter(Qt.Orientation.Horizontal)
        
        # Left panel - Semester list
        left_panel = QWidget()
        left_layout = QVBoxLayout(left_panel)
        left_layout.setContentsMargins(0, 0, 0, 0)
        
        # Semester list header
        semester_header = QHBoxLayout()
        semester_header.addWidget(QLabel("📋 Разделы"), alignment=Qt.AlignmentFlag.AlignLeft)
        add_semester_btn = QPushButton("➕ Добавить раздел")
        add_semester_btn.setStyleSheet("""
            QPushButton {
                background: #22c55e;
                color: white;
                border: none;
                padding: 8px 16px;
                border-radius: 6px;
                font-weight: bold;
            }
            QPushButton:hover {
                background: #16a34a;
            }
        """)
        add_semester_btn.clicked.connect(self._add_semester)
        semester_header.addWidget(add_semester_btn, alignment=Qt.AlignmentFlag.AlignRight)
        left_layout.addLayout(semester_header)

        # Semester list
        self.semester_list = QListWidget()
        self.semester_list.setStyleSheet("""
            QListWidget {
                background: #0b1220;
                border: 1px solid #334155;
                border-radius: 8px;
                padding: 5px;
            }
            QListWidget::item {
                padding: 10px;
                border-bottom: 1px solid #1e293b;
            }
            QListWidget::item:selected {
                background: #1e293b;
                border-left: 3px solid #60a5fa;
            }
        """)
        self.semester_list.itemClicked.connect(self._on_semester_selected)
        left_layout.addWidget(self.semester_list)

        # Semester controls
        semester_controls = QHBoxLayout()
        self.edit_semester_btn = QPushButton("✏️ Редактировать")
        self.edit_semester_btn.setEnabled(False)
        self.delete_semester_btn = QPushButton("🗑️ Удалить")
        self.delete_semester_btn.setEnabled(False)
        self.delete_semester_btn.setStyleSheet("""
            QPushButton {
                background: #ef4444;
                color: white;
                border: none;
                padding: 8px 16px;
                border-radius: 6px;
                font-weight: bold;
            }
            QPushButton:hover {
                background: #dc2626;
            }
        """)
        
        self.edit_semester_btn.clicked.connect(self._edit_semester)
        self.delete_semester_btn.clicked.connect(self._delete_semester)
        
        semester_controls.addWidget(self.edit_semester_btn)
        semester_controls.addWidget(self.delete_semester_btn)
        left_layout.addLayout(semester_controls)

        # Right panel - Details
        right_panel = QWidget()
        right_layout = QVBoxLayout(right_panel)
        right_layout.setContentsMargins(0, 0, 0, 0)

        # Details header
        details_header = QHBoxLayout()
        self.details_title = QLabel("Выберите раздел для редактирования")
        self.details_title.setStyleSheet("font-weight: bold; color: #94a3b8;")
        details_header.addWidget(self.details_title)
        right_layout.addLayout(details_header)

        # Semester title input
        self.semester_title_input = QLineEdit()
        self.semester_title_input.setPlaceholderText("Название раздела...")
        self.semester_title_input.setStyleSheet("""
            QLineEdit {
                padding: 10px;
                border: 1px solid #334155;
                border-radius: 6px;
                background: #111827;
                color: #e2e8f0;
            }
        """)
        self.semester_title_input.textChanged.connect(self._save_current_semester)
        right_layout.addWidget(QLabel("Название раздела:"))
        right_layout.addWidget(self.semester_title_input)

        # Labs list
        labs_header = QHBoxLayout()
        labs_header.addWidget(QLabel("🧪 Лабораторные работы"))
        add_lab_btn = QPushButton("➕ Добавить лабораторную работу")
        add_lab_btn.setStyleSheet("""
            QPushButton {
                background: #3b82f6;
                color: white;
                border: none;
                padding: 6px 12px;
                border-radius: 4px;
                font-size: 12px;
            }
            QPushButton:hover {
                background: #2563eb;
            }
        """)
        add_lab_btn.clicked.connect(self._add_lab)
        labs_header.addWidget(add_lab_btn)
        right_layout.addLayout(labs_header)

        self.labs_list = QListWidget()
        self.labs_list.setStyleSheet("""
            QListWidget {
                background: #0b1220;
                border: 1px solid #334155;
                border-radius: 8px;
                padding: 5px;
            }
            QListWidget::item {
                padding: 8px;
                border-bottom: 1px solid #1e293b;
            }
        """)
        self.labs_list.itemClicked.connect(self._on_lab_selected)
        right_layout.addWidget(self.labs_list)

        # Lab details
        lab_details_group = QWidget()
        lab_details_layout = QVBoxLayout(lab_details_group)
        
        self.lab_title_input = QLineEdit()
        self.lab_title_input.setPlaceholderText("Название лабораторной работы...")
        self.lab_title_input.setStyleSheet("""
            QLineEdit {
                padding: 8px;
                border: 1px solid #334155;
                border-radius: 6px;
                background: #111827;
                color: #e2e8f0;
            }
        """)
        self.lab_title_input.textChanged.connect(self._save_current_lab)
        
        self.lab_link_input = QLineEdit()
        self.lab_link_input.setPlaceholderText("Ссылка на работу...")
        self.lab_link_input.setStyleSheet("""
            QLineEdit {
                padding: 8px;
                border: 1px solid #334155;
                border-radius: 6px;
                background: #111827;
                color: #e2e8f0;
            }
        """)
        self.lab_link_input.textChanged.connect(self._save_current_lab)

        lab_details_layout.addWidget(QLabel("Название:"))
        lab_details_layout.addWidget(self.lab_title_input)
        lab_details_layout.addWidget(QLabel("Ссылка:"))
        lab_details_layout.addWidget(self.lab_link_input)

        # Lab controls
        lab_controls = QHBoxLayout()
        self.delete_lab_btn = QPushButton("🗑️ Удалить лабораторную работу")
        self.delete_lab_btn.setEnabled(False)
        self.delete_lab_btn.setStyleSheet("""
            QPushButton {
                background: #ef4444;
                color: white;
                border: none;
                padding: 6px 12px;
                border-radius: 4px;
                font-size: 12px;
            }
            QPushButton:hover {
                background: #dc2626;
            }
        """)
        self.delete_lab_btn.clicked.connect(self._delete_lab)
        lab_controls.addWidget(self.delete_lab_btn)
        lab_details_layout.addLayout(lab_controls)

        right_layout.addWidget(lab_details_group)

        # Add panels to splitter
        splitter.addWidget(left_panel)
        splitter.addWidget(right_panel)
        splitter.setSizes([300, 700])
        main_layout.addWidget(splitter)

        # Buttons
        buttons_layout = QHBoxLayout()
        self.save_btn = QPushButton("💾 Сохранить модуль")
        self.save_btn.setStyleSheet("""
            QPushButton {
                background: #22c55e;
                color: white;
                border: none;
                padding: 12px 24px;
                border-radius: 8px;
                font-weight: bold;
                font-size: 14px;
            }
            QPushButton:hover {
                background: #16a34a;
            }
        """)
        self.save_btn.clicked.connect(self.accept)
        
        cancel_btn = QPushButton("❌ Отмена")
        cancel_btn.setStyleSheet("""
            QPushButton {
                background: #64748b;
                color: white;
                border: none;
                padding: 12px 24px;
                border-radius: 8px;
                font-weight: bold;
                font-size: 14px;
            }
            QPushButton:hover {
                background: #475569;
            }
        """)
        cancel_btn.clicked.connect(self.reject)

        buttons_layout.addStretch()
        buttons_layout.addWidget(cancel_btn)
        buttons_layout.addWidget(self.save_btn)
        main_layout.addLayout(buttons_layout)

        # Initialize data
        self.current_module_data = module_data or {"title": "", "semesters": []}
        self.current_semester_index = -1
        self.current_lab_index = -1
        
        self._populate_semester_list()
        if self.semester_list.count() > 0:
            self.semester_list.setCurrentRow(0)
            self._on_semester_selected(self.semester_list.item(0))

    def _populate_semester_list(self):
        """Populate the semester list from module data"""
        self.semester_list.clear()
        for i, semester in enumerate(self.current_module_data.get("semesters", [])):
            item = QListWidgetItem(f"📋 {semester.get('title', f'Раздел {i+1}')}")
            item.setData(Qt.ItemDataRole.UserRole, i)
            self.semester_list.addItem(item)

    def _add_semester(self):
        """Add a new semester"""
        new_semester = {
            "id": len(self.current_module_data["semesters"]) + 1,
            "title": f"Новый раздел {len(self.current_module_data['semesters']) + 1}",
            "labs": []
        }
        self.current_module_data["semesters"].append(new_semester)
        
        # Update list
        self._populate_semester_list()
        
        # Select the new semester
        new_item = self.semester_list.item(self.semester_list.count() - 1)
        self.semester_list.setCurrentItem(new_item)
        self._on_semester_selected(new_item)

    def _edit_semester(self):
        """Edit selected semester"""
        current_item = self.semester_list.currentItem()
        if current_item:
            semester_index = current_item.data(Qt.ItemDataRole.UserRole)
            semester = self.current_module_data["semesters"][semester_index]
            
            # Create edit dialog
            dialog = QInputDialog(self)
            dialog.setWindowTitle("Редактировать раздел")
            dialog.setLabelText("Название раздела:")
            dialog.setTextValue(semester["title"])
            dialog.setInputMode(QInputDialog.InputMode.TextInput)
            
            if dialog.exec():
                new_title = dialog.textValue().strip()
                if new_title:
                    semester["title"] = new_title
                    current_item.setText(f"📋 {new_title}")
                    self.semester_title_input.setText(new_title)

    def _delete_semester(self):
        """Delete selected semester"""
        current_item = self.semester_list.currentItem()
        if current_item:
            reply = QMessageBox.question(self, "Подтверждение", 
                                       "Вы уверены, что хотите удалить этот раздел?",
                                       QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
            if reply == QMessageBox.StandardButton.Yes:
                semester_index = current_item.data(Qt.ItemDataRole.UserRole)
                self.current_module_data["semesters"].pop(semester_index)
                self._populate_semester_list()
                
                # Clear details
                self.semester_title_input.clear()
                self.labs_list.clear()
                self.lab_title_input.clear()
                self.lab_link_input.clear()
                self.edit_semester_btn.setEnabled(False)
                self.delete_semester_btn.setEnabled(False)
                self.delete_lab_btn.setEnabled(False)

    def _add_lab(self):
        """Add a new lab to current semester"""
        if self.current_semester_index == -1:
            QMessageBox.warning(self, "Внимание", "Сначала выберите раздел")
            return
            
        new_lab = {
            "id": len(self.current_module_data["semesters"][self.current_semester_index]["labs"]) + 1,
            "title": f"Новая лабораторная работа {len(self.current_module_data['semesters'][self.current_semester_index]['labs']) + 1}",
            "link": "#"
        }
        
        self.current_module_data["semesters"][self.current_semester_index]["labs"].append(new_lab)
        self._populate_labs_list()

    def _delete_lab(self):
        """Delete selected lab"""
        if self.current_lab_index == -1:
            return
            
        reply = QMessageBox.question(self, "Подтверждение", 
                                   "Вы уверены, что хотите удалить эту лабораторную работу?",
                                   QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        if reply == QMessageBox.StandardButton.Yes:
            self.current_module_data["semesters"][self.current_semester_index]["labs"].pop(self.current_lab_index)
            self._populate_labs_list()

    def _populate_labs_list(self):
        """Populate the labs list for current semester"""
        self.labs_list.clear()
        if self.current_semester_index != -1:
            semester = self.current_module_data["semesters"][self.current_semester_index]
            for i, lab in enumerate(semester["labs"]):
                item = QListWidgetItem(f"🧪 {lab['title']}")
                item.setData(Qt.ItemDataRole.UserRole, i)
                self.labs_list.addItem(item)

    def _on_semester_selected(self, item):
        """Handle semester selection"""
        if not item:
            return
            
        self.current_semester_index = item.data(Qt.ItemDataRole.UserRole)
        semester = self.current_module_data["semesters"][self.current_semester_index]
        
        self.details_title.setText(f"Редактирование: {semester['title']}")
        self.semester_title_input.setText(semester["title"])
        self._populate_labs_list()
        
        self.edit_semester_btn.setEnabled(True)
        self.delete_semester_btn.setEnabled(True)
        self.delete_lab_btn.setEnabled(False)

    def _on_lab_selected(self, item):
        """Handle lab selection"""
        if not item:
            return
            
        self.current_lab_index = item.data(Qt.ItemDataRole.UserRole)
        lab = self.current_module_data["semesters"][self.current_semester_index]["labs"][self.current_lab_index]
        
        self.lab_title_input.setText(lab["title"])
        self.lab_link_input.setText(lab["link"])
        self.delete_lab_btn.setEnabled(True)

    def _save_current_semester(self):
        """Save current semester title"""
        if self.current_semester_index != -1:
            new_title = self.semester_title_input.text().strip()
            if new_title:
                self.current_module_data["semesters"][self.current_semester_index]["title"] = new_title
                # Update list item
                current_item = self.semester_list.currentItem()
                if current_item:
                    current_item.setText(f"📋 {new_title}")

    def _save_current_lab(self):
        """Save current lab data"""
        if self.current_semester_index != -1 and self.current_lab_index != -1:
            lab = self.current_module_data["semesters"][self.current_semester_index]["labs"][self.current_lab_index]
            lab["title"] = self.lab_title_input.text().strip()
            lab["link"] = self.lab_link_input.text().strip()
            
            # Update list item
            current_item = self.labs_list.currentItem()
            if current_item:
                current_item.setText(f"🧪 {lab['title']}")

    def get_module_data(self):
        """Get the complete module data"""
        return {
            "title": self.title_input.text().strip(),
            "semesters": self.current_module_data["semesters"]
        }

class ThesisDialog(QDialog):
    def __init__(self, parent=None, title: str = "", thesis_data: Dict[str, Any] | None = None):
        super().__init__(parent)
        self.setWindowTitle(title)
        self.setModal(True)
        self.resize(500, 600)

        layout = QFormLayout(self)

        # Title
        self.title_input = QLineEdit()
        self.title_input.setText(thesis_data.get("title", "") if thesis_data else "")
        layout.addRow("Название:", self.title_input)

        # Topic
        self.topic_input = QLineEdit()
        self.topic_input.setText(thesis_data.get("topic", "") if thesis_data else "")
        layout.addRow("Тема:", self.topic_input)

        # Description
        self.description_input = QTextEdit()
        self.description_input.setPlainText(thesis_data.get("description", "") if thesis_data else "")
        layout.addRow("Описание:", self.description_input)

        # Preview Image
        self.preview_input = QLineEdit()
        self.preview_input.setText(thesis_data.get("previewImage", "") if thesis_data else "")
        layout.addRow("Превью изображение:", self.preview_input)

        # Link
        self.link_input = QLineEdit()
        self.link_input.setText(thesis_data.get("link", "") if thesis_data else "")
        layout.addRow("Ссылка:", self.link_input)

        # Key Features
        self.features_layout = QVBoxLayout()
        self.features_layout.addWidget(QLabel("Основные разделы:"))

        if thesis_data and "keyFeatures" in thesis_data:
            for feature in thesis_data["keyFeatures"]:
                self._add_feature_widget(feature)
        else:
            self._add_feature_widget()

        add_feature_btn = QPushButton("➕ Добавить раздел")
        add_feature_btn.clicked.connect(self._add_feature_widget)
        self.features_layout.addWidget(add_feature_btn)

        layout.addRow(self.features_layout)

        # Buttons
        self.btns = QDialogButtonBox(QDialogButtonBox.StandardButton.Save | QDialogButtonBox.StandardButton.Cancel)
        self.btns.accepted.connect(self.accept)
        self.btns.rejected.connect(self.reject)
        layout.addRow(self.btns)

    def _add_feature_widget(self, feature_text: str = ""):
        feature_widget = QWidget()
        feature_layout = QHBoxLayout(feature_widget)

        feature_input = QLineEdit()
        feature_input.setText(feature_text)
        feature_layout.addWidget(feature_input)

        self.features_layout.insertLayout(self.features_layout.count() - 1, feature_layout)

    def get_thesis_data(self):
        thesis_data = {
            "title": self.title_input.text(),
            "topic": self.topic_input.text(),
            "description": self.description_input.toPlainText(),
            "previewImage": self.preview_input.text(),
            "link": self.link_input.text(),
            "keyFeatures": []
        }

        # Extract features (simplified for demo)
        thesis_data["keyFeatures"].append("Пример раздела")

        return thesis_data

class CourseworkDialog(QDialog):
    def __init__(self, parent=None, title: str = "", coursework_data: Dict[str, Any] | None = None):
        super().__init__(parent)
        self.setWindowTitle(title)
        self.setModal(True)
        self.resize(500, 500)

        layout = QFormLayout(self)

        # Title
        self.title_input = QLineEdit()
        self.title_input.setText(coursework_data.get("title", "") if coursework_data else "")
        layout.addRow("Название:", self.title_input)

        # Semester
        self.semester_input = QLineEdit()
        self.semester_input.setText(coursework_data.get("semester", "") if coursework_data else "")
        layout.addRow("Семестр:", self.semester_input)

        # Description
        self.description_input = QTextEdit()
        self.description_input.setPlainText(coursework_data.get("description", "") if coursework_data else "")
        layout.addRow("Описание:", self.description_input)

        # Link
        self.link_input = QLineEdit()
        self.link_input.setText(coursework_data.get("link", "") if coursework_data else "")
        layout.addRow("Ссылка:", self.link_input)

        # Technologies
        self.technologies_layout = QVBoxLayout()
        self.technologies_layout.addWidget(QLabel("Технологии:"))

        if coursework_data and "technologies" in coursework_data:
            for tech in coursework_data["technologies"]:
                self._add_technology_widget(tech)
        else:
            self._add_technology_widget()

        add_tech_btn = QPushButton("➕ Добавить технологию")
        add_tech_btn.clicked.connect(self._add_technology_widget)
        self.technologies_layout.addWidget(add_tech_btn)

        layout.addRow(self.technologies_layout)

        # Buttons
        self.btns = QDialogButtonBox(QDialogButtonBox.StandardButton.Save | QDialogButtonBox.StandardButton.Cancel)
        self.btns.accepted.connect(self.accept)
        self.btns.rejected.connect(self.reject)
        layout.addRow(self.btns)

    def _add_technology_widget(self, tech_text: str = ""):
        tech_widget = QWidget()
        tech_layout = QHBoxLayout(tech_widget)

        tech_input = QLineEdit()
        tech_input.setText(tech_text)
        tech_layout.addWidget(tech_input)

        self.technologies_layout.insertLayout(self.technologies_layout.count() - 1, tech_layout)

    def get_coursework_data(self):
        coursework_data = {
            "title": self.title_input.text(),
            "semester": self.semester_input.text(),
            "description": self.description_input.toPlainText(),
            "link": self.link_input.text(),
            "technologies": []
        }

        # Extract technologies (simplified for demo)
        coursework_data["technologies"].append("Пример технологии")

        return coursework_data

class PracticalWorkDialog(QDialog):
    def __init__(self, parent=None, title: str = "", practical_data: Dict[str, Any] | None = None):
        super().__init__(parent)
        self.setWindowTitle(title)
        self.setModal(True)
        self.resize(500, 500)

        layout = QFormLayout(self)

        # Title
        self.title_input = QLineEdit()
        self.title_input.setText(practical_data.get("title", "") if practical_data else "")
        layout.addRow("Название:", self.title_input)

        # Semester
        self.semester_input = QLineEdit()
        self.semester_input.setText(practical_data.get("semester", "") if practical_data else "")
        layout.addRow("Семестр:", self.semester_input)

        # Description
        self.description_input = QTextEdit()
        self.description_input.setPlainText(practical_data.get("description", "") if practical_data else "")
        layout.addRow("Описание:", self.description_input)

        # Link
        self.link_input = QLineEdit()
        self.link_input.setText(practical_data.get("link", "") if practical_data else "")
        layout.addRow("Ссылка:", self.link_input)

        # Items
        self.items_layout = QVBoxLayout()
        self.items_layout.addWidget(QLabel("Практические работы:"))

        if practical_data and "items" in practical_data:
            for item in practical_data["items"]:
                self._add_item_widget(item)
        else:
            self._add_item_widget()

        add_item_btn = QPushButton("➕ Добавить работу")
        add_item_btn.clicked.connect(self._add_item_widget)
        self.items_layout.addWidget(add_item_btn)

        layout.addRow(self.items_layout)

        # Buttons
        self.btns = QDialogButtonBox(QDialogButtonBox.StandardButton.Save | QDialogButtonBox.StandardButton.Cancel)
        self.btns.accepted.connect(self.accept)
        self.btns.rejected.connect(self.reject)
        layout.addRow(self.btns)

    def _add_item_widget(self, item_text: str = ""):
        item_widget = QWidget()
        item_layout = QHBoxLayout(item_widget)

        item_input = QLineEdit()
        item_input.setText(item_text)
        item_layout.addWidget(item_input)

        self.items_layout.insertLayout(self.items_layout.count() - 1, item_layout)

    def get_practical_data(self):
        practical_data = {
            "title": self.title_input.text(),
            "semester": self.semester_input.text(),
            "description": self.description_input.toPlainText(),
            "link": self.link_input.text(),
            "items": []
        }

        # Extract items (simplified for demo)
        practical_data["items"].append("Пример работы")

        return practical_data

class PortfolioApp(QMainWindow):
    def __init__(self, repo_path: str = "."):
        super().__init__()
        self.repo_path = os.path.abspath(repo_path)
        self.manager = PortfolioManager(self.repo_path)
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Portfolio Manager - Студенческое портфолио")
        self.setGeometry(100, 100, 1400, 900)
        self.setStyleSheet("""
            QMainWindow { background: #0f172a; color: #e2e8f0; }
            QWidget { background: #0f172a; color: #e2e8f0; }
            QLabel { font-family: 'Segoe UI', Roboto, Helvetica, Arial, sans-serif; color: #e2e8f0; font-size: 14px; }
            QPushButton { 
                padding: 10px 16px; 
                border-radius: 8px; 
                border: 1px solid #334155; 
                background: #1e293b; 
                color: #e2e8f0; 
                font-weight: 500;
                transition: all 0.2s ease;
            }
            QPushButton:hover { 
                background: #334155; 
                border-color: #475569;
                transform: translateY(-1px);
            }
            QPushButton:pressed { transform: translateY(0); }
            QTableWidget { 
                border: 1px solid #334155; 
                background: #0b1220; 
                color: #e2e8f0; 
                gridline-color: #334155; 
                border-radius: 8px;
            }
            QHeaderView::section { 
                background: #1e293b; 
                color: #e2e8f0; 
                padding: 8px; 
                border: 1px solid #334155;
                font-weight: 600;
            }
            QProgressBar { 
                height: 10px; 
                border-radius: 5px; 
                background: #1e293b; 
                border: 1px solid #334155;
            }
            QProgressBar::chunk { 
                background-color: #22c55e; 
                border-radius: 5px;
            }
            QLineEdit, QTextEdit { 
                background: #111827; 
                color: #e2e8f0; 
                border: 1px solid #334155; 
                border-radius: 6px;
                padding: 8px;
            }
            QLineEdit:focus, QTextEdit:focus { border-color: #60a5fa; }
            QComboBox { 
                background: #111827; 
                color: #e2e8f0; 
                border: 1px solid #334155; 
                border-radius: 6px;
                padding: 8px;
            }
            QTabWidget::pane { border: 1px solid #334155; background: #0f172a; }
            QTabBar::tab { 
                background: #1e293b; 
                color: #e2e8f0; 
                padding: 8px 16px; 
                border: 1px solid #334155; 
                border-bottom: none; 
                border-radius: 6px 6px 0 0;
                margin-right: 2px;
            }
            QTabBar::tab:selected { background: #0f172a; border-bottom: 1px solid #0f172a; }
            QDialog { background: #0f172a; }
            QDialogButtonBox { background: transparent; }
        """)

        central = QWidget()
        self.setCentralWidget(central)
        main = QHBoxLayout(central)

        # Navigation
        nav = QVBoxLayout()
        nav.setContentsMargins(12,12,12,12)

        # Header
        header = QLabel("Portfolio Manager")
        header.setStyleSheet("font-size: 18px; font-weight: bold; color: #60a5fa; margin-bottom: 10px;")
        nav.addWidget(header)

        # Navigation buttons with icons
        self.education_btn = QPushButton("📚 Учебные модули")
        self.thesis_btn = QPushButton("🎓 Дипломная работа")
        self.courseworks_btn = QPushButton("📝 Курсовые работы")
        self.practical_btn = QPushButton("💻 Практические работы")
        self.deploy_btn = QPushButton("🚀 Автодеплой в GitHub")
        self.preview_btn = QPushButton("👀 Просмотр сайта")

        # Style navigation buttons
        nav_style = """
            QPushButton {
                text-align: left;
                padding: 12px 16px;
                border-radius: 8px;
                border: 1px solid #334155;
                background: #0b1220;
                color: #e2e8f0;
                font-weight: 500;
                margin-bottom: 8px;
            }
            QPushButton:hover {
                background: #1e293b;
                border-color: #475569;
            }
            QPushButton:pressed {
                background: #334155;
            }
        """
        
        for b in [self.education_btn, self.thesis_btn, self.courseworks_btn, self.practical_btn,
                 self.deploy_btn, self.preview_btn]:
            b.setStyleSheet(nav_style)
            b.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

        self.education_btn.clicked.connect(lambda: self.work_area.setCurrentIndex(0))
        self.thesis_btn.clicked.connect(lambda: self.work_area.setCurrentIndex(1))
        self.courseworks_btn.clicked.connect(lambda: self.work_area.setCurrentIndex(2))
        self.practical_btn.clicked.connect(lambda: self.work_area.setCurrentIndex(3))
        self.deploy_btn.clicked.connect(lambda: self.work_area.setCurrentIndex(4))
        self.preview_btn.clicked.connect(self.openSite)

        nav.addWidget(self.education_btn)
        nav.addWidget(self.thesis_btn)
        nav.addWidget(self.courseworks_btn)
        nav.addWidget(self.practical_btn)
        nav.addWidget(self.deploy_btn)
        nav.addWidget(self.preview_btn)
        
        # Spacer
        nav.addStretch()

        main.addLayout(nav, 1)

        # Work area
        self.work_area = QStackedWidget()

        # Education Modules Tab
        self.education_widget = self.create_education_widget()
        self.thesis_widget = self.create_thesis_widget()
        self.courseworks_widget = self.create_courseworks_widget()
        self.practical_widget = self.create_practical_widget()
        self.deploy_widget = self.create_deploy_widget()

        self.work_area.addWidget(self.education_widget)
        self.work_area.addWidget(self.thesis_widget)
        self.work_area.addWidget(self.courseworks_widget)
        self.work_area.addWidget(self.practical_widget)
        self.work_area.addWidget(self.deploy_widget)

        main.addWidget(self.work_area, 4)

        self.statusBar().showMessage("Готов к работе")

    def create_education_widget(self):
        w = QWidget()
        lay = QVBoxLayout(w)
        lay.addWidget(QLabel("📚 Управление учебными модулями"))

        self.add_education_btn = QPushButton("➕ Добавить учебный модуль")
        self.add_education_btn.clicked.connect(self.add_education_module)
        lay.addWidget(self.add_education_btn)

        self.education_table = QTableWidget()
        self.education_table.setColumnCount(3)
        self.education_table.setHorizontalHeaderLabels(["Название модуля", "Количество семестров"])
        if self.education_table.horizontalHeader():
            self.education_table.horizontalHeader().setStretchLastSection(True)
        self.education_table.setAlternatingRowColors(True)
        lay.addWidget(self.education_table)

        btns = QHBoxLayout()
        edit_btn = QPushButton("✏️ Редактировать")
        delete_btn = QPushButton("🗑️ Удалить")
        refresh_btn = QPushButton("🔄 Обновить")

        edit_btn.clicked.connect(self.edit_education_module)
        delete_btn.clicked.connect(self.delete_education_module)
        refresh_btn.clicked.connect(self.refresh_education_modules)

        for b in [edit_btn, delete_btn, refresh_btn]: btns.addWidget(b)
        lay.addLayout(btns)

        self.refresh_education_modules()
        return w

    def create_thesis_widget(self):
        w = QWidget()
        lay = QVBoxLayout(w)
        lay.addWidget(QLabel("🎓 Управление дипломной работой"))

        self.edit_thesis_btn = QPushButton("✏️ Редактировать дипломную работу")
        self.edit_thesis_btn.clicked.connect(self.edit_thesis)
        lay.addWidget(self.edit_thesis_btn)

        self.thesis_info = QTextEdit()
        self.thesis_info.setReadOnly(True)
        lay.addWidget(self.thesis_info)

        self.refresh_thesis()
        return w

    def create_courseworks_widget(self):
        w = QWidget()
        lay = QVBoxLayout(w)
        lay.addWidget(QLabel("📝 Управление курсовыми работами"))

        self.add_coursework_btn = QPushButton("➕ Добавить курсовую работу")
        self.add_coursework_btn.clicked.connect(self.add_coursework)
        lay.addWidget(self.add_coursework_btn)

        self.courseworks_table = QTableWidget()
        self.courseworks_table.setColumnCount(3)
        self.courseworks_table.setHorizontalHeaderLabels(["Название", "Семестр", "Технологии"])
        if self.courseworks_table.horizontalHeader():
            self.courseworks_table.horizontalHeader().setStretchLastSection(True)
        self.courseworks_table.setAlternatingRowColors(True)
        lay.addWidget(self.courseworks_table)

        btns = QHBoxLayout()
        edit_btn = QPushButton("✏️ Редактировать")
        delete_btn = QPushButton("🗑️ Удалить")
        refresh_btn = QPushButton("🔄 Обновить")

        edit_btn.clicked.connect(self.edit_coursework)
        delete_btn.clicked.connect(self.delete_coursework)
        refresh_btn.clicked.connect(self.refresh_courseworks)

        for b in [edit_btn, delete_btn, refresh_btn]: btns.addWidget(b)
        lay.addLayout(btns)

        self.refresh_courseworks()
        return w

    def create_practical_widget(self):
        w = QWidget()
        lay = QVBoxLayout(w)
        lay.addWidget(QLabel("💻 Управление практическими работами"))

        self.add_practical_btn = QPushButton("➕ Добавить практические работы")
        self.add_practical_btn.clicked.connect(self.add_practical_work)
        lay.addWidget(self.add_practical_btn)

        self.practical_table = QTableWidget()
        self.practical_table.setColumnCount(3)
        self.practical_table.setHorizontalHeaderLabels(["Название", "Семестр", "Количество работ"])
        if self.practical_table.horizontalHeader():
            self.practical_table.horizontalHeader().setStretchLastSection(True)
        self.practical_table.setAlternatingRowColors(True)
        lay.addWidget(self.practical_table)

        btns = QHBoxLayout()
        edit_btn = QPushButton("✏️ Редактировать")
        delete_btn = QPushButton("🗑️ Удалить")
        refresh_btn = QPushButton("🔄 Обновить")

        edit_btn.clicked.connect(self.edit_practical_work)
        delete_btn.clicked.connect(self.delete_practical_work)
        refresh_btn.clicked.connect(self.refresh_practical_works)

        for b in [edit_btn, delete_btn, refresh_btn]: btns.addWidget(b)
        lay.addLayout(btns)

        self.refresh_practical_works()
        return w

    def create_deploy_widget(self):
        w = QWidget()
        lay = QVBoxLayout(w)
        lay.addWidget(QLabel("🚀 Автодеплой в GitHub"))
        lay.addWidget(QLabel("Эта функция автоматически загружает все изменения в ваш GitHub репозиторий."))
        lay.addWidget(QLabel("Сообщение коммита:"))
        self.commit_input = QTextEdit()
        self.commit_input.setPlainText("Update portfolio content via Portfolio Manager")
        self.commit_input.setMaximumHeight(80)
        lay.addWidget(self.commit_input)
        self.deploy_btn = QPushButton("🚀 Загрузить в GitHub")
        self.deploy_btn.setStyleSheet("background-color:#28a745; color:white; font-weight:bold;")
        self.deploy_btn.clicked.connect(self.deploy_changes)
        lay.addWidget(self.deploy_btn)
        self.deploy_status = QLabel("")
        lay.addWidget(self.deploy_status)
        self.deploy_progress = QProgressBar()
        lay.addWidget(self.deploy_progress)
        lay.addStretch()
        return w

    def openSite(self):
        webbrowser.open("https://NSODAT.github.io/student-portfolio")

    # Education Modules Methods
    def refresh_education_modules(self):
        modules = self.manager.read_education_modules()
        self.education_table.setRowCount(len(modules))
        for i, module in enumerate(modules):
            self.education_table.setItem(i, 0, QTableWidgetItem(module.get("title", "")))
            self.education_table.setItem(i, 1, QTableWidgetItem(str(len(module.get("semesters", [])))))

    def add_education_module(self):
        dialog = EducationModuleDialog(self, "Добавить учебный модуль")
        if dialog.exec():
            data = dialog.get_module_data()
            modules = self.manager.read_education_modules()
            data["id"] = len(modules) + 1
            modules.append(data)
            if self.manager.write_education_modules(modules):
                self.refresh_education_modules()

    def edit_education_module(self):
        row = self.education_table.currentRow()
        if row < 0:
            QMessageBox.warning(self, "Внимание", "Выберите модуль для редактирования")
            return
        modules = self.manager.read_education_modules()
        if row >= len(modules):
            return
        dialog = EducationModuleDialog(self, "Редактировать учебный модуль", modules[row])
        if dialog.exec():
            updated = dialog.get_module_data()
            updated["id"] = modules[row]["id"]
            modules[row] = updated
            if self.manager.write_education_modules(modules):
                self.refresh_education_modules()

    def delete_education_module(self):
        row = self.education_table.currentRow()
        if row < 0:
            return
        reply = QMessageBox.question(self, "Подтверждение", "Вы уверены, что хотите удалить этот модуль?",
                                     QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        if reply == QMessageBox.StandardButton.Yes:
            modules = self.manager.read_education_modules()
            if row < len(modules):
                modules.pop(row)
                if self.manager.write_education_modules(modules):
                    self.refresh_education_modules()

    # Thesis Methods
    def refresh_thesis(self):
        thesis = self.manager.read_thesis()
        info = f"📝 {thesis.get('title', 'Дипломная работа')}\n\n"
        info += f"🎯 Тема: {thesis.get('topic', 'Не указана')}\n\n"
        info += f"📄 Описание: {thesis.get('description', 'Нет описания')}\n\n"
        info += f"🔗 Ссылка: {thesis.get('link', '#')}\n\n"
        info += "📋 Основные разделы:\n"
        for feature in thesis.get("keyFeatures", []):
            info += f"• {feature}\n"
        self.thesis_info.setPlainText(info)

    def edit_thesis(self):
        thesis = self.manager.read_thesis()
        dialog = ThesisDialog(self, "Редактировать дипломную работу", thesis)
        if dialog.exec():
            updated = dialog.get_thesis_data()
            if self.manager.write_thesis(updated):
                self.refresh_thesis()

    # Courseworks Methods
    def refresh_courseworks(self):
        courseworks = self.manager.read_courseworks()
        self.courseworks_table.setRowCount(len(courseworks))
        for i, cw in enumerate(courseworks):
            self.courseworks_table.setItem(i, 0, QTableWidgetItem(cw.get("title", "")))
            self.courseworks_table.setItem(i, 1, QTableWidgetItem(cw.get("semester", "")))
            self.courseworks_table.setItem(i, 2, QTableWidgetItem(", ".join(cw.get("technologies", []))))

    def add_coursework(self):
        dialog = CourseworkDialog(self, "Добавить курсовую работу")
        if dialog.exec():
            data = dialog.get_coursework_data()
            courseworks = self.manager.read_courseworks()
            data["id"] = len(courseworks) + 1
            courseworks.append(data)
            if self.manager.write_courseworks(courseworks):
                self.refresh_courseworks()

    def edit_coursework(self):
        row = self.courseworks_table.currentRow()
        if row < 0:
            QMessageBox.warning(self, "Внимание", "Выберите курсовую работу для редактирования")
            return
        courseworks = self.manager.read_courseworks()
        if row >= len(courseworks):
            return
        dialog = CourseworkDialog(self, "Редактировать курсовую работу", courseworks[row])
        if dialog.exec():
            updated = dialog.get_coursework_data()
            updated["id"] = courseworks[row]["id"]
            courseworks[row] = updated
            if self.manager.write_courseworks(courseworks):
                self.refresh_courseworks()

    def delete_coursework(self):
        row = self.courseworks_table.currentRow()
        if row < 0:
            return
        reply = QMessageBox.question(self, "Подтверждение", "Вы уверены, что хотите удалить эту курсовую работу?",
                                     QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        if reply == QMessageBox.StandardButton.Yes:
            courseworks = self.manager.read_courseworks()
            if row < len(courseworks):
                courseworks.pop(row)
                if self.manager.write_courseworks(courseworks):
                    self.refresh_courseworks()

    # Practical Works Methods
    def refresh_practical_works(self):
        practical_works = self.manager.read_practical_works()
        self.practical_table.setRowCount(len(practical_works))
        for i, pw in enumerate(practical_works):
            self.practical_table.setItem(i, 0, QTableWidgetItem(pw.get("title", "")))
            self.practical_table.setItem(i, 1, QTableWidgetItem(pw.get("semester", "")))
            self.practical_table.setItem(i, 2, QTableWidgetItem(str(len(pw.get("items", [])))))

    def add_practical_work(self):
        dialog = PracticalWorkDialog(self, "Добавить практические работы")
        if dialog.exec():
            data = dialog.get_practical_data()
            practical_works = self.manager.read_practical_works()
            data["id"] = len(practical_works) + 1
            practical_works.append(data)
            if self.manager.write_practical_works(practical_works):
                self.refresh_practical_works()

    def edit_practical_work(self):
        row = self.practical_table.currentRow()
        if row < 0:
            QMessageBox.warning(self, "Внимание", "Выберите практические работы для редактирования")
            return
        practical_works = self.manager.read_practical_works()
        if row >= len(practical_works):
            return
        dialog = PracticalWorkDialog(self, "Редактировать практические работы", practical_works[row])
        if dialog.exec():
            updated = dialog.get_practical_data()
            updated["id"] = practical_works[row]["id"]
            practical_works[row] = updated
            if self.manager.write_practical_works(practical_works):
                self.refresh_practical_works()

    def delete_practical_work(self):
        row = self.practical_table.currentRow()
        if row < 0:
            return
        reply = QMessageBox.question(self, "Подтверждение", "Вы уверены, что хотите удалить эти практические работы?",
                                     QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        if reply == QMessageBox.StandardButton.Yes:
            practical_works = self.manager.read_practical_works()
            if row < len(practical_works):
                practical_works.pop(row)
                if self.manager.write_practical_works(practical_works):
                    self.refresh_practical_works()

    # Deploy Methods
    def deploy_changes(self):
        commit_msg = self.commit_input.toPlainText().strip() or "Update portfolio content via Portfolio Manager"
        self.deploy_status.setText("🔄 Загрузка изменений в GitHub...")
        self.deploy_btn.setEnabled(False)
        self.deploy_progress.setValue(0)
        self._setup_deploy_worker(commit_msg)

    def _setup_deploy_worker(self, commit_msg: str):
        self.worker = DeployWorker(self.manager, commit_msg)
        self.thread = QThread()
        self.worker.moveToThread(self.thread)
        self.worker.finished.connect(self._deploy_finished)
        self.thread.started.connect(self.worker.run)
        self.thread.start()
        from PyQt6.QtCore import QTimer
        self._prog = 0
        self.progress_timer = QTimer()
        self.progress_timer.timeout.connect(self._advance_progress)
        self.progress_timer.start(120)

    def _advance_progress(self):
        if self._prog < 95:
            self._prog += 4
            self.deploy_progress.setValue(self._prog)
        else:
            if hasattr(self, 'progress_timer') and self.progress_timer.isActive():
                self.progress_timer.stop()

    def _deploy_finished(self, ok: bool):
        if hasattr(self, 'progress_timer') and self.progress_timer.isActive():
            self.progress_timer.stop()
        self.deploy_progress.setValue(100 if ok else 0)
        self.deploy_status.setText("✅ Изменения успешно загружены в GitHub!" if ok else "❌ Ошибка при загрузке изменений")
        self.deploy_btn.setEnabled(True)
        if hasattr(self, 'thread'):
            self.thread.quit()
            self.thread.wait()
        self.worker = None
        self.thread = None

class DeployWorker(QObject):
    finished = pyqtSignal(bool)
    def __init__(self, manager: PortfolioManager, commit_message: str):
        super().__init__()
        self.manager = manager
        self.commit_message = commit_message

    @pyqtSlot()
    def run(self):
        ok = self.manager.deploy_to_github(self.commit_message)
        self.finished.emit(ok)

def main():
    repo_path = os.path.dirname(os.path.abspath(__file__))
    app = QApplication(sys.argv)
    win = PortfolioApp(repo_path)
    win.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
