#S.P.E.A.K - System for Public Empowerment and Knowledge
#Made by the people, made for the people

#HANDLES ALL LOGIC RELATED TO AUTHENTICATION
#HANDLES ALL LOGIC RELATED TO AUTHENTICATION

from database import Database
from config import DB_CONFIG


class AuthValidator: #VALIDATOR FOR AUTH LOGIC
    
    @staticmethod
    def validate_login(username, password):
        """Validate login credentials."""
        if not username or not password:
            return False, "Please enter both School ID and password."
        
        if len(username) < 4:
            return False, "School ID must be at least 4 characters."
            
        return True, None
    
    @staticmethod
    def validate_registration(student_data): #VALIDATE REGISTRATION DATA
        required_fields = ['school_id', 'email', 'first_name', 'last_name', 
                          'contact_number', 'password']
        
        for field in required_fields:
            if not student_data.get(field):
                return False, "Please fill in all required fields marked with *"
        
        email = student_data['email']
        if '@' not in email or '.' not in email:
            return False, "Please enter a valid email address."
        
        password = student_data['password']
        if len(password) < 6:
            return False, "Password must be at least 6 characters long."
        
        if student_data['password'] != student_data.get('confirm_password'):
            return False, "Passwords do not match. Please try again."
        
        school_id = student_data['school_id']
        if len(school_id) < 5:
            return False, "Please enter a valid School ID."
        
        contact = student_data['contact_number']
        if len(contact) < 10:
            return False, "Please enter a valid contact number."
        
        return True, None


class AuthService: #AUTHENTICATION SERVICE
    
    def __init__(self):
        self.validator = AuthValidator()
        self.db = Database(**DB_CONFIG)
        
    def login(self, username, password): #LOGIN ATTEMPT VALIDATOR

        is_valid, error = self.validator.validate_login(username, password)
        if not is_valid:
            return False, error, None
        
        if not self.db.connect():
            return False, "Database connection error.", None
        
        success, message, user_data = self.db.authenticate_student(username, password)
        
        self.db.close()
        return success, message, user_data
    
    def register(self, student_data): #REGISTER NEW STUDENT
        
        is_valid, error = self.validator.validate_registration(student_data)
        if not is_valid:
            return False, error
        
        if not self.db.connect():
            return False, "Database connection error."
        
        success, message, student_id = self.db.register_student(student_data)
        
        self.db.close()
        
        if success:
            return True, f"Registration successful! Welcome, {student_data['first_name']}!"
        else:
            return False, message