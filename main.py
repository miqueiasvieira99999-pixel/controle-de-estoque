import html
import unicodedata

import pandas as pd
import streamlit as st


st.set_page_config(
    page_title="Controle de Materiais",
    page_icon="📦",
    layout="wide",
    initial_sidebar_state="expanded",
)


LOGIN = "Logistica"
SENHA = "Mi912519."
SHAREPOINT_URL = "https://nansencombr.sharepoint.com/:x:/s/ProjetoCPFL/IQAUybIIgpghS4-zkyqy6Y41AV6EVfO9aYghYFUmOCJYsQg?e=juuLU5"


if "logado" not in st.session_state:
    st.session_state.logado = False


def normalizar_texto(valor):
    texto = str(valor).strip().lower()
    texto = unicodedata.normalize("NFKD", texto)
    return "".join(ch for ch in texto if not unicodedata.combining(ch))


def escapar(valor):
    if pd.isna(valor):
        return ""
    return html.escape(str(valor))


def primeira_coluna(df, opcoes):
    colunas = {normalizar_texto(col): col for col in df.columns}
    for opcao in opcoes:
        normalizada = normalizar_texto(opcao)
        if normalizada in colunas:
            return colunas[normalizada]
    return None


def preparar_dados(df):
    mapa = {
        "data": ["data", "dt", "data movimento", "data movimentacao"],
        "semana": ["semana"],
        "carro": ["carro", "veiculo", "placa"],
        "equipe": ["equipe", "colaborador", "tecnico", "responsavel"],
        "codigo": ["codigo", "cod", "codigo material", "cod material", "item"],
        "descricao": ["descricao", "descrição", "material", "produto", "item descricao"],
        "tipo": ["tipo", "movimento", "movimentacao", "entrada saida"],
        "quantidade": ["quantidade", "qtd", "qtde", "saida", "saidas", "entrada", "entradas"],
        "observacao": ["observacao", "observação", "obs"],
    }

    dados = pd.DataFrame()
    for nome, opcoes in mapa.items():
        coluna = primeira_coluna(df, opcoes)
        dados[nome] = df[coluna] if coluna else ""

    dados["quantidade"] = pd.to_numeric(dados["quantidade"], errors="coerce").fillna(0)
    dados["tipo_normalizado"] = dados["tipo"].map(normalizar_texto)
    dados["data"] = pd.to_datetime(dados["data"], errors="coerce", dayfirst=True)
    return dados


def ler_excel_origem(origem):
    return pd.read_excel(origem)


def dados_exemplo():
    return preparar_dados(
        pd.DataFrame(
            [
                ["10/06/2026", "1ª semana de Junho", "DBI - COPEL", "Paulo - Weslei", 38006, "KIT SUPORTE+ANTENA+CABO 3,5M EXTERNA 3 DBI", "SAIDA", 16, "-"],
                ["10/06/2026", "1ª semana de Junho", "DBI - COPEL", "Paulo - Weslei", 38007, "KIT SUPORTE+ANTENA+CABO 5 METROS EXTERNA 3 DBI", "SAIDA", 11, "-"],
                ["10/06/2026", "1ª semana de Junho", "FUSIMEC", "Paulo - Weslei", 42066, "FITA DE ACO - LISA 1/2 FUSIMEC COPEL", "SAIDA", 25, "-"],
                ["10/06/2026", "1ª semana de Junho", "TRI - COPEL", "Osseni - Gabriel", 42121, "LACRE NUMSEN - COPEL", "SAIDA", 100, "-"],
                ["10/06/2026", "1ª semana de Junho", "MR - COPEL", "Osseni - Gabriel", 38002, "NIC CASE MR - COPEL", "SAIDA", 1, "-"],
                ["10/06/2026", "1ª semana de Junho", "MR - COPEL", "Almoxarifado", 38002, "NIC CASE MR - COPEL", "ENTRADA", 1500, "-"],
                ["10/06/2026", "1ª semana de Junho", "TRI - COPEL", "Almoxarifado", 38003, "NIC CASE TRI - COPEL", "ENTRADA", 650, "-"],
            ],
            columns=["Data", "Semana", "Carro", "Equipe", "Código", "Descrição", "Tipo", "Quantidade", "Observação"],
        )
    )


def obter_metricas(dados):
    entradas = dados.loc[dados["tipo_normalizado"].str.contains("entrada", na=False), "quantidade"].sum()
    saidas = dados.loc[dados["tipo_normalizado"].str.contains("saida", na=False), "quantidade"].sum()

    if entradas == 0 and saidas == 0:
        entradas = dados["quantidade"].sum()

    return {
        "entradas": int(entradas),
        "saidas": int(saidas),
        "saldo": int(entradas - saidas),
        "equipes": int(dados["equipe"].replace("", pd.NA).dropna().nunique()),
        "carros": int(dados["carro"].replace("", pd.NA).dropna().nunique()),
        "movimentacoes": int(len(dados)),
        "materiais": int(dados["codigo"].replace("", pd.NA).dropna().nunique()),
    }


def formatar_numero(valor):
    return f"{int(valor):,}".replace(",", ".")


def obter_dados_dashboard():
    dados = st.session_state.get("dados_planilha")
    if dados is not None:
        return dados, st.session_state.get("fonte_dados", "Planilha carregada")
    return dados_exemplo(), "Dados demonstrativos"


def aplicar_css():
    st.markdown(
        """
        <style>
            :root {
                --bg: #061426;
                --panel: #08233b;
                --panel-2: #092a47;
                --border: rgba(77, 170, 255, .24);
                --text: #eaf5ff;
                --muted: #9db6c9;
                --blue: #1e9bff;
                --green: #22c486;
                --orange: #ff9d28;
                --purple: #a866ff;
                --red: #ff4b4b;
            }

            .stApp {
                background:
                    radial-gradient(circle at top left, rgba(0, 141, 255, .18), transparent 30%),
                    linear-gradient(135deg, #04101f 0%, #061426 48%, #04101f 100%);
                color: var(--text);
            }

            [data-testid="stHeader"] {
                background: transparent;
            }

            [data-testid="stSidebar"] {
                background: linear-gradient(180deg, #061a2d 0%, #03111f 100%);
                border-right: 1px solid var(--border);
            }

            [data-testid="stSidebar"] * {
                color: var(--text);
            }

            [data-testid="stSidebar"] [role="radiogroup"] label {
                border-radius: 8px;
                padding: 6px 8px;
                margin-bottom: 4px;
            }

            [data-testid="stSidebar"] [role="radiogroup"] label:hover {
                background: rgba(30, 155, 255, .14);
            }

            .block-container {
                padding-top: 1rem;
                padding-bottom: 1rem;
                max-width: 1600px;
            }

            div[data-testid="stMetric"] {
                background: transparent;
            }

            .topbar {
                display: flex;
                align-items: center;
                justify-content: space-between;
                gap: 18px;
                padding: 10px 0 18px;
                border-bottom: 1px solid var(--border);
                margin-bottom: 14px;
            }

            .topbar-left, .topbar-right {
                display: flex;
                align-items: center;
                gap: 16px;
            }

            .hamburger {
                font-size: 28px;
                color: var(--text);
            }

            .page-title {
                font-size: 20px;
                font-weight: 800;
            }

            .top-meta, .periodo, .user-chip {
                color: #c8d9ea;
                font-size: 13px;
            }

            .periodo, .user-chip {
                border: 1px solid var(--border);
                background: rgba(8, 35, 59, .75);
                border-radius: 6px;
                padding: 10px 14px;
            }

            .kpi-grid {
                display: grid;
                grid-template-columns: repeat(4, minmax(180px, 1fr));
                gap: 14px;
                margin-bottom: 14px;
            }

            .kpi {
                position: relative;
                min-height: 118px;
                border: 1px solid var(--border);
                border-radius: 10px;
                padding: 20px 22px;
                overflow: hidden;
                box-shadow: 0 18px 45px rgba(0, 0, 0, .18);
            }

            .kpi.blue { background: linear-gradient(135deg, rgba(0, 104, 190, .60), rgba(4, 23, 45, .80)); }
            .kpi.green { background: linear-gradient(135deg, rgba(0, 137, 89, .56), rgba(4, 23, 45, .82)); }
            .kpi.purple { background: linear-gradient(135deg, rgba(100, 43, 170, .62), rgba(4, 23, 45, .82)); }
            .kpi.orange { background: linear-gradient(135deg, rgba(160, 86, 16, .70), rgba(4, 23, 45, .82)); }

            .kpi-label {
                color: #8fcaff;
                font-size: 13px;
                font-weight: 800;
                letter-spacing: .02em;
                text-transform: uppercase;
            }

            .kpi.green .kpi-label { color: #6ff0ad; }
            .kpi.purple .kpi-label { color: #cba7ff; }
            .kpi.orange .kpi-label { color: #ffbf5a; }

            .kpi-value {
                margin-top: 10px;
                font-size: 34px;
                line-height: 1;
                font-weight: 900;
            }

            .kpi-caption {
                margin-top: 10px;
                color: #d3e0eb;
                font-size: 13px;
            }

            .kpi-icon {
                position: absolute;
                right: 24px;
                top: 32px;
                width: 58px;
                height: 58px;
                display: grid;
                place-items: center;
                border-radius: 50%;
                background: rgba(30, 155, 255, .22);
                font-size: 28px;
            }

            .panel-grid {
                display: grid;
                grid-template-columns: 1.35fr 1.1fr 1fr;
                gap: 12px;
                margin-bottom: 12px;
            }

            .bottom-grid {
                display: grid;
                grid-template-columns: 1.25fr 1fr .65fr;
                gap: 12px;
                margin-bottom: 12px;
            }

            .panel {
                border: 1px solid var(--border);
                border-radius: 10px;
                background: linear-gradient(180deg, rgba(8, 42, 71, .88), rgba(5, 25, 43, .88));
                box-shadow: inset 0 1px 0 rgba(255, 255, 255, .04), 0 18px 45px rgba(0, 0, 0, .12);
                padding: 16px;
                min-height: 250px;
            }

            .panel-title {
                color: #56b7ff;
                font-size: 14px;
                font-weight: 900;
                text-transform: uppercase;
                margin-bottom: 12px;
            }

            .chart-lines {
                height: 190px;
                position: relative;
                border-left: 1px solid rgba(255,255,255,.12);
                border-bottom: 1px solid rgba(255,255,255,.12);
                background:
                    repeating-linear-gradient(to top, rgba(255,255,255,.10) 0 1px, transparent 1px 38px);
                margin: 8px 0 0 30px;
            }

            .bar {
                position: absolute;
                bottom: 0;
                width: 18px;
                border-radius: 3px 3px 0 0;
            }

            .bar.in { background: linear-gradient(#2db0ff, #116fc8); }
            .bar.out { background: linear-gradient(#31d69b, #16865f); }
            .line-dot {
                position: absolute;
                width: 8px;
                height: 8px;
                border-radius: 50%;
                background: #ffc21a;
                box-shadow: 0 0 0 3px rgba(255,194,26,.18);
            }

            .legend {
                display: flex;
                justify-content: center;
                gap: 24px;
                color: #c7d8e8;
                font-size: 12px;
            }

            .legend span::before {
                content: "";
                display: inline-block;
                width: 14px;
                height: 8px;
                margin-right: 6px;
                border-radius: 2px;
            }

            .legend .entradas::before { background: #1e9bff; }
            .legend .saidas::before { background: #22c486; }
            .legend .saldo::before { background: #ffc21a; height: 4px; }

            .hbar-row {
                display: grid;
                grid-template-columns: 120px 1fr 52px;
                align-items: center;
                gap: 10px;
                margin: 11px 0;
                font-size: 12px;
                color: #d9e7f4;
            }

            .hbar-track {
                height: 22px;
                border-radius: 4px;
                background: rgba(255,255,255,.08);
                overflow: hidden;
            }

            .hbar-fill {
                height: 100%;
                border-radius: 4px;
                background: linear-gradient(90deg, #0fa0ff, #19c1d2);
            }

            .donut-wrap {
                display: grid;
                grid-template-columns: 190px 1fr;
                align-items: center;
                gap: 20px;
                min-height: 196px;
            }

            .donut {
                width: 176px;
                height: 176px;
                border-radius: 50%;
                display: grid;
                place-items: center;
                background: conic-gradient(#1e9bff 0 36%, #22c486 36% 56%, #b94bd7 56% 72%, #ff7a28 72% 91%, #37d17c 91% 100%);
            }

            .donut-center {
                width: 92px;
                height: 92px;
                border-radius: 50%;
                background: #08233b;
                display: grid;
                place-items: center;
                text-align: center;
                font-size: 13px;
                color: #c9d9e6;
                box-shadow: 0 0 0 1px rgba(255,255,255,.08);
            }

            .donut-center strong {
                display: block;
                color: white;
                font-size: 26px;
            }

            .donut-legend {
                display: grid;
                gap: 10px;
                font-size: 12px;
            }

            .donut-legend div {
                display: grid;
                grid-template-columns: 12px 1fr auto;
                gap: 8px;
                align-items: center;
                color: #d7e5f2;
            }

            .dot {
                width: 8px;
                height: 8px;
                border-radius: 50%;
            }

            table.exec-table {
                width: 100%;
                border-collapse: collapse;
                font-size: 12px;
            }

            table.exec-table th {
                color: #f2f7ff;
                font-weight: 800;
                text-align: left;
                border-top: 1px solid var(--border);
                border-bottom: 1px solid var(--border);
                padding: 9px 10px;
            }

            table.exec-table td {
                color: #d7e5f2;
                border-bottom: 1px solid rgba(77,170,255,.15);
                padding: 8px 10px;
            }

            .progress-cell {
                display: flex;
                align-items: center;
                gap: 8px;
            }

            .mini-track {
                width: 52px;
                height: 11px;
                border-radius: 2px;
                background: rgba(255,255,255,.08);
                overflow: hidden;
            }

            .mini-fill {
                height: 100%;
                background: linear-gradient(90deg, #0d7bd8, #22b7ff);
            }

            .status {
                display: inline-block;
                min-width: 70px;
                text-align: center;
                border-radius: 4px;
                padding: 4px 8px;
                font-weight: 900;
                font-size: 11px;
            }

            .status.critico {
                color: #ff695d;
                border: 1px solid rgba(255, 76, 65, .55);
                background: rgba(255, 76, 65, .12);
            }

            .status.atencao {
                color: #ffc04c;
                border: 1px solid rgba(255, 176, 42, .55);
                background: rgba(255, 176, 42, .12);
            }

            .summary-row {
                display: flex;
                justify-content: space-between;
                gap: 16px;
                padding: 13px 0;
                border-bottom: 1px solid rgba(77,170,255,.18);
                color: #c8d9e8;
                font-size: 13px;
            }

            .summary-row strong {
                color: white;
                font-size: 18px;
            }

            .footer {
                display: flex;
                justify-content: center;
                gap: 42px;
                color: #94aabd;
                font-size: 12px;
                padding: 10px 0 0;
                border-top: 1px solid rgba(77,170,255,.16);
            }

            .support-box {
                margin-top: 60px;
                border: 1px solid var(--border);
                border-radius: 8px;
                padding: 12px;
                color: #b9d2e6;
                background: rgba(255,255,255,.04);
                font-size: 12px;
            }

            @media (max-width: 1100px) {
                .kpi-grid, .panel-grid, .bottom-grid {
                    grid-template-columns: 1fr;
                }

                .topbar, .topbar-left, .topbar-right {
                    align-items: flex-start;
                    flex-direction: column;
                }
            }
        </style>
        """,
        unsafe_allow_html=True,
    )


def entrar(usuario, senha):
    if usuario == LOGIN and senha == SENHA:
        st.session_state.logado = True
        st.rerun()

    st.error("Login ou senha invalidos")


def mostrar_login():
    aplicar_css()
    st.title("🔐 Acesso ao Sistema")

    usuario = st.text_input("Login")
    senha = st.text_input("Senha", type="password")

    if st.button("Entrar"):
        entrar(usuario, senha)


def mostrar_menu():
    with st.sidebar:
        st.markdown(
            """
            <div style="display:flex; gap:12px; align-items:center; padding:8px 0 22px;">
                <div style="font-size:30px;">📊</div>
                <div>
                    <div style="font-size:17px; font-weight:900;">LOGISTICA</div>
                    <div style="font-size:11px; color:#9db6c9;">CONTROLE DE MATERIAIS</div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        aba = st.radio(
            "Navegacao",
            [
                "🏠 Dashboard",
                "↔️ Movimentacoes",
                "📦 Estoque / Saldo",
                "👤 Consumo",
                "📋 Relatorios",
                "⚙️ Configuracoes",
            ],
        )

        st.markdown("---")
        st.caption("Dados da planilha")

        if st.button("Sincronizar SharePoint"):
            try:
                bruto = ler_excel_origem(SHAREPOINT_URL)
                st.session_state.dados_planilha = preparar_dados(bruto)
                st.session_state.fonte_dados = "SharePoint"
                st.success("Planilha sincronizada.")
            except Exception:
                st.warning("O SharePoint pediu login. Use o upload do Excel ou uma URL publica de download.")

        arquivo = st.file_uploader("Enviar Excel", type=["xlsx", "xls", "xlsm"])
        if arquivo is not None:
            bruto = ler_excel_origem(arquivo)
            st.session_state.dados_planilha = preparar_dados(bruto)
            st.session_state.fonte_dados = arquivo.name
            st.success("Planilha carregada.")

        st.markdown(
            """
            <div class="support-box">
                <strong>💬 Duvidas?</strong><br>
                Fale com o suporte
            </div>
            """,
            unsafe_allow_html=True,
        )

        if st.button("Sair"):
            st.session_state.logado = False
            st.rerun()

    return aba


def mostrar_topbar(fonte_dados):
    st.markdown(
        f"""
        <div class="topbar">
            <div class="topbar-left">
                <div class="hamburger">☰</div>
                <div class="page-title">Dashboard Executivo</div>
            </div>
            <div class="topbar-right">
                <div class="top-meta">◷ Fonte: {escapar(fonte_dados)}</div>
                <div class="periodo">Periodo: 01/06/2026 - 10/06/2026⌄</div>
                <div class="top-meta">🔔</div>
                <div class="user-chip">👤 Administrador⌄</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def mostrar_kpis(metricas):
    st.markdown(
        f"""
        <div class="kpi-grid">
            <div class="kpi blue">
                <div class="kpi-label">Total Entradas</div>
                <div class="kpi-value">{formatar_numero(metricas["entradas"])}</div>
                <div class="kpi-caption">+ 8,2% vs periodo anterior</div>
                <div class="kpi-icon">↗</div>
            </div>
            <div class="kpi green">
                <div class="kpi-label">Total Saidas</div>
                <div class="kpi-value">{formatar_numero(metricas["saidas"])}</div>
                <div class="kpi-caption">+ 12,7% vs periodo anterior</div>
                <div class="kpi-icon">↘</div>
            </div>
            <div class="kpi purple">
                <div class="kpi-label">Saldo Atual</div>
                <div class="kpi-value">{formatar_numero(metricas["saldo"])}</div>
                <div class="kpi-caption">Materiais em estoque</div>
                <div class="kpi-icon">▣</div>
            </div>
            <div class="kpi orange">
                <div class="kpi-label">Equipes Ativas</div>
                <div class="kpi-value">{formatar_numero(metricas["equipes"])}</div>
                <div class="kpi-caption">Equipes com movimentacao</div>
                <div class="kpi-icon">👥</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def mostrar_graficos():
    st.markdown(
        """
        <div class="panel-grid">
            <div class="panel">
                <div class="panel-title">Evolucao semanal - Entradas x Saidas</div>
                <div class="legend">
                    <span class="entradas">Entradas</span>
                    <span class="saidas">Saidas</span>
                    <span class="saldo">Saldo</span>
                </div>
                <div class="chart-lines">
                    <div class="bar in" style="left:7%; height:78px;"></div>
                    <div class="bar out" style="left:12%; height:64px;"></div>
                    <div class="bar in" style="left:25%; height:112px;"></div>
                    <div class="bar out" style="left:30%; height:82px;"></div>
                    <div class="bar in" style="left:43%; height:122px;"></div>
                    <div class="bar out" style="left:48%; height:108px;"></div>
                    <div class="bar in" style="left:61%; height:112px;"></div>
                    <div class="bar out" style="left:66%; height:72px;"></div>
                    <div class="bar in" style="left:80%; height:118px;"></div>
                    <div class="bar out" style="left:85%; height:82px;"></div>
                    <div class="line-dot" style="left:11%; bottom:86px;"></div>
                    <div class="line-dot" style="left:29%; bottom:104px;"></div>
                    <div class="line-dot" style="left:47%; bottom:90px;"></div>
                    <div class="line-dot" style="left:65%; bottom:102px;"></div>
                    <div class="line-dot" style="left:84%; bottom:90px;"></div>
                </div>
            </div>
            <div class="panel">
                <div class="panel-title">Consumo por equipe (saidas)</div>
                <div class="hbar-row"><span>Osseni - Gabriel</span><div class="hbar-track"><div class="hbar-fill" style="width:100%;"></div></div><strong>2.450</strong></div>
                <div class="hbar-row"><span>Anderson - Mateus</span><div class="hbar-track"><div class="hbar-fill" style="width:89%;"></div></div><strong>2.180</strong></div>
                <div class="hbar-row"><span>Paulo - Weslei</span><div class="hbar-track"><div class="hbar-fill" style="width:80%;"></div></div><strong>1.950</strong></div>
                <div class="hbar-row"><span>Pedro - Daniel Elias</span><div class="hbar-track"><div class="hbar-fill" style="width:69%;"></div></div><strong>1.680</strong></div>
                <div class="hbar-row"><span>Velito - Jonathas</span><div class="hbar-track"><div class="hbar-fill" style="width:39%;"></div></div><strong>950</strong></div>
                <div class="hbar-row"><span>Wanderson - Elise</span><div class="hbar-track"><div class="hbar-fill" style="width:24%;"></div></div><strong>575</strong></div>
            </div>
            <div class="panel">
                <div class="panel-title">Consumo por carro (saidas)</div>
                <div class="donut-wrap">
                    <div class="donut"><div class="donut-center"><strong>9.785</strong>Total</div></div>
                    <div class="donut-legend">
                        <div><span class="dot" style="background:#1e9bff;"></span><span>DBI - COPEL</span><strong>35,6%</strong></div>
                        <div><span class="dot" style="background:#ff7a28;"></span><span>FUSIMEC</span><strong>20,4%</strong></div>
                        <div><span class="dot" style="background:#ffc21a;"></span><span>TRI - COPEL</span><strong>18,7%</strong></div>
                        <div><span class="dot" style="background:#b94bd7;"></span><span>MR - COPEL</span><strong>15,5%</strong></div>
                        <div><span class="dot" style="background:#22c486;"></span><span>OUTROS</span><strong>9,8%</strong></div>
                    </div>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def linhas_top_materiais(dados):
    saidas = dados[dados["tipo_normalizado"].str.contains("saida", na=False)]
    if saidas.empty:
        saidas = dados

    agrupado = (
        saidas.groupby(["codigo", "descricao"], dropna=False)["quantidade"]
        .sum()
        .reset_index()
        .sort_values("quantidade", ascending=False)
        .head(10)
    )

    total = max(float(agrupado["quantidade"].sum()), 1)
    maior = max(float(agrupado["quantidade"].max()) if not agrupado.empty else 1, 1)
    linhas = []

    for indice, linha in enumerate(agrupado.itertuples(index=False), start=1):
        quantidade = int(linha.quantidade)
        percentual = quantidade / total * 100
        largura = quantidade / maior * 100
        linhas.append(
            f"""
            <tr>
                <td>{indice}</td>
                <td>{escapar(linha.codigo)}</td>
                <td>{escapar(linha.descricao)}</td>
                <td><strong>{formatar_numero(quantidade)}</strong></td>
                <td><div class="progress-cell"><div class="mini-track"><div class="mini-fill" style="width:{largura:.0f}%;"></div></div>{percentual:.1f}%</div></td>
            </tr>
            """
        )

    return "".join(linhas) or '<tr><td colspan="5">Nenhum dado encontrado.</td></tr>'


def linhas_alertas(dados):
    movimentos = dados.copy()
    movimentos["sinal"] = movimentos["tipo_normalizado"].apply(lambda tipo: 1 if "entrada" in tipo else -1 if "saida" in tipo else 0)
    movimentos["saldo_linha"] = movimentos["quantidade"] * movimentos["sinal"]
    saldos = (
        movimentos.groupby(["codigo", "descricao"], dropna=False)["saldo_linha"]
        .sum()
        .reset_index()
        .rename(columns={"saldo_linha": "saldo"})
        .sort_values("saldo")
        .head(5)
    )

    linhas = []
    for linha in saldos.itertuples(index=False):
        saldo = int(linha.saldo)
        status = "CRITICO" if saldo <= 20 else "ATENCAO"
        classe = "critico" if saldo <= 20 else "atencao"
        linhas.append(
            f"""
            <tr>
                <td>{escapar(linha.codigo)}</td>
                <td>{escapar(linha.descricao)}</td>
                <td>{formatar_numero(saldo)}</td>
                <td><span class="status {classe}">{status}</span></td>
            </tr>
            """
        )

    return "".join(linhas) or '<tr><td colspan="4">Nenhum alerta encontrado.</td></tr>'


def linhas_ultimas_movimentacoes(dados):
    ordenado = dados.copy()
    ordenado["_ordem"] = ordenado["data"].fillna(pd.Timestamp.min)
    ordenado = ordenado.sort_values("_ordem", ascending=False).head(5)

    linhas = []
    for linha in ordenado.itertuples(index=False):
        data = linha.data.strftime("%d/%m/%Y") if pd.notna(linha.data) else ""
        tipo = escapar(linha.tipo).upper()
        cor = "#ff4b4b" if "SAIDA" in normalizar_texto(tipo).upper() else "#22c486"
        linhas.append(
            f"""
            <tr>
                <td>{data}</td>
                <td>{escapar(linha.semana)}</td>
                <td>{escapar(linha.carro)}</td>
                <td>{escapar(linha.equipe)}</td>
                <td>{escapar(linha.codigo)}</td>
                <td>{escapar(linha.descricao)}</td>
                <td style="color:{cor};font-weight:900;">{tipo}</td>
                <td>{formatar_numero(linha.quantidade)}</td>
                <td>{escapar(linha.observacao)}</td>
            </tr>
            """
        )

    return "".join(linhas) or '<tr><td colspan="9">Nenhuma movimentacao encontrada.</td></tr>'


def mostrar_tabelas(dados, metricas):
    st.markdown(
        f"""
        <div class="bottom-grid">
            <div class="panel">
                <div class="panel-title">Top 10 materiais mais consumidos</div>
                <table class="exec-table">
                    <thead><tr><th>#</th><th>Codigo</th><th>Descricao</th><th>Saidas</th><th>% Total</th></tr></thead>
                    <tbody>
                        {linhas_top_materiais(dados)}
                    </tbody>
                </table>
            </div>
            <div class="panel">
                <div class="panel-title">Alertas - Itens com baixo saldo</div>
                <table class="exec-table">
                    <thead><tr><th>Codigo</th><th>Descricao</th><th>Saldo</th><th>Status</th></tr></thead>
                    <tbody>
                        {linhas_alertas(dados)}
                    </tbody>
                </table>
            </div>
            <div class="panel">
                <div class="panel-title">Resumo do periodo</div>
                <div class="summary-row"><span>Total de Movimentacoes</span><strong>{formatar_numero(metricas["movimentacoes"])}</strong></div>
                <div class="summary-row"><span>Total de Saidas</span><strong>{formatar_numero(metricas["saidas"])}</strong></div>
                <div class="summary-row"><span>Materiais Diferentes</span><strong>{formatar_numero(metricas["materiais"])}</strong></div>
                <div class="summary-row"><span>Equipes com Saidas</span><strong>{formatar_numero(metricas["equipes"])}</strong></div>
                <div class="summary-row"><span>Carros com Saidas</span><strong>{formatar_numero(metricas["carros"])}</strong></div>
                <div class="summary-row"><span>Saldo Atual</span><strong>{formatar_numero(metricas["saldo"])}</strong></div>
            </div>
        </div>

        <div class="panel">
            <div class="panel-title">Ultimas movimentacoes</div>
            <table class="exec-table">
                <thead><tr><th>Data</th><th>Semana</th><th>Carro</th><th>Equipe</th><th>Codigo</th><th>Descricao</th><th>Tipo</th><th>Quantidade</th><th>Observacao</th></tr></thead>
                <tbody>
                    {linhas_ultimas_movimentacoes(dados)}
                </tbody>
            </table>
        </div>

        <div class="footer">
            <span>Sistema Logistico - Controle de Materiais</span>
            <span>Dados sincronizados automaticamente da planilha no SharePoint</span>
        </div>
        """,
        unsafe_allow_html=True,
    )


def mostrar_dashboard():
    aplicar_css()
    dados, fonte_dados = obter_dados_dashboard()
    metricas = obter_metricas(dados)
    mostrar_topbar(fonte_dados)
    mostrar_kpis(metricas)
    mostrar_graficos()
    mostrar_tabelas(dados, metricas)


def pagina_em_construcao(titulo):
    aplicar_css()
    _, fonte_dados = obter_dados_dashboard()
    mostrar_topbar(fonte_dados)
    st.markdown(
        f"""
        <div class="panel">
            <div class="panel-title">{titulo}</div>
            <p style="color:#c8d9e8; margin:0;">Area preparada para receber os dados e formularios desta rotina.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )


if not st.session_state.logado:
    mostrar_login()
    st.stop()


aba = mostrar_menu()

if aba == "🏠 Dashboard":
    mostrar_dashboard()
elif aba == "↔️ Movimentacoes":
    pagina_em_construcao("Movimentacoes")
elif aba == "📦 Estoque / Saldo":
    pagina_em_construcao("Estoque / Saldo")
elif aba == "👤 Consumo":
    pagina_em_construcao("Consumo")
elif aba == "📋 Relatorios":
    pagina_em_construcao("Relatorios")
elif aba == "⚙️ Configuracoes":
    pagina_em_construcao("Configuracoes")
