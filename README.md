# Nordic Thingy:91 Backend-API

Welcome! This is the Backend-API for the Nordic Thingy:91, an easy-to-use battery-operated prototyping platform for cellular IoT. This Backend-API is part of the project of the Brown team for the Advanced Software Engineering class in 2024.

## Table of Contents

- [Nordic Thingy:91 Backend-API](#nordic-thingy91-backend-api)
  - [Table of Contents](#table-of-contents)
  - [Introduction](#introduction)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
  - [Technologies Used](#technologies-used)
  - [Documentations](#documentations)
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
   git clone https://github.com/ASE24-brown/thingy91-api-brown.git
   ```

2. Go inside the folder:
   
   ```sh
   cd thingy91-api-brown
   ```

## Using Docker

1. Download Docker and install it if not installed

   ```sh
   https://www.docker.com/products/docker-desktop/
   ```


2. Create a shared Docker network (needed for frontend and backend communication) (If you didn't do it already)
   ```sh
   docker network create shared_network
   ```

3. Launching Docker
   ```sh
   docker-compose up --build
   ```

## Using without Docker

1. Create a virtual environment:
   ```sh
   python -m venv venv
   ```
2. Activate the newly created environment:
   
   On Mac OS
   ```sh
   source venv/bin/activate
   ```

   On Windows use
   ```sh
   venv\Scripts\activate
   ```

4. Install the required packages:
   ```sh
   pip install -r requirements.txt
   ```

5. Run in two terminals, in the first one run :

   ```sh
   python auth.oauth2_server.py
   ```

6. then in a second terminal, run

   ```sh
   python run.py
   ```
## Documentations

To access Swagger Documentations
   ```sh
  http://localhost:8000/api/v1/doc
   ```

To access Sphinx Documentations

   ```sh
  http://localhost:8000/docs/index.html
   ```





## Technologies Used
   ```sh
  Aiohttp: A Python library for building asynchronous web applications.
  SQLAlchemy: A SQL toolkit and Object-Relational Mapping (ORM) library for Python.
  Paho MQTT: A Python client library for the MQTT protocol.
  SQLite: A C library that provides a lightweight, disk-based database.
   ```

## License

This project is licensed under the MIT License. See LICENSE file for more details.
