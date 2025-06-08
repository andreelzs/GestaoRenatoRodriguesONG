document.addEventListener('DOMContentLoaded', function () {
    // Função auxiliar para ler e parsear JSON de tags de script
    const getJsonFromScriptTag = (scriptTagId) => {
        const scriptTag = document.getElementById(scriptTagId);
        if (!scriptTag) {
            console.error(`Elemento script #${scriptTagId} não encontrado.`);
            return null;
        }
        try {
            return JSON.parse(scriptTag.textContent);
        } catch (e) {
            console.error(`Erro durante o parseamento JSON do script tag #${scriptTagId}:`, scriptTag.textContent, e);
            return null;
        }
    };

    // Objeto para rastrear gráficos renderizados
    const renderedCharts = {};

    // Funções de renderização para cada gráfico
    function renderGraficoVoluntariosStatus() {
        const chartId = 'graficoVoluntariosStatus';
        if (renderedCharts[chartId] || !document.getElementById(chartId)) return;

        const labels = getJsonFromScriptTag('voluntario-status-labels-data');
        const data = getJsonFromScriptTag('voluntario-status-data-data');
        if (labels && data && Array.isArray(labels) && Array.isArray(data)) {
            const ctx = document.getElementById(chartId).getContext('2d');
            new Chart(ctx, {
                type: 'bar',
                data: {
                    labels: labels,
                    datasets: [{
                        label: 'Número de Voluntários',
                        data: data,
                        backgroundColor: ['rgba(75, 192, 192, 0.7)', 'rgba(255, 99, 132, 0.7)'],
                        borderColor: ['rgba(75, 192, 192, 1)', 'rgba(255, 99, 132, 1)'],
                        borderWidth: 1
                    }]
                },
                options: { responsive: true, scales: { y: { beginAtZero: true, ticks: { stepSize: 1, precision: 0 } } }, plugins: { legend: { display: false } } }
            });
            renderedCharts[chartId] = true;
        } else {
            console.error("Dados inválidos ou ausentes para " + chartId);
        }
    }

    function renderGraficoDisponibilidadeVoluntarios() {
        const chartId = 'graficoDisponibilidadeVoluntarios';
        if (renderedCharts[chartId] || !document.getElementById(chartId)) return;

        const labels = getJsonFromScriptTag('disp-labels-data');
        const datasetsRaw = getJsonFromScriptTag('disp-datasets-data');
        if (labels && datasetsRaw && Array.isArray(labels) && Array.isArray(datasetsRaw)) {
            const turnosColors = [
                { bg: 'rgba(54, 162, 235, 0.5)', border: 'rgba(54, 162, 235, 1)' },
                { bg: 'rgba(255, 206, 86, 0.5)', border: 'rgba(255, 206, 86, 1)' },
                { bg: 'rgba(255, 99, 132, 0.5)', border: 'rgba(255, 99, 132, 1)' }
            ];
            const finalDatasets = datasetsRaw.map((dataset, index) => ({
                label: dataset.label,
                data: dataset.data,
                backgroundColor: turnosColors[index % turnosColors.length].bg,
                borderColor: turnosColors[index % turnosColors.length].border,
                borderWidth: 1
            }));
            const ctx = document.getElementById(chartId).getContext('2d');
            new Chart(ctx, {
                type: 'bar',
                data: { labels: labels, datasets: finalDatasets },
                options: { responsive: true, maintainAspectRatio: false, scales: { y: { beginAtZero: true, ticks: { stepSize: 1, precision: 0 } } }, plugins: { legend: { position: 'top' }, title: { display: true, text: 'Contagem de Voluntários Disponíveis por Dia e Turno' } } }
            });
            renderedCharts[chartId] = true;
        } else {
            console.error("Dados inválidos ou ausentes para " + chartId);
        }
    }

    function renderGraficoTarefasStatus() {
        const chartId = 'graficoTarefasStatus';
        if (renderedCharts[chartId] || !document.getElementById(chartId)) return;

        const labels = getJsonFromScriptTag('status-labels-data');
        const data = getJsonFromScriptTag('status-data-data');
        if (labels && data && Array.isArray(labels) && Array.isArray(data)) {
            const ctx = document.getElementById(chartId).getContext('2d');
            new Chart(ctx, {
                type: 'pie',
                data: {
                    labels: labels,
                    datasets: [{
                        label: 'Tarefas por Status',
                        data: data,
                        backgroundColor: ['rgba(255, 159, 64, 0.7)', 'rgba(54, 162, 235, 0.7)', 'rgba(75, 192, 192, 0.7)', 'rgba(153, 102, 255, 0.7)', 'rgba(255, 99, 132, 0.7)'],
                        borderColor: ['rgba(255, 159, 64, 1)', 'rgba(54, 162, 235, 1)', 'rgba(75, 192, 192, 1)', 'rgba(153, 102, 255, 1)', 'rgba(255, 99, 132, 1)'],
                        borderWidth: 1
                    }]
                },
                options: { responsive: true, plugins: { legend: { position: 'top' }, title: { display: false } } }
            });
            renderedCharts[chartId] = true;
        } else {
            console.error("Dados inválidos ou ausentes para " + chartId);
        }
    }

    function renderGraficoBeneficiariosGenero() {
        const chartId = 'graficoBeneficiariosGenero';
        if (renderedCharts[chartId] || !document.getElementById(chartId)) return;

        const labels = getJsonFromScriptTag('genero-labels-data');
        const data = getJsonFromScriptTag('genero-data-data');
        if (labels && data && Array.isArray(labels) && Array.isArray(data)) {
            const ctx = document.getElementById(chartId).getContext('2d');
            new Chart(ctx, {
                type: 'pie',
                data: {
                    labels: labels,
                    datasets: [{
                        label: 'Beneficiários por Gênero',
                        data: data,
                        backgroundColor: ['rgba(54, 162, 235, 0.7)', 'rgba(255, 99, 132, 0.7)', 'rgba(255, 206, 86, 0.7)', 'rgba(75, 192, 192, 0.7)', 'rgba(153, 102, 255, 0.7)'],
                        borderWidth: 1
                    }]
                },
                options: { responsive: true, plugins: { legend: { position: 'top' } } }
            });
            renderedCharts[chartId] = true;
        } else {
            console.error("Dados inválidos ou ausentes para " + chartId);
        }
    }

    function renderGraficoBeneficiariosEscolaridade() {
        const chartId = 'graficoBeneficiariosEscolaridade';
        if (renderedCharts[chartId] || !document.getElementById(chartId)) return;

        const labels = getJsonFromScriptTag('escolaridade-labels-data');
        const data = getJsonFromScriptTag('escolaridade-data-data');
        if (labels && data && Array.isArray(labels) && Array.isArray(data)) {
            const ctx = document.getElementById(chartId).getContext('2d');
            new Chart(ctx, {
                type: 'bar',
                data: {
                    labels: labels,
                    datasets: [{
                        label: 'Beneficiários por Escolaridade',
                        data: data,
                        backgroundColor: 'rgba(153, 102, 255, 0.7)',
                        borderColor: 'rgba(153, 102, 255, 1)',
                        borderWidth: 1
                    }]
                },
                options: { indexAxis: 'y', responsive: true, scales: { x: { beginAtZero: true, ticks: { stepSize: 1, precision: 0 } } }, plugins: { legend: { display: false } } }
            });
            renderedCharts[chartId] = true;
        } else {
            console.error("Dados inválidos ou ausentes para " + chartId);
        }
    }

    // Renderizar gráficos da aba ativa inicial (Voluntários)
    renderGraficoVoluntariosStatus();
    renderGraficoDisponibilidadeVoluntarios();

    // Lidar com a troca de abas para renderizar outros gráficos
    const tabElements = document.querySelectorAll('#dashboardAbas .nav-link');
    tabElements.forEach(tabEl => {
        tabEl.addEventListener('shown.bs.tab', function (event) {
            const targetPaneId = event.target.getAttribute('data-bs-target');
            if (targetPaneId === '#tarefas-conteudo') {
                renderGraficoTarefasStatus();
            } else if (targetPaneId === '#beneficiarios-conteudo') {
                renderGraficoBeneficiariosGenero();
                renderGraficoBeneficiariosEscolaridade();
            }
            // A aba Voluntários já é renderizada no início
        });
    });
});
