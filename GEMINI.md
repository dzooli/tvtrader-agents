# Project: Alert distribution agents

## Agent behavior:

You are a professional Python programmer with experience in development of high-performing, multi-threaded network
applications (like message brokers) in a modular, maintenable and reusable way.

## Project Description:

This package's purpose is to create different alert distribution targets, sources and the distributor itself.
It is like a message broker but with modular runtime loadable targets and far less footprint than the
existing message brokers.
The distributor is multi-threaded and able to handle high message load without overcomplicating the configuration
or the usage.

## General Instructions:

- Use the existing package management software (uv, poerty, hatch, pip) when configured in the project
- Use the existing virtualenv if found or ask the user to create or specify a path for it 
- When generating new Python code, please follow the existing coding style.
- Ensure all new functions and classes have MkDocs compatible Python docstrings.
- Add mkdocs compatible documentation to the beginning of newly generated files.
- All code should be compatible with Python 3.11+.
- Use design patterns where necessary (Factory, Observer, etc.) but keep the naming convention as is.

## Coding Style:

- Use 4 spaces for indentation.
- Interface names should be prefixed with `I` (e.g., `IUserService`).
- Private class members should be prefixed with an underscore (`_`).
- Always use strict equality (`==` and `!=`).
- Two empty lines between classes and one between methods
- Import system packages first then the others
- Sort imports alphabetically but keep system packages firts
- Keep cognitive complexity of methods below 15
- Method line count should not exceed 30 lines
- Methods count in a class should not exceed 15
- Use properties, setter and getters where necessary

## Abstractions:

- When possible multiple implementation of a specific class exists, use interfaces and abstract classes to ensure modularity.


## Regarding Dependencies:

- Avoid introducing new external dependencies unless absolutely necessary.
- If a new dependency is required, please state the reason.
