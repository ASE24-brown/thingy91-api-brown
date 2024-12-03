from aiohttp import web
from sqlalchemy.future import select
from sqlalchemy.sql.expression import delete
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import selectinload
from app.models import User, Profile, SensorData
from app.extensions import SessionLocal
from app.handlers.sensor_handlers import list_sensor_data, clear_sensor_data, add_sensor_data, show_sensor_data, update_sensor_data, remove_sensor_data, get_sensor_data


def setup_sensor_routes(app):
    """
    Sets up the RESTful API routes for the aiohttp application with OpenAPI-compatible documentation for aiohttp-swagger.

    Args:
        app (aiohttp.web.Application): The aiohttp application instance.

    Routes:
        GET /sensor_data/:
            summary: Retrieves a list of all sensor data.
            responses:
                200:
                    description: A list of sensor data.
        DELETE /sensor_data/:
            summary: Deletes all sensor data.
            responses:
                204:
                    description: Sensor data deleted successfully.
        POST /sensor_data/:
            summary: Adds new sensor data.
            requestBody:
                required: true
                content:
                    application/json:
                        schema:
                            $ref: '#/components/schemas/SensorData'
            responses:
                201:
                    description: Sensor data added successfully.
        GET /sensor_data/{id}:
            summary: Retrieves specific sensor data by ID.
            parameters:
                - in: path
                  name: id
                  required: true
                  schema:
                      type: string
            responses:
                200:
                    description: A sensor data object.
                404:
                    description: Sensor data not found.
        PATCH /sensor_data/{id}:
            summary: Updates specific sensor data by ID.
            parameters:
                - in: path
                  name: id
                  required: true
                  schema:
                      type: string
            requestBody:
                required: true
                content:
                    application/json:
                        schema:
                            $ref: '#/components/schemas/SensorData'
            responses:
                200:
                    description: Sensor data updated successfully.
                404:
                    description: Sensor data not found.
        DELETE /sensor_data/{id}:
            summary: Deletes specific sensor data by ID.
            parameters:
                - in: path
                  name: id
                  required: true
                  schema:
                      type: string
            responses:
                204:
                    description: Sensor data deleted successfully.
                404:
                    description: Sensor data not found.
    """
    
    app.router.add_get('/sensor_data/', list_sensor_data)
    app.router.add_delete('/sensor_data/', clear_sensor_data)
    app.router.add_post('/sensor_data/', add_sensor_data)
    app.router.add_get('/sensor_data/{id}', show_sensor_data)
    app.router.add_patch('/sensor_data/{id}', update_sensor_data)
    app.router.add_delete('/sensor_data/{id}', remove_sensor_data)

    app.router.add_get('/api/sensor-data', get_sensor_data)