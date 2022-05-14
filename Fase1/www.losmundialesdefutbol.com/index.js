var express = require('express');
var app = express();
const path = require('path');
const router = express.Router();

const equipos = require('./equipos');
const jugadores = require('./jugadores');
const mundiales = require('./mundiales');
const paises = require('./paises');

router.get('/',function(req,res){
    // jugadores.getJugadores();
    // paises.guardarPaises();
    // mundiales.guardarMundiales();
    // mundiales.guardarMundiales('premios');
    // equipos.guarderEquipos();
    res.sendFile(path.join(__dirname+'/testing.html'));
});

app.use('/', router);
app.listen(3000, function () {
    console.log('Example app listening on port 3000!');
    console.log('que;s');
});