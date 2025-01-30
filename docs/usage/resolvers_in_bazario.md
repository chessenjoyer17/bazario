# 🔗 Resolvers in Bazario
> 🎯 Smart dependency resolution for your application

## 🌟 Overview

In **Bazario**, **Resolvers** act as intelligent bridges between your application and IoC containers. They're the magic that makes dependency injection seamless and flexible! 

## 🏗️ Core Concepts

### 🎯 What are Resolvers?
Resolvers are sophisticated wrappers around your IoC container that:
- 🔄 Handle dependency resolution
- 🎨 Provide container abstraction
- 🛠️ Enable flexible integration
- 🔌 Support multiple IoC containers

## 💫 Key Features

| Feature | Description |
|---------|-------------|
| 🔄 Container Agnostic | Works with any IoC container |
| 🎯 Type Safety | Full type hinting support |
| ⚡ Performance | Optimized resolution paths |
| 🛡️ Abstraction | Clean separation of concerns |

## 🚀 Implementation Examples

### 📦 Basic Resolver Setup
```python
from typing import TypeVar

from bazario import Resolver
from your_container import Container

T = TypeVar("T")

class CustomResolver(Resolver):
    def __init__(self, container: Container) -> None:
        self._container = container
    
    def resolve(self, dependency_type: type[T]) -> T:
        return self._container.resolve(dependency_type)

# Can be used for example in testing
class SimpleResolver(Resolver):
    def resolve(self, dependency_type: type[T]) -> T:
        return dependency_type()
```

## ⚠️ Important Notes
!!! tip "💡 Pro Tips"
- Always test resolver configurations
- Use dependency injection best practices
- Keep your container configuration clean
- Consider using factory methods

!!! warning "🚨 Common Pitfalls"
- Avoid circular dependencies
- Don't mix different container types
- Handle resolution errors gracefully