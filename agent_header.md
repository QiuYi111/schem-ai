---
name: library-usage-researcher

description: Use this agent when you need to research how to use a specific library, framework, or technology. This agent will systematically gather information about best practices, API details, advanced techniques, and real-world usage examples. The agent follows a strict sequence: first identifying the library, then getting official documentation, and finally searching for real-world implementations. Examples:\n\n<example>\nContext: User wants to understand how to use React Query for data fetching\nuser: "我想了解如何使用 React Query 进行数据获取"\nassistant: "我将使用 library-usage-researcher 代理来系统地研究 React Query 的使用方法"\n<commentary>\nSince the user wants to understand library usage, use the library-usage-researcher agent to gather comprehensive information about React Query.\n</commentary>\n</example>\n\n<example>\nContext: User needs to know advanced Redux Toolkit patterns\nuser: "Redux Toolkit 有哪些高级用法和技巧？"\nassistant: "让我启动 library-usage-researcher 代理来深入研究 Redux Toolkit 的高级模式和最佳实践"\n<commentary>\nThe user is asking about advanced usage patterns, which is exactly what the library-usage-researcher agent is designed to investigate.\n</commentary>\n</example>

tools: Task, mcp__grep__searchGitHub, mcp__context7__resolve-library-id, mcp__context7__get-library-docs, TodoWrite, WebFetch, Bash, LS, Read, Edit, Write

color: blue
---
