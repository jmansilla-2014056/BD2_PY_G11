var DomParser = require('dom-parser');

const fs = require('fs');
let mundialesRaw = 'mundialesRaw.sql';
let equiposRaw = 'equiposRaw.sql';

let resultadosRaw = 'resultadosRaw.sql';
module.exports = {
	guardarMundiales: function (type = 'mundial') {
        this.clearFiles();
        var files = fs.readdirSync(__dirname + '/mundiales');
		// files = [files[0]];
		files.forEach(file => {
			fs.readFile(__dirname + '/mundiales/' + file, 'utf8' , (err, data) => {
				if (err) {
					console.error(err)
					return
				}
                let fileNameSplit = file.split('_');
                let year = fileNameSplit[0];
                if (fileNameSplit[1] == 'mundial.html' && 'mundial' == type)
				    this.getMundiales(data, year, mundialesRaw);                
                
                if (fileNameSplit[1] == 'resultados.html' && 'resultados' == type)
                    this.getResultados(data, year, resultadosRaw);
                
			});
		});
        console.log('Datos importados!');
	},
    clearFiles: function() {
        fs.readFile(mundialesRaw, 'utf8', function (err,data) {
            if (err) {
                return console.log(err);
            }
    
            fs.writeFile(mundialesRaw, '', 'utf8', function (err) {
                if (err) return console.log(err);
            });
        });
        fs.readFile(equiposRaw, 'utf8', function (err,data) {
            if (err) {
                return console.log(err);
            }
    
            fs.writeFile(equiposRaw, '', 'utf8', function (err) {
                if (err) return console.log(err);
            });
        });
    },

    // GET MUNDIALES=================================================================================
    getMundiales: function (htmlScript, year, fileName) {
		var parser = new DomParser();
		var dom = parser.parseFromString(htmlScript);
		var mundialInfo = dom.getElementsByClassName('rd-100-50 a-left clearfix')[0];
		var campeonDom = dom.getElementsByClassName('margen-xauto pad-y10 bb-1 margen-b10')[0];

		let datosIniciales = this.getDatosMundial(mundialInfo);
        datosIniciales.year = year;
        datosIniciales.campeon = this.getCampeonMundial(campeonDom);
        this.escribirConsulta(datosIniciales, fileName, 'mundial');

        // LLENAR TABLA DE EQUIPOS
        if (['1934', '1938'].includes(year)) {
            console.log('nueov');
            let datosPlanteles = this.getDatosSeleccion(dom.getElementsByClassName('margen-y15 a-center clearfix max-4')[0], year);
            datosPlanteles.forEach(datosPlantel => {
                this.escribirConsulta(datosPlantel, equiposRaw, 'equipo');
            });
        } else {
            let datosPlanteles = this.getDatosPlantel(dom.getElementsByTagName('table')[3], year);
            datosPlanteles.forEach(datosPlantel => {
                this.escribirConsulta(datosPlantel, equiposRaw, 'equipo');
            });;
        }        
    },
    getDatosMundial: function (dom) {
		var datosIniciales = {
            sede: null,
        };
        try {
            var infoPagraph = dom.getElementsByClassName('margen-l10')[0];
            var pais = infoPagraph.childNodes[0].outerHTML.trim().split(':')[1].trim();
            var paisString = `(SELECT id from pais where nombre = '${pais}' )`;
            datosIniciales.sede = paisString;
        } catch(e) {
            console.log('error en dom', dom);
        }        

		return datosIniciales;
    },
    getCampeonMundial: function (dom) {
        try {
            let link = dom.getElementsByTagName('a')[0].childNodes[3].outerHTML;
            return `(Select id from pais where nombre = '${link}')`
        } catch(e) {
            return 'null';
        }
    },
    // END MUNDIALES=================================================================================
    getDatosSeleccion: function(dom, year) {
        var names = dom.getElementsByTagName('a');
        var datosPlanteles = [];

        names.forEach((a, index) => {
            const countrySelect = `(SELECT id FROM pais where nombre = '${a.innerHTML}')`;
            var plantelData = {
                mundial: year,
                grupo: 'null',
                pais: countrySelect,
            };
            datosPlanteles.push(plantelData)
        });
        return datosPlanteles;
    },
    getDatosPlantel : function(dom, year){
        var trs = dom.getElementsByClassName('a-top');
        var datosPlanteles = [];

        trs.forEach((tr, index) => {
            var tds = tr.getElementsByTagName('td');
            var group = tds[0].innerHTML;
            var countries = tds[2].getElementsByTagName('a');

            countries.forEach(countryDom => {
                const country = countryDom.childNodes[2].outerHTML.trim();
                const countrySelect = `(SELECT id FROM pais where nombre = '${country}')`;
                var plantelData = {
                    mundial: year,
                    grupo: '"' + group + '"',
                    pais: countrySelect,
                };
                datosPlanteles.push(plantelData)
            });
        });
        return datosPlanteles;
    },
    // GET RESULTADOS=================================================================================
    getResultados: function (htmlScript, year, fileName) {
        var parser = new DomParser();
		var dom = parser.parseFromString(htmlScript);
		var mundialInfo = dom.getElementsByClassName('rd-100-50 a-left clearfix')[0];
		var campeonDom = dom.getElementsByClassName('margen-xauto pad-y10 bb-1 margen-b10')[0];

		let datosIniciales = this.getDatosMundial(mundialInfo);
        datosIniciales.year = year;
        datosIniciales.campeon = this.getCampeonMundial(campeonDom);
		console.log(datosIniciales);
        this.escribirConsulta(datosIniciales, fileName);
    },
    // END RESULTADOS=================================================================================
	escribirConsulta: function(datosIniciales, fileName, tableName) {
		const fieldNames = Object.keys(datosIniciales).join(',');
		const values = Object.values(datosIniciales).join(",");
		var sql = `INSERT INTO ${tableName} (${fieldNames}) values (${values});\n`;

		const fs = require('fs');
		fs.appendFileSync(fileName, sql);
	}
  };