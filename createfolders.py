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
    # Crear un archivo .gitkeep en cada carpeta
    with open(os.path.join(folder, '.gitkeep'), 'w') as f:
        pass

# Crear archivos básicos
open("YahooFinanceApp/.gitignore", 'a').close()
open("YahooFinanceApp/README.md", 'a').close()
open("YahooFinanceApp/requirements.txt", 'a').close()

print("Estructura de carpetas creada con éxito y .gitkeep añadidos")
