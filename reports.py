class reports:
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