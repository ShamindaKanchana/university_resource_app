#!/usr/bin/env python3
"""
Script to create test users for the University Resource App
"""

from app import create_app, db
from app.models.user import User, UserRole
from app.models.student import Student
from app.models.lecturer import Lecturer, LecturerPosition
from app.models.category import Category
from app.models.resource import Resource
from app.models.resource_download import ResourceDownload
from datetime import date

def create_test_data():
    app = create_app()
    
    with app.app_context():
        # Create tables if they don't exist
        db.create_all()
        
        # Clear existing data (optional - comment out if you want to keep existing data)
        print("Clearing existing test data...")
        ResourceDownload.query.delete()
        Resource.query.delete()
        Student.query.delete()
        Lecturer.query.delete()
        User.query.delete()
        Category.query.delete()
        
        # Create categories
        print("Creating categories...")
        categories = [
            Category(name="Lecture Notes", description="Class lecture materials and notes"),
            Category(name="Assignments", description="Assignment files and solutions"),
            Category(name="Exams", description="Past exam papers and solutions"),
            Category(name="Research Papers", description="Academic research and publications"),
            Category(name="Lab Manuals", description="Laboratory instructions and manuals"),
        ]
        
        for category in categories:
            db.session.add(category)
        
        # Create test users
        print("Creating test users...")
        
        # Student user
        student_user = User(
            username="student1",
            email="student1@university.edu",
            role=UserRole.student
        )
        student_user.set_password("student123")
        
        student_profile = Student(
            user=student_user,
            full_name="John Student",
            registration_number="STU2023001",
            academic_year=3,
            faculty="Engineering",
            department="Computer Science",
            contact_number="123-456-7890",
            enrolled_date=date.today(),
            can_upload=True
        )
        
        # Lecturer user
        lecturer_user = User(
            username="lecturer1",
            email="lecturer1@university.edu",
            role=UserRole.lecturer
        )
        lecturer_user.set_password("lecturer123")
        
        lecturer_profile = Lecturer(
            user=lecturer_user,
            full_name="Dr. Jane Lecturer",
            employee_id="LEC2023001",
            department="Computer Science",
            position=LecturerPosition.professor,
            office_location="Building A, Room 101",
            contact_number="098-765-4321",
            joined_date=date.today()
        )
        
        # Add users and profiles to database
        db.session.add(student_user)
        db.session.add(student_profile)
        db.session.add(lecturer_user)
        db.session.add(lecturer_profile)
        
        # Commit all changes
        db.session.commit()
        
        print("\nTest users created successfully!")
        print("\nLogin credentials:")
        print("Student: username='student1', password='student123'")
        print("Lecturer: username='lecturer1', password='lecturer123'")
        print("\nAvailable endpoints:")
        print("• http://localhost:5000/ - Home page")
        print("• http://localhost:5000/auth/login - Login page")
        print("• http://localhost:5000/student/dashboard - Student dashboard (requires login)")
        print("• http://localhost:5000/lecturer/dashboard - Lecturer dashboard (requires login)")
        print("• http://localhost:5000/student/browse - Browse resources (requires login)")
        print("• http://localhost:5000/resources/upload - Upload resources (requires student login)")

if __name__ == "__main__":
    create_test_data()
