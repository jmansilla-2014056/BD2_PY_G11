# Libraries
import csv
import datetime
import mysql.connector as database
import numpy as np
import sys, os
from dotenv import load_dotenv

# app
from covidIndex import covidIndex, covidTempQuery
from reports import reports
from utils import bcolors

load_dotenv()

connection = database.connect(
    user=os.getenv('MYSQL_USER'),
    password=os.getenv('MYSQL_PASSWORD'),
    host=os.getenv('MYSQL_HOST'),
    database=os.getenv('MYSQL_DATABASE'))

cursor = connection.cursor(buffered=True)
initialRoute = 'covid.csv'

# ETL tools
extracted = None
transformed = None

def main():
    showMenu()

def showMenu():
    tcolor = bcolors.DISABLED
    lcolor = bcolors.DISABLED

    if extracted != None:
        tcolor = bcolors.WHITE

    if transformed != None:
        lcolor = bcolors.WHITE

    print(bcolors.HEADER + '         WELCOME!')
    print('========================')
    print('')
    print(bcolors.WHITE + '1. Extraer informacion')
    print(tcolor + '2. Transformacion de informacion') 
    print(lcolor + '3. Carga de informacion') 
    print(bcolors.WHITE + '3. Clear tables data')
    print('4. Reports')
    print('0. Exit')

    option = input()
    if option == '1':
        try:
            extractInfo()
        except Exception as e:
            print(f"Error READING CSV, YOU R IN TROUBLES: {e}")
    if option == '2':
        transformInfo()
    if option == '3':
        loadInfo()
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
    reportData = reports.reportsParams['r'+n]
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

def extractInfo():
    try:
        with open(initialRoute, newline='') as csvfile:
            data = csv.reader(csvfile, delimiter=',', quotechar='"')
            global extracted
            extracted = list(data)
            count = str(len(extracted))
            addLog('info', 'Data extracted', count + ' rows extracted.')
            print('Data extracted successfully!!')
    except Exception as e:
        addLog('error', 'Extract info fail', str(e))

def transformInfo():
    try:
        global extracted
        global transformed
        transformed = []
        index = 0
        for row in extracted:
            if index == 0:
                index = index + 1
                continue
            
            index = index + 1
            if not row[covidIndex.continent[0]] or row[covidIndex.continent[0]] == '' :
                continue
            # TODO: add all missing filters 
            transformed.append(row)

        addLog('info', 'Data Transformed', 'Final rows passed: ' + str(len(transformed)))
    except Exception as e:
        addLog('error', 'Transform info failed', str(e))

def loadInfo():
    try:
        global transformed
        if transformed == None:
            return

        batches = transformed
        np.array_split(batches, 100)

        for batch in batches:
            for row in batch:
                statement = f'''INSERT INTO temp ({','.join(covidIndex.fieldNames)}) VALUES ('{"','".join(row)}')'''
                # print(statement)
                excecuteStatement('mysql', statement)
                commitStatement('mysql')

            addLog('info', 'Data Loaded', 'Rows loaded in batch: ' + str(len(row)))
    except Exception as e:
        addLog('error', 'Load info failed', str(e))

def commitStatement(database):
    try:
        if database == 'mysql':
                connection.commit()

        if database =='sqlserver1':
            print('excecute sql server query')
    except Exception as e:
        addLog('error', 'Executing Commit, rollback will be running', str(e))
        if database == 'mysql':
            connection.rollback()

def excecuteStatement(database, statement):
    try:
        if database == 'mysql':
            cursor.execute(statement)

        if database =='sqlserver1':
            print('excecute sql server query')
    except Exception as e:
        addLog('error', 'Executing Query in ' + database, str(e))

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

def addLog(type, message, description):
    if type == 'error':
        print(bcolors.FAIL + message + ". Please check logs for more info. "+ bcolors.WHITE)
        print(description)

    currentDT = datetime.datetime.now()
    date = currentDT.strftime("%Y/%m/%d %H:%M:%S")
    logType = formatColumn(type.upper(), 10, ' ')
    fMessage = formatColumn(message, 50, ' ')
    fLog= open(f"logs.txt","a+")
    fLog.write(date + "\t" + logType + "\t" + fMessage + "\t" + description + "\n")
    fLog.close()

if __name__ == "__main__":
    main()