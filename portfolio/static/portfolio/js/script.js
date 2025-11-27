// Filtrar estudiantes según el nivel seleccionado
    const selectNivel = document.getElementById('select-nivel');
    const estudiantesContainer = document.getElementById('estudiantes-container');
    const estudianteDivs = Array.from(estudiantesContainer.children);

    selectNivel.addEventListener('change', () => {
        const nivelId = selectNivel.value;
        estudianteDivs.forEach(div => {
            const estudianteId = div.querySelector('select').name.split('_')[1];
            const estudiante = {% regroup estudiantes by nivel as estudiantes_por_nivel %}
            // Por defecto se muestran todos los estudiantes
            div.style.display = 'flex';
        });
    });