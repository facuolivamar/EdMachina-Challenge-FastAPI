INSERT INTO carreras (nombre_carrera)
VALUES ('Ingeniería en Sistemas');

INSERT INTO personas (nombre_persona, apellido_persona, email_persona, numero_dni_persona, fecha_nacimiento_persona)
VALUES ('Juan', 'Pérez', 'juan.perez@example.com', 12345678, '1980-05-15');

INSERT INTO materias (nombre_materia, anio_materia, carrera_id)
VALUES ('Matemáticas I', 2024, 1); -- asumiendo que el id de la carrera es 1

INSERT INTO registros (calificacion_final, fecha_inicio_cursado, fecha_fin_cursado, activo, materia_id, persona_id)
VALUES (8.5, '2024-03-01', '2024-07-01', true, 1, 1); -- asumiendo que los ids de materia y persona son 1
