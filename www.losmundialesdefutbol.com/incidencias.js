let fs = require('fs');

let script = "use bd2_mundiales;\n"
script += "INSERT INTO incidencia (jugador, mundial, jugo, no_jugo, goles, yellow_card, red_card, ganados, empatados, perdidos) VALUES \n"
fs.readFile('cargaIncidencia.csv', 'utf-8', (err, data) => {
  if(err) {
    console.log('error: ', err);
  } else {
    let lineas = data.split('\r\n')
    for (let i = 1; i < lineas.length; i++) {
        const linea = lineas[i].split(',')
        script += `((SELECT id FROM jugador WHERE nombre = '${linea[0]}'), `
        script += `${linea[1]}, ${linea[4]}, ${linea[5]}, ${linea[6]}, `
        script += `${linea[7]}, ${linea[8]}, ${linea[9]}, ${linea[10]}, `
        script += `${linea[11]})`
        if(i < lineas.length - 1) script += ",\n"
    }
    fs.writeFile('incidencia.sql', script, (err) => {
        if (err) {
            console.error(err)
            return
        }
    })
  }
});


