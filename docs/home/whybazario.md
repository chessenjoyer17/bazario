# 🎯 Why Choose Bazario?

!!! tip "<span style="font-size: 1.5em">🔄 Synchronous & Asynchronous Support</span>"
    <span style="font-size: 1.3em">Most libraries require choosing between synchronous or asynchronous processing, limiting flexibility.</span>

    <span style="font-size: 1.4em">✨ **Bazario's Solution**:</span>  
    <span style="font-size: 1.3em">The `bazario.asyncio` package supports both synchronous and asynchronous handling, giving you complete freedom in your application architecture.</span>

!!! success "<span style="font-size: 1.5em">🎮 IoC Container Control</span>"
    <span style="font-size: 1.3em">Traditional libraries handle IoC containers internally, leading to bugs and side effects, reducing performance with multiple parallel containers.</span>

    <span style="font-size: 1.4em">✨ **Bazario's Solution**:</span>  
    <span style="font-size: 1.3em">
        Bazario allows the client to control the IoC container and scope creation, giving full control over the container’s lifecycle and preventing performance issues or side effects caused by redundant container instances.
    </span>

!!! abstract "<span style="font-size: 1.5em">🧩 Enhanced Modularity</span>"
    <span style="font-size: 1.3em">In other libraries, integrating different DI frameworks is challenging without rewriting significant portions of the logic.</span>

    <span style="font-size: 1.4em">✨ **Bazario's Solution**:</span>  
    <span style="font-size: 1.3em">
        Bazario solves this problem by utilizing a modular resolvers system, allowing easy integration with any DI framework. This provides the ability to use Bazario in different environments without being tied to a specific DI framework.
    </span>

!!! note "<span style="font-size: 1.5em">⚡ SOLID Principles Adherence</span>"
    <span style="font-size: 1.3em">Some libraries do not fully adhere to SOLID principles, making the code more complex and harder to maintain.</span>

    <span style="font-size: 1.4em">✨ **Bazario's Solution**:</span>  
    <span style="font-size: 1.3em">
        Bazario fully adheres to SOLID principles, particularly ISP (Interface Segregation Principle). For example, instead of tightly coupling everything to a Dispatcher, Bazario separates responsibilities by introducing the Publisher protocol for event publication and the Sender protocol for sending requests, leading to better responsibility separation and reduced unnecessary dependencies.
    </span>

!!! tip "<span style="font-size: 1.5em">🔱 Dependency Separation</span>"
    <span style="font-size: 1.3em">Traditional controllers handle both request parsing and handler resolution, increasing complexity and reducing testability.</span>

    <span style="font-size: 1.4em">✨ **Bazario's Solution**:</span>  
    <span style="font-size: 1.3em">
        Bazario addresses this by delegating all handler routing responsibilities to Bazario, allowing controllers to focus solely on parsing requests. This improves responsibility separation and makes controller code cleaner and more testable.
    </span>

!!! success "<span style="font-size: 1.5em">🔗 Advanced Pipeline System</span>"
    <span style="font-size: 1.3em">Many libraries lack effective ways to implement cross-cutting concerns like logging, validation, or error handling.</span>

    <span style="font-size: 1.4em">✨ **Bazario's Solution**:</span>  
    <span style="font-size: 1.3em">
        Bazario addresses this by offering a sophisticated behavior pipeline system that allows developers to:     
    </span>

    - <span style="font-size: 1.3em">🔄 Middleware without handler modifications</span>
    - <span style="font-size: 1.3em">🧩 Reusable components</span>
    - <span style="font-size: 1.3em">⚙️ Flexible request/notification chains</span>
    - <span style="font-size: 1.3em">📊 Centralized monitoring</span>
    - <span style="font-size: 1.3em">📝 Unified logging</span>
    - <span style="font-size: 1.3em">❌ Consistent error handling</span>

    <span style="font-size: 1.5em">
        This powerful pipeline system allows developers to manage complex workflows efficiently and with minimal code duplication.
    </span>
    

!!! abstract "<span style="font-size: 1.5em">⚙️ Flexible Processing Control</span>"
    <span style="font-size: 1.3em">Developers face challenges when introducing new processing requirements, especially when they require changing existing handler logic.</span>

    <span style="font-size: 1.4em">✨ **Bazario's Solution**:</span>  
    <span style="font-size: 1.3em">
        Bazario offers flexible control over how requests and notifications are processed through: 
    </span>
    
    - <span style="font-size: 1.3em">🎯 Type-specific pipeline behaviors</span>
    - <span style="font-size: 1.3em">🌐 Global behavior configuration</span>
    - <span style="font-size: 1.3em">📋 Configurable execution order</span>
    - <span style="font-size: 1.3em">🔄 Non-intrusive requirement integration</span>

