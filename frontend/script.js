document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('registroForm');
    const messageDiv = document.getElementById('message');
    const personaSelect = document.getElementById('persona_id');
    const materiaSelect = document.getElementById('materia_id');
    const carreraSelect = document.getElementById('carrera_id');

    // Fetch data for dropdowns
    fetchDropdownData('persona', personaSelect, formatPersonaOption);
    fetchDropdownData('materia', materiaSelect, formatMateriaOption);
    fetchDropdownData('carrera', carreraSelect, formatCarreraOption);

    form.addEventListener('submit', function(e) {
        e.preventDefault();
        
        // Validate form
        if (!validateForm()) {
            return;
        }

        // Collect form data
        const formData = {
            calificacion_final: parseFloat(document.getElementById('calificacion_final').value) || null,
            fecha_inicio_cursado: document.getElementById('fecha_inicio_cursado').value,
            fecha_fin_cursado: document.getElementById('fecha_fin_cursado').value || null,
            activo: document.getElementById('activo').checked,
            persona_id: parseInt(personaSelect.value),
            materia_id: parseInt(materiaSelect.value),
            carrera_id: parseInt(carreraSelect.value)
        };

        // Send data to API
        fetch('http://localhost:8080/registro', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(formData),
        })
        .then(response => response.json())
        .then(data => {
            messageDiv.innerHTML = `<div class="alert alert-success">Registro exitoso! ID del registro para su trazabilidad: ${data.id}</div>`;
            form.reset();
        })
        .catch((error) => {
            messageDiv.innerHTML = '<div class="alert alert-danger">Error: ' + error.message + '</div>';
        });
    });

    function validateForm() {
        let isValid = true;
        messageDiv.innerHTML = '';

        // Validate calificacion_final
        const calificacionFinal = parseFloat(document.getElementById('calificacion_final').value);
        if (calificacionFinal && (calificacionFinal <= 0 || calificacionFinal > 10)) {
            messageDiv.innerHTML += '<div class="alert alert-danger">Calificación Final debe ser mayor que 0 y menor o igual que 10.</div>';
            isValid = false;
        }

        // Validate required fields
        ['fecha_inicio_cursado', 'persona_id', 'materia_id', 'carrera_id'].forEach(field => {
            if (!document.getElementById(field).value) {
                messageDiv.innerHTML += '<div class="alert alert-danger">' + field + ' es obligatorio.</div>';
                isValid = false;
            }
        });

        // Validate fecha_fin_cursado is after fecha_inicio_cursado
        const fechaInicio = new Date(document.getElementById('fecha_inicio_cursado').value);
        const fechaFin = new Date(document.getElementById('fecha_fin_cursado').value);
        if (fechaFin && fechaFin < fechaInicio) {
            messageDiv.innerHTML += '<div class="alert alert-danger">Fecha Fin Cursado tiene que ser posterior o igual a Fecha Inicio Cursado.</div>';
            isValid = false;
        }

        return isValid;
    }

    function fetchDropdownData(endpoint, selectElement, formatOption) {
        fetch(`http://localhost:8080/${endpoint}`)
            .then(response => response.json())
            .then(data => {
                data.forEach(item => {
                    const option = document.createElement('option');
                    option.value = item.id;
                    option.textContent = formatOption(item);
                    selectElement.appendChild(option);
                });
            })
            .catch(error => {
                console.error(`Error fetching ${endpoint}:`, error);
                messageDiv.innerHTML += `<div class="alert alert-danger">Error fetching ${endpoint}.</div>`;
            });
    }

    function formatPersonaOption(persona) {
        return `${persona.id} - ${persona.nombre_persona} ${persona.apellido_persona} (DNI: ${persona.numero_dni_persona})`;
    }

    function formatMateriaOption(materia) {
        return `${materia.id} - ${materia.nombre_materia} (Año: ${materia.anio_materia})`;
    }

    function formatCarreraOption(carrera) {
        return `${carrera.id} - ${carrera.nombre_carrera}`;
    }
});