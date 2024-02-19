# Sympoly - Home Assignment

## Introduction

Hi dear candidate! We are glad to see you here. This assignment is a part of our hiring process. It is designed to test your skills and knowledge in the field of Python programming language. We hope you will enjoy it.

In this assignment you will be asked to create a FastAPI application for parsing and serving invoices data.

## Guidelines

> Personal Note: This assignment should be fun and exploratory. We want to see how you approach a problem and how you solve it. Try to be creative and show us your best.

1. The project must be implemented using Python 3.10.
2. The project must be managed in a virtual environment.
   - We recommend using [Poetry](https://python-poetry.org/) for dependency management.
3. The backend must be implemented using [FastAPI](https://fastapi.tiangolo.com/).
4. Data-models should be implemented using [Pydantic](https://docs.pydantic.dev/latest/) (v2).
5. Please use MongoDB for data persistence, (we recommend using [Beanie](https://beanie-odm.dev/) for integration with FastAPI and Pydantic).
6. Maintain a clear and readable code style, using modern Python idioms and typing.
7. You can use any libraries you see necessary, if a solution already exists, there is no need to reinvent the wheel.
8. This project has a parsing component, so you will need to implement a parser for the invoices, try to make it a robust self-contained component that acts like a library.
9. There is no need to implement any sort of authentication or authorization, focus on the requirements.
10. Please work on your own, and do not share your solution with others.
    - You can use any public resources or consult with ChatGPT but keep in mind that we want to see your own solution, and not a copy-pasted one.
11. If you think that some parts of the assignment are not clear, or you seem to feel stuck, please contact us and we will try to help you. We want you to succeed.
12. The submission details will be described at the end of this document.

## The Assignment

"Mercury Invoices" is a new startup that provides services for parsing invoices and expense reports, and extracting data from them. They have a new client that wants to use this service, and they need to implement a new API for their client.

The client manages expenses using the new and exclusive file format **".EXRF"** (Expense Report Format). The specifications of the format are attached to the [Mercury EXRF Specification](/Mercury-EXRF.md) file.

"Mercury Invoices" want you to implement a new API for their client to parse and serve invoices data of the new format.

## The Requirements

1. Create a parser library for the new format using the specifications provided in [EXRF-Specs.md](/EXRF-Specs.md) file.
   - The library must be able to parse (only) the new .exrf format and return a structured data object.
   - The parsed data object should be easy to use, generic, and extensible.
   - In addition to the core functionality above, the library should be extended to support specific implementations of the new format.  
     (as described in the [Mercury-EXRF.md](/Mercury-EXRF.md) file).
   - The shape of the data object is yours to decide, but it needs to be easy to handle (from a programmer's perspective).
   - The library should handle all the edge cases of the new format.
   - In case of a parsing error, the library should raise a clear and readable exception describing the specific error.
2. Create a FastAPI application that exposes the following endpoints
   - invoices
     - `POST /invoices` - Upload a new .exrf file, parse it, save it to the database and return the parsed data.
     - `GET /invoices` - Return a list of all the invoices in the database.
     - `GET /invoices/{invoice_id}` - Return a single invoice by its id.
     - `DELETE /invoices/{invoice_id}` - Delete a single invoice by its id.

### Notes

- You can use the `exrf_examples` directory that contains some example invoices for reference and testing your solution.
- Although we do not provide them, you should consider testing bad-formatted invoices and edge cases.

### Bonus

Before approaching the bonus tasks, please make sure that you have completed all the requirements.
The bonus tasks are not mandatory, but they will give you extra points, you can choose to implement one or more of them as you see fit.

- (Bonus 1) Extend the `GET /invoices` endpoint to support filtering and/or pagination.

- (Bonus 2) Create a new endpoint `GET /export` that returns a CSV file that contains all the invoices in the database.

- (Bonus 3) Create a user interface for application to help the client manage the invoices. It can be anything from a simple HTML page to a full-blown React application.

## Submission

To submit your solution, please follow these steps:

1. Add a README file with the following information:

   - How to run your application.
   - How to use your application.
   - Any additional information you think is relevant.

2. Create a new public repository on your GitHub account and push your solution to it.

3. Send us an email with the link to the repository, including your full name and the position you are applying for.

Contact Details: Guy Tsitsiashvili, <guyts@sympoly.net>

Good luck! We are looking forward to seeing your solution.
