var DomParser = require('dom-parser');
module.exports = {
	guardarPaises: function () {
		const fs = require('fs');
        let paisesRAw = 'paisesRaw.sql';
        fs.readFile(paisesRAw, 'utf8', function (err,data) {
            if (err) {
                return console.log(err);
            }
    
            fs.writeFile(paisesRAw, '', 'utf8', function (err) {
                if (err) return console.log(err);
            });
        });

        fs.readFile(__dirname + '/selecciones.html', 'utf8' , (err, data) => {
            if (err) {
                console.error(err)
                return
            }
            this.getPaises(data, paisesRAw);
        });
	},
    getPaises: function (htmlScript, fileName) {
		var parser = new DomParser();
		var dom = parser.parseFromString(htmlScript);
		var sections = dom.getElementsByClassName('left margen-t2');

		let datosIniciales = this.getDatosActuales(sections);
		console.log(datosIniciales);
        datosIniciales.forEach(datos => {
            this.escribirConsulta(datos, fileName);
        });
    },
    getDatosActuales: function (dom, datosIniciales) {
		var datosIniciales = [];
        dom.forEach(countryContainer => {
            try {
                let node = countryContainer.childNodes[1];
                // console.log(countryContainer.childNodes[1]);
                console.log(node.childNodes[4].outerHTML);
                datosIniciales.push({'nombre': node.childNodes[4].outerHTML.trim().replace('\t  ', '')});
            } catch (e) {
                console.log(e);
            }
            // console.log(countryContainer.childNodes);
        });

		return datosIniciales;
    },
	escribirConsulta: function(datosIniciales, fileName) {
		const fieldNames = Object.keys(datosIniciales).join(',');
		const values = Object.values(datosIniciales).join("','");
		var sql = `INSERT INTO pais (${fieldNames}) values ('${values}');\n`;

		const fs = require('fs');
		fs.appendFileSync(fileName, sql);
	}
  };