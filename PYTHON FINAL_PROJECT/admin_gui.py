#S.P.E.A.K - System for Public Empowerment and Knowledge
#Made by the people, made for the people

#ADMIN'S DASHBOARD GUI
#ADMIN'S DASHBOARD GUI

from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QPushButton, QTableWidget, QTableWidgetItem, QComboBox,
    QTextEdit, QMessageBox, QHeaderView, QFrame
)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QFont, QColor


class AdminDashboard(QMainWindow): #ADMIN DASHBOARD TO MANAGE AND VIEW COMPLAINTS
    
    logout_requested = pyqtSignal()
    
    def __init__(self):
        super().__init__()
        self.current_admin = None
        self._setup_window()
        self._setup_ui()
        
    def _setup_window(self):
        self.setWindowTitle("S.P.E.A.K - Admin Dashboard")
        self.setGeometry(100, 100, 1200, 700)
        
    def _setup_ui(self):
        central = QWidget()
        self.setCentralWidget(central)
        
        main_layout = QVBoxLayout(central)
        main_layout.setSpacing(20)
        main_layout.setContentsMargins(30, 20, 30, 20)
        
        self._add_header(main_layout)
        
        self._add_filters(main_layout)
        
        self._add_complaints_table(main_layout)
        
        self._add_details_panel(main_layout)
        
    def _add_header(self, layout):
        header_layout = QHBoxLayout()
        
        title = QLabel("Complaint Management Dashboard")
        title_font = QFont()
        title_font.setPointSize(18)
        title_font.setBold(True)
        title.setFont(title_font)
        header_layout.addWidget(title)
        
        header_layout.addStretch()
        
        self.admin_label = QLabel("Admin: Not logged in")
        admin_font = QFont()
        admin_font.setPointSize(10)
        self.admin_label.setFont(admin_font)
        header_layout.addWidget(self.admin_label)
        
        logout_btn = QPushButton("Logout")
        logout_btn.setMaximumWidth(100)
        logout_btn.clicked.connect(self.logout_requested.emit)
        header_layout.addWidget(logout_btn)
        
        layout.addLayout(header_layout)
        
    def _add_filters(self, layout): #FILTER OPTIONS
        filter_frame = QFrame()
        filter_frame.setFrameStyle(QFrame.Shape.StyledPanel)
        filter_frame.setStyleSheet("QFrame { background-color: #f5f5f5; border-radius: 5px; }")
        
        filter_layout = QHBoxLayout(filter_frame)
        filter_layout.setContentsMargins(15, 10, 15, 10)
        
        filter_layout.addWidget(QLabel("Filter by Program:"))
        self.program_filter = QComboBox()
        self.program_filter.addItems([
            "All Programs",
            "Bachelor of Science in Computer Science",
            "Bachelor of Science in Information Technology",
            "Bachelor of Science in Information Systems",
            "Bachelor of Science in Computer Engineering"
        ])
        self.program_filter.currentTextChanged.connect(self.filter_complaints)
        self.program_filter.setMinimumWidth(300)
        filter_layout.addWidget(self.program_filter)
        
        filter_layout.addSpacing(20)
        
        filter_layout.addWidget(QLabel("Filter by Status:"))
        self.status_filter = QComboBox()
        self.status_filter.addItems([
            "All Status",
            "Pending",
            "In Progress",
            "Resolved"
        ])
        self.status_filter.currentTextChanged.connect(self.filter_complaints)
        filter_layout.addWidget(self.status_filter)
        
        filter_layout.addStretch()
        
        refresh_btn = QPushButton("Refresh")
        refresh_btn.clicked.connect(self.load_complaints)
        filter_layout.addWidget(refresh_btn)
        
        layout.addWidget(filter_frame)
        
    def _add_complaints_table(self, layout): #COMPLAINTS TABLE
        table_label = QLabel("Complaints List")
        label_font = QFont()
        label_font.setPointSize(12)
        label_font.setBold(True)
        table_label.setFont(label_font)
        layout.addWidget(table_label)
        
        self.complaints_table = QTableWidget()
        self.complaints_table.setColumnCount(6)
        self.complaints_table.setHorizontalHeaderLabels([
            "ID", "Student ID", "Program", "Subject", "Status", "Date"
        ])
        
        header = self.complaints_table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(2, QHeaderView.ResizeMode.Stretch)
        header.setSectionResizeMode(3, QHeaderView.ResizeMode.Stretch)
        header.setSectionResizeMode(4, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(5, QHeaderView.ResizeMode.ResizeToContents)
        
        self.complaints_table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.complaints_table.setSelectionMode(QTableWidget.SelectionMode.SingleSelection)
        self.complaints_table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.complaints_table.itemSelectionChanged.connect(self.on_complaint_selected)
        
        layout.addWidget(self.complaints_table)
        
    def _add_details_panel(self, layout): #COMPLAINT DETAILS AND ACTIONS PANEL
        details_label = QLabel("Complaint Details")
        label_font = QFont()
        label_font.setPointSize(12)
        label_font.setBold(True)
        details_label.setFont(label_font)
        layout.addWidget(details_label)
        
        details_frame = QFrame()
        details_frame.setFrameStyle(QFrame.Shape.StyledPanel)
        details_frame.setStyleSheet("QFrame { background-color: #f9f9f9; border-radius: 5px; }")
        details_frame.setMaximumHeight(200)
        
        details_layout = QVBoxLayout(details_frame)
        details_layout.setContentsMargins(15, 15, 15, 15)
        
        self.details_text = QTextEdit()
        self.details_text.setReadOnly(True)
        self.details_text.setPlaceholderText("Select a complaint to view details...")
        details_layout.addWidget(self.details_text)
        
        button_layout = QHBoxLayout()
        button_layout.addStretch()
        
        self.in_progress_btn = QPushButton("Mark as In Progress")
        self.in_progress_btn.setEnabled(False)
        self.in_progress_btn.clicked.connect(lambda: self.update_status("In Progress"))
        button_layout.addWidget(self.in_progress_btn)
        
        self.resolve_btn = QPushButton("Mark as Resolved")
        self.resolve_btn.setEnabled(False)
        self.resolve_btn.setStyleSheet("QPushButton { background-color: #4CAF50; color: white; padding: 8px 20px; }")
        self.resolve_btn.clicked.connect(lambda: self.update_status("Resolved"))
        button_layout.addWidget(self.resolve_btn)
        
        details_layout.addLayout(button_layout)
        layout.addWidget(details_frame)
        
        self.selected_complaint_id = None
        
    def set_admin(self, admin_name):
        self.current_admin = admin_name
        self.admin_label.setText(f"Admin: {admin_name}")
        
    def load_complaints(self):
        from database import Database
        from config import DB_CONFIG
        
        db = Database(**DB_CONFIG)
        if db.connect():
            complaints_data = db.get_all_complaints()
            db.close()
            
            complaints = []
            for c in complaints_data:
                complaints.append((
                    c['id'],
                    c['school_id'],
                    c['program'],
                    c['subject'],
                    c['status'],
                    c['date']
                ))
            
            self.all_complaints_full = complaints_data
            self.all_complaints = complaints
            self.display_complaints(complaints)
        else:
            self.all_complaints = []
            self.display_complaints([])
            
    def display_complaints(self, complaints): #DISPLAY COMPLAINTS IN THE TABLE
        self.complaints_table.setRowCount(len(complaints))
            
        for row, complaint in enumerate(complaints):
            for col, data in enumerate(complaint):
                item = QTableWidgetItem(str(data))
                    
                #STATUS COLOR CODES
                if col == 4:  
                    if data == "Pending":
                        item.setForeground(QColor("#ff9800"))
                    elif data == "In Progress":
                        item.setForeground(QColor("#2196F3"))
                    elif data == "Resolved":
                        item.setForeground(QColor("#4CAF50"))
                    
                self.complaints_table.setItem(row, col, item)
        
    def filter_complaints(self): #FILTER COMPLAINTS BASED ON SELECTED FILTERS
        program = self.program_filter.currentText()
        status = self.status_filter.currentText()
        
        filtered = self.all_complaints
        
        #FILTER BY PROGRAM
        if program != "All Programs":
            filtered = [c for c in filtered if c[2] == program]
        
        #FILTER BY STATUS
        if status != "All Status":
            filtered = [c for c in filtered if c[4] == status]
        
        self.display_complaints(filtered)
        
    def on_complaint_selected(self): #HANDLE COMPLAINT SELECTION
        selected = self.complaints_table.selectedItems()
        if not selected:
            self.details_text.clear()
            self.in_progress_btn.setEnabled(False)
            self.resolve_btn.setEnabled(False)
            return
        
        row = selected[0].row()
        complaint_id = self.complaints_table.item(row, 0).text()
        
        complaint = None
        for c in self.all_complaints_full:
            if str(c['id']) == complaint_id:
                complaint = c
                break
        
        if not complaint:
            return
        
        self.selected_complaint_id = complaint_id
        
        details = f"""
Complaint ID: {complaint['id']}
Student ID: {complaint['school_id']}
Program: {complaint['program']}
Status: {complaint['status']}
Date Submitted: {complaint['date']}
Category: {complaint['category']}
Location: {complaint['location']}

Subject: {complaint['subject']}

Description:
{complaint['description']}
        """
        
        self.details_text.setText(details.strip())
        
        status = complaint['status']
        if status == "Resolved":
            self.in_progress_btn.setEnabled(False)
            self.resolve_btn.setEnabled(False)
        elif status == "In Progress":
            self.in_progress_btn.setEnabled(False)
            self.resolve_btn.setEnabled(True)
        else:
            self.in_progress_btn.setEnabled(True)
            self.resolve_btn.setEnabled(True)
        
    def update_status(self, new_status): #UPDATE COMPLAINT STATUS
        if not self.selected_complaint_id:
            return
        
        reply = QMessageBox.question(
            self,
            "Confirm Status Change",
            f"Mark complaint #{self.selected_complaint_id} as {new_status}?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            from database import Database
            from config import DB_CONFIG
            
            db = Database(**DB_CONFIG)
            if db.connect():
                success, message = db.update_complaint_status(
                    self.selected_complaint_id, 
                    new_status
                )
                db.close()
                
                if success:
                    QMessageBox.information(self, "Status Updated", message)
                    self.load_complaints()
                else:
                    QMessageBox.warning(self, "Update Failed", message)