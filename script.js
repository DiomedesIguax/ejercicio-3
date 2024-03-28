function generarGraficas() {
    var fileInput = document.getElementById('fileInput');
    var file = fileInput.files[0];
    var formData = new FormData();
    formData.append('archivo', file);

    // Envía la solicitud POST al servidor
    fetch('/guardar_csv', {
        method: 'POST',
        headers: {
            'Accept': 'application/json',
        },
        body: formData
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Error en la solicitud: ' + response.statusText);
        }
        return response.json();
    })
    .then(data => {
        // Muestra las gráficas
        mostrarGraficas(data.prediccion_knn, data.prediccion_mlp);
    })
    .catch(error => console.error('Error:', error));
}

function mostrarGraficas(prediccion_knn, prediccion_mlp) {
    // Crea los datos para las gráficas
    var datos_knn = {
        x: prediccion_knn,
        type: 'histogram',
        name: 'Predicciones KNN'
    };

    var datos_mlp = {
        x: prediccion_mlp,
        type: 'histogram',
        name: 'Predicciones MLP'
    };

    var layout = {
        title: 'Clasificaciones Finales',
        xaxis: { title: 'Quality' },
        yaxis: { title: 'Cantidad' }
    };

    // Crea la gráfica
    var graficas = [datos_knn, datos_mlp];
    Plotly.newPlot('graficas', graficas, layout);
}
