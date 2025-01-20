**Bazario** is a lightweight handler routing library designed for modular applications. It simplifies development by providing centralized mechanisms for handling requests (Requests) and events (Notifications), with efficient handler routing and support for both synchronous and asynchronous operations.


## Installation
Bazario is available on [PyPI](https://pypi.org/project/bazario/)

``` bash
pip install bazario
```

## ✨ Key Features

- **Request Handling**: A streamlined mechanism for handling requests with clear separation of responsibilities.
- **Event Handling**: Unified event publication and handling (Notifications) supporting both standard and async/await syntax while maintaining efficient in-memory processing.
- **Modular Architecture**: Clear separation of business logic, ports, and infrastructure, simplifying development and maintenance.
- **IoC Container Integration**: Support for DI frameworks enabling easy dependency management and modular configuration.
- **Testability**: Use of abstractions to easily mock infrastructure adapters for unit testing.
- **Asynchronous Support**: The **bazario.asyncio** package enables asynchronous handling, providing flexibility for applications requiring async logic.
- **Dependency Separation**: Controllers delegate handler resolution to **Bazario**, focusing solely on request parsing. This improves separation of responsibilities and enhances code maintainability.
- **Pipeline Behaviors**: Flexible middleware system for implementing cross-cutting concerns like logging, validation, and error handling without modifying handler logic.
- **Configurable Processing Chain**: Ability to create custom processing pipelines for both requests and notifications, enabling sophisticated pre- and post-processing workflows.

Bazario is optimized for synchronous in-memory processing and handler routing, making it ideal for applications requiring modularity, simplicity, and flexible handler management.