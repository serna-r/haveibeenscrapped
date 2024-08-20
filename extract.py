import pandas as pd
from urllib.request import Request, urlopen
from bs4 import BeautifulSoup

# Url for pwned sites
url = 'https://haveibeenpwned.com/PwnedWebsites'
# Download html
req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
webpage = urlopen(req).read()

# Procesar el HTML con BeautifulSoup
soup = BeautifulSoup(webpage, 'html.parser')

# Lista para almacenar los datos extraídos
data = []

# Encontrar todos los divs que contienen la información
for item in soup.find_all('div', class_='col-sm-10'):
    nombre = item.find('h3').text.strip()
    descripcion = item.find_all('p')[0].text.strip()  # Descripción en el primer 

    
    # Extraer la información de los 
    detalles = item.find_all('strong')
    breach_date = detalles[0].next_sibling.strip()  # Breach date
    compromised_accounts = detalles[2].next_sibling.strip()  # Compromised accounts
    compromised_data = detalles[3].next_sibling.strip()  # Compromised data
    
    # If passwords are compromised in the breach add them
    if 'passwords' in compromised_data.lower():
        # Agregar los datos a la lista
        data.append({
            'Nombre': nombre,
            'Breach Date': breach_date,
            'Compromised Accounts': compromised_accounts,
            'Compromised Data': compromised_data,
            'Descripción': descripcion,
        })

# Crear un DataFrame de pandas
df = pd.DataFrame(data)

# Guardar el DataFrame en un archivo CSV
df.to_csv('datos_extraidos.csv', index=False)

print("Datos extraídos y guardados en 'datos_extraidos.csv'")