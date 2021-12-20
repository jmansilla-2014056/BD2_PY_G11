import csv
import mysql.connector as database
import sys, os
from dotenv import load_dotenv
import covidIndex 

load_dotenv()

connection = database.connect(
    user=os.getenv('MYSQL_USER'),
    password=os.getenv('MYSQL_PASSWORD'),
    host=os.getenv('MYSQL_HOST'),
    database=os.getenv('MYSQL_DATABASE'))


class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    WHITE  = '\33[37m'

cursor = connection.cursor(buffered=True)
initialRoute = 'entrada.csv'

reportsParams = {
    "r4" : { # PROMEDIO TOTAL POR PAIS
        "query" : '''SELECT c.name, ROUND(AVG(IFNULL(t.totalDamage,0)),5) as average FROM tsunami t
                JOIN country c ON c.id = t.countryId
                GROUP BY c.id
            ORDER BY average DESC;''',
        "c1": {
            "size": 40,
            "name": "COUNTRY"
        },
        "c2": {
            "size": 10,
            "name": "DAMAGE AVG"
        },
    },
    "r5" : { # TOP 5 PAISES CON MAS MUERTES
        "query" : '''SELECT c.name, SUM(IFNULL(t.totalDeaths,0)) as deaths FROM tsunami t
                JOIN country c ON c.id = t.countryId
                GROUP BY c.id
            ORDER BY deaths DESC LIMIT 5;''',
        "c1": {
            "size": 40,
            "name": "COUNTRY"
        },
        "c2": {
            "size": 7,
            "name": "DEATHS"
        },
    },
    "r6" : { # TOP 5 A;OS CON MAS MUERTES
        "query": '''SELECT ti.year, SUM(IFNULL(t.totalDeaths,0)) as deaths FROM tsunami t
                JOIN Time ti ON ti.id = t.TimeId
                GROUP BY ti.year
            ORDER BY deaths DESC LIMIT 5;''',
        "c1": {
            "size": 4,
            "name": "YEAR"
        },
        "c2": {
            "size": 7,
            "name": "DEATHS"
        },
    },
    "r7" : { # TOP 5 A;OS CON MAS TSUNAMIS
        "query": '''SELECT ti.year, count(*) as tsunamis FROM tsunami t
            JOIN Time ti ON ti.id = t.TimeId
            GROUP BY ti.year
        ORDER BY tsunamis DESC LIMIT 5;''',
        "c1": {
            "size": 4,
            "name": "YEAR"
        },
        "c2": {
            "size": 8,
            "name": "TSUNAMIS"
        },
    },
    "r8" : { # TOP 5 PAISES CON MAYOR NUMERO DE CASAS DESTRUIDAS
        "query" : '''SELECT c.name, SUM(IFNULL(t.totalHousesDestroyed,0)) as houses FROM tsunami t
                JOIN country c ON c.id = t.countryId
                GROUP BY c.id
            ORDER BY houses DESC LIMIT 5;''',
        "c1": {
            "size": 40,
            "name": "COUNTRY"
        },
        "c2": {
            "size": 16,
            "name": "HOUSES DESTROYED"
        },
    },
    "r9" : { # TOP 5 PAISES CON MAYOR NUMERO DE CASAS DA;ADAS
        "query" : '''SELECT c.name, SUM(IFNULL(t.totalHousesDamaged,0)) as houses FROM tsunami t
                JOIN country c ON c.id = t.countryId
                GROUP BY c.id
            ORDER BY houses DESC LIMIT 5;''',
        "c1": {
            "size": 40,
            "name": "COUNTRY"
        },
        "c2": {
            "size": 14,
            "name": "HOUSES DAMAGED"
        },
    },
    "r10" : { # PROMEDIO DE ALTURA MAXIMA POR PAIS
        "query": '''SELECT c.name, ROUND(AVG(IFNULL(t.maximumWaterHeight,0)),5) as average FROM tsunami t
                JOIN country c ON c.id = t.countryId
                GROUP BY c.id
            ORDER BY average DESC;''',
        "c1": {
            "size": 40,
            "name": "COUNTRY"
        },
        "c2": {
            "size": 10,
            "name": "MAX HEIGHT"
        },
    },
}

def main():
    showMenu()

def showMenu():
    print(bcolors.HEADER + '         WELCOME!')
    print('========================')
    print('')
    print(bcolors.WHITE + '1. Read CSV')
    print('2. Drop and create tables')
    print('3. Clear tables data')
    print('4. Reports')
    print('0. Exit')

    option = input()
    if option == '1':
        try:
            saveInitialData()
            connection.commit()
        except Exception as e:
            print(f"Error READING CSV, YOU R IN TROUBLES: {e}")
    if option == '2':
        clearTables()
        createTables()
    if option == '3':
        try:
            print('limpiar data')
        except Exception as e:
            print(f"Error CLEANING DATA: {e}")
    if option == '4':
        reportsMenu()
    elif option == '0':
        quit()

    showMenu()

def reportsMenu():
    print("\n\n ====REPORTS====")
    print('Please insert report number (1 to 10, insert 0 to go Back):')
    option = input()
    try:
        # crear reporte
        print('Crear reporte')

    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        print(exc_type, exc_tb.tb_lineno)
        print(f"Error printing report {option}, YOU R IN TROUBLES: {e}")

    reportsMenu()

def reporte1():
    tsunamiRecords = 'SELECT COUNT(*) FROM tsunami'
    timeRecords = 'SELECT COUNT(*) FROM Time'
    countriesRecords = 'SELECT COUNT(*) FROM country'
    try:
        cursor.execute(tsunamiRecords)
        print('Tsunami table records: '+ str(cursor.fetchone()[0]))
        cursor.execute(timeRecords)
        print('Time table records: '+ str(cursor.fetchone()[0]))
        cursor.execute(countriesRecords)
        print('Country table records: '+ str(cursor.fetchone()[0]))
    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        print(exc_type, exc_tb.tb_lineno)
        print(f"Error printing report 2: {e}")
    
def reporte2():
    statement = '''SELECT yr, GROUP_CONCAT(CONCAT(NAME, ' (', cuenta,')') ORDER BY cuenta DESC SEPARATOR '|' ) countries FROM (
            SELECT ti.year AS yr, c.name, COUNT(*) AS cuenta
            FROM tsunami t
                JOIN country c ON c.id = t.countryId
                JOIN Time ti ON ti.id = t.TimeId
                GROUP BY yr, name
            ORDER BY yr, cuenta, NAME) AS alias
        GROUP BY yr;'''

    cursor.execute(statement)
    f= open("report_02.txt","w+")
    formatYear = formatColumn('Year', 5, ' ')
    country1 = formatColumn('country 1', 40, ' ')
    country2 = formatColumn('country 2', 40, ' ')
    country3 = formatColumn('country 3', 40, ' ')
    country4 = formatColumn('country 4', 40, ' ')
    country5 = formatColumn('country 5', 40, ' ')
    try:
        f.write(formatYear + "\t" + country1 + "\t" + country2 + "\t" + country3 + "\t" + country4 + "\t" + country5 + "\n")
        for (yr, countries) in cursor:
            formatYear = formatColumn(yr, 5, ' ')
            countriesStr = countries.split('|')
            maxRange = min(len(countriesStr), 5)
            countryList = ''
            for i in range(maxRange):
                countryList = countryList + formatColumn(countriesStr[i] or '', 40, ' ')+"\t"
            f.write(formatYear + "\t" + countryList + "\n")
        f.close()
    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        print(exc_type, exc_tb.tb_lineno)
        print(f"Error printing report 2: {e}")

def reporte3():
    statement = '''SELECT country, GROUP_CONCAT(CONCAT(yr, ' (', cuenta,')') ORDER BY cuenta DESC SEPARATOR '|' )FROM (
            SELECT c.name AS country, ti.year AS yr, COUNT(*) AS cuenta
            FROM tsunami t
                JOIN country c ON c.id = t.countryId
                JOIN Time ti ON ti.id = t.TimeId
                GROUP BY NAME, yr
            ORDER BY cuenta desc, yr) AS alias
        GROUP BY country;'''

    cursor.execute(statement)
    f= open("report_03.txt","w+")
    formatYear = formatColumn('Country', 40, ' ')
    country1 = formatColumn('Year 1', 8, ' ')
    country2 = formatColumn('Year 2', 8, ' ')
    country3 = formatColumn('year 3', 8, ' ')
    country4 = formatColumn('year 4', 8, ' ')
    country5 = formatColumn('year 5', 8, ' ')
    try:
        f.write(formatYear + "\t" + country1 + "\t" + country2 + "\t" + country3 + "\t" + country4 + "\t" + country5 + "\n")
        for (yr, countries) in cursor:
            formatYear = formatColumn(yr, 40, ' ')
            countriesStr = countries.split('|')
            maxRange = min(len(countriesStr), 5)
            countryList = ''
            for i in range(maxRange):
                countryList = countryList + formatColumn(countriesStr[i] or '', 8, ' ')+"\t"
            f.write(formatYear + "\t" + countryList + "\n")
        f.close()
    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        print(exc_type, exc_tb.tb_lineno)
        print(f"Error printing report 3: {e}")

def reporte4omas(n):
    reportData = reportsParams['r'+n]
    statement = reportData['query']
    c1 = reportData['c1']
    c2 = reportData['c2']
    
    try:
        cursor.execute(statement)

        f= open(f"report_{n}.txt","w+")
        firstColumn = formatColumn(c1['name'], c1['size'], ' ')
        secondColumn = formatColumn(c2['name'], c2['size'], ' ')
        f.write(firstColumn + "\t" + secondColumn + "\n")
        for (column1, column2) in cursor:
            firstColumn = formatColumn(column1, c1['size'], ' ')
            secondColumn = formatColumn(column2, c2['size'], ' ')
            f.write(firstColumn + "\t" + secondColumn + "\n")
        f.close()
    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        print(exc_tb.tb_lineno)
        print(f"Error printing report {n}: {e}")

def formatColumn(text, lenght, character):
    return str(text).ljust(lenght, character)

def saveInitialData():
    with open(initialRoute, newline='') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=',', quotechar='"')
        count = 0
        for row in spamreader:
            print(row)
            # Hacer lo que se necesite para guardar la data 
            count = count + 1

def clearTables():
    try:
        statement = 'DROP TABLE IF EXISTS temp;'
        cursor.execute(statement)
        statement = 'DROP TABLE IF EXISTS continent;'
        cursor.execute(statement)
        statement = 'DROP TABLE IF EXISTS country;'
        cursor.execute(statement)
        statement = 'DROP TABLE IF EXISTS fecha;'
        cursor.execute(statement)
        statement = 'DROP TABLE IF EXISTS vaccinates_data;'
        cursor.execute(statement)
        statement = 'DROP TABLE IF EXISTS testunits;'
        cursor.execute(statement)
        statement = 'DROP TABLE IF EXISTS reproduction_rate_data;'
        cursor.execute(statement)
        statement = 'DROP TABLE IF EXISTS cases_per_day_data;'
        cursor.execute(statement)
        statement = 'DROP TABLE IF EXISTS population_index_data;'
        cursor.execute(statement)
        connection.commit()
        print(f"Database cleared!")
    except database.Error as e:
        print(f"Error clearing database: {e}")

def createTables():
    try:
        print(f"Database created!")
    except database.Error as e:
        print(f"Error creating tables: {e}")

if __name__ == "__main__":
    main()