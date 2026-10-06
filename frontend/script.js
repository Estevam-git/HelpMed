// =====================
// MODAL (substitui alert e confirm)
// =====================

function mostrarAlerta(texto) {
    return new Promise((resolve) => {
        document.getElementById('modal-texto').textContent = texto;
        document.getElementById('modal-ok').classList.remove('hidden');
        document.getElementById('modal-cancelar').classList.add('hidden');
        document.getElementById('modal-overlay').classList.remove('hidden');

        document.getElementById('modal-ok').onclick = () => {
            document.getElementById('modal-overlay').classList.add('hidden');
            resolve();
        };
    });
}

function mostrarConfirmacao(texto) {
    return new Promise((resolve) => {
        document.getElementById('modal-texto').textContent = texto;
        document.getElementById('modal-ok').classList.remove('hidden');
        document.getElementById('modal-cancelar').classList.remove('hidden');
        document.getElementById('modal-overlay').classList.remove('hidden');

        document.getElementById('modal-ok').onclick = () => {
            document.getElementById('modal-overlay').classList.add('hidden');
            resolve(true);
        };
        document.getElementById('modal-cancelar').onclick = () => {
            document.getElementById('modal-overlay').classList.add('hidden');
            resolve(false);
        };
    });
}

/* =============================================
   HelpMed — Lógica da Interface
   Conecta os botões com a API Python via PyWebView
   ============================================= */

// Aguarda o PyWebView carregar a API
window.addEventListener('pywebviewready', function () {
    console.log("PyWebView pronto!");
    atualizarBadges();
});

// =====================
// NAVEGAÇÃO DO MENU
// =====================

document.querySelectorAll('.menu-item').forEach(item => {
    item.addEventListener('click', () => {
        // Remove active de todos
        document.querySelectorAll('.menu-item').forEach(i => i.classList.remove('active'));
        document.querySelectorAll('.page').forEach(p => p.classList.remove('active'));

        // Ativa o clicado
        item.classList.add('active');
        const pagina = item.getAttribute('data-page');
        document.getElementById('page-' + pagina).classList.add('active');

        // Atualiza dados da página ao entrar
        if (pagina === 'fila') carregarFila();
        if (pagina === 'atendimento') carregarAtendimento();
        if (pagina === 'historico') carregarHistorico();
    });
});

// =====================
// TRIAGEM
// =====================

// Toggles sim/não
document.querySelectorAll('.toggle-btn').forEach(btn => {
    btn.addEventListener('click', () => {
        const grupo = btn.parentElement;
        grupo.querySelectorAll('.toggle-btn').forEach(b => b.classList.remove('selected'));
        btn.classList.add('selected');
    });
});

// Slider de dor
const sliderDor = document.getElementById('input-dor');
const valorDor = document.getElementById('dor-valor');
sliderDor.addEventListener('input', () => {
    valorDor.textContent = sliderDor.value;
});

// Botão registrar paciente
document.getElementById('btn-registrar').addEventListener('click', async () => {
    const nome = document.getElementById('input-nome').value.trim();
    const sintomas = document.getElementById('input-sintomas').value.trim();

    if (!nome) {
        await mostrarAlerta('Digite o nome do paciente.');
        return;
    }
    if (!sintomas) {
        await mostrarAlerta('Descreva os sintomas.');
        return;
    }

    // Coleta respostas
    const respostas = {
        inconsciente: obterToggle('inconsciente'),
        dificuldade_respirar: obterToggle('dificuldade_respirar'),
        hemorragia: obterToggle('hemorragia'),
        dor_peito: obterToggle('dor_peito'),
        trauma_grave: obterToggle('trauma_grave'),
        temperatura: parseFloat(document.getElementById('input-temperatura').value) || 36.5,
        nivel_dor: parseInt(sliderDor.value) || 0,
    };

    // Chama a API Python
    const resultado = await window.pywebview.api.registrar_paciente(nome, sintomas, respostas);

    // Mostra resultado
    const card = document.getElementById('resultado-card');
    card.className = 'resultado-card resultado-' + resultado.cor;
    document.getElementById('resultado-nome').textContent = '👤 ' + resultado.nome;
    document.getElementById('resultado-protocolo').textContent = '📋 Protocolo: ' + resultado.protocolo;
    document.getElementById('resultado-cor').textContent = '🏷️ ' + resultado.cor + ' — ' + resultado.descricao;
    document.getElementById('resultado-tempo').textContent = '⏱️ Tempo máximo de espera: ' + resultado.tempo_max;
    document.getElementById('resultado-triagem').classList.remove('hidden');

    // Limpa formulário
    document.getElementById('input-nome').value = '';
    document.getElementById('input-sintomas').value = '';
    document.getElementById('input-temperatura').value = '36.5';
    sliderDor.value = 0;
    valorDor.textContent = '0';
    document.querySelectorAll('.toggle-btn[data-valor="false"]').forEach(b => {
        b.parentElement.querySelectorAll('.toggle-btn').forEach(x => x.classList.remove('selected'));
        b.classList.add('selected');
    });

    atualizarBadges();
});

function obterToggle(campo) {
    const selecionado = document.querySelector(`.toggle-btn.selected[data-campo="${campo}"]`);
    return selecionado ? selecionado.getAttribute('data-valor') === 'true' : false;
}

// =====================
// FILA DE ESPERA
// =====================

async function carregarFila() {
    const fila = await window.pywebview.api.ver_fila();
    const container = document.getElementById('lista-fila');

    if (fila.length === 0) {
        container.innerHTML = '<p class="vazio">Nenhum paciente na fila.</p>';
        return;
    }

    container.innerHTML = fila.map(p => `
        <div class="fila-item cor-${p.cor}">
            <div class="fila-posicao">${p.posicao}º</div>
            <div class="fila-dados">
                <h4>${p.nome} <span class="tag tag-${p.cor}">${p.cor}</span></h4>
                <p>${p.protocolo} — ${p.descricao_prioridade} — Espera máx: ${p.tempo_max}</p>
                <p>Sintomas: ${p.sintomas}</p>
                <p>Chegada: ${p.horario}</p>
            </div>
        </div>
    `).join('');
}

// =====================
// ATENDIMENTO
// =====================

document.getElementById('btn-chamar').addEventListener('click', async () => {
    const resultado = await window.pywebview.api.chamar_proximo();

    if (!resultado) {
        await mostrarAlerta('Fila vazia — nenhum paciente para atender.');
        return;
    }

    if (resultado.erro) {
        await mostrarAlerta(resultado.erro);
        return;
    }

    mostrarAtendimento(resultado);
    atualizarBadges();
});

document.getElementById('btn-acao').addEventListener('click', async () => {
    const input = document.getElementById('input-acao');
    const acao = input.value.trim();

    if (!acao) {
        await mostrarAlerta('Digite a ação a ser registrada.');
        return;
    }

    await window.pywebview.api.registrar_acao(acao);
    input.value = '';
    atualizarAcoes();
});

// Enter no campo de ação
document.getElementById('input-acao').addEventListener('keypress', (e) => {
    if (e.key === 'Enter') document.getElementById('btn-acao').click();
});

document.getElementById('btn-undo').addEventListener('click', async () => {
    const desfeita = await window.pywebview.api.desfazer_acao();

    if (!desfeita) {
        await mostrarAlerta('Nenhuma ação para desfazer.');
        return;
    }

    atualizarAcoes();
});

document.getElementById('btn-finalizar').addEventListener('click', async () => {
    if (!(await mostrarConfirmacao('Finalizar este atendimento?'))) return;

    const resultado = await window.pywebview.api.finalizar_atendimento();

    if (resultado) {
        await mostrarAlerta(`Atendimento de ${resultado.nome} finalizado e salvo no histórico.`);
        document.getElementById('sem-paciente').classList.remove('hidden');
        document.getElementById('com-paciente').classList.add('hidden');
        atualizarBadges();
    }
});

async function carregarAtendimento() {
    const paciente = await window.pywebview.api.paciente_em_atendimento();

    if (paciente) {
        mostrarAtendimento(paciente);
    } else {
        document.getElementById('sem-paciente').classList.remove('hidden');
        document.getElementById('com-paciente').classList.add('hidden');
    }
}

function mostrarAtendimento(dados) {
    document.getElementById('sem-paciente').classList.add('hidden');
    document.getElementById('com-paciente').classList.remove('hidden');

    const card = document.getElementById('paciente-atendimento-card');
    card.className = 'paciente-card cor-' + dados.cor;

    document.getElementById('atend-nome').textContent = dados.nome;
    document.getElementById('atend-cor').textContent = dados.cor;
    document.getElementById('atend-cor').className = 'tag tag-' + dados.cor;
    document.getElementById('atend-protocolo').textContent = 'Protocolo: ' + dados.protocolo;
    document.getElementById('atend-sintomas').textContent = 'Sintomas: ' + dados.sintomas;

    atualizarAcoes();
}

async function atualizarAcoes() {
    const acoes = await window.pywebview.api.ver_acoes();
    const lista = document.getElementById('lista-acoes');

    if (acoes.length === 0) {
        lista.innerHTML = '<p class="vazio" style="padding: 12px">Nenhuma ação registrada.</p>';
        return;
    }

    lista.innerHTML = acoes.map((acao, i) => `
        <li>${i + 1}. ${acao}</li>
    `).join('');
}

// =====================
// HISTÓRICO
// =====================

document.getElementById('btn-buscar').addEventListener('click', async () => {
    const termo = document.getElementById('input-busca').value.trim();
    if (!termo) return;

    let resultados;

    // Se parece protocolo (HC-XXXX)
    if (termo.toUpperCase().startsWith('HC-')) {
        const paciente = await window.pywebview.api.buscar_historico_protocolo(termo.toUpperCase());
        resultados = paciente ? [paciente] : [];
    } else {
        resultados = await window.pywebview.api.buscar_historico_nome(termo);
    }

    renderizarHistorico(resultados);
});

// Enter no campo de busca
document.getElementById('input-busca').addEventListener('keypress', (e) => {
    if (e.key === 'Enter') document.getElementById('btn-buscar').click();
});

document.getElementById('btn-ver-todos').addEventListener('click', carregarHistorico);

async function carregarHistorico() {
    const historico = await window.pywebview.api.ver_historico();
    renderizarHistorico(historico);
}

function renderizarHistorico(lista) {
    const container = document.getElementById('lista-historico');

    if (lista.length === 0) {
        container.innerHTML = '<p class="vazio">Nenhum registro encontrado.</p>';
        return;
    }

    container.innerHTML = lista.map(p => `
        <div class="historico-item cor-${p.cor}">
            <h4>${p.nome} <span class="tag tag-${p.cor}">${p.cor}</span></h4>
            <p>${p.protocolo} — ${p.sintomas}</p>
            <p>Atendido às ${p.horario}</p>
            ${p.acoes.length > 0 ? `
                <div class="acoes-hist">
                    ${p.acoes.map(a => `<span>• ${a}</span>`).join('')}
                </div>
            ` : ''}
        </div>
    `).join('');
}

// =====================
// BADGES (contadores)
// =====================

async function atualizarBadges() {
    try {
        const totalFila = await window.pywebview.api.total_fila();
        const totalHist = await window.pywebview.api.total_historico();
        document.getElementById('badge-fila').textContent = totalFila;
        document.getElementById('badge-historico').textContent = totalHist;
    } catch (e) {
        // API ainda não carregou
    }
}