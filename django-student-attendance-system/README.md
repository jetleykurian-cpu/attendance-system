# Django Student Attendance System

This is a comprehensive Student Attendance Management System developed for educational purposes using Python (Django). It supports multiple user roles: HOD/Admin, Staff/Teachers, Students, and Parents, providing a complete solution for managing academic attendance, results, feedback, and more.

## Features of this Project

### A. Admin/HOD Users Can

1. View Overall Summary Charts of Students Performance, Staffs Performances, Courses, Subjects, Leave, etc.
2. Manage Staffs (Add, Update and Delete)
3. Manage Students (Add, Update and Delete)
4. Manage Parents (Add, Update and Delete)
5. Manage Courses (Add, Update and Delete)
6. Manage Subjects (Add, Update and Delete)
7. Manage Sessions (Add, Update and Delete)
8. View and Manage Student Attendance Reports
9. Review and Reply to Student/Staff/Parent Feedback
10. Review (Approve/Reject) Student/Staff/Parent Leave Applications
11. Upload and manage profile pictures
12. Access interactive dashboards with charts and analytics

### B. Staff/Teachers Can

1. View Summary Charts related to their students, subjects, leave status, etc.
2. Take and Update Students Attendance
3. Add and Update Student Results
4. Apply for Leave
5. Send Feedback to HOD
6. Manage assigned subjects and courses
7. View attendance reports for their classes

### C. Students Can

1. View Summary Charts related to their attendance, subjects, leave status, etc.
2. View Personal Attendance History
3. View Academic Results and Grades
4. Apply for Leave
5. Send Feedback to HOD
6. Track performance across subjects

### D. Parents Can

1. View their child's attendance records and summary charts
2. View their child's academic results and performance graphs
3. Apply for leave on behalf of their child
4. Send feedback to HOD
5. Receive notifications for new attendance and results
6. Monitor child's overall academic progress

## Technologies Used

- **Backend**: Django 3.0.7 (Python Web Framework)
- **Database**: SQLite (default), configurable to MySQL
- **Frontend**: HTML, CSS, JavaScript, Bootstrap, jQuery, Chart.js, DataTables
- **Other**: Python libraries for data visualization and management

## Download and Installation

### Download

Download the project files directly from the source and extract to your desired folder.

### Pre-Requisites

1. Install Python Latest Version [https://www.python.org/downloads/]
2. Install Pip (Package Manager) [https://pip.pypa.io/en/stable/installing/]

### Installation Steps

1. **Navigate to the Project Folder**
   - Open the extracted `django-student-attendance-system` folder.

2. **Create and Activate Virtual Environment**

   Install Virtual Environment:
   ```
   $ pip install virtualenv
   ```

   Create Virtual Environment:
   - Windows: `$ python -m venv venv`
   - Mac/Linux: `$ python3 -m venv venv`

   Activate Virtual Environment:
   - Windows: `$ venv\scripts\activate`
   - Mac/Linux: `$ source venv/bin/activate`

3. **Install Requirements**
   ```
   $ pip install -r requirements.txt
   ```

4. **Configure Settings**
   - Open `student_management_system/settings.py`
   - Ensure `ALLOWED_HOSTS = ['*']` (already set)

5. **Run Database Migrations**
   ```
   $ python manage.py migrate
   ```

6. **Create Super User (HOD)**
   ```
   $ python manage.py createsuperuser
   ```
   Or run the provided script:
   ```
   $ python create_admin.py
   ```

7. **(Optional) Create Sample Data**
   ```
   $ python create_sample_data.py
   ```

8. **Check Database (Optional)**
   ```
   $ python check_db.py
   ```

9. **Run the Server**
   - Windows: `$ python manage.py runserver`
   - Mac/Linux: `$ python3 manage.py runserver`

   Access at: `http://127.0.0.1:8000/`

## How to Use the System

1. **Access the Application**
   - Open browser and go to `http://127.0.0.1:8000/`

2. **Login**
   - Use credentials below or create your own.

3. **Default/Sample Login Credentials**

   - **HOD/Admin**:
     - Email: admin@gmail.com
     - Password: admin

   - **Staff/Teacher**:
     - Email: staff2@gmail.com
     - Password: staff2

   - **Student**:
     - Email: student2@gmail.com
     - Password: student2
   

   - **Parent**:
     - Create a parent user via admin panel or manually.
     - Example: parent2@gmail.com / parent2 (if created via sample data)

   **All Enrolled Students' Login Credentials**:
   - Run the following command to view all student usernames and emails:
     ```
     $ python student_credentials.py
     ```
     Note: Passwords are securely hashed and cannot be displayed. If you need to reset passwords, use the Django admin interface.

4. **Navigation and Usage**
   - **As HOD/Admin**: Use the admin panel to manage all entities. View dashboards for analytics.
   - **As Staff**: Mark attendance, add results, view student lists.
   - **As Student**: Check attendance, view results, apply leave.
   - **As Parent**: Monitor child's data, view reports.

5. **Key Features**
   - Interactive charts for attendance and performance.
   - AJAX-powered dynamic updates (e.g., attendance fetching).
   - File uploads for profile pictures.
   - Role-based access control.

## Support

- Add a Star 🌟 to this Repository
- For issues, check the code or contact the developer.

## License

Educational use only.