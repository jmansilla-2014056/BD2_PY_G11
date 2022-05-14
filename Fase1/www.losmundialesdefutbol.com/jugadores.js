var DomParser = require('dom-parser');
module.exports = {
	getJugadores: function () {
		const fs = require('fs');
		let jugadoresRawFile = 'jugadoresRaw.sql';
		fs.readFile(jugadoresRawFile, 'utf8', function (err,data) {
			if (err) {
				return console.log(err);
			}

			fs.writeFile(jugadoresRawFile, '', 'utf8', function (err) {
				if (err) return console.log(err);
			});
		});
		var files = fs.readdirSync(__dirname + '/jugadores');
		// files = [files[0]];
		files.forEach(file => {
			fs.readFile(__dirname + '/jugadores/' + file, 'utf8' , (err, data) => {
				if (err) {
					console.error(err)
					return
				}
				this.getJugador(data, jugadoresRawFile);
			});
		});
	},
    getJugador: function (htmlScript, fileName) {
		var parser = new DomParser();
		var dom = parser.parseFromString(htmlScript);
		var sections = dom.getElementsByClassName('margen-y15');
		var datosIniciales = {
			nombre: '', 
			posicion: '', 
			numero_camiseta: '', 
			altura: '', 
			fecha_nacimiento: '', 
			lugar_nacimiento: '', 
			apodo: '', 
			sitio_oficial: '', 
			twitter: '', 
			mundiales: '', 
			total_partidos: '', 
			campeon: '', 
			goles_anotados: '', 
			promedio_gol: '',
			pais: ''
		}
		datosIniciales.pais = this.getPais(dom.getElementsByClassName('rd-100-30 a-center clearfix pad-t5 margen-b10')[0]);
		datosIniciales = this.getDatosActuales(sections[0], datosIniciales);
		datosIniciales = this.getEstadisticas(sections[1], datosIniciales);
		console.log(datosIniciales);
		this.escribirConsulta(datosIniciales, fileName);
		return datosIniciales;
    },
	getPais: function (dom) {
		let href = dom.getElementsByTagName('a')[0];
		return href.childNodes[2].outerHTML;
	},
    getDatosActuales: function (dom, datosIniciales) {
      	var trs = dom.getElementsByTagName('tr');
		var nombreJugador = dom.getElementsByTagName('h2')[0].innerHTML;
		datosIniciales.nombre = nombreJugador.replaceAll("[^-_/.,\\p{L}0-9 ]+","");
	  	trs.forEach(tr => {
			var tds = tr.getElementsByTagName('td');
			var columnName = tds[0].getElementsByTagName('b')[0].innerHTML;
			switch(columnName) {
				case 'Nombre completo:':
					nombreJugador = tds[1].getElementsByTagName('span')[0].innerHTML.replaceAll("[^-_/.,\\p{L}0-9 ]+","").replaceAll("'", '');
					datosIniciales.nombre = nombreJugador
					break;
				case 'Posici&oacute;n:':
					datosIniciales.posicion = tds[1].innerHTML
					break;
				case 'N&uacute;meros de camiseta:':
					datosIniciales.numero_camiseta = tds[1].innerHTML.trim()
					break;
				case 'Altura:':
					datosIniciales.altura = tds[1].innerHTML
					break;
				case ' Fecha de Nacimiento:':
					datosIniciales.fecha_nacimiento = tds[1].innerHTML
					break;
				case 'Lugar de nacimiento:':
					datosIniciales.lugar_nacimiento = tds[1].innerHTML
					break;
				case 'Apodo:':
					datosIniciales.apodo = tds[1].innerHTML
					break;
				case 'Sitio Web Oficial:':
					datosIniciales.sitio_oficial = tds[1].innerHTML
					break;
				case 'Twitter:':
					datosIniciales.twitter = tds[1].innerHTML
					break;
			}
		});

		return datosIniciales;
    },
	getEstadisticas: function(dom, datosIniciales) {
		var trData = dom.getElementsByTagName('tr')[1];
		var tdData = trData.getElementsByTagName('td');
		datosIniciales.mundiales = tdData[0].innerHTML.trim().split('<br/>')[0];
		datosIniciales.total_partidos = tdData[1].innerHTML.trim().split('<br/>')[0];
		return datosIniciales;
	},
	escribirConsulta: function(datosIniciales, fileName) {
		const fieldNames = Object.keys(datosIniciales).join(',');
		const values = Object.values(datosIniciales).join("','");
		var sql = `INSERT INTO jugador_raw (${fieldNames}) values ('${values}');\n`;

		const fs = require('fs');
		fs.appendFileSync(fileName, sql);
	}
  };