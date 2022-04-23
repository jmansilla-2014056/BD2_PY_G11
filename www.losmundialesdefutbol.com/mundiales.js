var DomParser = require('dom-parser');

const fs = require('fs');
let mundialesRaw = 'mundialesRaw.sql';
let equiposRaw = 'equiposRaw.sql';

let resultadosRaw = 'resultadosRaw.sql';
let premiosMundialRaw = 'premiosMundial.sql';
module.exports = {
	guardarMundiales: function (type = 'mundial') {
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
                
                if (fileNameSplit[1] == 'premios.html' && 'premios' == type) {
                    // this.clearFiles(premiosMundialRaw);
                    this.getPremios(data, year, premiosMundialRaw);
                }
                
			});
		});
        console.log('Datos importados!');
	},
    clearFiles: function(file) {
        fs.readFile(file, 'utf8', function (err,data) {
            if (err) {
                return console.log(err);
            }
    
            fs.writeFile(file, '', 'utf8', function (err) {
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
    // GET PREMIOS=================================================================================
    getPremios: function (htmlScript, year, fileName) {
        var parser = new DomParser();
		var dom = parser.parseFromString(htmlScript);
		var blockPremios = dom.getElementsByClassName('a-center')[0];
		let balonBotin = this.getBalonBotin(blockPremios, year);    
		let premiosPais = this.getPremiosPais(blockPremios, year);
        balonBotin.forEach(datos => {
            this.escribirConsulta(datos, fileName, 'premios_mundial_jugador');
        });
        premiosPais.forEach(datos => {
            this.escribirConsulta(datos, fileName, 'premios_mundial');
        });
    },
    getBalonBotin(dom, year) {
        const premios = dom.getElementsByClassName('rd-100-30');
        const datosPremios = [];
        premios.forEach(premioDiv => {
            let jugador = premioDiv.childNodes[3].innerHTML.trim()
                .replaceAll("'", '')
				.replaceAll("ć", 'c')
				.replaceAll('ę', 'e')
				.replaceAll('ł', 'l')
				.replaceAll('Ć', 'C')
				.replaceAll('ń', 'n');
            if (jugador !== '-') {
                jugador = premioDiv.childNodes[3].getElementsByTagName('a')[0].innerHTML;
                const premio = premioDiv.childNodes[1].innerHTML.trim();
                const country = premioDiv.childNodes[3].getElementsByTagName('img')[0].getAttribute('alt');
                datospremio = {
                    premio: `(SELECT id FROM premio WHERE descripcion = '${premio}')`,
                    mundial: year,
                    // jugador: `(SELECT id FROM premio WHERE descripcion = '${premio}')`,
                    jugador_name: "'"+jugador+"'",
                    pais: `(SELECT id FROM pais WHERE nombre = '${country}')`,
                }
                datosPremios.push(datospremio);
            }
        });

        const premiosjugador = dom.getElementsByClassName('rd-100-45');
        premiosjugador.forEach((premioDiv, index) => {
            if (index > 1) {
                return;
            }

            let jugador = premioDiv.getElementsByTagName('p')[1].innerHTML.trim();
            if (jugador !== '-') {
                jugadores = premioDiv.getElementsByTagName('a');
                const premio = premioDiv.getElementsByTagName('p')[0].innerHTML.trim();
                const country = premioDiv.getElementsByTagName('img')[0].getAttribute('alt');
                jugadores.forEach(jugador => {
                    const jugadornm = jugador.innerHTML.trim()
                    .replaceAll("'", '')
                    .replaceAll("ć", 'c')
                    .replaceAll('ę', 'e')
                    .replaceAll('ł', 'l')
                    .replaceAll('Ć', 'C')
                    .replaceAll('ń', 'n');

                    datospremio = {
                        premio: `(SELECT id FROM premio WHERE descripcion = '${premio}')`,
                        mundial: year,
                        // jugador: `(SELECT id FROM premio WHERE descripcion = '${premio}')`,
                        jugador_name: "'"+jugadornm+"'",
                        pais: `(SELECT id FROM pais WHERE nombre = '${country}')`,
                    }
                    datosPremios.push(datospremio);
                });
            }
        });
        return datosPremios;
    },
    getPremiosPais(dom, year) {
        const premios = dom.getElementsByClassName('rd-100-45');
        const datosPremios = [];
        premios.forEach((premioDiv, index) => {
            if (index <= 1) {
                return;
            }

            let pais = premioDiv.getElementsByTagName('p')[1].innerHTML.trim();
            if (pais !== '-') {
                paises = premioDiv.getElementsByTagName('a');
                const premio = premioDiv.getElementsByTagName('p')[0].innerHTML.trim();
                paises.forEach(pais => {
                    datospremio = {
                        premio: `(SELECT id FROM premio WHERE descripcion = '${premio}')`,
                        mundial: year,
                        id_pais: `(SELECT id FROM pais WHERE nombre = '${pais.innerHTML}')`,
                    }
                    datosPremios.push(datospremio);
                });
            }
        });
        return datosPremios;
    },
    // END PREMIOS=================================================================================
	escribirConsulta: function(datosIniciales, fileName, tableName) {
		const fieldNames = Object.keys(datosIniciales).join(',');
		const values = Object.values(datosIniciales).join(",");
		var sql = `INSERT INTO ${tableName} (${fieldNames}) values (${values});\n`;
        // console.log(sql);
		const fs = require('fs');
		fs.appendFileSync(fileName, sql);
	}
  };