CREATE PROCEDURE info_pais(country int, sede int, visitante int)
BEGIN
    CASE
        WHEN country IS NOT NULL and sede IS NULL and visitante IS NULL THEN
            SELECT  m.year as mundial, m.sede, if(m.campeon = m.sede, "SI", "NO") AS ES_sede, m.campeon, p.*
            FROM mundial m, pais c, partido p WHERE m.campeon = c.id and c.id = country ;
        WHEN country IS NULL and sede IS NOT NULL and visitante IS NULL THEN
            SELECT  m.year as mundial, m.sede, if(m.campeon = m.sede, "SI", "NO") AS ES_sede, m.campeon, p.*
            FROM mundial m, pais c, partido p WHERE m.sede = c.id and c.id = sede ;
        WHEN country IS NOT NULL and sede IS NULL and visitante IS NOT NULL and visitante = 1 THEN
                SELECT  m.year as mundial, m.sede, if(m.campeon = m.sede, "SI", "NO") AS ES_sede, m.campeon, p.*
                FROM mundial m, pais c, partido p WHERE p.equipo2 = c.id and c.id = country ;
         WHEN country IS NOT NULL and sede IS NULL and visitante IS NOT NULL and visitante = 0 THEN
                    SELECT  m.year as mundial, m.sede, if(m.campeon = m.sede, "SI", "NO") AS ES_sede, m.campeon, p.*
                    FROM mundial m, pais c, partido p WHERE p.equipo1 = c.id and c.id = country ;
    END CASE;
END;