# Data Service

## Overview

This is a Data Service, which part of telegram project - "DeutschLernen" designed for working with data and provide data from DB. 
The application provides logic to other services.

## Dependensy

This service provide data from another service: HttpService, BotService, AuthService and DwhService via grpc connection. 

## Prerequisites

- Python 3.8 or higher
- Use Poetry for a dependency installation from pyproject.toml:
(Install poetry and execute comand "poetry install")

## Environment

For enviroment installetion, you need to create you own .env and .test.env file
In cfg/config.py please write link to your cfg files
For a template use file: .template.env

## Installation

### Clone the Repository

https://github.com/AlenaMeshcheriakova/DataService.git
cd DataService

### Starting project

For start up project, use: /src/grpc/main_grpc.py
