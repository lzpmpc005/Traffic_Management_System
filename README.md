
<h1>
  <br /><br /><strong>Traffic Management System</strong>
</h1>

[![Latest release](https://img.shields.io/github/v/release/aregtech/areg-sdk?label=Latest%20release&style=social)]()
[![GitHub commits](https://img.shields.io/github/commits-since/aregtech/areg-sdk/v1.5.0.svg?style=social)]()
[![Stars](https://img.shields.io/github/stars/aregtech/areg-sdk?style=social)]()
[![Fork](https://img.shields.io/github/forks/aregtech/areg-sdk?style=social)]()
[![Watchers](https://img.shields.io/github/watchers/aregtech/areg-sdk?style=social)]()
[![Wiki Pages](https://img.shields.io/badge/AREG%20Wiki%20Pages-8-brightgreen?style=social&logo=wikipedia)]()

---

<!-- markdownlint-disable -->
## Project Status[![](https://raw.githubusercontent.com/aregtech/areg-sdk/master/docs/img/pin.svg)](#project-status)
<table class="no-border">
 
  </tr>
  <tr>
    <td><img src="" alt=""/></td>
    <td><img src="https://img.shields.io/badge/OS-linux%20%7C%20windows-blue??style=flat&logo=Linux&logoColor=b0c0c0&labelColor=363D44" alt="Operating systems"/></td>
    <td colspan="2"><img src="https://img.shields.io/badge/CPU-x86%20%7C%20x86__64%20%7C%20arm%20%7C%20aarch64-blue?style=flat&logo=amd&logoColor=b0c0c0&labelColor=363D44" alt="CPU Architect"/></td>
  </tr>
</table>

---

## Introduction[![](https://raw.githubusercontent.com/aregtech/areg-sdk/master/docs/img/pin.svg)](#introduction)

**Bookstore** 
This project is part of a Django-based book management system. It provides the following features:
- Add books and authors
- View inventory and filter books
- Update and delete books
- Bulk delete books


## Installation and Run

1. Create a virtual environment and install dependencies:
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



2. Clone the project to your local machine:

```bash
git clone https://github.com/lzpmpc005/Traffic_Management_System.git
cd Traffic_Management_System
cd traffic_management_system
```
3. Perform database migration:
```
python manage.py migrate
```
4. Run the development server:
```
python manage.py runserver
```
5. Visit http://localhost:8000/ to view the project.

> 💡 xxx [xxx](). 

---

## Table of contents[![](https://raw.githubusercontent.com/aregtech/areg-sdk/master/docs/img/pin.svg)](#table-of-contents)
- [Project Status](#project-status)
- [Introduction](#introduction)
- [Installation and Run](#installation-and-run)
  - [Installing PostgreSQL on Windows:](#installing-postgresql-on-windows)
  - [Installing PostgreSQL on macOS:](#installing-postgresql-on-macos)
  - [Installing PostgreSQL on Linux:](#installing-postgresql-on-linux)
- [Table of contents](#table-of-contents)
- [API Endpoints](#api-endpoints)
- [Models](#models)
- [Thank you all!](#thank-you-all)

---
