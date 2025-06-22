# Task Management System

## Table of Contents
- [About Project](#about-project)
- [Installation](#installation)
- [Run the Project](#run-the-project)
- [Features](#features)
- [Testing](#testing)
- [Contribution](#contribution)
- [License](#license)
- [Contact Me](#contact-me)

## About Project
The **Task Management System** is a web application designed to help users efficiently manage tasks by creating, updating, and tracking their progress. It provides an intuitive interface for managing personal or team-based task assignments.

## Installation
Follow these steps to clone the repository and install the required dependencies:

```sh
# Clone the repository
git clone https://github.com/anandsundaramoorthysa/Task-Management-System.git

# Navigate into the project directory
cd Task-Management-System

# Create and activate a virtual environment (optional but recommended)
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`

# Install dependencies
pip install -r requirements.txt
```

## Run the Project
To start the application, execute the following command:

```sh
python app.py
```

Then open your browser and go to `http://127.0.0.1:5000/` to access the Task Management System.

## Features
- User authentication and authorization
- Task creation, assignment, and tracking
- Task prioritization and due date management
- Intuitive user interface for task management
- Responsive design for mobile and desktop usage
- Secure database storage for task records

## Testing

![Pytest](https://img.shields.io/badge/Tested%20With-Pytest-blue?logo=pytest)
![Coverage](https://img.shields.io/badge/Test%20Coverage-70%25%2B-brightgreen)

This project includes **unit tests**, **integration tests**, and **API tests** to ensure reliability, correctness, and performance of all features. All test cases are organized in test_app.py.

### How to Run Tests

Activate your environment and run the following command for testing:
```bash
coverage run test_app.py                  
coverage report    
coverage html #To generate a visual HTML report
```
Then open htmlcov/index.html to check it out the test coverage report.

## Contribution
Contributions are welcome! If you'd like to contribute, please follow these steps:
1. Fork the repository.
2. Create a new branch (`git checkout -b feature-branch`).
3. Commit your changes (`git commit -m 'Add new feature'`).
4. Push to the branch (`git push origin feature-branch`).
5. Open a Pull Request.

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contact Me
If you have any questions or would like to collaborate, feel free to reach out:

- **Email**: [sanand03072005@gmail.com](mailto:sanand03072005@gmail.com?subject=Inquiry%20About%20Task%20Management%20System%20Project&body=Hi%20Anand,%0A%0AI'm%20interested%20in%20learning%20more%20about%20the%20Task%20Management%20System%20you%20developed.%20I%20have%20some%20questions%20about%20how%20it%20manages%20tasks%2C%20authentication%2C%20and%20collaboration%20features.%20Additionally%2C%20I%20would%20like%20to%20discuss%20potential%20collaborations.%0A%0AThank%20you!%0A%0ABest%20regards,%0A[Your%20Name])
- **LinkedIn**: [Anand Sundaramoorthy](https://www.linkedin.com/in/anandsundaramoorthysa/)

