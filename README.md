# Traffic Management System

Automated traffic management system implemented with Django and PostgreSQL
---

## Table of contents[![](https://raw.githubusercontent.com/aregtech/areg-sdk/master/docs/img/pin.svg)](#table-of-contents)
- [Requirements](#project-status)
- [Introduction](#introduction)
- [Installation and Run](#installation-and-run)
  - [Installing PostgreSQL on Windows:](#installing-postgresql-on-windows)
  - [Installing PostgreSQL on macOS:](#installing-postgresql-on-macos)
  - [Installing PostgreSQL on Linux:](#installing-postgresql-on-linux)
- [Contribution](#Contribution)

---

<!-- markdownlint-disable -->
## Requirements[![](https://raw.githubusercontent.com/aregtech/areg-sdk/master/docs/img/pin.svg)](#requirements)
1. For Mac OS


2. For Windows
- setuptools==69.0.3
- wheel==0.42.0

---

## Introduction[![](https://raw.githubusercontent.com/aregtech/areg-sdk/master/docs/img/pin.svg)](#introduction)

**Traffic_Management_System**   
This project is a simulating traffic management system, developed with Django and use PostgreSQL as a local database server. It has been implemented with the following features:
- Register Owners
- Register Vehicles
- Recognize Vehicles and Logging Information
- Detect Violation
- Issue Fine and send Notice by Email
- Analyse Traffice Flow
- Generate and Retrieve Traffic Report
- Detect and Predict Congestion and Notify Drivers by Email


## Installation and Run

### I. Install Django and PostgreSQL:
```bash
pip install django # For Linux/macOS/Windows
```
### Installing PostgreSQL on Windows:

1. **Download the Installer**:
   - Visit the [PostgreSQL official website](https://www.postgresql.org/download/windows/).
   - Choose the version suitable for your system and download the installer.

2. **Run the Installer**:
   - Double-click the downloaded installer to launch the installation wizard.
   - Follow the prompts in the wizard, you can accept the default options.

3. **Set Password**:
   - During the installation, you will be prompted to set a password for the database superuser (default is "postgres"). Remember this password as it will be used for accessing the database later.

4. **Complete Installation**:
   - Once the installation is complete, the PostgreSQL server will start automatically.

### Installing PostgreSQL on macOS:

1. **Install using Homebrew**:
   - Open Terminal.
   - Install Homebrew (if not already installed): `/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"`
   - Install PostgreSQL using Homebrew: `brew install postgresql`

2. **Initialize the Database**:
   - Run the initialization command: `initdb /usr/local/var/postgres`

3. **Start PostgreSQL Server**:
   - Run the command: `pg_ctl -D /usr/local/var/postgres start`

4. **Complete Installation**:
   - The PostgreSQL server will run in the background.

### Installing PostgreSQL on Linux:

1. **Install using Package Manager**:
   - For Ubuntu/Debian:
     ```
     sudo apt-get update
     sudo apt-get install postgresql
     ```
   - For CentOS/RHEL:
     ```
     sudo yum update
     sudo yum install postgresql-server postgresql-contrib
     ```

2. **Initialize the Database**:
   - Run the initialization command: `sudo postgresql-setup initdb`

3. **Start PostgreSQL Server**:
   - For Ubuntu/Debian: `sudo service postgresql start`
   - For CentOS/RHEL: `sudo systemctl start postgresql`

4. **Set up Auto Start (Optional)**:
   - For Ubuntu/Debian: `sudo update-rc.d postgresql enable`
   - For CentOS/RHEL: `sudo systemctl enable postgresql`

5. **Complete Installation**:
   - PostgreSQL server will run in the background.

Once installed, you can use the respective client tools to connect to the PostgreSQL database and start managing databases and development work.


### II. Clone the repository and Run:

```bash
git clone https://github.com/lzpmpc005/Traffic_Management_System.git
```

1. Navigate to the repository
```bash
cd Traffic_Management_System
```
2. Install dependencies using pip:
```bash
pip install -r requirements.txt
```
3. Navigate to the Project
```bash
cd traffic_management_system
```
4. Configure `traffic_management_system/settings.py` according to you database and email server:
- Database Server
```python
DATABASES = {
   'default': {
      'ENGINE': 'django.db.backends.postgresql_psycopg2',
      'NAME': 'your_postgresql_database',
      'USER': 'your_postgresql_username',
      'PASSWORD': 'your_postgresql_password',
      'HOST': 'localhost', # modify if yours is different
      'PORT': '5432', # modify if yours is different
   }
}
```

- Email Server
```python
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp-mail.outlook.com'    
# Modify according to your email server
EMAIL_PORT = 587     
# Modify according to your email server
EMAIL_USE_TLS = True 
EMAIL_HOST_USER = 'your email address' 
EMAIL_HOST_PASSWORD = 'your email password' 
```

5. Perform database migration:
```
python manage.py makemigrations
python manage.py migrate
```
6. Run the local server:
```
python manage.py runserver
```

7. Excute 'TrafficFlow.py' and 'Violators.py' in PythonScripts to simulate logging, violation detection and Issue Fine.

> [!NOTE]
> If you want to recieve email as an owner, you need to use 'CreateOwner.py', 'IssueDriverLicense.py', 'RegisterVehicles.py' sequentially and remember to change the values inside accordingly.   

> Then change the vehicle id as you just registered in 'Violators.py' and Excute   

> If you encounter excuting outside Django project error, try excute in shell:   
```
python manage.py shell
exec(open('PythonScripts/CreateOwner.py').read())
```

8. Excute 'UpdateFine.py' to simulate increasing fine for delaying payment.

9. Retrieve Traffic Reports
- For current Period (default as 10 minutes) and all Junction:
   http://localhost:8000/traffic_management/report
- For current Period (default as 10 minutes) and specific Junction:
   http://localhost:8000/traffic_management/report?Junction_id=7
- For a certain Period and all Junction:
   http://localhost:8000/traffic_management/report?Date=2024-02-11&Time_From=00:00:00&Time_To=23:59:59
- For a certain Period and specific Junction:
   http://localhost:8000/traffic_management/report?Date=2024-02-11&Time_From=00:00:00&Time_To=23:59:59&Junction_id=7

> [!NOTE]
> Keep 'TrafficFlow.py' running if you want to see data for the first two scenarios.   

> The report will be opened automaticly, and the default saving path is 'E:\\LU_Leipzig\\ProgramClinic\\Project3\\traffic_report.pdf', please change accordingly inside views.py

> 💡 xxx [xxx] (To be continue). 

---
 ## Contribution
 
If you want to contribute or comment on this project, email lihongtaoix7@gmail.com.