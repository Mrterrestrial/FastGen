# FastGen - Project Scaffolding Tool

[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.8%2B-blue.svg)](https://www.python.org/)
[![Poetry](https://img.shields.io/badge/managed%20with-poetry-blue.svg)](https://python-poetry.org/)

FastGen is a powerful command-line tool that makes it easy to scaffold projects in any environment. It comes with a variety of predefined templates to help you get started quickly. You can also create and share custom templates tailored to your specific needs, ensuring a consistent project structure for your entire team.

---

## **Key Features**
**Interactive CLI** → Create projects step-by-step with guided prompts  
**Predefined Templates** → Start instantly with ready-to-use project structures  
**Modular & Extendable** → Add new templates easily in YAML format  

---

## **Project Structure**
```
├── fastgen
│  ├── __init__.py
│  ├── core                     # Core logic for project
│  │  ├── __init__.py
│  │  ├── cli_manager.py        # Handles CLI interactions
│  │  ├── project_manager.py    # Manages project creation
│  │  └── template_manager.py   # Manages templates
│  └── main.py
├── templates                   # project templates in YAML format
│   ├── basic_dart.yaml
│   ├── basic_python.yaml
│   ├── fastapi.yaml
│   └── php_web.yaml
├── tests
├── generated_projects          # User-created projects (ignored in Git)
├── poetry.lock                 # Poetry dependency lock file
├── pyproject.toml              # Poetry package configuration
├── README.md
└── LICENSE
```

---

## **Installation**

FastGen uses **Poetry** for package management. If you don’t have Poetry installed, install it [here](https://python-poetry.org/docs/).  

### 1. Clone the Repository
```sh
git clone https://github.com/Mrterrestrial/FastGen.git
cd FastGen
```
### 2. Install Dependencies Using Poetry
```sh
poetry install
```
---

## **Usage**
FastGen provides a simple **command-line interface** to generate projects efficiently.

### Display Help
```sh
poetry run fastgen help
```

### List Available Templates
```sh
poetry run fastgen list
```

### Create a New Project
```sh
poetry run fastgen create
```
---

## **Templates**
FastGen comes with **basic predefined templates** to test:

| Template      | Description |
|--------------|------------|
| **Basic Python** | A minimal Python project structure |
|**Basic Dart** | A simple Dart project setup |
| **FastAPI** | A FastAPI-based backend  |
| **PHP Web** | A PHP backend with HTML & CSS frontend |

You can **add your own templates** in the `templates/` directory using YAML.

---

## **Contributing**
We **welcome contributions** to improve FastGen! To contribute:
1. **Fork** the repository.
2. Create a **new branch**.
3. **Commit your changes** and push to your fork.
4. Submit a **Pull Request** for review.

---

## *Support & Community**
💬 **Have questions or feature requests?** Feel free to **open an issue** or **start a discussion**!  
If you like FastGen, consider **starring the repository** on GitHub! ⭐  
