from backend.main_api import app

print([route.path for route in app.routes])