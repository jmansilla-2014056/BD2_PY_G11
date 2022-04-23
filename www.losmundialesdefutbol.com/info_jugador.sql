CREATE DEFINER=`bases2`@`%` PROCEDURE `info_jugador`(nombre varchar(200), jugadorId int)
BEGIN
	DECLARE whereId VARCHAR(255) DEFAULT '';
    DECLARE whereNombre VARCHAR(255) DEFAULT '';
    if jugadorId is not null then
		set whereId = concat(' and j.id = ', jugadorId);
    end if;
    if nombre is not null then
		set whereNombre = concat(' and j.nombre like \'%', nombre,'%\'');
    end if;
    
	# Datos generales    
    set @generalData = 'select 
			j.id,
			j.nombre,
			j.fech_nacimiento_date as fecha_nacimiento,
			ifnull(j.altura, \'desconocida\') as altura,
			ifnull(j.apodo, \'\') as apodo
		 from jugador j
		 join pais p on p.id = j.pais
		 where 1 ';
    set @finalQuery = concat(@generalData, whereId, whereNombre, ';');
    
	PREPARE myquery FROM @finalQuery;
	EXECUTE myquery;
    
    # Datos de premios
    set @premiosData = 'select 
			j.id, 
			j.nombre, 
			pr.descripcion as premio, 
			pmj.mundial
		from premios_mundial_jugador pmj
		join premio pr on pr.id = pmj.premio
		join jugador j on j.id = pmj.jugador
		where 1 ';
	set @finalQuery = concat(@premiosData, whereId, whereNombre, ';');
    
	PREPARE myquery FROM @finalQuery;
	EXECUTE myquery;
    
END