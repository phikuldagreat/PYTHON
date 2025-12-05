#S.P.E.A.K - System for Public Empowerment and Knowledge
#Made by the people, made for the people

#MAIN APPLICATION FILE
#MAIN APPLICATION FILE

from PyQt6.QtWidgets import QApplication
from auth_gui import LoginWindow, RegisterWindow
from admin_gui import AdminDashboard
from student_gui import StudentDashboard
from auth_logic import AuthService


class AuthController:
    
    def __init__(self):
        self.auth_service = AuthService()
        self.login_window = LoginWindow()
        self.register_window = RegisterWindow()
        self.admin_dashboard = AdminDashboard()
        
        # Don't create student_dashboard here - create it after login
        self.student_dashboard = None  # Initialize as None
        
        self._connect_signals()
        
    def _connect_signals(self):
        # Login window signals
        self.login_window.login_clicked.connect(self.handle_login)
        self.login_window.register_requested.connect(self.show_register_window)
        self.login_window.admin_login_requested.connect(self.handle_admin_login)
        
        # Register window signals
        self.register_window.registration_complete.connect(self.handle_registration)
        self.register_window.back_to_login.connect(self.show_login_window)
        
        # Admin dashboard signals
        self.admin_dashboard.logout_requested.connect(self.show_login_window)
    
    def handle_login(self, username, password):
        # Check if admin login
        if username.lower() == "admin":
            self.handle_admin_login(password)
            return
            
        success, message, user_data = self.auth_service.login(username, password)
        
        if success:
            self.login_window.hide()
            self.login_window.clear_fields()
            
            # Create NEW student dashboard with user_data and db
            self.student_dashboard = StudentDashboard(user_data, self.auth_service.db)
            
            # Connect logout signal
            self.student_dashboard.logout_requested.connect(self.show_login_window)
            
            # Show dashboard
            self.student_dashboard.show()
        else:
            self.login_window.show_error("Login Failed", message)
    
    def handle_admin_login(self, password):
        if password == "admin123":
            self.login_window.hide()
            self.login_window.clear_fields()
            self.admin_dashboard.set_admin("Administrator")
            self.admin_dashboard.load_complaints()
            self.admin_dashboard.show()
        else:
            self.login_window.show_error("Access Denied", "Invalid admin credentials")
    
    def handle_registration(self, student_data): #PROCESS REGISTRATION DATA
        try:
            success, message = self.auth_service.register(student_data)
            
            if success:
                self.register_window.show_success("Registration Successful", message)
                self.show_login_window()
            else:
                self.register_window.show_error("Registration Failed", message)
        except Exception as e:
            print(f"Registration error: {e}")  # DEBUG
            import traceback
            traceback.print_exc()  # DEBUG - shows full error
            self.register_window.show_error("Error", f"An error occurred: {str(e)}")
    
    def show_register_window(self):
        self.login_window.hide()
        self.register_window.show()
    
    def show_login_window(self):
        self.register_window.hide()
        self.admin_dashboard.hide()
        
        # Hide student dashboard if it exists
        if self.student_dashboard:
            self.student_dashboard.hide()
        
        self.register_window.clear_fields()
        self.login_window.show()
    
    def start(self):
        self.login_window.show()


def main():
    app = QApplication([])
    controller = AuthController()
    controller.start()
    app.exec()


if __name__ == "__main__":
    main()