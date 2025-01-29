# 📦 Installation Guide

## 🚀 Quick Start

=== "pip"
    ```bash
    pip install bazario
    ```

=== "poetry"
    ```bash
    poetry add bazario
    ```

=== "pipenv"
    ```bash
    pipenv install bazario
    ```

=== "uv"
    ```bash
    uv pip install bazario
    #or
    uv add bazario
    ```


!!! tip "💡 Pro Tip"
    For development purposes, install with extra dependencies:

    - to install with dishka
    ```bash
    pip install bazario[dishka]
    ```

    - to install with punq
    ```bash
    pip install bazario[punq]
    ```

---

## 🔧 Requirements

!!! info "System Requirements"
    - Python 3.8 or higher
    - pip 20.0 or higher
    - Virtual environment (recommended)

??? abstract "Supported Python Versions"
    | Version | Status |
    |---------|--------|
    | 3.11    | ✅     |
    | 3.10    | ✅     |
    | 3.9     | ✅     |
    | 3.8     | ✅     |
    | < 3.8   | ❌     |

---

## 🔍 Verification

!!! example "Verify Installation"
    ```python
    import bazario

    print(f"Bazario version: {bazario.__version__}")
    ```

!!! success "Expected Output"
    ```
    Bazario version: 1.0.0
    ```

---

## 🎯 Next Steps

!!! note "Getting Started"
    1. ✨ Create your first application
    2. 📖 Read the documentation
    3. 🔧 Configure your environment
    4. 🚀 Deploy your application

!!! tip "Best Practices"
    - Use virtual environments
    - Keep dependencies updated
    - Follow the security guidelines
    - Check for updates regularly

---

## ❓ Troubleshooting

??? question "Common Issues"
    === "Import Errors"
        ```python
        ImportError: No module named 'bazario'
        ```
        **Solution**: Verify installation and Python path
        ```bash
        pip list | grep bazario
        ```

    === "Version Conflicts"
        ```python
        pkg_resources.VersionConflict
        ```
        **Solution**: Update dependencies
        ```bash
        pip install --upgrade bazario
        ```

    === "Permission Errors"
        ```bash
        Permission denied: '/usr/local/lib/python3.x/site-packages'
        ```
        **Solution**: Use virtual environment or `--user` flag
        ```bash
        pip install --user bazario
        ```

---

!!! warning "⚠️ Important Notes"
    - Always backup your data before upgrading
    - Check compatibility with your existing code
    - Review the changelog before updating
    - Test in development environment first

---

!!! success "🎉 Ready to Start!"
    You've successfully installed Bazario! Check out our Quick Start Guide to begin building your application.
