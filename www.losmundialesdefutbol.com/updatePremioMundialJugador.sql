update premios_mundial_jugador pm 
join jugador j on trim(j.nombre) = trim(pm.jugador_name)
set pm.jugador = j.id where pm.id > 0;