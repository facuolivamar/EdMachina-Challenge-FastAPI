INSERT INTO carreras (nombre_carrera)
VALUES ('Ingeniería en Sistemas'),
       ('Licenciatura en Matemáticas'),
       ('Arquitectura'),
       ('Medicina'),
       ('Licenciatura en Física');

INSERT INTO personas (nombre_persona, apellido_persona, email_persona, numero_dni_persona, fecha_nacimiento_persona, direccion_persona, telefono_persona, anio_inscripcion_persona)
VALUES ('Juan', 'Pérez', 'juan.perez@example.com', 12345678, '1980-05-15', 'Calle Falsa 123', 112233, 2022),
       ('Ana', 'Gómez', 'ana.gomez@example.com', 87654321, '1992-07-20', 'Avenida Siempre Viva 742', 2233445, 2023),
       ('Carlos', 'Lopez', 'carlos.lopez@example.com', 23456789, '1985-09-10', 'Calle Primera 45', 3344556, 2021),
       ('María', 'Martinez', 'maria.martinez@example.com', 98765432, '1990-11-30', 'Boulevard Central 678', 44556, 2024),
       ('Laura', 'Fernandez', 'laura.fernandez@example.com', 13579246, '1988-03-05', 'Calle Secundaria 89', 55667, 2020);

INSERT INTO materias (nombre_materia, anio_materia)
VALUES ('Matemáticas I', 2024),
       ('Álgebra Lineal', 2024),
       ('Anatomía Humana', 2024),
       ('Física I', 2024),
       ('Diseño Arquitectónico', 2024);

INSERT INTO registros (calificacion_final, fecha_inicio_cursado, fecha_fin_cursado, activo, materia_id, persona_id, carrera_id)
VALUES (8.5, '2024-03-01', '2024-07-01', true, 1, 1, 1),  -- Juan Pérez, Ingeniería en Sistemas, Matemáticas I
       (9.0, '2024-03-15', '2024-07-10', true, 2, 2, 1),  -- Ana Gómez, Ingeniería en Sistemas, Álgebra Lineal
       (7.5, '2024-04-01', '2024-07-30', true, 3, 3, 4),  -- Carlos Lopez, Medicina, Anatomía Humana
       (8.0, '2024-05-01', '2024-08-01', true, 4, 4, 5),  -- María Martinez, Licenciatura en Física, Física I
       (9.5, '2024-02-01', '2024-06-01', true, 5, 5, 3);  -- Laura Fernandez, Arquitectura, Diseño Arquitectónico
