document.addEventListener('DOMContentLoaded', function () {
    // Função auxiliar para ler e parsear JSON de tags de script
    const getJsonFromScriptTag = (scriptTagId) => {
        const scriptTag = document.getElementById(scriptTagId);
        if (!scriptTag) {
            console.error(`Elemento script #${scriptTagId} não encontrado.`);
            return null;
        }
        const rawText = scriptTag.textContent;
        console.log(`Conteúdo bruto do script tag #${scriptTagId}:`, rawText);
        try {
            let parsedData = JSON.parse(rawText);
            console.log(`Dados após 1º parse de #${scriptTagId}:`, parsedData, `É array? ${Array.isArray(parsedData)}`, `É string? ${typeof parsedData === 'string'}`);
            
            if (typeof parsedData === 'string') {
                console.log(`Tentando 2º parse para #${scriptTagId} pois o 1º resultou em string.`);
                parsedData = JSON.parse(parsedData); // Tenta o segundo parse
                console.log(`Dados após 2º parse de #${scriptTagId}:`, parsedData, `É array? ${Array.isArray(parsedData)}`);
            }
            
            // Log final do estado dos dados antes de retornar
            console.log(`Dados finais (antes de retornar) de #${scriptTagId}:`, parsedData, Array.isArray(parsedData) ? "É um array" : "NÃO é um array");
            return parsedData;
        } catch (e) {
            console.error(`Erro durante o parseamento JSON do script tag #${scriptTagId}:`, rawText, e);
            return null;
        }
    };

    // Gráfico de Tarefas por Status (Pizza)
    if (document.getElementById('graficoTarefasStatus')) {
        const statusLabels = getJsonFromScriptTag('status-labels-data');
        const statusData = getJsonFromScriptTag('status-data-data');
        
        console.log("Para graficoTarefasStatus - statusLabels:", statusLabels, "É array?", Array.isArray(statusLabels));
        console.log("Para graficoTarefasStatus - statusData:", statusData, "É array?", Array.isArray(statusData));

        if (statusLabels && statusData && Array.isArray(statusLabels) && Array.isArray(statusData)) {
            const ctxTarefasStatus = document.getElementById('graficoTarefasStatus').getContext('2d');
            new Chart(ctxTarefasStatus, {
                type: 'pie',
                data: {
                    labels: statusLabels,
                    datasets: [{
                        label: 'Tarefas por Status',
                        data: statusData,
                        backgroundColor: ['rgba(255, 159, 64, 0.7)', 'rgba(54, 162, 235, 0.7)', 'rgba(75, 192, 192, 0.7)', 'rgba(153, 102, 255, 0.7)', 'rgba(255, 99, 132, 0.7)'],
                        borderColor: ['rgba(255, 159, 64, 1)', 'rgba(54, 162, 235, 1)', 'rgba(75, 192, 192, 1)', 'rgba(153, 102, 255, 1)', 'rgba(255, 99, 132, 1)'],
                        borderWidth: 1
                    }]
                },
                options: { responsive: true, plugins: { legend: { position: 'top' }, title: { display: false } } }
            });
        } else {
            console.error("Dados inválidos ou ausentes para graficoTarefasStatus. Labels é array:", Array.isArray(statusLabels), "Data é array:", Array.isArray(statusData));
        }
    }

    // Gráfico de Status dos Voluntários (Barra)
    if (document.getElementById('graficoVoluntariosStatus')) {
        const voluntarioStatusLabels = getJsonFromScriptTag('voluntario-status-labels-data');
        const voluntarioStatusData = getJsonFromScriptTag('voluntario-status-data-data');

        console.log("Para graficoVoluntariosStatus - voluntarioStatusLabels:", voluntarioStatusLabels, "É array?", Array.isArray(voluntarioStatusLabels));
        console.log("Para graficoVoluntariosStatus - voluntarioStatusData:", voluntarioStatusData, "É array?", Array.isArray(voluntarioStatusData));
        
        if (voluntarioStatusLabels && voluntarioStatusData && Array.isArray(voluntarioStatusLabels) && Array.isArray(voluntarioStatusData)) {
            const ctxVoluntariosStatus = document.getElementById('graficoVoluntariosStatus').getContext('2d');
            new Chart(ctxVoluntariosStatus, {
                type: 'bar',
                data: {
                    labels: voluntarioStatusLabels,
                    datasets: [{
                        label: 'Número de Voluntários',
                        data: voluntarioStatusData,
                        backgroundColor: ['rgba(75, 192, 192, 0.7)', 'rgba(255, 99, 132, 0.7)'],
                        borderColor: ['rgba(75, 192, 192, 1)', 'rgba(255, 99, 132, 1)'],
                        borderWidth: 1
                    }]
                },
                options: { responsive: true, scales: { y: { beginAtZero: true, ticks: { stepSize: 1, precision: 0 } } }, plugins: { legend: { display: false } } }
            });
        } else {
            console.error("Dados inválidos ou ausentes para graficoVoluntariosStatus. Labels é array:", Array.isArray(voluntarioStatusLabels), "Data é array:", Array.isArray(voluntarioStatusData));
        }
    }

    // Gráfico de Beneficiários por Gênero (Pizza)
    if (document.getElementById('graficoBeneficiariosGenero')) {
        const generoLabels = getJsonFromScriptTag('genero-labels-data');
        const generoData = getJsonFromScriptTag('genero-data-data');

        console.log("Para graficoBeneficiariosGenero - generoLabels:", generoLabels, "É array?", Array.isArray(generoLabels));
        console.log("Para graficoBeneficiariosGenero - generoData:", generoData, "É array?", Array.isArray(generoData));

        if (generoLabels && generoData && Array.isArray(generoLabels) && Array.isArray(generoData)) {
            const ctxBeneficiariosGenero = document.getElementById('graficoBeneficiariosGenero').getContext('2d');
            new Chart(ctxBeneficiariosGenero, {
                type: 'pie',
                data: {
                    labels: generoLabels,
                    datasets: [{
                        label: 'Beneficiários por Gênero',
                        data: generoData,
                        backgroundColor: ['rgba(54, 162, 235, 0.7)', 'rgba(255, 99, 132, 0.7)', 'rgba(255, 206, 86, 0.7)', 'rgba(75, 192, 192, 0.7)', 'rgba(153, 102, 255, 0.7)'],
                        borderWidth: 1
                    }]
                },
                options: { responsive: true, plugins: { legend: { position: 'top' } } }
            });
        } else {
            console.error("Dados inválidos ou ausentes para graficoBeneficiariosGenero. Labels é array:", Array.isArray(generoLabels), "Data é array:", Array.isArray(generoData));
        }
    }
    
    // Gráfico de Beneficiários por Escolaridade (Barra)
    if (document.getElementById('graficoBeneficiariosEscolaridade')) {
        const escolaridadeLabels = getJsonFromScriptTag('escolaridade-labels-data');
        const escolaridadeData = getJsonFromScriptTag('escolaridade-data-data');

        console.log("Para graficoBeneficiariosEscolaridade - escolaridadeLabels:", escolaridadeLabels, "É array?", Array.isArray(escolaridadeLabels));
        console.log("Para graficoBeneficiariosEscolaridade - escolaridadeData:", escolaridadeData, "É array?", Array.isArray(escolaridadeData));

        if (escolaridadeLabels && escolaridadeData && Array.isArray(escolaridadeLabels) && Array.isArray(escolaridadeData)) {
            const ctxBeneficiariosEscolaridade = document.getElementById('graficoBeneficiariosEscolaridade').getContext('2d');
            new Chart(ctxBeneficiariosEscolaridade, {
                type: 'bar',
                data: {
                    labels: escolaridadeLabels,
                    datasets: [{
                        label: 'Beneficiários por Escolaridade',
                        data: escolaridadeData,
                        backgroundColor: 'rgba(153, 102, 255, 0.7)',
                        borderColor: 'rgba(153, 102, 255, 1)',
                        borderWidth: 1
                    }]
                },
                options: { indexAxis: 'y', responsive: true, scales: { x: { beginAtZero: true, ticks: { stepSize: 1, precision: 0 } } }, plugins: { legend: { display: false } } }
            });
        } else {
            console.error("Dados inválidos ou ausentes para graficoBeneficiariosEscolaridade. Labels é array:", Array.isArray(escolaridadeLabels), "Data é array:", Array.isArray(escolaridadeData));
        }
    }

    // Gráfico de Disponibilidade de Voluntários (Barras Agrupadas)
    if (document.getElementById('graficoDisponibilidadeVoluntarios')) {
        const dispLabels = getJsonFromScriptTag('disp-labels-data');
        const dispDatasetsRaw = getJsonFromScriptTag('disp-datasets-data');

        console.log("Para graficoDisponibilidadeVoluntarios - dispLabels:", dispLabels, "É array?", Array.isArray(dispLabels));
        console.log("Para graficoDisponibilidadeVoluntarios - dispDatasetsRaw:", dispDatasetsRaw, "É array?", Array.isArray(dispDatasetsRaw));
        
        if (dispLabels && dispDatasetsRaw && Array.isArray(dispLabels) && Array.isArray(dispDatasetsRaw)) {
            const turnosColors = [
                { bg: 'rgba(54, 162, 235, 0.5)', border: 'rgba(54, 162, 235, 1)' }, // Manhã (Azul)
                { bg: 'rgba(255, 206, 86, 0.5)', border: 'rgba(255, 206, 86, 1)' }, // Tarde (Amarelo)
                { bg: 'rgba(255, 99, 132, 0.5)', border: 'rgba(255, 99, 132, 1)' }    // Noite (Vermelho)
            ];

            const finalDispDatasets = dispDatasetsRaw.map((dataset, index) => {
                return {
                    label: dataset.label,
                    data: dataset.data,
                    backgroundColor: turnosColors[index % turnosColors.length].bg,
                    borderColor: turnosColors[index % turnosColors.length].border,
                    borderWidth: 1
                };
            });

            console.log("Para graficoDisponibilidadeVoluntarios - finalDispDatasets:", finalDispDatasets);

            const ctxDisponibilidadeVoluntarios = document.getElementById('graficoDisponibilidadeVoluntarios').getContext('2d');
            new Chart(ctxDisponibilidadeVoluntarios, {
                type: 'bar',
                data: {
                    labels: dispLabels,
                    datasets: finalDispDatasets
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false, // Adicionado para melhor ajuste em telas pequenas
                    scales: { y: { beginAtZero: true, ticks: { stepSize: 1, precision: 0 } } },
                    plugins: { legend: { position: 'top' }, title: { display: true, text: 'Contagem de Voluntários Disponíveis por Dia e Turno' } }
                }
            });
        } else {
            console.error("Dados inválidos ou ausentes para graficoDisponibilidadeVoluntarios. Labels é array:", Array.isArray(dispLabels), "Data é array:", Array.isArray(dispDatasetsRaw));
        }
    }
});
