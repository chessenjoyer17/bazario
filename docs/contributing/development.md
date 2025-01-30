# Development Setup 🛠️

This guide will help you set up your development environment for contributing to Bazario.

## Prerequisites 📋

- Python 3.10 or higher 🐍
- pip (Python package installer) 📦
- git 🌿

## Setting Up Your Development Environment 🚀

1. Clone the repository:
   ```bash
   git clone https://github.com/chessenjoyer17/bazario.git
   cd bazario
   ```

2. Create and activate a virtual environment, for example, with uv 🏗️:
    ```bash
    uv venv

    source .venv/bin/activate
    ```

## Development Tools 🔧

- pytest : For running tests ✅
- mypy : For static type checking 🔍
- ruff : For code linting and formatting🎨

## Pre-commit Hooks 🎣
We use pre-commit hooks to ensure code quality. To set up:

1. Install pre-commit:
    ```bash
    pip install pre-commit
    ```

2. Install the git hooks ⚓:
    ```bash
    pre-commit install
    ```

## Making Changes 🔄

1. Create a new branch 🌿:
    ```bash
    git checkout -b feature/your-feature-name
    ```

2. Make your changes ✏️

3. Run tests and quality checks ✅

4. Commit your changes 💾

5. Push to your fork 🚀

6. Create a Pull Request 📬

## Need Help? 💡
If you need help or have questions:

1. Check the documentation 📖

2. Create an issue 🎫

3. Reach out to the maintainers 💬

Happy coding! 🎉  