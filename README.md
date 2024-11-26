# Nordic Thingy:91 Backend-API

Welcome! This is the Backend-API for the Nordic Thingy:91, an easy-to-use battery-operated prototyping platform for cellular IoT. This Backend-API is part of the project of the Brown team for the Advanced Software Engineering class in 2024.

## Table of Contents

- [Nordic Thingy:91 Backend-API](#nordic-thingy91-backend-api)
  - [Table of Contents](#table-of-contents)
  - [Introduction](#introduction)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
  - [Usage](#usage)
  - [Testing](#testing)
  - [Technologies Used](#technologies-used)
  - [License](#license)

## Introduction

This Backend-API provides functionalities to interact with the Nordic Thingy:91 devices. It uses Aiohttp for asynchronous operations and SQLAlchemy for database interactions.

## Prerequisites

Before you begin, ensure you have met the following requirements:

- You have Python 3.8 or later installed on your machine.
- You have `pip` (Python package installer) installed.

## Installation

1. Clone the repository:

   ```sh
   git clone https://github.com/yourusername/thingy91-backend-api.git
   cd thingy91-backend-api

2. Create a virtual environment:
    ```sh
    python -m venv venv
    source venv/bin/activate
    
    # On Windows use     
    env\Scripts\activate

3. Install the required packages:
   ```sh
   pip install -r requirements.txt

## Usage

1. Run in two terminals, in the first one run :

  ```sh
  python auth/oauth2_server.py
  ```

2. then in the second one, run

  ```sh
  python run.py
  ```


## Using Docker

  ```sh
  docker-compose up --build
  ```



## Technologies Used
   ```sh
Aiohttp: A Python library for building asynchronous web applications.
SQLAlchemy: A SQL toolkit and Object-Relational Mapping (ORM) library for Python.
Paho MQTT: A Python client library for the MQTT protocol.
SQLite: A C library that provides a lightweight, disk-based database.

## License

This project is licensed under the MIT License. See LICENSE file for more details.
