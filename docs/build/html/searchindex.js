Search.setIndex({"alltitles": {"AlertMe documentation": [[5, null]], "Contents:": [[5, null]], "Module contents": [[0, "module-app"], [1, "module-app.handlers"], [2, "module-app.routes"], [3, "module-auth"], [7, "module-mqtt"]], "Submodules": [[0, "submodules"], [1, "submodules"], [2, "submodules"], [3, "submodules"], [7, "submodules"]], "Subpackages": [[0, "subpackages"]], "app package": [[0, null]], "app.extensions module": [[0, "module-app.extensions"]], "app.handlers package": [[1, null]], "app.handlers.device_handlers module": [[1, "module-app.handlers.device_handlers"]], "app.handlers.sensor_handlers module": [[1, "module-app.handlers.sensor_handlers"]], "app.handlers.user_handlers module": [[1, "module-app.handlers.user_handlers"]], "app.models module": [[0, "module-app.models"]], "app.routes package": [[2, null]], "app.routes.auth_routes module": [[2, "module-app.routes.auth_routes"]], "app.routes.device_routes module": [[2, "module-app.routes.device_routes"]], "app.routes.sensor_routes module": [[2, "module-app.routes.sensor_routes"]], "app.routes.user_routes module": [[2, "module-app.routes.user_routes"]], "auth package": [[3, null]], "auth.auth module": [[3, "module-auth.auth"]], "auth.login module": [[3, "module-auth.login"]], "auth.oauth2_server module": [[3, "module-auth.oauth2_server"]], "config module": [[4, null]], "mqtt package": [[7, null]], "mqtt.mqtt_handler module": [[7, "module-mqtt.mqtt_handler"]], "run module": [[8, null]], "thingy91-api-brown": [[6, null]]}, "docnames": ["app", "app.handlers", "app.routes", "auth", "config", "index", "modules", "mqtt", "run"], "envversion": {"sphinx": 64, "sphinx.domains.c": 3, "sphinx.domains.changeset": 1, "sphinx.domains.citation": 1, "sphinx.domains.cpp": 9, "sphinx.domains.index": 1, "sphinx.domains.javascript": 3, "sphinx.domains.math": 2, "sphinx.domains.python": 4, "sphinx.domains.rst": 2, "sphinx.domains.std": 2, "sphinx.ext.viewcode": 1}, "filenames": ["app.rst", "app.handlers.rst", "app.routes.rst", "auth.rst", "config.rst", "index.rst", "modules.rst", "mqtt.rst", "run.rst"], "indexentries": {}, "objects": {"": [[0, 0, 0, "-", "app"], [3, 0, 0, "-", "auth"], [4, 0, 0, "-", "config"], [7, 0, 0, "-", "mqtt"], [8, 0, 0, "-", "run"]], "app": [[0, 0, 0, "-", "extensions"], [1, 0, 0, "-", "handlers"], [0, 1, 1, "", "init_app"], [0, 0, 0, "-", "models"], [2, 0, 0, "-", "routes"]], "app.extensions": [[0, 1, 1, "", "init_db"], [0, 1, 1, "", "reset_db"], [0, 1, 1, "", "setup_db"]], "app.handlers": [[1, 1, 1, "", "add_sensor_data"], [1, 1, 1, "", "add_user"], [1, 1, 1, "", "associate_user_to_device"], [1, 1, 1, "", "clear_sensor_data"], [1, 1, 1, "", "clear_users"], [1, 0, 0, "-", "device_handlers"], [1, 1, 1, "", "get_all_device_statuses"], [1, 1, 1, "", "get_all_sensor_data_for_device"], [1, 1, 1, "", "get_all_sensor_data_for_user_device"], [1, 1, 1, "", "get_device_status"], [1, 1, 1, "", "get_sensor_data"], [1, 1, 1, "", "list_sensor_data"], [1, 1, 1, "", "list_users"], [1, 1, 1, "", "register_user"], [1, 1, 1, "", "remove_sensor_data"], [1, 1, 1, "", "remove_user"], [1, 0, 0, "-", "sensor_handlers"], [1, 1, 1, "", "show_sensor_data"], [1, 1, 1, "", "show_user"], [1, 1, 1, "", "update_sensor_data"], [1, 1, 1, "", "update_user"], [1, 0, 0, "-", "user_handlers"]], "app.handlers.device_handlers": [[1, 1, 1, "", "associate_user_to_device"], [1, 1, 1, "", "check_device_status"], [1, 1, 1, "", "get_all_device_statuses"], [1, 1, 1, "", "get_all_sensor_data_for_device"], [1, 1, 1, "", "get_all_sensor_data_for_user_device"], [1, 1, 1, "", "get_all_sensor_data_for_user_devices"], [1, 1, 1, "", "get_device_status"], [1, 1, 1, "", "get_sensor_data_with_user_and_device_info"]], "app.handlers.sensor_handlers": [[1, 1, 1, "", "add_sensor_data"], [1, 1, 1, "", "clear_sensor_data"], [1, 1, 1, "", "get_sensor_data"], [1, 1, 1, "", "list_sensor_data"], [1, 1, 1, "", "remove_sensor_data"], [1, 1, 1, "", "show_sensor_data"], [1, 1, 1, "", "update_sensor_data"]], "app.handlers.user_handlers": [[1, 1, 1, "", "add_user"], [1, 1, 1, "", "clear_users"], [1, 1, 1, "", "list_users"], [1, 1, 1, "", "register_user"], [1, 1, 1, "", "remove_user"], [1, 1, 1, "", "show_user"], [1, 1, 1, "", "update_user"]], "app.models": [[0, 2, 1, "", "Device"], [0, 2, 1, "", "Profile"], [0, 2, 1, "", "SensorData"], [0, 2, 1, "", "User"]], "app.models.Device": [[0, 3, 1, "", "id"], [0, 3, 1, "", "last_updated"], [0, 3, 1, "", "name"], [0, 3, 1, "", "sensordata"], [0, 3, 1, "", "status"], [0, 3, 1, "", "user"], [0, 3, 1, "", "user_id"]], "app.models.Profile": [[0, 3, 1, "", "description"], [0, 3, 1, "", "id"], [0, 3, 1, "", "level"], [0, 3, 1, "", "name"], [0, 3, 1, "", "type"], [0, 3, 1, "", "user"], [0, 3, 1, "", "user_id"]], "app.models.SensorData": [[0, 3, 1, "", "appId"], [0, 3, 1, "", "data"], [0, 3, 1, "", "device"], [0, 3, 1, "", "device_id"], [0, 3, 1, "", "id"], [0, 3, 1, "", "messageType"], [0, 3, 1, "", "ts"], [0, 3, 1, "", "user"], [0, 3, 1, "", "user_id"]], "app.models.User": [[0, 4, 1, "", "check_password"], [0, 3, 1, "", "device"], [0, 3, 1, "", "email"], [0, 3, 1, "", "id"], [0, 3, 1, "", "password"], [0, 3, 1, "", "profile"], [0, 3, 1, "", "sensordata"], [0, 4, 1, "", "set_password"], [0, 3, 1, "", "username"]], "app.routes": [[2, 0, 0, "-", "auth_routes"], [2, 0, 0, "-", "device_routes"], [2, 0, 0, "-", "sensor_routes"], [2, 1, 1, "", "setup_routes"], [2, 0, 0, "-", "user_routes"]], "app.routes.auth_routes": [[2, 1, 1, "", "setup_auth_routes"]], "app.routes.device_routes": [[2, 1, 1, "", "setup_device_routes"]], "app.routes.sensor_routes": [[2, 1, 1, "", "setup_sensor_routes"]], "app.routes.user_routes": [[2, 1, 1, "", "setup_user_routes"]], "auth": [[3, 2, 1, "", "OAuth2Session"], [3, 0, 0, "-", "auth"], [3, 0, 0, "-", "login"], [3, 0, 0, "-", "oauth2_server"]], "auth.OAuth2Session": [[3, 4, 1, "", "authorization_url"], [3, 4, 1, "", "fetch_token"], [3, 4, 1, "", "generate_jwt_token"]], "auth.auth": [[3, 2, 1, "", "OAuth2Session"]], "auth.auth.OAuth2Session": [[3, 4, 1, "", "authorization_url"], [3, 4, 1, "", "fetch_token"], [3, 4, 1, "", "generate_jwt_token"]], "auth.login": [[3, 1, 1, "", "handle_callback"], [3, 1, 1, "", "login_user"]], "auth.oauth2_server": [[3, 2, 1, "", "AuthorizationCode"], [3, 2, 1, "", "AuthorizationCodeGrant"], [3, 2, 1, "", "Client"], [3, 1, 1, "", "authorize"], [3, 1, 1, "", "generate_access_token"], [3, 1, 1, "", "query_client"], [3, 1, 1, "", "save_token"], [3, 1, 1, "", "token"]], "auth.oauth2_server.AuthorizationCode": [[3, 4, 1, "", "get_redirect_uri"], [3, 4, 1, "", "get_scope"]], "auth.oauth2_server.AuthorizationCodeGrant": [[3, 4, 1, "", "authenticate_user"], [3, 4, 1, "", "delete_authorization_code"], [3, 4, 1, "", "query_authorization_code"], [3, 4, 1, "", "save_authorization_code"]], "auth.oauth2_server.Client": [[3, 4, 1, "", "check_client_secret"], [3, 4, 1, "", "check_endpoint_auth_method"], [3, 4, 1, "", "check_grant_type"], [3, 4, 1, "", "check_redirect_uri"], [3, 4, 1, "", "check_response_type"], [3, 4, 1, "", "get_allowed_scope"], [3, 4, 1, "", "get_client_id"], [3, 4, 1, "", "get_default_redirect_uri"], [3, 4, 1, "", "get_redirect_uri"]], "mqtt": [[7, 0, 0, "-", "mqtt_handler"], [7, 1, 1, "", "start_mqtt_listener"]], "mqtt.mqtt_handler": [[7, 1, 1, "", "insert_data"], [7, 1, 1, "", "on_connect"], [7, 1, 1, "", "on_message"], [7, 1, 1, "", "start_mqtt_listener"]], "run": [[8, 1, 1, "", "main"]]}, "objnames": {"0": ["py", "module", "Python module"], "1": ["py", "function", "Python function"], "2": ["py", "class", "Python class"], "3": ["py", "attribute", "Python attribute"], "4": ["py", "method", "Python method"]}, "objtypes": {"0": "py:module", "1": "py:function", "2": "py:class", "3": "py:attribute", "4": "py:method"}, "terms": {"": 1, "404": 1, "A": 1, "The": [0, 1, 2, 3, 7], "access": 3, "add": [1, 2, 5], "add_sensor_data": 1, "add_us": 1, "against": 0, "aiohttp": [0, 2, 7], "all": [1, 2], "allow": 3, "an": [1, 3, 7], "api": [2, 5], "app": [5, 6, 7], "appid": [0, 6], "applic": [0, 2, 3, 7, 8], "associ": [1, 3, 7], "associate_user_to_devic": 1, "async": [0, 1, 3, 7, 8], "asyncsess": [1, 7], "auth": [5, 6], "auth_rout": [0, 6], "authent": 3, "authenticate_us": [3, 6], "author": [3, 6], "authorization_base_url": 3, "authorization_cod": 3, "authorization_url": [3, 6], "authorizationcod": [3, 6], "authorizationcodegr": [3, 6], "base": [0, 3], "belong": 1, "between": 7, "bool": 0, "broker": 7, "brown": 5, "callback": [2, 7], "check": [0, 3], "check_client_secret": [3, 6], "check_device_statu": 1, "check_endpoint_auth_method": [3, 6], "check_grant_typ": [3, 6], "check_password": [0, 6], "check_redirect_uri": [3, 6], "check_response_typ": [3, 6], "class": [0, 3], "clear_sensor_data": 1, "clear_us": 1, "client": [3, 6, 7], "client_id": 3, "client_secret": 3, "client_secret_bas": 3, "clientmixin": 3, "clientsess": 3, "code": 3, "config": [5, 6], "configur": 2, "connack": 7, "connect": 7, "contain": [1, 7], "content": 6, "creat": [1, 2], "creation": 1, "data": [0, 1, 2, 6, 7], "databas": [0, 1, 7], "default": 3, "delet": [1, 2, 3], "delete_authorization_cod": [3, 6], "descript": [0, 6], "detail": [1, 5], "devic": [0, 1, 2, 6, 7], "device_handl": 5, "device_id": [0, 2, 6, 7], "device_rout": [0, 6], "dict": 7, "dictionari": 3, "drop": 0, "email": [0, 6], "endpoint": 3, "ensur": 7, "entri": 8, "error": 1, "exchang": 3, "extens": 6, "failur": 1, "fals": 0, "fetch": 3, "fetch_token": [3, 6], "flag": 7, "form": 3, "found": [1, 3], "from": [1, 2, 3, 7], "function": 7, "gener": 3, "generate_access_token": [3, 6], "generate_jwt_token": [3, 6], "get": [1, 2, 3], "get_all_device_status": 1, "get_all_sensor_data_for_devic": 1, "get_all_sensor_data_for_user_devic": 1, "get_allowed_scop": [3, 6], "get_client_id": [3, 6], "get_default_redirect_uri": [3, 6], "get_device_statu": 1, "get_redirect_uri": [3, 6], "get_scop": [3, 6], "get_sensor_data": 1, "get_sensor_data_with_user_and_device_info": 1, "given": 3, "grant_typ": 3, "handl": [1, 2, 3], "handle_callback": [3, 6], "handler": 5, "hash": 0, "i": [1, 3, 7], "id": [0, 1, 2, 3, 6, 7], "indic": 1, "inform": 3, "init_app": [0, 6], "init_db": [0, 6], "initi": [0, 3, 8], "insert": 7, "insert_data": [6, 7], "instanc": [0, 2, 7], "int": 7, "its": 1, "json": 1, "jwt": 3, "kwarg": [0, 3], "last_upd": [0, 6], "level": [0, 6], "list": [1, 2], "list_sensor_data": 1, "list_us": 1, "listen": [7, 8], "log": 2, "login": [2, 6], "login_us": [3, 6], "main": [6, 8], "match": [0, 3], "messag": [1, 7], "messagetyp": [0, 6], "method": 3, "model": 6, "modul": [5, 6], "mqtt": [5, 6, 8], "mqtt_handler": 6, "mqttmessag": 7, "msg": 7, "name": [0, 6], "new": [1, 2], "none": [0, 3, 7, 8], "oauth2": 3, "oauth2_serv": 6, "oauth2request": 3, "oauth2sess": [3, 6], "object": [1, 3], "on_connect": [6, 7], "on_messag": [6, 7], "one": 3, "oper": 1, "option": 3, "otherwis": [0, 3], "packag": [5, 6], "param": 1, "paramet": [0, 1, 2, 3, 7], "password": [0, 6], "patch": 2, "payload": 7, "plain": 0, "point": 8, "post": 2, "privat": 7, "profil": [0, 2, 6], "proper": 7, "provid": 3, "publish": 7, "queri": 3, "query_authorization_cod": [3, 6], "query_cli": [3, 6], "rc": 7, "receiv": [3, 7], "recreat": 0, "redirect": 3, "redirect_uri": 3, "regist": 2, "register_us": 1, "registr": 1, "remove_sensor_data": 1, "remove_us": 1, "request": [1, 3], "reset_db": [0, 6], "respons": [1, 3, 7], "response_typ": 3, "rest": 2, "restructuredtext": 5, "result": 7, "retriev": [1, 2], "return": [0, 1, 3, 7, 8], "rout": [0, 6], "run": [5, 6], "save": 3, "save_authorization_cod": [3, 6], "save_token": [3, 6], "scope": 3, "secret": 3, "see": 5, "sensor": [1, 2, 7], "sensor_data": 2, "sensor_handl": 5, "sensor_rout": [0, 6], "sensordata": [0, 6], "sent": 7, "server": [0, 3, 7], "session": [1, 7], "set": [0, 2, 7], "set_password": [0, 6], "setup": 0, "setup_auth_rout": [0, 2], "setup_db": [0, 6], "setup_device_rout": [0, 2], "setup_rout": [0, 2], "setup_sensor_rout": [0, 2], "setup_user_rout": [0, 2], "show": 3, "show_sensor_data": 1, "show_us": 1, "sourc": [0, 1, 2, 3, 7, 8], "specif": [1, 2], "specifi": 1, "start": [7, 8], "start_mqtt_listen": [6, 7], "state": 3, "statu": [0, 1, 2, 6], "status": 1, "store": [0, 3], "str": [0, 7], "string": 3, "submodul": [5, 6], "subpackag": 6, "success": [1, 3], "syntax": 5, "t": [0, 6], "text": 0, "thingy91": 5, "token": [3, 6], "token_endpoint_auth_method": 3, "token_url": 3, "topic": 7, "true": 0, "type": [0, 1, 6], "up": 2, "updat": [1, 2], "update_sensor_data": 1, "update_us": 1, "uri": 3, "url": 3, "us": [3, 5], "user": [0, 1, 2, 3, 6, 7], "user_handl": 5, "user_id": [0, 6], "user_rout": [0, 6], "userdata": 7, "userdata_set": 7, "usernam": [0, 6], "verifi": 3, "web": [0, 1, 2, 7, 8], "when": 7, "which": 7, "without": 3, "your": 5}, "titles": ["app package", "app.handlers package", "app.routes package", "auth package", "config module", "AlertMe documentation", "thingy91-api-brown", "mqtt package", "run module"], "titleterms": {"alertm": 5, "api": 6, "app": [0, 1, 2], "auth": 3, "auth_rout": 2, "brown": 6, "config": 4, "content": [0, 1, 2, 3, 5, 7], "device_handl": 1, "device_rout": 2, "document": 5, "extens": 0, "handler": 1, "login": 3, "model": 0, "modul": [0, 1, 2, 3, 4, 7, 8], "mqtt": 7, "mqtt_handler": 7, "oauth2_serv": 3, "packag": [0, 1, 2, 3, 7], "rout": 2, "run": 8, "sensor_handl": 1, "sensor_rout": 2, "submodul": [0, 1, 2, 3, 7], "subpackag": 0, "thingy91": 6, "user_handl": 1, "user_rout": 2}})