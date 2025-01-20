In **Bazario**, **Resolvers** are simply wrappers around the client's IoC (Inversion of Control) container. They are used by the framework to resolve handlers and behaviors, allowing for independence from any specific container.

### Key Points:
- **Resolvers** abstract the dependency resolution process, enabling Bazario to work with different IoC containers.
- They help in resolving **Request Handlers** and **Pipeline Behaviors** without being tied to a particular container.
- This flexibility allows you to use any IoC container of your choice, while Bazario handles the resolution behind the scenes.

Resolvers make Bazario modular, decoupling it from the underlying IoC container, and ensuring a consistent and flexible integration.