# 🔄 Pipeline Behaviors in Bazario
> 🌊 Flow control and middleware magic

---

## 🎯 Overview
Pipeline behaviors in **Bazario** enable pre- and post-processing logic for requests and notifications. These behaviors form a chain around the core handler logic and can modify or enhance the data flow.

## 🛠️ Implementation Examples

### 🔐 Authentication Check Behavior
```python
from bazario import (
    PipelineBehavior,
    Resolver,
    HandleNext,
    Request,
    Notification,
)

class AuthenticationCheckBehavior(PipelineBehavior[Request, Any]):
    def __init__(self, user_provider: UserProvider) -> None:
        self._user_provider = user_provider

    def handle(self, request: Request, handle_next: HandleNext[Request, Any]) -> Any:
        # ✨ Security check
        if not self._user_provider.is_authenticated():
            raise PermissionError("User is not authenticated.")
        
        # 🔄 Continue to next handler
        return handle_next(request)
```

## 📊 Event Store Behavior
```python
class AddToEventStoreBehavior(PipelineBehavior[Notification, None]):
    def __init__(self, event_store: EventStore) -> None:
        self._event_store = event_store

    def handle(
        self, 
        request: Notification, 
        handle_next: HandleNext[Notification, None],
    ) -> None:
        # 📝 Store event
        self._event_store.add(request)
        # ➡️ Proceed to next
        return handle_next(request)
```

## 📧 Email Notification Behavior
```python
class PostAddedEmailBehavior(PipelineBehavior[PostAdded, None]):
    def __init__(self, email_service: EmailService) -> None:
        self._email_service = email_service

    def handle(self, request: PostAdded, handle_next: HandleNext[PostAdded, None]) -> None:
        # 📨 Send email
        self._email_service.send_email(
            to_user_id=request.user_id,
            subject="Thank you for adding a post!",
            body=f"Dear User {request.user_id}, thank you for your post with ID {request.post_id}!"
        )
        # ➡️ Continue chain
        return handle_next(request)
```

## 🔌 Registration Guide

📝 Register Your Behaviors
```python
from bazario import Registry

def provide_registry() -> Registry:
    registry = Registry()
    
    # 🔄 Pipeline Execution Order:
    # 1️⃣ Authentication Check
    # 2️⃣ Event Store
    # 3️⃣ Validation
    # 4️⃣ Email Notification
    registry.add_pipeline_behaviors(Request, AuthenticationCheckBehavior)
    registry.add_pipeline_behaviors(Notification, AddToEventStoreBehavior)
    registry.add_pipeline_behaviors(AddPost, AddPostValidationBehavior)
    registry.add_pipeline_behaviors(PostAdded, PostAddedEmailBehavior)

    return registry
```

## 🎯 Execution Flow Rules

- 🌍 Global First : Base type behaviors (Request/Notification) execute first

- 📍 Specific Second : Concrete type behaviors follow

- 📝 Order Matters : Behaviors execute in registration order

- 🔄 Chain Formation : All applicable behaviors form an execution chain

## ⚡ Example Flow
```python
def provide_registry() -> Registry:
    registry = Registry()
    
    registry.add_behaviors(Request, RequestLoggingBehavior)
    registry.add_behaviors(AddPost, ValidationBehavior, MetricsBehavior)

    return registry

# 🔄 Execution sequence:
# 1️⃣ RequestLoggingBehavior
# 2️⃣ ValidationBehavior
# 3️⃣ MetricsBehavior
# 4️⃣ Actual AddPost handler
```

## 🔧 IoC Container Setup
```python
# Add to your container
container.register(Registry, provide_registry)
```

## 💡 Pro Tips
- 🎯 Keep behaviors focused on single responsibilities

- 🔍 Use behaviors for cross-cutting concerns

- 📊 Consider adding monitoring in behaviors

- 🛡️ Implement error handling where appropriate

<details>
<summary>📚 Original Documentation</summary>
    <span style="font-size: 1.3em">
        Pipeline behaviors in Bazario enable pre- and post-processing logic for requests and notifications. These behaviors form a chain around the core handler logic and can modify or enhance the data flow.
    </span>
</details>