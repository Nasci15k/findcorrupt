"""
OLHO DE DEUS — Transparência Parlamentar Brasileira
Dashboard de vigilância cidadã sobre gastos públicos, CEAP, bens declarados e redes de influência.
"""

import streamlit as st
import pandas as pd
import numpy as np
import requests
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import json
from datetime import datetime, timedelta
import time
from scipy import stats
import warnings
warnings.filterwarnings('ignore')

# ─────────────────────────────────────────────
# CONFIG
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="OLHO DE DEUS — Transparência Parlamentar",
    page_icon="👁",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ─────────────────────────────────────────────
# DESIGN SYSTEM (fiel ao site original)
# ─────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Bebas+Neue&family=Source+Sans+3:wght@400;600;700&family=JetBrains+Mono:wght@400&display=swap');

:root {
    --bg-primary: #0a0a0c;
    --bg-secondary: #111114;
    --bg-tertiary: #1a1a1f;
    --bg-card: rgba(17,17,20,0.85);
    --accent-red: #e04545;
    --accent-amber: #d4a03a;
    --accent-teal: #3d9996;
    --accent-blue: #4682b4;
    --accent-purple: #9b59b6;
    --text-primary: #f5f5f3;
    --text-secondary: #9a9ca8;
    --text-muted: #7a7c88;
    --border: #232328;
    --border-hover: #35353d;
    --font-display: 'Bebas Neue', sans-serif;
    --font-body: 'Source Sans 3', system-ui, sans-serif;
    --font-mono: 'JetBrains Mono', monospace;
}

/* Reset Streamlit */
.stApp { background-color: var(--bg-primary) !important; }
.main .block-container { padding: 0 1.5rem 2rem 1.5rem; max-width: 1400px; }
[data-testid="stHeader"] { background: transparent; }
[data-testid="stSidebar"] { background: var(--bg-secondary); border-right: 1px solid var(--border); }
footer { display: none !important; }
#MainMenu { display: none !important; }
.stDeployButton { display: none !important; }

/* Typography */
html, body, .stApp, .stMarkdown, p, div, span {
    font-family: var(--font-body) !important;
    color: var(--text-primary);
}

/* Top nav bar */
.top-nav {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 1rem 0 1.5rem 0;
    border-bottom: 1px solid var(--border);
    margin-bottom: 1.5rem;
}
.nav-brand {
    font-family: var(--font-display) !important;
    font-size: 1.6rem;
    letter-spacing: 0.08em;
    color: var(--text-primary) !important;
    display: flex;
    align-items: center;
    gap: 0.5rem;
}
.nav-brand span { color: var(--accent-red); }
.nav-subtitle {
    font-family: var(--font-mono) !important;
    font-size: 0.65rem;
    color: var(--text-muted);
    letter-spacing: 0.12em;
    text-transform: uppercase;
}
.nav-source {
    font-family: var(--font-mono) !important;
    font-size: 0.65rem;
    color: var(--text-muted);
    letter-spacing: 0.05em;
}

/* Stat cards */
.stat-card {
    background: var(--bg-card);
    border: 1px solid var(--border);
    border-radius: 6px;
    padding: 1.25rem 1.5rem;
    transition: border-color 0.2s;
}
.stat-card:hover { border-color: var(--border-hover); }
.stat-label {
    font-family: var(--font-mono) !important;
    font-size: 0.65rem;
    color: var(--text-muted);
    text-transform: uppercase;
    letter-spacing: 0.1em;
    margin-bottom: 0.4rem;
}
.stat-value {
    font-family: var(--font-display) !important;
    font-size: 2rem;
    line-height: 1;
    color: var(--text-primary);
    letter-spacing: 0.02em;
}
.stat-value.red { color: var(--accent-red); }
.stat-value.amber { color: var(--accent-amber); }
.stat-value.teal { color: var(--accent-teal); }
.stat-sub {
    font-size: 0.7rem;
    color: var(--text-muted);
    margin-top: 0.3rem;
    font-family: var(--font-mono) !important;
}

/* Section headers */
.section-header {
    font-family: var(--font-display) !important;
    font-size: 1.4rem;
    letter-spacing: 0.06em;
    color: var(--text-primary);
    margin: 1.5rem 0 1rem 0;
    display: flex;
    align-items: center;
    gap: 0.6rem;
}
.section-header .dot {
    width: 6px; height: 6px;
    border-radius: 50%;
    background: var(--accent-red);
    display: inline-block;
}
.section-header.amber .dot { background: var(--accent-amber); }
.section-header.teal .dot { background: var(--accent-teal); }

/* Tabs */
.stTabs [data-baseweb="tab-list"] {
    background: transparent;
    border-bottom: 1px solid var(--border);
    gap: 0;
}
.stTabs [data-baseweb="tab"] {
    font-family: var(--font-body) !important;
    font-size: 0.8rem;
    font-weight: 600;
    color: var(--text-muted) !important;
    background: transparent !important;
    border: none !important;
    padding: 0.6rem 1.2rem !important;
    letter-spacing: 0.04em;
    text-transform: uppercase;
}
.stTabs [aria-selected="true"] {
    color: var(--text-primary) !important;
    border-bottom: 2px solid var(--accent-red) !important;
}
.stTabs [data-baseweb="tab-panel"] { padding-top: 1.2rem; }

/* Inputs */
.stTextInput input, .stSelectbox select, div[data-baseweb="select"] {
    background: var(--bg-tertiary) !important;
    border: 1px solid var(--border) !important;
    border-radius: 4px !important;
    color: var(--text-primary) !important;
    font-family: var(--font-body) !important;
    font-size: 0.85rem !important;
}
.stTextInput input:focus { border-color: var(--accent-red) !important; }
label { color: var(--text-secondary) !important; font-size: 0.78rem !important; font-weight: 600 !important; text-transform: uppercase !important; letter-spacing: 0.06em !important; }

/* Tables */
.stDataFrame { background: var(--bg-secondary); }
[data-testid="stDataFrame"] { border: 1px solid var(--border); border-radius: 6px; overflow: hidden; }

/* Alerts / banners */
.alert-red {
    background: rgba(224,69,69,0.08);
    border: 1px solid rgba(224,69,69,0.3);
    border-radius: 6px;
    padding: 1rem 1.25rem;
    margin: 0.5rem 0;
}
.alert-amber {
    background: rgba(212,160,58,0.08);
    border: 1px solid rgba(212,160,58,0.3);
    border-radius: 6px;
    padding: 1rem 1.25rem;
    margin: 0.5rem 0;
}
.alert-teal {
    background: rgba(61,153,150,0.08);
    border: 1px solid rgba(61,153,150,0.3);
    border-radius: 6px;
    padding: 1rem 1.25rem;
    margin: 0.5rem 0;
}
.alert-title {
    font-family: var(--font-display) !important;
    font-size: 0.95rem;
    letter-spacing: 0.05em;
    margin-bottom: 0.3rem;
}
.alert-title.red { color: var(--accent-red); }
.alert-title.amber { color: var(--accent-amber); }
.alert-title.teal { color: var(--accent-teal); }
.alert-body { font-size: 0.82rem; color: var(--text-secondary); line-height: 1.5; }

/* Tag badges */
.badge {
    display: inline-block;
    font-family: var(--font-mono) !important;
    font-size: 0.6rem;
    padding: 0.2em 0.5em;
    border-radius: 3px;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.08em;
}
.badge-red { background: rgba(224,69,69,0.15); color: var(--accent-red); border: 1px solid rgba(224,69,69,0.3); }
.badge-amber { background: rgba(212,160,58,0.15); color: var(--accent-amber); border: 1px solid rgba(212,160,58,0.3); }
.badge-green { background: rgba(52,168,83,0.15); color: #34a853; border: 1px solid rgba(52,168,83,0.3); }
.badge-teal { background: rgba(61,153,150,0.15); color: var(--accent-teal); border: 1px solid rgba(61,153,150,0.3); }

/* Scrollbar */
::-webkit-scrollbar { width: 6px; height: 6px; }
::-webkit-scrollbar-track { background: var(--bg-secondary); }
::-webkit-scrollbar-thumb { background: var(--border-hover); border-radius: 3px; }

/* Buttons */
.stButton button {
    background: var(--bg-tertiary) !important;
    border: 1px solid var(--border) !important;
    color: var(--text-primary) !important;
    font-family: var(--font-body) !important;
    font-size: 0.78rem !important;
    font-weight: 600 !important;
    text-transform: uppercase !important;
    letter-spacing: 0.06em !important;
    border-radius: 4px !important;
    padding: 0.4rem 1rem !important;
}
.stButton button:hover {
    border-color: var(--accent-red) !important;
    color: var(--accent-red) !important;
}

/* Metric override */
[data-testid="stMetric"] {
    background: var(--bg-card);
    border: 1px solid var(--border);
    border-radius: 6px;
    padding: 1rem 1.25rem !important;
}
[data-testid="stMetricLabel"] { color: var(--text-muted) !important; font-size: 0.65rem !important; text-transform: uppercase; letter-spacing: 0.1em; font-family: var(--font-mono) !important; }
[data-testid="stMetricValue"] { font-family: var(--font-display) !important; color: var(--text-primary) !important; font-size: 1.8rem !important; }
[data-testid="stMetricDelta"] { font-size: 0.75rem !important; font-family: var(--font-mono) !important; }

/* Plotly charts dark */
.js-plotly-plot { border-radius: 6px; }

/* Progress / spinner */
.stSpinner > div { border-top-color: var(--accent-red) !important; }

/* Horizontal divider */
hr { border-color: var(--border) !important; margin: 1rem 0 !important; }

/* Hide streamlit branding */
[data-testid="stToolbar"] { display: none; }

/* Expandable */
.streamlit-expanderHeader {
    background: var(--bg-tertiary) !important;
    border: 1px solid var(--border) !important;
    color: var(--text-secondary) !important;
    font-size: 0.78rem !important;
    font-weight: 600 !important;
    text-transform: uppercase !important;
    letter-spacing: 0.06em !important;
}

/* Slider */
.stSlider [data-baseweb="slider"] .rc-slider-track { background: var(--accent-red) !important; }
.stSlider [data-baseweb="slider"] .rc-slider-handle { border-color: var(--accent-red) !important; }
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# PLOTLY THEME
# ─────────────────────────────────────────────
PLOT_LAYOUT = dict(
    paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='rgba(0,0,0,0)',
    font=dict(family='Source Sans 3, system-ui', color='#9a9ca8', size=11),
    title_font=dict(family='Bebas Neue', color='#f5f5f3', size=18),
    legend=dict(bgcolor='rgba(0,0,0,0)', font=dict(color='#9a9ca8', size=10)),
    xaxis=dict(gridcolor='#232328', linecolor='#232328', tickfont=dict(color='#7a7c88'), title_font=dict(color='#9a9ca8')),
    yaxis=dict(gridcolor='#232328', linecolor='#232328', tickfont=dict(color='#7a7c88'), title_font=dict(color='#9a9ca8')),
    margin=dict(l=10, r=10, t=40, b=10),
)
COLORS = ['#e04545','#d4a03a','#3d9996','#4682b4','#9b59b6','#34a853','#e67e22','#1abc9c']

# ─────────────────────────────────────────────
# API FUNCTIONS
# ─────────────────────────────────────────────

@st.cache_data(ttl=3600, show_spinner=False)
def fetch_ceap_data(ano: int) -> pd.DataFrame:
    """Baixa dados CEAP direto da Câmara."""
    import zipfile, io
    url = f"https://www.camara.leg.br/cotas/Ano-{ano}.csv.zip"
    try:
        r = requests.get(url, timeout=60)
        r.raise_for_status()
        with zipfile.ZipFile(io.BytesIO(r.content)) as z:
            csv_name = [n for n in z.namelist() if n.endswith('.csv')][0]
            with z.open(csv_name) as f:
                df = pd.read_csv(f, sep=';', encoding='utf-8', low_memory=False)
        return df
    except Exception as e:
        st.error(f"Erro ao baixar dados de {ano}: {e}")
        return pd.DataFrame()

@st.cache_data(ttl=3600, show_spinner=False)
def fetch_deputados_lista() -> pd.DataFrame:
    """Lista todos os deputados ativos via API REST da Câmara."""
    try:
        all_deps = []
        pagina = 1
        while True:
            url = f"https://dadosabertos.camara.leg.br/api/v2/deputados?pagina={pagina}&itens=100&ordem=ASC&ordenarPor=nome"
            r = requests.get(url, timeout=30)
            data = r.json()
            deps = data.get('dados', [])
            if not deps:
                break
            all_deps.extend(deps)
            if len(deps) < 100:
                break
            pagina += 1
        return pd.DataFrame(all_deps)
    except:
        return pd.DataFrame()

@st.cache_data(ttl=86400, show_spinner=False)
def fetch_deputado_detalhe(dep_id: int) -> dict:
    """Busca detalhes completos de um deputado."""
    try:
        r = requests.get(f"https://dadosabertos.camara.leg.br/api/v2/deputados/{dep_id}", timeout=15)
        return r.json().get('dados', {})
    except:
        return {}

@st.cache_data(ttl=86400, show_spinner=False)
def fetch_bens_declarados(dep_id: int) -> list:
    """Busca bens declarados via API da Câmara."""
    try:
        r = requests.get(f"https://dadosabertos.camara.leg.br/api/v2/deputados/{dep_id}/discursos?pagina=1&itens=5", timeout=15)
        return r.json().get('dados', [])
    except:
        return []

@st.cache_data(ttl=3600, show_spinner=False)
def fetch_votacoes_recentes() -> pd.DataFrame:
    """Busca votações recentes na Câmara."""
    try:
        r = requests.get("https://dadosabertos.camara.leg.br/api/v2/votacoes?pagina=1&itens=20&ordem=DESC&ordenarPor=dataHoraRegistro", timeout=15)
        data = r.json().get('dados', [])
        return pd.DataFrame(data)
    except:
        return pd.DataFrame()

@st.cache_data(ttl=3600, show_spinner=False)
def fetch_proposicoes_recentes() -> pd.DataFrame:
    """Busca proposições recentes."""
    try:
        hoje = datetime.now().strftime('%Y-%m-%d')
        mes_passado = (datetime.now() - timedelta(days=30)).strftime('%Y-%m-%d')
        r = requests.get(f"https://dadosabertos.camara.leg.br/api/v2/proposicoes?dataInicio={mes_passado}&dataFim={hoje}&pagina=1&itens=20", timeout=15)
        data = r.json().get('dados', [])
        return pd.DataFrame(data)
    except:
        return pd.DataFrame()

@st.cache_data(ttl=1800, show_spinner=False)
def fetch_partidos() -> pd.DataFrame:
    """Busca lista de partidos."""
    try:
        r = requests.get("https://dadosabertos.camara.leg.br/api/v2/partidos?pagina=1&itens=50&ordem=ASC&ordenarPor=sigla", timeout=15)
        return pd.DataFrame(r.json().get('dados', []))
    except:
        return pd.DataFrame()

# ─────────────────────────────────────────────
# ANALISE FUNCTIONS
# ─────────────────────────────────────────────

def analise_benford(valores: pd.Series) -> dict:
    vals = valores[valores > 0].dropna()
    if len(vals) < 30:
        return None
    primeiros = vals.apply(lambda v: int(str(abs(v)).replace('.','').replace(',','').lstrip('0')[0]) if str(abs(v)).replace('.','').replace(',','').lstrip('0') else None).dropna()
    contagem = primeiros.value_counts().sort_index()
    total = len(primeiros)
    freq_obs = {d: contagem.get(d, 0) / total for d in range(1, 10)}
    freq_esp = {d: np.log10(1 + 1/d) for d in range(1, 10)}
    obs = [contagem.get(d, 0) for d in range(1, 10)]
    esp = [freq_esp[d] * total for d in range(1, 10)]
    chi2, p_valor = stats.chisquare(obs, esp)
    return {'observado': freq_obs, 'esperado': freq_esp, 'chi2': chi2, 'p_valor': p_valor, 'significativo': p_valor < 0.05, 'n': total}

def calcular_hhi(df_dep: pd.DataFrame) -> dict:
    if df_dep.empty or 'vlrLiquido' not in df_dep.columns:
        return None
    total = df_dep['vlrLiquido'].sum()
    if total == 0:
        return None
    por_forn = df_dep.groupby('txtFornecedor')['vlrLiquido'].sum().sort_values(ascending=False)
    partic = por_forn / total
    hhi = sum(p**2 for p in partic) * 10000
    nivel = 'BAIXO' if hhi < 1500 else 'MODERADO' if hhi < 2500 else 'ALTO' if hhi < 5000 else 'MUITO ALTO'
    return {'hhi': hhi, 'nivel': nivel, 'n_fornecedores': len(por_forn), 'top1_pct': partic.iloc[0]*100 if len(partic)>0 else 0, 'top_fornecedores': por_forn.head(5)}

def detectar_anomalias(df_dep: pd.DataFrame) -> list:
    alertas = []
    if df_dep.empty:
        return alertas
    # Valores redondos
    vals = df_dep['vlrLiquido']
    redondos = vals.apply(lambda v: v > 0 and (v % 1000 < 0.01 or v % 500 < 0.01)).sum()
    pct_red = redondos / len(vals) * 100 if len(vals) > 0 else 0
    if pct_red > 30:
        alertas.append({'tipo': 'VALORES REDONDOS', 'nivel': 'amber', 'msg': f'{pct_red:.1f}% dos gastos são valores redondos (múltiplos de R$500/1000). Padrão suspeito em {redondos} transações.'})
    # HHI
    hhi_r = calcular_hhi(df_dep)
    if hhi_r and hhi_r['hhi'] > 2500:
        alertas.append({'tipo': 'CONCENTRAÇÃO DE FORNECEDOR', 'nivel': 'red', 'msg': f'HHI = {hhi_r["hhi"]:,.0f} ({hhi_r["nivel"]}). O fornecedor principal recebe {hhi_r["top1_pct"]:.1f}% dos gastos.'})
    # Benford
    bfd = analise_benford(df_dep['vlrLiquido'])
    if bfd and bfd['significativo']:
        alertas.append({'tipo': 'LEI DE BENFORD', 'nivel': 'red', 'msg': f'Desvio estatístico detectado (χ²={bfd["chi2"]:.1f}, p={bfd["p_valor"]:.4f}). Distribuição dos gastos não segue padrão natural esperado.'})
    # Gastos no fim de semana
    if 'datEmissao' in df_dep.columns:
        try:
            df_dep = df_dep.copy()
            df_dep['data'] = pd.to_datetime(df_dep['datEmissao'], errors='coerce')
            fds = df_dep[df_dep['data'].dt.dayofweek >= 5]
            pct_fds = len(fds) / len(df_dep) * 100 if len(df_dep) > 0 else 0
            if pct_fds > 15:
                alertas.append({'tipo': 'GASTOS EM FIM DE SEMANA', 'nivel': 'amber', 'msg': f'{pct_fds:.1f}% das transações ocorreram em fins de semana ({len(fds)} notas). Merece atenção.'})
        except:
            pass
    return alertas

def formatar_brl(valor):
    if pd.isna(valor): return "R$ 0"
    if valor >= 1_000_000:
        return f"R$ {valor/1_000_000:.1f}M"
    elif valor >= 1_000:
        return f"R$ {valor/1_000:.0f}K"
    return f"R$ {valor:,.0f}".replace(",","X").replace(".",",").replace("X",".")

# ─────────────────────────────────────────────
# STATE
# ─────────────────────────────────────────────
if 'ceap_df' not in st.session_state:
    st.session_state.ceap_df = pd.DataFrame()
if 'ceap_loaded' not in st.session_state:
    st.session_state.ceap_loaded = False

# ─────────────────────────────────────────────
# HEADER
# ─────────────────────────────────────────────
st.markdown("""
<div class="top-nav">
    <div>
        <div class="nav-brand">👁 OLHO DE <span>DEUS</span></div>
        <div class="nav-subtitle">Transparência Parlamentar Brasileira · Dados Abertos</div>
    </div>
    <div class="nav-source">Fonte: Câmara dos Deputados · API Aberta · CEAP 2023–2026</div>
</div>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# TABS PRINCIPAIS
# ─────────────────────────────────────────────
tab_visao, tab_deps, tab_busca, tab_comparar, tab_anomalias, tab_live = st.tabs([
    "VISÃO GERAL", "DEPUTADOS", "BUSCAR DEPUTADO", "COMPARAR", "ANOMALIAS IA", "AO VIVO"
])

# ══════════════════════════════════════════════
# TAB 1 — VISÃO GERAL
# ══════════════════════════════════════════════
with tab_visao:
    # Carregamento de dados
    col_ctrl1, col_ctrl2, col_ctrl3 = st.columns([2, 2, 2])
    with col_ctrl1:
        anos_sel = st.multiselect("Anos", [2023, 2024, 2025, 2026], default=[2024, 2025], key="anos_visao")
    with col_ctrl2:
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("🔄 Carregar / Atualizar Dados", key="btn_load"):
            st.session_state.ceap_df = pd.DataFrame()
            st.session_state.ceap_loaded = False

    if anos_sel and not st.session_state.ceap_loaded:
        dfs = []
        prog = st.progress(0, text="Baixando dados da Câmara...")
        for i, ano in enumerate(anos_sel):
            prog.progress((i) / len(anos_sel), text=f"Baixando {ano}...")
            df_ano = fetch_ceap_data(ano)
            if not df_ano.empty:
                dfs.append(df_ano)
        prog.progress(1.0, text="Processando...")
        if dfs:
            df = pd.concat(dfs, ignore_index=True)
            # Normalize column names
            df.columns = [c.strip() for c in df.columns]
            if 'vlrLiquido' not in df.columns and 'vlrDocumento' in df.columns:
                df['vlrLiquido'] = df['vlrDocumento']
            df['vlrLiquido'] = pd.to_numeric(df['vlrLiquido'], errors='coerce').fillna(0)
            df = df[df['vlrLiquido'] > 0]
            st.session_state.ceap_df = df
            st.session_state.ceap_loaded = True
        prog.empty()

    df = st.session_state.ceap_df

    if df.empty:
        st.markdown("""
        <div class="alert-teal">
            <div class="alert-title teal">👆 SELECIONE OS ANOS E CARREGUE OS DADOS</div>
            <div class="alert-body">Escolha um ou mais anos acima e clique em "Carregar / Atualizar Dados". Os dados são baixados diretamente da API da Câmara dos Deputados.</div>
        </div>
        """, unsafe_allow_html=True)
    else:
        # ── KPI CARDS
        total_gasto = df['vlrLiquido'].sum()
        n_deps = df['txNomeParlamentar'].nunique() if 'txNomeParlamentar' in df.columns else 0
        n_transacoes = len(df)
        n_fornecedores = df['txtFornecedor'].nunique() if 'txtFornecedor' in df.columns else 0
        media_dep = total_gasto / n_deps if n_deps > 0 else 0
        maior_gasto = df.groupby('txNomeParlamentar')['vlrLiquido'].sum().max() if 'txNomeParlamentar' in df.columns else 0

        c1, c2, c3, c4, c5, c6 = st.columns(6)
        cards = [
            (c1, "TOTAL GASTO", f"R$ {total_gasto/1e9:.2f}B", "red", "bilhões de reais"),
            (c2, "DEPUTADOS", f"{n_deps:,}", "", "com gastos registrados"),
            (c3, "TRANSAÇÕES", f"{n_transacoes:,}", "amber", "notas fiscais/recibos"),
            (c4, "FORNECEDORES", f"{n_fornecedores:,}", "teal", "CNPJs/CPFs únicos"),
            (c5, "MÉDIA/DEP.", formatar_brl(media_dep), "", "por deputado no período"),
            (c6, "MAIOR GASTO", formatar_brl(maior_gasto), "red", "por 1 deputado"),
        ]
        for col, label, val, color, sub in cards:
            with col:
                st.markdown(f"""
                <div class="stat-card">
                    <div class="stat-label">{label}</div>
                    <div class="stat-value {color}">{val}</div>
                    <div class="stat-sub">{sub}</div>
                </div>
                """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        # ── CHARTS ROW 1
        col_a, col_b = st.columns([3, 2])

        with col_a:
            st.markdown('<div class="section-header"><span class="dot"></span> GASTOS POR CATEGORIA</div>', unsafe_allow_html=True)
            if 'txtDescricao' in df.columns:
                cat = df.groupby('txtDescricao')['vlrLiquido'].sum().sort_values(ascending=True).tail(12)
                fig = go.Figure(go.Bar(
                    x=cat.values, y=cat.index,
                    orientation='h',
                    marker_color=COLORS[0],
                    marker_line_width=0,
                    text=[formatar_brl(v) for v in cat.values],
                    textposition='outside',
                    textfont=dict(size=9, color='#9a9ca8'),
                ))
                fig.update_layout(**PLOT_LAYOUT, height=380)
                st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})

        with col_b:
            st.markdown('<div class="section-header amber"><span class="dot"></span> GASTOS POR PARTIDO</div>', unsafe_allow_html=True)
            if 'sgPartido' in df.columns:
                part = df.groupby('sgPartido')['vlrLiquido'].sum().sort_values(ascending=False).head(15)
                fig = go.Figure(go.Bar(
                    x=part.index, y=part.values,
                    marker_color=[COLORS[i % len(COLORS)] for i in range(len(part))],
                    marker_line_width=0,
                ))
                fig.update_layout(**PLOT_LAYOUT, height=380)
                fig.update_xaxes(tickangle=45)
                st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})

        # ── CHARTS ROW 2
        col_c, col_d = st.columns(2)

        with col_c:
            st.markdown('<div class="section-header teal"><span class="dot"></span> EVOLUÇÃO MENSAL</div>', unsafe_allow_html=True)
            if 'numAno' in df.columns and 'numMes' in df.columns:
                df['periodo'] = df['numAno'].astype(str) + '-' + df['numMes'].astype(str).str.zfill(2)
                mensal = df.groupby('periodo')['vlrLiquido'].sum().reset_index().sort_values('periodo')
                fig = go.Figure(go.Scatter(
                    x=mensal['periodo'], y=mensal['vlrLiquido'],
                    fill='tozeroy',
                    fillcolor='rgba(224,69,69,0.08)',
                    line=dict(color='#e04545', width=2),
                    mode='lines',
                ))
                fig.update_layout(**PLOT_LAYOUT, height=280)
                st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})

        with col_d:
            st.markdown('<div class="section-header"><span class="dot"></span> GASTOS POR ESTADO (UF)</div>', unsafe_allow_html=True)
            if 'sgUF' in df.columns:
                uf = df.groupby('sgUF')['vlrLiquido'].sum().reset_index()
                uf.columns = ['UF', 'Total']
                fig = px.choropleth(
                    uf, locations='UF', locationmode='geojson-id',
                    color='Total', color_continuous_scale=['#1a1a1f', '#e04545'],
                    scope='south america',
                )
                fig.update_layout(**PLOT_LAYOUT, height=280, coloraxis_showscale=False)
                fig.update_geos(bgcolor='rgba(0,0,0,0)', lakecolor='rgba(0,0,0,0)', landcolor='#1a1a1f', countrycolor='#232328', showframe=False)
                st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})

        # ── TOP DEPUTIES TABLE
        st.markdown('<div class="section-header"><span class="dot"></span> TOP 20 MAIORES GASTADORES</div>', unsafe_allow_html=True)
        if 'txNomeParlamentar' in df.columns:
            top_deps = df.groupby(['txNomeParlamentar', 'sgPartido', 'sgUF']).agg(
                Total=('vlrLiquido', 'sum'),
                Transacoes=('vlrLiquido', 'count'),
                Fornecedores=('txtFornecedor', 'nunique')
            ).reset_index().sort_values('Total', ascending=False).head(20)
            top_deps['Total_fmt'] = top_deps['Total'].apply(formatar_brl)
            top_deps['Media'] = (top_deps['Total'] / top_deps['Transacoes']).apply(formatar_brl)
            display_cols = ['txNomeParlamentar', 'sgPartido', 'sgUF', 'Total_fmt', 'Transacoes', 'Fornecedores', 'Media']
            rename = {'txNomeParlamentar': 'Deputado', 'sgPartido': 'Partido', 'sgUF': 'UF', 'Total_fmt': 'Total Gasto', 'Transacoes': 'Nº Notas', 'Fornecedores': 'Fornecedores', 'Media': 'Média/Nota'}
            st.dataframe(top_deps[display_cols].rename(columns=rename), use_container_width=True, hide_index=True)

# ══════════════════════════════════════════════
# TAB 2 — DEPUTADOS (ranking completo)
# ══════════════════════════════════════════════
with tab_deps:
    st.markdown('<div class="section-header"><span class="dot"></span> RANKING COMPLETO DE DEPUTADOS</div>', unsafe_allow_html=True)

    df = st.session_state.ceap_df
    if df.empty:
        st.info("Carregue os dados na aba Visão Geral primeiro.")
    else:
        col_f1, col_f2, col_f3 = st.columns(3)
        with col_f1:
            partidos_disp = ['Todos'] + sorted(df['sgPartido'].dropna().unique().tolist()) if 'sgPartido' in df.columns else ['Todos']
            partido_filtro = st.selectbox("Partido", partidos_disp, key="dep_partido")
        with col_f2:
            ufs_disp = ['Todos'] + sorted(df['sgUF'].dropna().unique().tolist()) if 'sgUF' in df.columns else ['Todos']
            uf_filtro = st.selectbox("Estado (UF)", ufs_disp, key="dep_uf")
        with col_f3:
            categorias_disp = ['Todas'] + sorted(df['txtDescricao'].dropna().unique().tolist()) if 'txtDescricao' in df.columns else ['Todas']
            cat_filtro = st.selectbox("Categoria de Gasto", categorias_disp, key="dep_cat")

        df_filt = df.copy()
        if partido_filtro != 'Todos' and 'sgPartido' in df_filt.columns:
            df_filt = df_filt[df_filt['sgPartido'] == partido_filtro]
        if uf_filtro != 'Todos' and 'sgUF' in df_filt.columns:
            df_filt = df_filt[df_filt['sgUF'] == uf_filtro]
        if cat_filtro != 'Todas' and 'txtDescricao' in df_filt.columns:
            df_filt = df_filt[df_filt['txtDescricao'] == cat_filtro]

        ranking = df_filt.groupby(['txNomeParlamentar', 'sgPartido', 'sgUF']).agg(
            Total=('vlrLiquido', 'sum'),
            Transacoes=('vlrLiquido', 'count'),
            Fornecedores=('txtFornecedor', 'nunique'),
        ).reset_index().sort_values('Total', ascending=False).reset_index(drop=True)
        ranking.index += 1
        ranking['Total_fmt'] = ranking['Total'].apply(formatar_brl)
        ranking['Media'] = (ranking['Total'] / ranking['Transacoes']).apply(formatar_brl)

        st.markdown(f"<div style='font-family:var(--font-mono);font-size:0.7rem;color:var(--text-muted);margin-bottom:0.5rem'>{len(ranking):,} deputados encontrados</div>", unsafe_allow_html=True)

        display = ranking[['txNomeParlamentar','sgPartido','sgUF','Total_fmt','Transacoes','Fornecedores','Media']].rename(columns={
            'txNomeParlamentar': 'Deputado', 'sgPartido': 'Partido', 'sgUF': 'UF',
            'Total_fmt': 'Total Gasto', 'Transacoes': 'Nº Notas', 'Media': 'Média/Nota'
        })
        st.dataframe(display, use_container_width=True)

# ══════════════════════════════════════════════
# TAB 3 — BUSCAR DEPUTADO (perfil individual)
# ══════════════════════════════════════════════
with tab_busca:
    st.markdown('<div class="section-header"><span class="dot"></span> PERFIL INDIVIDUAL DO DEPUTADO</div>', unsafe_allow_html=True)

    df = st.session_state.ceap_df
    if df.empty:
        st.info("Carregue os dados na aba Visão Geral primeiro.")
    else:
        nomes = sorted(df['txNomeParlamentar'].dropna().unique().tolist()) if 'txNomeParlamentar' in df.columns else []
        dep_sel = st.selectbox("🔍 Buscar deputado por nome", nomes, key="busca_dep")

        if dep_sel:
            df_dep = df[df['txNomeParlamentar'] == dep_sel].copy()

            # Info básica
            partido = df_dep['sgPartido'].iloc[0] if 'sgPartido' in df_dep.columns else 'N/D'
            uf = df_dep['sgUF'].iloc[0] if 'sgUF' in df_dep.columns else 'N/D'
            total = df_dep['vlrLiquido'].sum()
            n_notas = len(df_dep)
            n_forn = df_dep['txtFornecedor'].nunique() if 'txtFornecedor' in df_dep.columns else 0

            col_info, col_kpis = st.columns([1, 3])
            with col_info:
                # Busca foto via API
                deps_lista = fetch_deputados_lista()
                foto_url = ""
                dep_id = None
                if not deps_lista.empty and 'nome' in deps_lista.columns:
                    match = deps_lista[deps_lista['nome'].str.upper().str.contains(dep_sel[:15].upper(), na=False)]
                    if not match.empty:
                        dep_id = match.iloc[0].get('id')
                        foto_url = match.iloc[0].get('urlFoto', '')

                if foto_url:
                    st.image(foto_url, width=140)
                else:
                    st.markdown('<div style="width:140px;height:140px;background:var(--bg-tertiary);border:1px solid var(--border);border-radius:6px;display:flex;align-items:center;justify-content:center;font-size:3rem">👤</div>', unsafe_allow_html=True)

                st.markdown(f"""
                <div style="margin-top:0.8rem">
                    <div style="font-family:var(--font-display);font-size:1rem;color:var(--text-primary);letter-spacing:0.04em">{dep_sel}</div>
                    <div style="font-family:var(--font-mono);font-size:0.65rem;color:var(--text-muted);margin-top:0.2rem">{partido} · {uf}</div>
                </div>
                """, unsafe_allow_html=True)

            with col_kpis:
                k1, k2, k3, k4 = st.columns(4)
                with k1:
                    st.markdown(f'<div class="stat-card"><div class="stat-label">Total Gasto</div><div class="stat-value red">{formatar_brl(total)}</div></div>', unsafe_allow_html=True)
                with k2:
                    st.markdown(f'<div class="stat-card"><div class="stat-label">Nº de Notas</div><div class="stat-value">{n_notas:,}</div></div>', unsafe_allow_html=True)
                with k3:
                    st.markdown(f'<div class="stat-card"><div class="stat-label">Fornecedores</div><div class="stat-value amber">{n_forn}</div></div>', unsafe_allow_html=True)
                with k4:
                    media_nota = total/n_notas if n_notas > 0 else 0
                    st.markdown(f'<div class="stat-card"><div class="stat-label">Média/Nota</div><div class="stat-value teal">{formatar_brl(media_nota)}</div></div>', unsafe_allow_html=True)

            st.markdown("<br>", unsafe_allow_html=True)

            # Alertas
            alertas = detectar_anomalias(df_dep)
            if alertas:
                st.markdown('<div class="section-header"><span class="dot"></span> ALERTAS DE ANOMALIAS</div>', unsafe_allow_html=True)
                for alerta in alertas:
                    nivel = alerta['nivel']
                    st.markdown(f"""
                    <div class="alert-{nivel}">
                        <div class="alert-title {nivel}">⚠ {alerta['tipo']}</div>
                        <div class="alert-body">{alerta['msg']}</div>
                    </div>
                    """, unsafe_allow_html=True)
                st.markdown("<br>", unsafe_allow_html=True)

            # Charts do deputado
            col_g1, col_g2 = st.columns(2)
            with col_g1:
                st.markdown('<div class="section-header amber"><span class="dot"></span> GASTOS POR CATEGORIA</div>', unsafe_allow_html=True)
                if 'txtDescricao' in df_dep.columns:
                    cat_dep = df_dep.groupby('txtDescricao')['vlrLiquido'].sum().sort_values(ascending=True)
                    fig = go.Figure(go.Bar(x=cat_dep.values, y=cat_dep.index, orientation='h',
                        marker_color='#d4a03a', marker_line_width=0))
                    fig.update_layout(**PLOT_LAYOUT, height=320)
                    st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})

            with col_g2:
                st.markdown('<div class="section-header teal"><span class="dot"></span> TOP FORNECEDORES</div>', unsafe_allow_html=True)
                if 'txtFornecedor' in df_dep.columns:
                    top_forn = df_dep.groupby('txtFornecedor')['vlrLiquido'].sum().sort_values(ascending=False).head(10)
                    fig = go.Figure(go.Bar(x=top_forn.values, y=[f[:30] for f in top_forn.index], orientation='h',
                        marker_color='#3d9996', marker_line_width=0))
                    fig.update_layout(**PLOT_LAYOUT, height=320)
                    st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})

            # Evolução mensal
            st.markdown('<div class="section-header"><span class="dot"></span> EVOLUÇÃO MENSAL DOS GASTOS</div>', unsafe_allow_html=True)
            if 'numAno' in df_dep.columns and 'numMes' in df_dep.columns:
                df_dep['periodo'] = df_dep['numAno'].astype(str) + '-' + df_dep['numMes'].astype(str).str.zfill(2)
                mensal_dep = df_dep.groupby('periodo')['vlrLiquido'].sum().reset_index().sort_values('periodo')
                fig = go.Figure(go.Scatter(x=mensal_dep['periodo'], y=mensal_dep['vlrLiquido'],
                    fill='tozeroy', fillcolor='rgba(224,69,69,0.08)', line=dict(color='#e04545', width=2), mode='lines+markers',
                    marker=dict(size=5, color='#e04545')))
                fig.update_layout(**PLOT_LAYOUT, height=220)
                st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})

            # Tabela de transações
            with st.expander("VER TODAS AS TRANSAÇÕES"):
                cols_show = [c for c in ['datEmissao','txtDescricao','txtFornecedor','txtCNPJCPF','vlrLiquido'] if c in df_dep.columns]
                df_show = df_dep[cols_show].sort_values('vlrLiquido', ascending=False)
                if 'vlrLiquido' in df_show.columns:
                    df_show['vlrLiquido'] = df_show['vlrLiquido'].apply(lambda v: f"R$ {v:,.2f}".replace(",","X").replace(".",",").replace("X","."))
                st.dataframe(df_show.rename(columns={'datEmissao':'Data','txtDescricao':'Categoria','txtFornecedor':'Fornecedor','txtCNPJCPF':'CNPJ/CPF','vlrLiquido':'Valor'}), use_container_width=True)

# ══════════════════════════════════════════════
# TAB 4 — COMPARAR DEPUTADOS
# ══════════════════════════════════════════════
with tab_comparar:
    st.markdown('<div class="section-header"><span class="dot"></span> COMPARAR DEPUTADOS LADO A LADO</div>', unsafe_allow_html=True)

    df = st.session_state.ceap_df
    if df.empty:
        st.info("Carregue os dados na aba Visão Geral primeiro.")
    else:
        nomes = sorted(df['txNomeParlamentar'].dropna().unique().tolist()) if 'txNomeParlamentar' in df.columns else []

        col_s1, col_s2 = st.columns(2)
        with col_s1:
            dep_a = st.selectbox("Deputado A", nomes, key="comp_a")
        with col_s2:
            dep_b = st.selectbox("Deputado B", nomes, index=min(1, len(nomes)-1), key="comp_b")

        if dep_a and dep_b and dep_a != dep_b:
            dfa = df[df['txNomeParlamentar'] == dep_a]
            dfb = df[df['txNomeParlamentar'] == dep_b]

            def get_stats(d, nome):
                total = d['vlrLiquido'].sum()
                n = len(d)
                forn = d['txtFornecedor'].nunique() if 'txtFornecedor' in d.columns else 0
                partido = d['sgPartido'].iloc[0] if 'sgPartido' in d.columns and len(d) > 0 else 'N/D'
                uf = d['sgUF'].iloc[0] if 'sgUF' in d.columns and len(d) > 0 else 'N/D'
                return {'nome': nome, 'total': total, 'n': n, 'forn': forn, 'media': total/n if n>0 else 0, 'partido': partido, 'uf': uf}

            sa, sb = get_stats(dfa, dep_a), get_stats(dfb, dep_b)

            # KPI comparison
            metrics = [('Total Gasto', 'total', formatar_brl), ('Nº de Notas', 'n', lambda v: f"{v:,}"), ('Fornecedores', 'forn', lambda v: f"{v:,}"), ('Média/Nota', 'media', formatar_brl)]
            for label, key, fmt in metrics:
                c1, c2, c3 = st.columns([2,1,2])
                val_a = sa[key]
                val_b = sb[key]
                color_a = 'red' if val_a > val_b else 'teal'
                color_b = 'red' if val_b > val_a else 'teal'
                with c1:
                    st.markdown(f'<div class="stat-card" style="text-align:right"><div class="stat-label">{dep_a[:25]}</div><div class="stat-value {color_a}">{fmt(val_a)}</div></div>', unsafe_allow_html=True)
                with c2:
                    st.markdown(f'<div style="text-align:center;padding-top:1.2rem;font-family:var(--font-mono);font-size:0.65rem;color:var(--text-muted);text-transform:uppercase;letter-spacing:0.1em">{label}</div>', unsafe_allow_html=True)
                with c3:
                    st.markdown(f'<div class="stat-card"><div class="stat-label">{dep_b[:25]}</div><div class="stat-value {color_b}">{fmt(val_b)}</div></div>', unsafe_allow_html=True)

            st.markdown("<br>", unsafe_allow_html=True)

            # Radar chart
            st.markdown('<div class="section-header teal"><span class="dot"></span> COMPARAÇÃO POR CATEGORIA</div>', unsafe_allow_html=True)
            if 'txtDescricao' in df.columns:
                cats_a = dfa.groupby('txtDescricao')['vlrLiquido'].sum()
                cats_b = dfb.groupby('txtDescricao')['vlrLiquido'].sum()
                all_cats = list(set(cats_a.index.tolist() + cats_b.index.tolist()))

                fig = go.Figure()
                fig.add_trace(go.Scatterpolar(r=[cats_a.get(c, 0) for c in all_cats] + [cats_a.get(all_cats[0], 0)],
                    theta=all_cats + [all_cats[0]], fill='toself', name=dep_a[:20],
                    line_color='#e04545', fillcolor='rgba(224,69,69,0.15)'))
                fig.add_trace(go.Scatterpolar(r=[cats_b.get(c, 0) for c in all_cats] + [cats_b.get(all_cats[0], 0)],
                    theta=all_cats + [all_cats[0]], fill='toself', name=dep_b[:20],
                    line_color='#3d9996', fillcolor='rgba(61,153,150,0.15)'))
                fig.update_layout(**PLOT_LAYOUT, height=400, polar=dict(bgcolor='rgba(0,0,0,0)',
                    radialaxis=dict(visible=True, gridcolor='#232328', tickfont=dict(color='#7a7c88', size=8)),
                    angularaxis=dict(gridcolor='#232328', tickfont=dict(color='#9a9ca8', size=9))))
                st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})

# ══════════════════════════════════════════════
# TAB 5 — ANOMALIAS IA
# ══════════════════════════════════════════════
with tab_anomalias:
    st.markdown('<div class="section-header"><span class="dot"></span> SCANNER DE ANOMALIAS — TODOS OS DEPUTADOS</div>', unsafe_allow_html=True)

    df = st.session_state.ceap_df
    if df.empty:
        st.info("Carregue os dados na aba Visão Geral primeiro.")
    else:
        if st.button("🔬 Executar Scanner de Anomalias (todos os deputados)", key="btn_scan"):
            deps_lista_nomes = df['txNomeParlamentar'].dropna().unique().tolist() if 'txNomeParlamentar' in df.columns else []
            resultados = []
            prog = st.progress(0, text="Analisando deputados...")

            for i, nome in enumerate(deps_lista_nomes):
                prog.progress((i+1)/len(deps_lista_nomes), text=f"Analisando {nome[:30]}...")
                df_dep = df[df['txNomeParlamentar'] == nome]
                alertas = detectar_anomalias(df_dep)
                if alertas:
                    partido = df_dep['sgPartido'].iloc[0] if 'sgPartido' in df_dep.columns else 'N/D'
                    uf = df_dep['sgUF'].iloc[0] if 'sgUF' in df_dep.columns else 'N/D'
                    total = df_dep['vlrLiquido'].sum()
                    for a in alertas:
                        resultados.append({'Deputado': nome, 'Partido': partido, 'UF': uf, 'Total': formatar_brl(total), 'Alerta': a['tipo'], 'Nível': a['nivel'].upper(), 'Detalhe': a['msg'][:80]})

            prog.empty()
            if resultados:
                df_res = pd.DataFrame(resultados)
                n_red = len(df_res[df_res['Nível'] == 'RED'])
                n_amb = len(df_res[df_res['Nível'] == 'AMBER'])

                c1, c2, c3 = st.columns(3)
                with c1:
                    st.markdown(f'<div class="stat-card"><div class="stat-label">Alertas Críticos</div><div class="stat-value red">{n_red}</div></div>', unsafe_allow_html=True)
                with c2:
                    st.markdown(f'<div class="stat-card"><div class="stat-label">Alertas de Atenção</div><div class="stat-value amber">{n_amb}</div></div>', unsafe_allow_html=True)
                with c3:
                    st.markdown(f'<div class="stat-card"><div class="stat-label">Deputados Sinalizados</div><div class="stat-value">{df_res["Deputado"].nunique()}</div></div>', unsafe_allow_html=True)

                st.markdown("<br>", unsafe_allow_html=True)

                # Gráfico de tipos de alerta
                tipo_count = df_res['Alerta'].value_counts()
                fig = go.Figure(go.Bar(x=tipo_count.index, y=tipo_count.values,
                    marker_color=['#e04545','#d4a03a','#3d9996','#4682b4'][:len(tipo_count)], marker_line_width=0))
                fig.update_layout(**PLOT_LAYOUT, height=200, title_text="DISTRIBUIÇÃO DE ALERTAS")
                st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})

                st.dataframe(df_res, use_container_width=True, hide_index=True)
            else:
                st.success("Nenhuma anomalia significativa detectada nos dados carregados.")

        st.markdown("""
        <div class="alert-teal">
            <div class="alert-title teal">METODOLOGIA DE DETECÇÃO</div>
            <div class="alert-body">
                <b>Lei de Benford:</b> Analisa se os primeiros dígitos dos valores seguem a distribuição logarítmica natural. Desvios indicam possível manipulação.<br><br>
                <b>HHI (Índice Herfindahl-Hirschman):</b> Mede concentração de gastos em poucos fornecedores. HHI > 2500 indica alta concentração suspeita.<br><br>
                <b>Valores Redondos:</b> Alta proporção de valores exatos (múltiplos de R$500/1000) pode indicar estimativas irregulares.<br><br>
                <b>Gastos em Fim de Semana:</b> Proporção acima de 15% de notas emitidas em sábados/domingos é atípica.
            </div>
        </div>
        """, unsafe_allow_html=True)

# ══════════════════════════════════════════════
# TAB 6 — AO VIVO (API REST Câmara)
# ══════════════════════════════════════════════
with tab_live:
    st.markdown('<div class="section-header"><span class="dot"></span> CÂMARA AO VIVO — DADOS EM TEMPO REAL</div>', unsafe_allow_html=True)

    col_live1, col_live2 = st.columns(2)

    with col_live1:
        st.markdown('<div class="section-header amber"><span class="dot"></span> VOTAÇÕES RECENTES</div>', unsafe_allow_html=True)
        with st.spinner("Buscando votações..."):
            votacoes = fetch_votacoes_recentes()
        if not votacoes.empty:
            cols_v = [c for c in ['dataHoraRegistro', 'descricao', 'siglaOrgao'] if c in votacoes.columns]
            if cols_v:
                st.dataframe(votacoes[cols_v].rename(columns={'dataHoraRegistro':'Data/Hora','descricao':'Descrição','siglaOrgao':'Órgão'}).head(10), use_container_width=True, hide_index=True)
        else:
            st.markdown('<div class="alert-amber"><div class="alert-body">Dados indisponíveis no momento.</div></div>', unsafe_allow_html=True)

    with col_live2:
        st.markdown('<div class="section-header teal"><span class="dot"></span> PROPOSIÇÕES RECENTES (30 DIAS)</div>', unsafe_allow_html=True)
        with st.spinner("Buscando proposições..."):
            proposicoes = fetch_proposicoes_recentes()
        if not proposicoes.empty:
            cols_p = [c for c in ['siglaTipo','numero','ano','ementa'] if c in proposicoes.columns]
            if cols_p:
                st.dataframe(proposicoes[cols_p].rename(columns={'siglaTipo':'Tipo','numero':'Nº','ano':'Ano','ementa':'Ementa'}).head(10), use_container_width=True, hide_index=True)
        else:
            st.markdown('<div class="alert-teal"><div class="alert-body">Dados indisponíveis no momento.</div></div>', unsafe_allow_html=True)

    # Partidos
    st.markdown('<div class="section-header"><span class="dot"></span> PARTIDOS COM REPRESENTAÇÃO ATUAL</div>', unsafe_allow_html=True)
    with st.spinner("Buscando partidos..."):
        partidos = fetch_partidos()
    if not partidos.empty:
        cols_part = [c for c in ['sigla', 'nome', 'lider'] if c in partidos.columns]
        if not cols_part:
            cols_part = list(partidos.columns[:4])
        # partido chart
        if 'sigla' in partidos.columns and not st.session_state.ceap_df.empty:
            df_temp = st.session_state.ceap_df
            if 'sgPartido' in df_temp.columns:
                part_gastos = df_temp.groupby('sgPartido')['vlrLiquido'].sum().sort_values(ascending=False).head(20)
                fig = go.Figure(go.Bar(
                    x=part_gastos.index, y=part_gastos.values,
                    marker_color=[COLORS[i % len(COLORS)] for i in range(len(part_gastos))],
                    marker_line_width=0,
                ))
                fig.update_layout(**PLOT_LAYOUT, height=280, title_text="TOTAL GASTO POR PARTIDO")
                st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
        st.dataframe(partidos[cols_part].head(20), use_container_width=True, hide_index=True)

    # Footer
    st.markdown("""
    <br>
    <div style="border-top:1px solid var(--border);padding-top:1rem;display:flex;justify-content:space-between;align-items:center">
        <div style="font-family:var(--font-mono);font-size:0.6rem;color:var(--text-muted)">
            OLHO DE DEUS · Dados: Câmara dos Deputados · dadosabertos.camara.leg.br · CC0 Domínio Público
        </div>
        <div style="font-family:var(--font-mono);font-size:0.6rem;color:var(--text-muted)">
            Atualizado: {dt}
        </div>
    </div>
    """.format(dt=datetime.now().strftime('%d/%m/%Y %H:%M')), unsafe_allow_html=True)
