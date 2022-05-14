var DomParser = require('dom-parser');
module.exports = {
	guarderEquipos: function () {
		const fs = require('fs');
		let jugadorEquipoFile = 'jugadorEquipo.sql';
		fs.readFile(jugadorEquipoFile, 'utf8', function (err,data) {
			if (err) {
				return console.log(err);
			}

			fs.writeFile(jugadorEquipoFile, '', 'utf8', function (err) {
				if (err) return console.log(err);
			});
		});
		var files = fs.readdirSync(__dirname + '/planteles');
		// files = [files[0], files[2], files[3]];
		files.forEach((file) => {
			fs.readFile(__dirname + '/planteles/' + file, 'utf8' , (err, data) => {
				if (err) {
					console.error(err)
					return
				}
                let fileNameSplit = file.split('_');
                let year = fileNameSplit[0];
				this.getEquipoInfo(data, jugadorEquipoFile, year);
			});
		});
	},
    getEquipoInfo: function (htmlScript, fileName, year) {
		var parser = new DomParser();
		var dom = parser.parseFromString(htmlScript);
		var pais = this.getPais(dom.getElementsByClassName('main-content')[0]);
		var sections = dom.getElementsByClassName('clearfix bb-2');
		var datosJugadorEquipo = [];
		try {
			if(sections.length > 0) {
				let Arqueros = this.getJugadores(sections[0], pais, year, 1); // Arqueros
				let Defensores = this.getJugadores(sections[1 + Arqueros.length], pais, year, 2); // Defensores
				let Mediocampistas = this.getJugadores(sections[2 + Arqueros.length + Defensores.length], pais, year, 3); // Mediocampistas
				let Delanteros = this.getJugadores(sections[3 + Arqueros.length + Defensores.length + Mediocampistas.length], pais, year, 4); // Delanteros

				// Hasta 1954 fue que los jugadores tuvieron camisetas
				datosJugadorEquipo = Arqueros.concat(Defensores,Mediocampistas,Delanteros)

				// 1950, 1974, 1978, 1982

				console.log(datosJugadorEquipo);
				datosJugadorEquipo.forEach(datosIniciales => {
					this.escribirConsulta(datosIniciales, fileName);
				});
			}
			console.log('mundial ', year, 'pais', pais, ' cargados');
		} catch (error) {
			console.log(year,pais);
			// throw new Error("Something went badly wrong!");
		}
    },
	getPais: function (dom) {
		let href = dom.getElementsByTagName('a')[0];
		return href.childNodes[4].outerHTML;
	},
    getJugadores: function (dom, pais, mundial, posicionId) {
		let condEquipo = '';
		const extraRow = [1950, 1974, 1978, 1982].includes(mundial);
		
		if(extraRow) {
			condEquipo = 'order by grupo limit 1';
		}

		const filas = dom.getElementsByClassName('pad-y5 clearfix bb-2');
		const queryPais = `(select id from pais where nombre = '${pais.trim()}')`;
		const queryEquipo = `(select id from equipo where pais = ${queryPais} and mundial = ${mundial} ${condEquipo})`

		let datosIniciales = [];
		filas.forEach(fila => {
			const camisa = fila.getElementsByClassName('wpx-80 a-center left')[0].innerHTML.trim();
			const domNombreJugador = fila.getElementsByTagName('a')[0];
			const nombreJudador = domNombreJugador.innerHTML.trim()
				.replaceAll("'", '')
				.replaceAll("ć", 'c')
				.replaceAll('ę', 'e')
				.replaceAll('ł', 'l')
				.replaceAll('Ć', 'C')
				.replaceAll('ń', 'n')
				;
			let data = {
				id_jugador: `(select id from jugador where nombre = '${nombreJudador}' and pais = ${queryPais})`,
				id_equipo: queryEquipo,
				id_posicion: posicionId,
				numero_camiseta: camisa,
			};
			datosIniciales.push(data);
			
			if(extraRow) {
				data = {
					id_jugador: `(select id from jugador where nombre = '${nombreJudador}' and pais = ${queryPais})`,
					id_equipo: `(select id from equipo where pais = ${queryPais} and mundial = ${mundial}) order by grupo desc limit 1`,
					id_posicion: posicionId,
					numero_camiseta: camisa,
				};
				datosIniciales.push(data);
			}
		});
		// console.log(datosIniciales);
		return datosIniciales;
    },
	escribirConsulta: function(datosIniciales, fileName) {
		const fieldNames = Object.keys(datosIniciales).join(',');
		const values = Object.values(datosIniciales).join(",");
		var sql = `INSERT INTO jugador_equipo (${fieldNames}) values (${values});\n`;

		const fs = require('fs');
		fs.appendFileSync(fileName, sql);
	}
  };