update jugador set  
	dia_nacimiento = substring(fecha_nacimiento, 1, 2),
    mes_nacimiento = substring(fecha_nacimiento, 7, LENGTH(fecha_nacimiento) - 14),
    anio_nacimiento = SUBSTRING(fecha_nacimiento, -5, 4)
where fecha_nacimiento != '' and id > 0;

update ignore jugador set fech_nacimiento_date =  
	concat(anio_nacimiento, '-',
    (case
		when mes_nacimiento = 'enero' then 1
		when mes_nacimiento = 'febrero' then 2
		when mes_nacimiento = 'marzo' then 3
		when mes_nacimiento = 'abril' then 4
		when mes_nacimiento = 'mayo' then 5
		when mes_nacimiento = 'junio' then 6
		when mes_nacimiento = 'julio' then 7
		when mes_nacimiento = 'agosto' then 8
		when mes_nacimiento = 'septiembre' then 9
		when mes_nacimiento = 'octubre' then 10
		when mes_nacimiento = 'noviembre' then 11
		else 12
	end), '-',
        (if (length(dia_nacimiento) = 1, concat('0',dia_nacimiento), dia_nacimiento)))
 where id > 0 and fecha_nacimiento != '';