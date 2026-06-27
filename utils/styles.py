import streamlit as st

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