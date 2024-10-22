import os

# Definir las carpetas que queremos crear
folders = [
    "YahooFinanceApp/data/raw",
    "YahooFinanceApp/data/processed",
    "YahooFinanceApp/notebooks",
    "YahooFinanceApp/src/api",
    "YahooFinanceApp/src/visualization",
    "YahooFinanceApp/src/dashboard",
    "YahooFinanceApp/src/etl",
    "YahooFinanceApp/tests",
    "YahooFinanceApp/docs/database_schema",
    "YahooFinanceApp/docs/user_guide",
    "YahooFinanceApp/powerbi",
    "YahooFinanceApp/assets",
    "YahooFinanceApp/config"
]

# Crear las carpetas
for folder in folders:
    os.makedirs(folder, exist_ok=True)

# Crear archivos básicos
open("YahooFinanceApp/.gitignore", 'a').close()
open("YahooFinanceApp/README.md", 'a').close()
open("YahooFinanceApp/requirements.txt", 'a').close()

print("Estructura de carpetas creada con éxito")
