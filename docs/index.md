# 🚀 Bazario

**Bazario** is a lightweight handler routing library designed for modular applications. It simplifies development by providing centralized mechanisms for handling requests (Requests) and events (Notifications), with efficient handler routing and support for both synchronous and asynchronous operations.

<div class="grid cards" markdown>

-   :material-download:{ .lg .middle } __Quick Installation__

    ---

    Get started with Bazario through PyPI:
    ```bash
    pip install bazario
    ```

</div>

## ✨ Key Features

<div class="grid cards" markdown>

-   :material-routes:{ .lg .middle } __Request Handling__

    ---

    A streamlined mechanism for handling requests with clear separation of responsibilities.

-   :material-bell-ring:{ .lg .middle } __Event Handling__

    ---

    Unified event publication and handling (Notifications) supporting both standard and async/await syntax while maintaining efficient in-memory processing.

-   :material-puzzle:{ .lg .middle } __Modular Architecture__

    ---

    Clear separation of business logic, ports, and infrastructure, simplifying development and maintenance.

-   :material-source-branch:{ .lg .middle } __IoC Container Integration__

    ---

    Support for DI frameworks enabling easy dependency management and modular configuration.

-   :material-test-tube:{ .lg .middle } __Testability__

    ---

    Use of abstractions to easily mock infrastructure adapters for unit testing.

-   :material-lightning-bolt:{ .lg .middle } __Asynchronous Support__

    ---

    The **bazario.asyncio** package enables asynchronous handling, providing flexibility for applications requiring async logic.

-   :material-layers-triple:{ .lg .middle } __Dependency Separation__

    ---

    Controllers delegate handler resolution to **Bazario**, focusing solely on request parsing. This improves separation of responsibilities and enhances code maintainability.

-   :material-pipe:{ .lg .middle } __Pipeline Behaviors__

    ---

    Flexible middleware system for implementing cross-cutting concerns like logging, validation, and error handling without modifying handler logic.

-   :material-cog-sync:{ .lg .middle } __Configurable Processing Chain__

    ---

    Ability to create custom processing pipelines for both requests and notifications, enabling sophisticated pre- and post-processing workflows.

</div>

!!! note "Optimization"
    Bazario is optimized for synchronous in-memory processing and handler routing, making it ideal for applications requiring modularity, simplicity, and flexible handler management.
