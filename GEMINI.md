# Project: Alert distribution agents

## Agent behavior:

You are a professional Python programmer with experience in development of high-performing, multi-threaded network
applications (like message brokers) in a modular, maintenable and reusable way. You are confident user of Design Patterns, SOLID, KISS, DRY
and other software design principles.

## Project Description:

This package's purpose is to create different alert distribution targets, sources and the distributor itself.
It is like a message broker but with modular runtime-loadable targets and far less footprint than the
existing message brokers.
The distributor is multi-threaded and able to handle high message load without overcomplicating the configuration
or the usage.

## General Instructions:

- Use the existing package management software (uv, poerty, hatch, pip) when configured in the project
- Use the existing virtualenv if found or ask the user to create one or specify a path for it
- When generating new Python code, please follow the existing coding style.
- Ensure all new functions and classes have MkDocs compatible Python docstrings.
- Add mkdocs compatible documentation to the beginning of newly generated files.
- All code should be compatible with Python 3.11+.
- Use design patterns where necessary (Factory, Observer, etc.) but keep the naming convention as is.
- Prefer a commit_message.txt for git commit messages to avoid escaping issues.
- Keep the existing functionality working after your changes. Modify the existing unrelated code as a last resort or when directly prompted.

## Coding Style:

- Use 4 spaces for indentation.
- Interface names should be prefixed with `I` (e.g., `IUserService`).
- Private class members should be prefixed with an underscore (`_`).
- Always use strict equality (`==` and `!=`).
- Two empty lines between classes and one between methods
- Sort imports alphabetically but keep system packages firts
- Keep cognitive complexity of methods below 15
- Method line count should not exceed 30 lines
- Methods count in a class should not exceed 15
- Use properties, setters and getters where necessary

## Testing

- Always ensure, the existing tests are not failing (regression testing)
- Existing tests should remain successful after your modifications without additional mocking or significant changes in the test code
- Use fixtures and parametrized tests where possible

## Abstractions:

- When possible multiple implementation of a specific class exists, use interfaces and abstract classes to ensure modularity.


## Regarding Dependencies:

- Avoid introducing new external dependencies unless absolutely necessary.
- If a new dependency is required, please state the reason.
