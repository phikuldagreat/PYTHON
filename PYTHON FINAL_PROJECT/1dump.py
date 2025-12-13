# #ADD THIS METHOD TO YOUR AdminDashboard CLASS

# def _add_login_history_button(self, layout): #ADD LOGIN HISTORY BUTTON TO FILTERS
#     """
#     ADD THIS METHOD CALL IN _add_filters() METHOD, RIGHT AFTER self._add_refresh_button(filter_layout)
#     REPLACE: filter_layout.addStretch() WITH THIS
#     """
#     login_history_btn = QPushButton("View Login History")
#     login_history_btn.setMinimumWidth(180)
#     login_history_btn.setMinimumHeight(40)
#     login_history_btn.setFont(QFont("Arial", 11))
#     login_history_btn.clicked.connect(self.show_login_history_dialog)
#     login_history_btn.setStyleSheet(StyleSheet.get_button_style("secondary"))
#     layout.addWidget(login_history_btn)

# def show_login_history_dialog(self): #SHOW LOGIN HISTORY IN A DIALOG
#     from PyQt6.QtWidgets import QDialog, QVBoxLayout, QLabel, QPushButton, QLineEdit
    
#     dialog = QDialog(self)
#     dialog.setWindowTitle("Student Login History")
#     dialog.setMinimumWidth(700)
#     dialog.setMinimumHeight(500)
#     dialog.setStyleSheet(StyleSheet.get_main_window_style())
    
#     layout = QVBoxLayout(dialog)
#     layout.setSpacing(15)
#     layout.setContentsMargins(20, 20, 20, 20)
    
#     #SEARCH INPUT
#     search_layout = QHBoxLayout()
#     search_label = QLabel("Enter Student ID:")
#     search_label.setFont(QFont("Arial", 11))
#     search_layout.addWidget(search_label)
    
#     student_id_input = QLineEdit()
#     student_id_input.setPlaceholderText("e.g., 2021-12345")
#     student_id_input.setMinimumHeight(35)
#     student_id_input.setFont(QFont("Arial", 11))
#     student_id_input.setStyleSheet(StyleSheet.get_input_style())
#     search_layout.addWidget(student_id_input)
    
#     search_btn = QPushButton("Search")
#     search_btn.setMinimumWidth(100)
#     search_btn.setMinimumHeight(35)
#     search_btn.setFont(QFont("Arial", 11))
#     search_btn.setStyleSheet(StyleSheet.get_button_style("primary"))
#     search_layout.addWidget(search_btn)
    
#     layout.addLayout(search_layout)
    
#     #RESULTS TABLE
#     results_label = QLabel("Login History")
#     results_label.setFont(QFont("Arial", 12, QFont.Weight.Bold))
#     layout.addWidget(results_label)
    
#     history_table = QTableWidget()
#     history_table.setColumnCount(3)
#     history_table.setHorizontalHeaderLabels(["Login Time", "IP Address", "Student Info"])
    
#     header = history_table.horizontalHeader()
#     header.setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents)
#     header.setSectionResizeMode(1, QHeaderView.ResizeMode.ResizeToContents)
#     header.setSectionResizeMode(2, QHeaderView.ResizeMode.Stretch)
    
#     history_table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
#     history_table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
#     history_table.setStyleSheet(StyleSheet.get_table_style())
#     layout.addWidget(history_table)
    
#     #SEARCH FUNCTION
#     def search_history():
#         student_id = student_id_input.text().strip()
#         if not student_id:
#             QMessageBox.warning(dialog, "Input Required", "Please enter a Student ID.")
#             return
        
#         from database import Database
#         from config import DB_CONFIG
        
#         db = Database(**DB_CONFIG)
#         if db.connect():
#             #GET STUDENT INFO
#             db.cursor.execute(
#                 "SELECT id, first_name, last_name, program FROM students WHERE school_id = %s",
#                 (student_id,)
#             )
#             student = db.cursor.fetchone()
            
#             if not student:
#                 QMessageBox.warning(dialog, "Not Found", f"No student found with ID: {student_id}")
#                 db.close()
#                 return
            
#             #GET LOGIN HISTORY
#             history = db.get_login_history(student['id'], limit=50)
#             db.close()
            
#             #DISPLAY RESULTS
#             history_table.setRowCount(len(history))
#             student_info = f"{student['first_name']} {student['last_name']} - {student['program']}"
            
#             for row, login in enumerate(history):
#                 history_table.setItem(row, 0, QTableWidgetItem(login['login_time']))
#                 history_table.setItem(row, 1, QTableWidgetItem(login['ip_address'] or "N/A"))
#                 history_table.setItem(row, 2, QTableWidgetItem(student_info))
            
#             results_label.setText(f"Login History - {len(history)} records found")
#         else:
#             QMessageBox.critical(dialog, "Database Error", "Could not connect to database.")
    
#     search_btn.clicked.connect(search_history)
#     student_id_input.returnPressed.connect(search_history)
    
#     #CLOSE BUTTON
#     close_btn = QPushButton("Close")
#     close_btn.setMinimumWidth(120)
#     close_btn.setMinimumHeight(40)
#     close_btn.setFont(QFont("Arial", 11))
#     close_btn.clicked.connect(dialog.close)
#     close_btn.setStyleSheet(StyleSheet.get_button_style("danger"))
#     layout.addWidget(close_btn, alignment=Qt.AlignmentFlag.AlignRight)
    
#     dialog.exec()


# #===========================================
# #INTEGRATION INSTRUCTIONS:
# #===========================================
# #1. ADD BOTH METHODS ABOVE TO YOUR AdminDashboard CLASS
# #
# #2. MODIFY THE _add_filters() METHOD:
# #   FIND THIS LINE:
# #       filter_layout.addStretch()
# #       self._add_refresh_button(filter_layout)
# #   
# #   REPLACE WITH:
# #       self._add_refresh_button(filter_layout)
# #       filter_layout.addSpacing(10)
# #       self._add_login_history_button(filter_layout)
# #
# #3. DONE! THE BUTTON WILL APPEAR NEXT TO THE REFRESH BUTTON