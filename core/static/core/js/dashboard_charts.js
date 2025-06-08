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
                options: { responsive: true, maintainAspectRatio: false, scales: { y: { beginAtZero: true, ticks: { stepSize: 1, precision: 0 } } }, plugins: { legend: { display: false } } }
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
                options: { responsive: true, maintainAspectRatio: false, plugins: { legend: { position: 'top' }, title: { display: false } } }
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
                options: { responsive: true, maintainAspectRatio: false, plugins: { legend: { position: 'top' } } }
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
                options: { indexAxis: 'y', responsive: true, maintainAspectRatio: false, scales: { x: { beginAtZero: true, ticks: { stepSize: 1, precision: 0 } } }, plugins: { legend: { display: false } } }
            });
            renderedCharts[chartId] = true;
        } else {
            console.error("Dados inválidos ou ausentes para " + chartId);
        }
    }

    function renderGraficoTarefasPrioridade() {
        const chartId = 'graficoTarefasPrioridade';
        if (renderedCharts[chartId] || !document.getElementById(chartId)) return;

        const labels = getJsonFromScriptTag('prioridade-labels-data');
        const data = getJsonFromScriptTag('prioridade-data-data');
        if (labels && data && Array.isArray(labels) && Array.isArray(data)) {
            const ctx = document.getElementById(chartId).getContext('2d');
            new Chart(ctx, {
                type: 'pie', // Ou 'bar' se preferir
                data: {
                    labels: labels,
                    datasets: [{
                        label: 'Tarefas Ativas por Prioridade',
                        data: data,
                        backgroundColor: ['rgb(6, 108, 148)', 'rgba(255, 159, 64, 0.7)', 'rgb(255, 145, 0)', 'rgb(173, 10, 10)'],
                        borderColor: ['rgb(6, 108, 148)', 'rgba(255, 159, 64, 1)', 'rgb(255, 145, 0)', 'rgb(173, 10, 10)'],
                        borderWidth: 1
                    }]
                },
                options: { responsive: true, maintainAspectRatio: false, plugins: { legend: { position: 'top' } } }
            });
            renderedCharts[chartId] = true;
        } else {
            console.error("Dados inválidos ou ausentes para " + chartId);
        }
    }

    function renderGraficoBeneficiariosFaixaEtaria() {
        const chartId = 'graficoBeneficiariosFaixaEtaria';
        if (renderedCharts[chartId] || !document.getElementById(chartId)) return;

        const labels = getJsonFromScriptTag('faixa-etaria-labels-data');
        const data = getJsonFromScriptTag('faixa-etaria-data-data');
        if (labels && data && Array.isArray(labels) && Array.isArray(data)) {
            const ctx = document.getElementById(chartId).getContext('2d');
            new Chart(ctx, {
                type: 'bar',
                data: {
                    labels: labels,
                    datasets: [{
                        label: 'Beneficiários por Faixa Etária',
                        data: data,
                        backgroundColor: 'rgba(75, 192, 192, 0.7)',
                        borderColor: 'rgba(75, 192, 192, 1)',
                        borderWidth: 1
                    }]
                },
                options: { responsive: true, maintainAspectRatio: false, scales: { y: { beginAtZero: true, ticks: { stepSize: 1, precision: 0 } } }, plugins: { legend: { display: false } } }
            });
            renderedCharts[chartId] = true;
        } else {
            console.error("Dados inválidos ou ausentes para " + chartId);
        }
    }

    function renderGraficoBeneficiariosCidade() {
        const chartId = 'graficoBeneficiariosCidade';
        if (renderedCharts[chartId] || !document.getElementById(chartId)) return;

        const labels = getJsonFromScriptTag('cidade-labels-data');
        const data = getJsonFromScriptTag('cidade-data-data');
        if (labels && data && Array.isArray(labels) && Array.isArray(data)) {
            const ctx = document.getElementById(chartId).getContext('2d');
            new Chart(ctx, {
                type: 'bar', // Pode ser 'pie' se poucas cidades
                data: {
                    labels: labels,
                    datasets: [{
                        label: 'Top 10 Cidades (Beneficiários)',
                        data: data,
                        backgroundColor: 'rgba(255, 159, 64, 0.7)',
                        borderColor: 'rgba(255, 159, 64, 1)',
                        borderWidth: 1
                    }]
                },
                options: { indexAxis: 'y', responsive: true, maintainAspectRatio: false, scales: { x: { beginAtZero: true, ticks: { stepSize: 1, precision: 0 } } }, plugins: { legend: { display: false } } }
            });
            renderedCharts[chartId] = true;
        } else {
            console.error("Dados inválidos ou ausentes para " + chartId);
        }
    }

    function renderGraficoBeneficiariosRenda() {
        const chartId = 'graficoBeneficiariosRenda';
        if (renderedCharts[chartId] || !document.getElementById(chartId)) return;

        const labels = getJsonFromScriptTag('renda-labels-data');
        const data = getJsonFromScriptTag('renda-data-data');
        if (labels && data && Array.isArray(labels) && Array.isArray(data)) {
            const ctx = document.getElementById(chartId).getContext('2d');
            new Chart(ctx, {
                type: 'pie', // Ou 'bar'
                data: {
                    labels: labels,
                    datasets: [{
                        label: 'Beneficiários por Renda Familiar',
                        data: data,
                        backgroundColor: ['rgba(255, 99, 132, 0.7)', 'rgba(54, 162, 235, 0.7)', 'rgba(255, 206, 86, 0.7)', 'rgba(75, 192, 192, 0.7)', 'rgba(153, 102, 255, 0.7)'],
                        borderWidth: 1
                    }]
                },
                options: { responsive: true, maintainAspectRatio: false, plugins: { legend: { position: 'top' } } }
            });
            renderedCharts[chartId] = true;
        } else {
            console.error("Dados inválidos ou ausentes para " + chartId);
        }
    }

    function renderGraficoCertificadosPorCurso() {
        const chartId = 'graficoCertificadosPorCurso';
        if (renderedCharts[chartId] || !document.getElementById(chartId)) return;

        const labels = getJsonFromScriptTag('curso-cert-labels-data');
        const data = getJsonFromScriptTag('curso-cert-data-data');
        if (labels && data && Array.isArray(labels) && Array.isArray(data)) {
            if (labels.length === 0 && data.length === 0) {
                console.warn(`Gráfico '${chartId}': Não há dados de certificados para exibir para o período selecionado. Labels e Data estão vazios.`);
                // Opcionalmente, limpar o canvas e mostrar uma mensagem
                const canvas = document.getElementById(chartId);
                if (canvas) {
                    const ctx = canvas.getContext('2d');
                    ctx.clearRect(0, 0, canvas.width, canvas.height);
                    // ctx.font = "14px Arial";
                    // ctx.fillStyle = "gray";
                    // ctx.textAlign = "center";
                    // ctx.fillText("Nenhum certificado encontrado para o período.", canvas.width / 2, canvas.height / 2);
                }
                renderedCharts[chartId] = true; // Marcar como "renderizado" para não tentar de novo
                return; // Não prosseguir para renderizar com Chart.js se não há dados
            }

            const ctx = document.getElementById(chartId).getContext('2d');
            new Chart(ctx, {
                type: 'bar',
                data: {
                    labels: labels,
                    datasets: [{
                        label: 'Certificados por Curso',
                        data: data,
                        backgroundColor: 'rgba(54, 162, 235, 0.7)',
                        borderColor: 'rgba(54, 162, 235, 1)',
                        borderWidth: 1
                    }]
                },
                options: { indexAxis: 'y', responsive: true, maintainAspectRatio: false, scales: { x: { beginAtZero: true, ticks: { stepSize: 1, precision: 0 } } }, plugins: { legend: { display: false } } }
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
                renderGraficoTarefasPrioridade();
            } else if (targetPaneId === '#beneficiarios-conteudo') {
                renderGraficoBeneficiariosGenero();
                renderGraficoBeneficiariosEscolaridade();
                renderGraficoBeneficiariosFaixaEtaria();
                renderGraficoBeneficiariosCidade();
                renderGraficoBeneficiariosRenda();
            } else if (targetPaneId === '#cursos-cert-conteudo') {
                renderGraficoCertificadosPorCurso();
            }
            // A aba Voluntários já é renderizada no início
        });
    });
});
