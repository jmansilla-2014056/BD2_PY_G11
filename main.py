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

# Data marts
createModels = False
createMarts = False
showReports = False

def main():
    showMenu()

def showMenu():
    tcolor = bcolors.DISABLED
    lcolor = bcolors.DISABLED
    cModel = bcolors.DISABLED
    cMarts = bcolors.DISABLED
    cRep = bcolors.DISABLED

    if extracted != None:
        tcolor = bcolors.WHITE

    if transformed != None:
        lcolor = bcolors.WHITE

    if createModels:
        cModel = bcolors.WHITE

    if createMarts:
        cMarts = bcolors.WHITE

    if showReports:
        cRep = bcolors.WHITE

    print(bcolors.HEADER + '         WELCOME!')
    print('========================')
    print('')
    print(bcolors.WHITE + '1. Extraer informacion')
    print(tcolor + '2. Transformacion de informacion') 
    print(lcolor + '3. Carga de informacion') 
    print(cModel + '3. Crear modelo')
    print(cMarts + '4. Crear Datamarts')
    print(cRep + '5. Reportes')
    print(bcolors.WHITE + '0. Exit')

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
            jump = False

            fieldIndex = 0
            fieldBlacklist = [
                covidIndex.iso_code,
                covidIndex.continent,
                covidIndex.location,
                covidIndex.date,
                covidIndex.total_cases,
                covidIndex.new_cases,
                covidIndex.new_cases_smoothed,
                covidIndex.total_deaths,
                covidIndex.new_deaths,
                covidIndex.new_deaths_smoothed,
                covidIndex.total_cases_per_million,
                covidIndex.new_cases_per_million,
                covidIndex.new_cases_smoothed_per_million,
                covidIndex.total_deaths_per_million,
                covidIndex.new_deaths_per_million,
                covidIndex.new_deaths_smoothed_per_million,
                covidIndex.stringency_index,
                covidIndex.population,
                covidIndex.population_density,
                covidIndex.median_age,
                covidIndex.aged_65_older,
                covidIndex.aged_70_older,
                covidIndex.gdp_per_capita,
                covidIndex.extreme_poverty,
                covidIndex.cardiovasc_death_rate,
                covidIndex.diabetes_prevalence,
                covidIndex.handwashing_facilities,
                covidIndex.hospital_beds_per_thousand,
                covidIndex.life_expectancy,
                covidIndex.human_development_index
            ]
            for field in row:
                if fieldIndex in fieldBlacklist and field == '':
                    jump = True
                    fieldIndex = fieldIndex + 1
                    break
                
                fieldIndex = fieldIndex + 1
            if jump:
                break

            transformed.append(row)

        addLog('info', 'Data Transformed', 'Final rows passed: ' + str(len(transformed)))
    except Exception as e:
        addLog('error', 'Transform info failed', str(e))

def loadInfo():
    statement = ''
    try:
        global transformed
        if transformed == None:
            return

        batches = np.array_split(transformed, 100)

        for batch in batches:
            for row in batch:
                statement = f'''INSERT INTO temp ({','.join(covidIndex.fieldNames)}) VALUES ("{'","'.join(row)}")'''
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
        print(statement)
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