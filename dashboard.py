
# Para rodar: streamlit run dashboard.py
# Dependências: pip install streamlit plotly pandas numpy

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from pathlib import Path
import unicodedata


# Configurações da página
st.set_page_config(
    page_title="Análise dos dados | empresa hipotética",
    page_icon="🛍️",
    layout="wide",
    initial_sidebar_state="expanded"
)


# Paleta de cores padrão
C = {
    "fundo":       "#06025e",
    "card":        "#0d0c6b",
    "card_borda":  "#1e1c8a",
    "roxo":        "#9900ff",
    "amarelo":     "#FFD700",
    "azul":        "#00BFFF",
    "laranja":     "#FF9900",
    "verde":       "#00e676",
    "vermelho":    "#FF4444",
    "texto":       "#FFFFFF",
    "texto_muted": "#9999cc",
}


# Template Plotly
PLOTLY_TEMPLATE = dict(
    layout=dict(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color=C["texto"], family="'Segoe UI', sans-serif"),
        xaxis=dict(gridcolor="rgba(255,255,255,1)", zerolinecolor="rgba(255,255,255,1)", automargin=True),
        yaxis=dict(gridcolor="rgba(255,255,255,1)", zerolinecolor="rgba(255,255,255,1)", automargin=True),
        legend=dict(bgcolor="rgba(0,0,0,0)", bordercolor="rgba(255,255,255,1)", font=dict(color=C["texto"])),
        margin=dict(t=40, b=10, l=10, r=140),
        hoverlabel=dict(bgcolor="#1a1850", font_color="rgba(255,255,255,1)", font_size=13),
    )
)

# CSS Global (ajustes finais)
st.markdown(f"""
<style>
  @import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;600;700;800&display=swap');

  html, body, [class*="css"] {{
      font-family: 'Space Grotesk', sans-serif;
      background-color: {C["fundo"]} !important;
      color: {C["texto"]} !important;
  }}
  [data-testid="stAppViewContainer"] {{ background-color: {C["fundo"]}; }}
  [data-testid="stSidebar"] {{
      background: linear-gradient(180deg, #030240 0%, #06025e 100%);
      border-right: 1px solid {C["card_borda"]};
  }}
  [data-testid="stSidebar"] * {{ color: {C["texto"]} !important; }}

  .stTabs [data-baseweb="tab"] {{
      color: {C["texto"]} !important;
  }}
  .stTabs [aria-selected="true"] {{
      color: {C["texto"]} !important;
  }}

  /* Botões e selects na sidebar */
  section[data-testid="stSidebar"] button, section[data-testid="stSidebar"] .stButton > button {{
      background-color: {C["card"]} !important;
      color: {C["texto"]} !important;
      border: 1px solid {C["card_borda"]} !important;
      border-radius: 8px;
      padding: 6px 10px;
  }}
  section[data-testid="stSidebar"] .stSelectbox, 
  section[data-testid="stSidebar"] .stMultiSelect,
  section[data-testid="stSidebar"] .stSelectbox div[role="button"],
  section[data-testid="stSidebar"] .stMultiSelect div[role="button"] {{
    background-color: #0d0c6b !important;
    color: #FFFFFF !important;
  }}
  section[data-testid="stSidebar"] .stSelectbox span,
  section[data-testid="stSidebar"] .stMultiSelect span {{
    color: #FFFFFF !important;
  }}

  /* Tags selecionadas na sidebar com fundo vermelho */
  section[data-testid="stSidebar"] div[data-baseweb="tag"] {{
      background-color: {C["vermelho"]} !important;
      color: white !important;
      border-radius: 6px !important;
  }}
  section[data-testid="stSidebar"] div[data-baseweb="tag"] span {{ color: white !important; font-weight:700; }}

  .alerta-causa {{
      background: linear-gradient(135deg, #001a66 0%, #0d0c6b 100%);
      border: 1px solid {C["azul"]};
      border-left: 4px solid {C["azul"]};
      border-radius: 8px; padding: 16px 20px; margin-bottom: 16px;
      color: {C["texto"]};
  }}
  .alerta-causa strong {{ color: {C["azul"]}; }}

  /* Cards e layout */
  .kpi-grid {{ display: grid; grid-template-columns: repeat(6, 1fr); gap: 12px; margin-bottom: 24px; }}
  .kpi-card {{
      background: linear-gradient(135deg, {C["card"]} 0%, #0a094f 100%);
      border: 1px solid {C["card_borda"]};
      border-radius: 12px;
      padding: 16px 14px;
      position: relative;
      overflow: hidden;
      transition: transform 0.2s;
  }}
  .kpi-card::before {{
      content: '';
      position: absolute; top: 0; left: 0; right: 0; height: 3px;
      background: var(--accent);
  }}
  .kpi-card:hover {{ transform: translateY(-2px); }}
  .kpi-label {{ font-size: 10px; font-weight: 700; letter-spacing: 1px; color: {C["texto_muted"]}; text-transform: uppercase; margin-bottom: 6px; }}
  .kpi-value {{ font-size: 22px; font-weight: 800; color: {C["texto"]}; line-height: 1.1; }}
  .kpi-sub {{ font-size: 11px; color: {C["texto"]}; margin-top: 4px; }}
  .kpi-icon {{ position: absolute; top: 12px; right: 12px; font-size: 20px; opacity: 0.4; }}

  .chart-card {{
      background: linear-gradient(135deg, {C["card"]} 0%, #0a094f 100%);
      border: 1px solid {C["card_borda"]};
      border-radius: 12px;
      padding: 20px;
      margin-bottom: 16px;
  }}
  .chart-title {{
      font-size: 13px; font-weight: 700; letter-spacing: 0.5px;
      color: {C["texto"]}; text-transform: uppercase; margin-bottom: 4px;
  }}
  .chart-subtitle {{ font-size: 17px; font-weight: 700; color: {C["texto"]}; margin-bottom: 16px; }}

  .insight-box {{
      background: linear-gradient(135deg, #1a0050 0%, #0d0c6b 100%);
      border: 1px solid {C["roxo"]};
      border-radius: 12px; padding: 20px 24px;
  }}
  .insight-box h4 {{ color: {C["roxo"]} !important; margin: 0 0 12px 0; font-size: 14px; letter-spacing: 1px; text-transform: uppercase; }}
  .insight-box li {{ color: {C["texto"]}; font-size: 14px; line-height: 1.8; }}

  .stDataFrame {{ border-radius: 8px; overflow: hidden; }}
  div[data-testid="stDataFrameResizable"] {{ border: 1px solid {C["card_borda"]}; border-radius: 8px; }}

  hr {{ border-color: {C['card_borda']}; margin: 20px 0; }}
  ::-webkit-scrollbar {{ width: 6px; }}
  ::-webkit-scrollbar-track {{ background: {C['fundo']}; }}
  ::-webkit-scrollbar-thumb {{ background: {C['card_borda']}; border-radius: 3px; }}
</style>
""", unsafe_allow_html=True)

# Função para carregar dados 
@st.cache_data
def carregar_dados():
    """
    Carrega os CSV e retorna dicionário com bases.
    """
    possiveis = [
        Path("base_dados"),
        Path("../base_dados"),
        Path("notebooks/base_dados"),
    ]
    base = next((p for p in possiveis if p.exists()), Path("."))

    def normalizar(s):
        """Remove acentos e coloca em minúsculo """
        if pd.isna(s): return s
        return unicodedata.normalize('NFKD', str(s)).encode('ASCII','ignore').decode().lower().strip()

    pedidos    = pd.read_csv(base / "pedidos.csv",         parse_dates=["data_pedido"])
    clientes   = pd.read_csv(base / "clientes.csv",        parse_dates=["data_cadastro"])
    produtos   = pd.read_csv(base / "produtos.csv")
    itens      = pd.read_csv(base / "itens_pedido.csv")
    tickets    = pd.read_csv(base / "tickets_suporte.csv", parse_dates=["data_abertura","data_resolucao"])
    avaliacoes = pd.read_csv(base / "avaliacoes.csv")

    pedidos["valor_total"] = pedidos.groupby("canal_venda")["valor_total"].transform(
        lambda x: x.fillna(x.median())
    )
    itens["desconto_aplicado"]   = itens["desconto_aplicado"].fillna(0)
    itens["valor_liquido_item"]  = (
        itens["preco_praticado"] * itens["quantidade"] * (1 - itens["desconto_aplicado"])
    ).round(2)
    tickets["tempo_resolucao_dias"] = (tickets["data_resolucao"] - tickets["data_abertura"]).dt.days

    for col in ["canal_aquisicao"]:
        clientes[col] = clientes[col].apply(normalizar)
    for col in ["status", "canal_venda"]:
        pedidos[col] = pedidos[col].apply(normalizar)

    df = pedidos.merge(
        clientes[["id","segmento","canal_aquisicao","estado","cidade"]],
        left_on="cliente_id", right_on="id", suffixes=("","_cli")
    )
    df["Ano"]       = df["data_pedido"].dt.year.astype(int)
    df["Mes"]       = df["data_pedido"].dt.month.astype(int)
    df["Trimestre"] = df["data_pedido"].dt.quarter.astype(int)
    df["Ano_Mes"]   = df["data_pedido"].dt.to_period("M").astype(str)
    df["Periodo_Q"] = df["data_pedido"].dt.to_period("Q").astype(str)
    meses = {1:"Jan",2:"Fev",3:"Mar",4:"Abr",5:"Mai",6:"Jun",
             7:"Jul",8:"Ago",9:"Set",10:"Out",11:"Nov",12:"Dez"}
    df["Mes_Nome"]  = df["Mes"].map(meses)

    produtos["margem_pct"] = (
        (produtos["preco_unitario"] - produtos["custo_unitario"])
        / produtos["preco_unitario"] * 100
    ).round(2)

    tickets_enr = tickets.merge(
        clientes[["id","canal_aquisicao","segmento"]], left_on="cliente_id", right_on="id"
    )
    tickets_enr["Ano_Mes"] = tickets_enr["data_abertura"].dt.to_period("M").astype(str)
    tickets_enr["Ano"]     = tickets_enr["data_abertura"].dt.year.astype(int)
    tickets_enr["Mes"]     = tickets_enr["data_abertura"].dt.month.astype(int)

    av_enr = avaliacoes.merge(
        pedidos[["id","status","canal_venda"]], left_on="pedido_id", right_on="id", suffixes=("","_ped")
    ).merge(
        clientes[["id","canal_aquisicao","segmento"]], left_on="cliente_id", right_on="id", suffixes=("","_cli")
    )

    return {
        "df":        df,
        "itens":     itens,
        "produtos":  produtos,
        "tickets":   tickets_enr,
        "avaliacoes":av_enr,
        "clientes":  clientes,
    }

# Carrega dados 
dados = carregar_dados()
df_raw    = dados["df"]
itens     = dados["itens"]
produtos  = dados["produtos"]
tickets   = dados["tickets"]
avaliacoes= dados["avaliacoes"]

anos_disponiveis = sorted(df_raw["Ano"].unique().tolist())
ano_opts = [a for a in anos_disponiveis if a in (2023, 2024)]
if not ano_opts:
    ano_opts = anos_disponiveis  # fallback

seg_opts = sorted(df_raw["segmento"].dropna().unique().tolist())
canal_opts = sorted(df_raw["canal_aquisicao"].dropna().unique().tolist())
cvenda_opts = sorted(df_raw["canal_venda"].dropna().unique().tolist())

# Inicializa session_state com defaults caso não existam
if "ano_sel" not in st.session_state:
    st.session_state["ano_sel"] = ano_opts.copy()
if "seg_sel" not in st.session_state:
    st.session_state["seg_sel"] = seg_opts.copy()
if "canal_sel" not in st.session_state:
    st.session_state["canal_sel"] = canal_opts.copy()
if "cvenda_sel" not in st.session_state:
    st.session_state["cvenda_sel"] = cvenda_opts.copy()

# Callback para resetar filtros
def reset_filters():
    st.session_state["ano_sel"] = ano_opts.copy()
    st.session_state["seg_sel"] = seg_opts.copy()
    st.session_state["canal_sel"] = canal_opts.copy()
    st.session_state["cvenda_sel"] = cvenda_opts.copy()
    
with st.sidebar:
    st.markdown(f"""
    <div style="text-align:center; padding: 0 0 18px 0;">
        <div style="font-size:18px; font-weight:800; color:{C['texto']};">Empresa Hipotética</div>
        <div style="font-size:11px; color:{C['texto']}; letter-spacing:2px;">ANALYTICS DASHBOARD</div>
    </div>
    <hr style="border-color:{C['card_borda']}; margin-bottom:12px;">
    """, unsafe_allow_html=True)

    st.markdown(f"<div style='font-size:11px;font-weight:700;letter-spacing:1px;color:{C['texto']};text-transform:uppercase;margin-bottom:6px;'>Período</div>", unsafe_allow_html=True)
    st.multiselect("", options=ano_opts, default=st.session_state["ano_sel"], key="ano_sel", label_visibility="collapsed")

    st.markdown(f"<div style='font-size:11px;font-weight:700;letter-spacing:1px;color:{C['texto']};text-transform:uppercase;margin:12px 0 6px 0;'>Segmento</div>", unsafe_allow_html=True)
    st.multiselect("", options=seg_opts, default=st.session_state["seg_sel"], key="seg_sel", label_visibility="collapsed")

    st.markdown(f"<div style='font-size:11px;font-weight:700;letter-spacing:1px;color:{C['texto']};text-transform:uppercase;margin:12px 0 6px 0;'>Canal de Aquisição</div>", unsafe_allow_html=True)
    st.multiselect("", options=canal_opts, default=st.session_state["canal_sel"], key="canal_sel", label_visibility="collapsed")

    st.markdown(f"<div style='font-size:11px;font-weight:700;letter-spacing:1px;color:{C['texto']};text-transform:uppercase;margin:12px 0 6px 0;'>Canal de Venda</div>", unsafe_allow_html=True)
    st.multiselect("", options=cvenda_opts, default=st.session_state["cvenda_sel"], key="cvenda_sel", label_visibility="collapsed")

    st.markdown("<br>", unsafe_allow_html=True)
    st.button("🔄  Resetar filtros", use_container_width=True, on_click=reset_filters)

    st.markdown(f"""
    <hr style="border-color:{C['card_borda']}; margin-top:12px;">
    <div style="font-size:10px;color:{C['texto']};text-align:center;">
        · Empresa Hipotética<br>Base: 15.000 pedidos · 2023–2024
    </div>
    """, unsafe_allow_html=True)

# Recupera seleções a partir do session_state
ano_sel = st.session_state.get("ano_sel", ano_opts)
seg_sel = st.session_state.get("seg_sel", seg_opts)
canal_sel = st.session_state.get("canal_sel", canal_opts)
cvenda_sel = st.session_state.get("cvenda_sel", cvenda_opts)

# Exige ao menos uma opção em cada filtro
if not ano_sel or not seg_sel or not canal_sel or not cvenda_sel:
    st.warning("⚠️ Selecione ao menos uma opção em cada filtro.")
    st.stop()

# Aplica filtros
df = df_raw.copy()
df = df[df["Ano"].isin(ano_sel)]
df = df[df["segmento"].isin(seg_sel) & df["canal_aquisicao"].isin(canal_sel) & df["canal_venda"].isin(cvenda_sel)]

pedidos_ids = set(df["id"].tolist())
tk = tickets[tickets["pedido_id"].isin(pedidos_ids)] if "pedido_id" in tickets.columns else tickets
av = avaliacoes[avaliacoes["pedido_id"].isin(pedidos_ids)] if "pedido_id" in avaliacoes.columns else avaliacoes

# configurações padrões para todas as abas
itens_status = itens.merge(df[["id","status"]], left_on="pedido_id", right_on="id", how="inner")

agg_prod = itens_status.groupby("produto_id").agg(
    Total_Unidades=("quantidade","sum"),
    Receita_Total=("valor_liquido_item","sum"),
).reset_index().merge(
    produtos[["id","nome","categoria","subcategoria","margem_pct"]],
    left_on="produto_id", right_on="id", how="left"
).sort_values("Total_Unidades", ascending=False)


# KPIs
st.markdown(f"""
<div style="display:flex; align-items:baseline; gap:16px; margin-bottom:8px;">
    <h1 style="margin:0; font-size:28px; font-weight:800; color:{C['texto']};">. Analytics Dashboard</h1>
    <span style="font-size:13px; color:{C['texto']};">· Empresa</span>
</div>
<p style="color:{C['texto']}; font-size:13px; margin-bottom:24px;">
    Análise exploratória de 15.000 pedidos (2023–2024) para identificação de causa raiz de cancelamentos.
    {'<b style="color:'+C['amarelo']+';">Filtro ativo: '+", ".join(map(str,ano_sel))+'</b>' if ano_sel else ''}
</p>
""", unsafe_allow_html=True)

total_pedidos  = len(df)
receita_total  = df["valor_total"].sum()
ticket_medio   = df["valor_total"].mean()
taxa_cancel    = (df["status"] == "cancelado").mean() * 100
taxa_devolv    = (df["status"] == "devolvido").mean() * 100
nota_media     = av["nota"].mean() if len(av) else 0
total_tickets  = len(tk)
taxa_resolucao = (tk["status"] == "resolvido").mean() * 100 if len(tk) else 0

# Variação YoY
yoy_txt = ""
if set([2023,2024]).issubset(set(df_raw["Ano"].unique())) and set([2023,2024]).issubset(set(df["Ano"].unique())):
    r23 = df[df["Ano"]==2023]["valor_total"].sum() if 2023 in df["Ano"].values else 0
    r24 = df[df["Ano"]==2024]["valor_total"].sum() if 2024 in df["Ano"].values else 0
    if r23 > 0:
        yoy = (r24-r23)/r23*100
        sinal = "↑" if yoy > 0 else "↓"
        cor_yoy = C["verde"] if yoy > 0 else C["vermelho"]
        yoy_txt = f'<span style="color:{cor_yoy}">{sinal} {abs(yoy):.1f}% YoY</span>'

st.markdown(f"""
<div class="kpi-grid">
  <div class="kpi-card" style="--accent:{C['roxo']}">
    <span class="kpi-icon">📦</span>
    <div class="kpi-label">Total de Pedidos</div>
    <div class="kpi-value">{total_pedidos:,}</div>
    <div class="kpi-sub">15.000 no período total</div>
  </div>
  <div class="kpi-card" style="--accent:{C['amarelo']}">
    <span class="kpi-icon">💰</span>
    <div class="kpi-label">Receita Total</div>
    <div class="kpi-value">R$ {receita_total/1e6:.2f}M</div>
    <div class="kpi-sub">{yoy_txt if yoy_txt else 'Jan 2023 – Dez 2024'}</div>
  </div>
  <div class="kpi-card" style="--accent:{C['azul']}">
    <span class="kpi-icon">🎟️</span>
    <div class="kpi-label">Ticket Médio</div>
    <div class="kpi-value">R$ {ticket_medio:,.0f}</div>
    <div class="kpi-sub">Mediana: R$ {df['valor_total'].median():,.0f}</div>
  </div>
  <div class="kpi-card" style="--accent:{C['vermelho']}">
    <span class="kpi-icon">❌</span>
    <div class="kpi-label">Taxa Cancelamento</div>
    <div class="kpi-value" style="color:{C['vermelho']}">{taxa_cancel:.1f}%</div>
    <div class="kpi-sub">+ {taxa_devolv:.1f}% devoluções</div>
  </div>
  <div class="kpi-card" style="--accent:{C['laranja']}">
    <span class="kpi-icon">🎧</span>
    <div class="kpi-label">Tickets Suporte</div>
    <div class="kpi-value">{total_tickets:,}</div>
    <div class="kpi-sub">{taxa_resolucao:.0f}% resolvidos</div>
  </div>
  <div class="kpi-card" style="--accent:{C['verde']}">
    <span class="kpi-icon">⭐</span>
    <div class="kpi-label">Avaliação Média</div>
    <div class="kpi-value" style="color:{C['verde']}">{nota_media:.2f}<span style="font-size:13px;color:{C['texto']}"> /5</span></div>
    <div class="kpi-sub">{len(av):,} avaliações</div>
  </div>
</div>
""", unsafe_allow_html=True)

# Nome das abas
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📊  Visao Geral",
    "📦  Produtos e Receita",
    "👥  Clientes e Segmentos",
    "🔴  Causa Raiz",
    "🗂️  Dados Detalhados",
])

# ABA 1 — Visão geral
with tab1:
    col_a, col_b = st.columns([1.1, 0.9])

    # Evolução mensal
    with col_a:
        st.markdown(f"""
        <div class="chart-card">
        <div class="chart-subtitle">Evolução Mensal de Pedidos — 2023 vs 2024</div>
        """, unsafe_allow_html=True)

        evol = df.groupby(["Ano","Mes","Mes_Nome"]).agg(
            Pedidos=("id","count"), Receita=("valor_total","sum")
        ).reset_index().sort_values(["Ano","Mes"])

        fig_evol = go.Figure()
        cores_ano = {2023: C["roxo"], 2024: C["amarelo"]}
        for ano, grp in evol.groupby("Ano"):
            fig_evol.add_trace(go.Scatter(
                x=grp["Mes_Nome"], y=grp["Pedidos"],
                mode="lines+markers",
                name=str(ano),
                line=dict(color=cores_ano.get(ano, C["roxo"]), width=3),
                marker=dict(size=8, symbol="circle"),
                hovertemplate=f"<b>{ano}</b><br>%{{x}}: <b>%{{y:,}}</b> pedidos<extra></extra>",
            ))
        fig_evol.update_layout(**PLOTLY_TEMPLATE["layout"])
        fig_evol.update_layout(
            height=280,
            legend=dict(orientation="h", y=1.15, x=0),
            xaxis=dict(
                categoryorder="array",
                categoryarray=["Jan","Fev","Mar","Abr","Mai","Jun","Jul","Ago","Set","Out","Nov","Dez"],
                automargin=True
            )
        )

        st.plotly_chart(fig_evol, use_container_width=True, config={"displayModeBar": False, "responsive": True})
        st.markdown("</div>", unsafe_allow_html=True)

    # Distribuição de status
    with col_b:
        st.markdown(f"""
        <div class="chart-card">
        <div class="chart-subtitle">Distribuição de Status dos Pedidos</div>
        """, unsafe_allow_html=True)

        status_df = df["status"].value_counts().reset_index()
        status_df.columns = ["Status","Qtd"]
        status_df["Pct"] = (status_df["Qtd"]/status_df["Qtd"].sum()*100).round(2)

        CORES_STATUS = {
            "entregue":    C["roxo"],
            "cancelado":   C["amarelo"],
            "devolvido":   C["laranja"],
            "em_transito": C["azul"],
        }
        status_df["cor"] = status_df["Status"].map(CORES_STATUS)

        fig_rosca = go.Figure(go.Pie(
            labels=status_df["Status"].str.capitalize().str.replace("_"," "),
            values=status_df["Qtd"],
            hole=0.65,
            marker=dict(colors=status_df["cor"], line=dict(color="#06025e", width=3)),
            hovertemplate="<b>%{label}</b><br>%{value:,} pedidos<br>%{percent}<extra></extra>",
            textfont=dict(size=13, color="white"),
        ))
        fig_rosca.add_annotation(
            text=f"<b>{total_pedidos:,}</b><br>pedidos",
            x=0.5, y=0.5, showarrow=False,
            font=dict(size=14, color="white"),
        )

        fig_rosca.update_layout(**PLOTLY_TEMPLATE["layout"])
        fig_rosca.update_layout(
            height=280,
            showlegend=True,
            legend=dict(orientation="h", y=-0.1, x=0.1),
            margin=dict(t=40, b=10, l=10, r=120)
        )

        st.plotly_chart(fig_rosca, use_container_width=True, config={"displayModeBar": False, "responsive": True})
        st.markdown("</div>", unsafe_allow_html=True)

    # Volume vs Taxa de cancelamento por mês
    st.markdown(f"""
    <div class="chart-card">
    <div class="chart-subtitle">Volume de Pedidos vs. Taxa de Cancelamento por Mês</div>
    """, unsafe_allow_html=True)

    cancel_mes = df.groupby(["Ano","Mes","Mes_Nome"]).agg(
        Total=("id","count"),
        Cancelados=("status", lambda x:(x=="cancelado").sum()),
    ).reset_index()
    cancel_mes["Taxa_Cancel"] = (cancel_mes["Cancelados"]/cancel_mes["Total"]*100).round(2)
    cancel_mes = cancel_mes.sort_values(["Ano","Mes"])
    cancel_mes["Periodo"] = cancel_mes["Mes_Nome"] + " " + cancel_mes["Ano"].astype(str)

    fig_dual = make_subplots(specs=[[{"secondary_y": True}]])
    fig_dual.add_trace(go.Bar(
        x=cancel_mes["Periodo"], y=cancel_mes["Total"],
        name="Volume de Pedidos", marker_color=C["roxo"], opacity=0.75,
        hovertemplate="<b>%{x}</b><br>Pedidos: <b>%{y:,}</b><extra></extra>",
    ), secondary_y=False)
    fig_dual.add_trace(go.Scatter(
        x=cancel_mes["Periodo"], y=cancel_mes["Taxa_Cancel"],
        name="% Cancelamento", mode="lines+markers",
        line=dict(color=C["amarelo"], width=2.5),
        marker=dict(size=7),
        hovertemplate="<b>%{x}</b><br>Cancelamento: <b>%{y:.1f}%</b><extra></extra>",
    ), secondary_y=True)

    fig_dual.update_layout(**PLOTLY_TEMPLATE["layout"])
    fig_dual.update_layout(
        height=300,
        legend=dict(orientation="h", y=1.12, x=0),
        margin=dict(t=40, b=40, l=40, r=120)
    )

    fig_dual.update_yaxes(title_text="Nº de Pedidos", secondary_y=False,
                          gridcolor="rgba(255,255,255,0.07)", title_font_color=C["roxo"])
    fig_dual.update_yaxes(title_text="Taxa de Cancelamento (%)", secondary_y=True,
                          gridcolor="rgba(255,255,255,0)", title_font_color=C["amarelo"])
    st.plotly_chart(fig_dual, use_container_width=True, config={"displayModeBar": False, "responsive": True})
    st.markdown("</div>", unsafe_allow_html=True)

    # Insight — Sazonalidade 
    st.markdown("""
    <div class="insight-box" style="margin-top:8px;">
        <h4>Insight — Sazonalidade</h4>
        <ul>
            <li>Ao plotar a curva de evolução de pedidos, é possível observar um padrão de sazonalidade que se repete em ambos os anos.</li>
            <li>Os meses de Fevereiro/Março representam o período de menor volume de pedidos (pós-festas). A hipótese é que o consumidor está descapitalizado em decorrência das festas de final de ano.</li>
            <li>É um momento interessante para focar em campanhas de reativação de clientes antigos e ofertas em produtos com menor ticket médio.</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

# ABA 2 — Produtos e receita
with tab2:
    top10 = agg_prod.head(10).copy()

    col1, col2 = st.columns(2)

    with col1:
        st.markdown(f"""
        <div class="chart-card">
        <div class="chart-subtitle">Top 10 — Unidades Vendidas</div>
        """, unsafe_allow_html=True)

        fig_top = go.Figure(go.Bar(
            x=top10["Total_Unidades"][::-1],
            y=top10["nome"].apply(lambda x: x[:22]+"…" if len(x)>22 else x)[::-1],
            orientation="h",
            marker=dict(
                color=top10["Total_Unidades"][::-1],
                colorscale=[[0, "#3d0099"],[1, C["roxo"]]],
                showscale=False,
            ),
            text=top10["Total_Unidades"][::-1].apply(lambda x: f"{x:,}"),
            textposition="outside",
            textfont=dict(color="white", size=11),
            hovertemplate="<b>%{y}</b><br>Unidades: <b>%{x:,}</b><extra></extra>",
        ))
        fig_top.update_layout(**PLOTLY_TEMPLATE["layout"])
        fig_top.update_layout(
            height=350,
            xaxis=dict(showgrid=False, automargin=True),
            yaxis=dict(showgrid=False),
            margin=dict(t=40, b=10, l=10, r=120)
        )
        fig_top.update_traces(textposition='outside', cliponaxis=False)
        st.plotly_chart(fig_top, use_container_width=True, config={"displayModeBar": False, "responsive": True})
        st.markdown("</div>", unsafe_allow_html=True)

    with col2:
        st.markdown(f"""
        <div class="chart-card">
        <div class="chart-subtitle">Top 10 — Receita Gerada (R$)</div>
        """, unsafe_allow_html=True)

        top10_r = agg_prod.sort_values("Receita_Total", ascending=False).head(10)
        fig_rec = go.Figure(go.Bar(
            x=top10_r["Receita_Total"][::-1],
            y=top10_r["nome"].apply(lambda x: x[:22]+"…" if len(x)>22 else x)[::-1],
            orientation="h",
            marker=dict(
                color=top10_r["Receita_Total"][::-1],
                colorscale=[[0,"#5c4a00"],[1, C["amarelo"]]],
                showscale=False,
            ),
            text=top10_r["Receita_Total"][::-1].apply(lambda v: f"R$ {v/1000:.0f}k"),
            textposition="outside",
            textfont=dict(color="white", size=11),
            hovertemplate="<b>%{y}</b><br>Receita: <b>R$ %{x:,.0f}</b><extra></extra>",
        ))
        fig_rec.update_layout(**PLOTLY_TEMPLATE["layout"])
        fig_rec.update_layout(
            height=350,
            xaxis=dict(showgrid=False, automargin=True),
            yaxis=dict(showgrid=False),
            margin=dict(t=40, b=10, l=10, r=140)
        )
        fig_rec.update_traces(textposition='outside', cliponaxis=False)
        st.plotly_chart(fig_rec, use_container_width=True, config={"displayModeBar": False, "responsive": True})
        st.markdown("</div>", unsafe_allow_html=True)

    # Margem por categoria
    st.markdown(f"""
    <div class="chart-card">
    <div class="chart-subtitle">Margem Bruta Média por Categoria de Produto</div>
    """, unsafe_allow_html=True)

    margem_cat = produtos.groupby("categoria").agg(
        Margem_Media=("margem_pct","mean"),
        Qtd_Produtos=("id","count"),
        Preco_Medio=("preco_unitario","mean"),
    ).reset_index().sort_values("Margem_Media", ascending=True)

    media_geral = margem_cat["Margem_Media"].mean()
    cores_margem = [C["verde"] if v >= media_geral else C["laranja"] for v in margem_cat["Margem_Media"]]

    fig_marg = go.Figure(go.Bar(
        x=margem_cat["Margem_Media"],
        y=margem_cat["categoria"],
        orientation="h",
        marker_color=cores_margem,
        text=margem_cat["Margem_Media"].apply(lambda v: f"{v:.1f}%"),
        textposition="outside",
        textfont=dict(color="white"),
        hovertemplate="<b>%{y}</b><br>Margem: <b>%{x:.1f}%</b><br>Produtos: <b>%{customdata}</b><extra></extra>",
        customdata=margem_cat["Qtd_Produtos"],
    ))
    fig_marg.add_vline(x=media_geral, line_dash="dash", line_color="rgba(255,255,255,0.35)",
                       annotation_text=f"Média: {media_geral:.1f}%", annotation_font_color="white")
    fig_marg.update_layout(**PLOTLY_TEMPLATE["layout"])
    fig_marg.update_layout(
        height=300,
         xaxis=dict(showgrid=False, automargin=True),
         margin=dict(t=40, b=10, l=10, r=120)
    )
    fig_marg.update_traces(textposition='outside', cliponaxis=False)
    st.plotly_chart(fig_marg, use_container_width=True, config={"displayModeBar": False, "responsive": True})
    st.markdown("</div>", unsafe_allow_html=True)

    # Insight — Produtos
    st.markdown("""
    <div class="insight-box" style="margin-top:8px;">
        <h4>Insight — Produtos</h4>
        <ul>
            <li>Ao cruzar a quantidade de produtos vendidos com a receita gerada, percebe-se que nem todos os produtos com mais unidades vendidas são os com maiores receitas e, caso a quantidade de tickets de suporte for alta para esses produtos, temos implicações relevantes para a empresa.</li>
            <li>Uma análise relevante seria verificar qual tipo de produto resulta em mais tickets de suporte. Dessa forma, conseguiríamos verificar se os produtos com mais unidades vendidas, mais receita total ou nenhuma dessas categorias são as que estão causando os altos cancelamentos apresentados.</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)


# ABA 3 — Clientes e segmentos
with tab3:
    seg_stats = df.groupby("segmento").agg(
        Qtd=("id","count"),
        Ticket_Medio=("valor_total","mean"),
        Receita=("valor_total","sum"),
        Cancelados=("status", lambda x:(x=="cancelado").sum()),
        Devolvidos=("status", lambda x:(x=="devolvido").sum()),
    ).reset_index()
    seg_stats["Taxa_Cancel"] = (seg_stats["Cancelados"]/seg_stats["Qtd"]*100).round(2)
    seg_stats["Taxa_Devolv"] = (seg_stats["Devolvidos"]/seg_stats["Qtd"]*100).round(2)

    col_s1, col_s2, col_s3 = st.columns(3)

    with col_s1:
        st.markdown(f"""<div class="chart-card">
        <div class="chart-subtitle">Ticket Médio por Segmento</div>""", unsafe_allow_html=True)

        fig_seg = go.Figure(go.Bar(
            x=seg_stats["segmento"], y=seg_stats["Ticket_Medio"],
            marker_color=[C["roxo"], C["amarelo"]],
            text=seg_stats["Ticket_Medio"].apply(lambda v: f"R$ {v:,.0f}"),
            textposition="outside", textfont=dict(color="white", size=13),
            hovertemplate="<b>%{x}</b><br>Ticket Médio: <b>R$ %{y:,.2f}</b><extra></extra>",
        ))
        fig_seg.update_layout(**PLOTLY_TEMPLATE["layout"])
        fig_seg.update_layout(
             height=280,
             yaxis=dict(showgrid=True, tickprefix="R$ "),
             xaxis=dict(showgrid=False, automargin=True),
             margin=dict(t=40, b=10, l=10, r=120)
        )
        fig_seg.update_traces(textposition='outside', cliponaxis=False)
        st.plotly_chart(fig_seg, use_container_width=True, config={"displayModeBar": False, "responsive": True})
        st.markdown("</div>", unsafe_allow_html=True)

    with col_s2:
        st.markdown(f"""<div class="chart-card">
        <div class="chart-subtitle">Distribuição de Valores (Boxplot)</div>""", unsafe_allow_html=True)

        fig_box = go.Figure()
        cores_box = {"B2C": C["roxo"], "B2B": C["amarelo"]}
        for seg, grp in df.groupby("segmento"):
            fig_box.add_trace(go.Box(
                y=grp["valor_total"], name=seg,
                marker_color=cores_box.get(seg, C["azul"]),
                line_color=cores_box.get(seg, C["azul"]),
                fillcolor=cores_box.get(seg, C["azul"]),
                boxmean=True,
                hovertemplate="<b>"+seg+"</b><br>%{y:,.0f}<extra></extra>",
            ))
        fig_box.update_layout(**PLOTLY_TEMPLATE["layout"])
        fig_box.update_layout(
             height=280,
             yaxis=dict(tickprefix="R$ "), showlegend=True,
             margin=dict(t=40, b=10, l=10, r=120)
        )

        st.plotly_chart(fig_box, use_container_width=True, config={"displayModeBar": False, "responsive": True})
        st.markdown("</div>", unsafe_allow_html=True)

    with col_s3:
        st.markdown(f"""<div class="chart-card">
        <div class="chart-subtitle">Taxa de Cancelamento por Segmento</div>""", unsafe_allow_html=True)

        fig_cancel_seg = go.Figure(go.Bar(
            x=seg_stats["segmento"],
            y=seg_stats["Taxa_Cancel"],
            marker_color=[C["roxo"], C["amarelo"]],
            text=seg_stats["Taxa_Cancel"].apply(lambda v: f"{v:.1f}%"),
            textposition="outside", textfont=dict(color="white", size=13),
            hovertemplate="<b>%{x}</b><br>Cancelamentos: <b>%{y:.2f}%</b><extra></extra>",
        ))
        fig_cancel_seg.update_layout(**PLOTLY_TEMPLATE["layout"])
        fig_cancel_seg.update_layout(
             height=280,
             yaxis=dict(ticksuffix="%", showgrid=True),
             xaxis=dict(showgrid=False, automargin=True),
             margin=dict(t=40, b=10, l=10, r=120)
        )
        fig_cancel_seg.update_traces(textposition='outside', cliponaxis=False)
        st.plotly_chart(fig_cancel_seg, use_container_width=True, config={"displayModeBar": False, "responsive": True})
        st.markdown("</div>", unsafe_allow_html=True)

    # Insight estatístico
    st.markdown(f"""
    <div class="insight-box">
        <h4>Insight — Segmentos e Teste Estatístico</h4>
        <ul>
            <li>Ao tentar formular um teste de hipóteses para verificar se existe diferença estatisticamente relevante entre os dois segmentos, percebi que o volume de pedidos baratos é muito maior do que o volume de pedidos caros, o que impossibilitou usar testes tradicionais (que pressupõem uma distribuição normal para os dados).</li>
            <li>Desse modo, apliquei uma transformação logarítmica com teste T de Welch. O p-valor resultante foi menor do que 0.05, o que permitiu rejeitar H0, evidenciando que a diferença de ticket médio entre B2B e B2C é significativa e estrutural.</li>
            <li>Com o ticket médio do B2B se revelando drasticamente superior ao do B2C, é possível inferir que os clientes B2B são os que mais trazem rentabilidade para a Empresa.</li>
            <li>Se a alta taxa de cancelamentos e devoluções estiver atingindo a base B2B, o faturamento da empresa tende a cair drasticamente. Recomenda-se proteger o segmento B2B com SLA e atendimento dedicado.</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

    # Avaliações por status
    st.markdown(f"""
    <div class="chart-card" style="margin-top:16px;">
    <div class="chart-subtitle">Nota Média por Status do Pedido</div>""", unsafe_allow_html=True)

    av_status = av.groupby("status")["nota"].mean().reset_index()
    av_status.columns = ["Status","Nota_Media"]
    av_status["Nota_Media"] = av_status["Nota_Media"].round(2)
    cores_av = [C["verde"] if v >= 3.5 else C["vermelho"] for v in av_status["Nota_Media"]]

    fig_av = go.Figure(go.Bar(
        x=av_status["Status"].str.capitalize(),
        y=av_status["Nota_Media"],
        marker_color=cores_av,
        text=av_status["Nota_Media"].apply(lambda v: f"★ {v:.2f}"),
        textposition="outside", textfont=dict(color="white", size=13),
        hovertemplate="<b>%{x}</b><br>Nota: <b>%{y:.2f}/5</b><extra></extra>",
    ))
    fig_av.add_hline(y=3.5, line_dash="dash", line_color="rgba(255,255,255,0.3)",
                     annotation_text="Threshold 3.5", annotation_font_color="white")
    fig_av.update_layout(**PLOTLY_TEMPLATE["layout"])
    fig_av.update_layout(
        height=260,
        yaxis=dict(range=[0,5.5], showgrid=True),
        xaxis=dict(showgrid=False, automargin=True),
        margin=dict(t=40, b=10, l=10, r=120)
    )
    fig_av.update_traces(textposition='outside', cliponaxis=False)
    st.plotly_chart(fig_av, use_container_width=True, config={"displayModeBar": False, "responsive": True})
    st.markdown("</div>", unsafe_allow_html=True)

# ABA 4 — Causa raiz
with tab4:
    st.markdown(f"""
    <div class="alerta-causa">
        <strong>Possível causa raiz</strong><br>
        <span>
        O canal <strong>paid_search</strong> apresenta taxa de cancelamento de <strong>30,74%</strong> — consistente em todos os trimestres analisados. Os demais canais operam entre 11–12%. Isso representa um problema estrutural, não sazonal.
        </span>
    </div>
    """, unsafe_allow_html=True)

    canal_stats = df.groupby("canal_aquisicao").agg(
        Total=("id","count"),
        Cancelados=("status", lambda x:(x=="cancelado").sum()),
        Devolvidos=("status", lambda x:(x=="devolvido").sum()),
        Ticket_Medio=("valor_total","mean"),
        Receita=("valor_total","sum"),
    ).reset_index()
    canal_stats["Taxa_Cancel"] = (canal_stats["Cancelados"]/canal_stats["Total"]*100).round(2)
    canal_stats["Taxa_Devolv"] = (canal_stats["Devolvidos"]/canal_stats["Total"]*100).round(2)
    canal_stats["Taxa_Problema"]= (canal_stats["Taxa_Cancel"]+canal_stats["Taxa_Devolv"]).round(2)
    canal_stats = canal_stats.sort_values("Taxa_Cancel", ascending=True)

    col_c1, col_c2 = st.columns([1, 1])

    # Taxa de Cancelamento por Canal
    with col_c1:
        st.markdown(f"""<div class="chart-card">
        <div class="chart-subtitle">Taxa de Cancelamento por Canal de Aquisição</div>""", unsafe_allow_html=True)

        cores_canal = [C["vermelho"] if c=="paid_search" else C["roxo"]
                       for c in canal_stats["canal_aquisicao"]]
        fig_canal = go.Figure(go.Bar(
            x=canal_stats["Taxa_Cancel"],
            y=canal_stats["canal_aquisicao"],
            orientation="h",
            marker_color=cores_canal,
            text=canal_stats["Taxa_Cancel"].apply(lambda v: f"{v:.1f}%"),
            textposition="outside", textfont=dict(color="white", size=12),
            hovertemplate="<b>%{y}</b><br>Cancelamento: <b>%{x:.2f}%</b><extra></extra>",
        ))
        fig_canal.update_layout(**PLOTLY_TEMPLATE["layout"])
        fig_canal.update_layout(
            height=280,
            xaxis=dict(ticksuffix="%", showgrid=False, automargin=True),
            yaxis=dict(showgrid=False),
            margin=dict(t=40, b=10, l=10, r=140)
        )
        fig_canal.update_traces(textposition='outside', cliponaxis=False)
        st.plotly_chart(fig_canal, use_container_width=True, config={"displayModeBar": False, "responsive": True})
        st.markdown("</div>", unsafe_allow_html=True)

    # Matriz de Performance (distribuição) 
    with col_c2:
        st.markdown(f"""<div class="chart-card">
        <div class="chart-subtitle">Matriz de Performance: Cancelamento vs Ticket Médio</div>""", unsafe_allow_html=True)

        CORES_CANAIS = {
            "paid_search":  C["vermelho"],
            "organico":     C["amarelo"],
            "indicacao":    C["azul"],
            "redes_sociais":C["roxo"],
        }
        canal_stats["cor"] = canal_stats["canal_aquisicao"].map(CORES_CANAIS).fillna(C["roxo"])

        y_axis_max = 35.0
        sizes = canal_stats["Total"].astype(float)
        desired_max_marker = 80.0
        sizeref = 2.0 * sizes.max() / (desired_max_marker ** 2) if sizes.max() > 0 else 1.0

        x_min = max(0, canal_stats["Ticket_Medio"].min() * 0.85) if len(canal_stats) else 0
        x_max = canal_stats["Ticket_Medio"].max() * 1.15 if canal_stats["Ticket_Medio"].max() > 0 else 1

        fig_matrix = go.Figure()
        media_ticket = canal_stats["Ticket_Medio"].mean() if len(canal_stats) else 0
        media_cancel = canal_stats["Taxa_Cancel"].mean() if len(canal_stats) else 0

        fig_matrix.add_shape(type="rect", x0=media_ticket, x1=x_max,
                             y0=0, y1=media_cancel, fillcolor="rgba(0,230,118,0.04)",
                             line=dict(width=0))
        fig_matrix.add_shape(type="rect", x0=x_min, x1=media_ticket,
                             y0=media_cancel, y1=y_axis_max,
                             fillcolor="rgba(255,68,68,0.04)", line=dict(width=0))

        for _, row in canal_stats.iterrows():
            fig_matrix.add_trace(go.Scatter(
                x=[row["Ticket_Medio"]], y=[row["Taxa_Cancel"]],
                mode="markers+text",
                marker=dict(
                    size=[row["Total"]],
                    sizemode='area',
                    sizeref=sizeref,
                    sizemin=20,
                    color=row["cor"],
                    opacity=0.95,
                    line=dict(color="white", width=1.5)
                ),
                text=[row["canal_aquisicao"].replace("_"," ")],
                textposition="middle center",
                textfont=dict(size=12, color="white", family="'Segoe UI', sans-serif"),
                hovertemplate=f"<b>{row['canal_aquisicao']}</b><br>Ticket Médio: R$ {row['Ticket_Medio']:,.0f}<br>Cancelamento: {row['Taxa_Cancel']:.1f}%<br>Pedidos: {row['Total']:,}<extra></extra>",
                showlegend=False,
            ))

        fig_matrix.add_vline(x=media_ticket, line_dash="dot", line_color="rgba(255,255,255,0.2)")
        fig_matrix.add_hline(y=media_cancel, line_dash="dot", line_color="rgba(255,255,255,0.2)")

        fig_matrix.update_layout(**PLOTLY_TEMPLATE["layout"])
        fig_matrix.update_layout(
             height=320,
             xaxis=dict(title="Ticket Médio (R$)", tickprefix="R$ ", range=[x_min, x_max], automargin=True),
             yaxis=dict(title="Taxa de Cancelamento (%)", ticksuffix="%", range=[0, y_axis_max], automargin=True),
             margin=dict(t=40, b=40, l=40, r=140)
        )

        fig_matrix.update_traces(cliponaxis=False)
        st.plotly_chart(fig_matrix, use_container_width=True, config={"displayModeBar": False, "responsive": True})
        st.markdown("</div>", unsafe_allow_html=True)

    # Consistência histórica de cancelamentos de paid search
    st.markdown(f"""<div class="chart-card">
    <div class="chart-subtitle">Consistência histórica de cancelamentos de paid search</div>""", unsafe_allow_html=True)

    hist = df.groupby(["Periodo_Q","canal_aquisicao"]).agg(
        Total=("id","count"),
        Cancelados=("status", lambda x:(x=="cancelado").sum()),
    ).reset_index()
    hist["Taxa_Cancel"] = (hist["Cancelados"]/hist["Total"]*100).round(2)
    hist = hist.sort_values("Periodo_Q")

    ps   = hist[hist["canal_aquisicao"]=="paid_search"]
    out  = hist[hist["canal_aquisicao"]!="paid_search"].groupby("Periodo_Q")["Taxa_Cancel"].mean().reset_index()

    fig_hist = go.Figure()
    fig_hist.add_trace(go.Scatter(
        x=ps["Periodo_Q"], y=ps["Taxa_Cancel"],
        mode="lines+markers", name="paid_search",
        line=dict(color=C["vermelho"], width=3),
        marker=dict(size=9, symbol="circle"),
        fill="tozeroy", fillcolor="rgba(255,68,68,0.08)",
        hovertemplate="<b>paid_search</b> · %{x}<br>Cancelamento: <b>%{y:.1f}%</b><extra></extra>",
    ))
    fig_hist.add_trace(go.Scatter(
        x=out["Periodo_Q"], y=out["Taxa_Cancel"],
        mode="lines+markers", name="Demais canais (média)",
        line=dict(color=C["verde"], width=3),
        marker=dict(size=9, symbol="diamond"),
        hovertemplate="<b>Demais canais</b> · %{x}<br>Cancelamento: <b>%{y:.1f}%</b><extra></extra>",
    ))
    fig_hist.update_layout(**PLOTLY_TEMPLATE["layout"])
    fig_hist.update_layout(
        height=300,
        yaxis=dict(ticksuffix="%"),
        legend=dict(orientation="h", y=1.15, x=0),
        margin=dict(t=40, b=40, l=40, r=120)
    )
    st.plotly_chart(fig_hist, use_container_width=True, config={"displayModeBar": False, "responsive": True})
    st.markdown("</div>", unsafe_allow_html=True)

    # Conclusão de possível causa raiz
    st.markdown(f"""
    <div class="insight-box" style="margin-top:8px;">
        <h4>Conclusão de possível causa raiz</h4>
        <ul>
            <li>Ao cruzarmos a origem do cliente com seu comportamento de cancelamento, percebe-se que a maior taxa de cancelamento é decorrente do paid search. Isso pode estar ocorrendo por falta de alinhamento entre o que a empresa oferece e o que o cliente espera do produto.</li>
            <li>Percebe-se também que as redes sociais possuem a menor taxa de cancelamento e maior ticket médio quando comparada aos outros canais. Isso revela que a maioria dos tickets de suporte são decorrentes de atraso ou dúvida.</li>
            <li>O canal paid_search tem 30.74% de cancelamento, quase 3× acima dos outros canais e isso é observado em todos os oito trimestres analisados — evidencia problema estrutural, não sazonal.</li>
            <li>No quarto trimestre de 2023 a Empresa teve um pico de tickets, decorrente do aumento do volume de pedidos (3.429 pedidos). A possível razão é que campanhas de paid search atraem clientes com expectativas diferentes (prazo, preço ou qualidade).</li>
            <li>Recomendação: revisar criativos e segmentação do paid_search; realocar investimento temporariamente para canais de indicação e redes sociais; proteger o segmento B2B (ticket médio ~6× maior).</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)


# ABA 5 — Dados detalhados
with tab5:
    st.markdown(f"""<div class="chart-card">
    <div class="chart-subtitle">Desempenho por Canal de Aquisição × Segmento</div>""",
    unsafe_allow_html=True)

    tabela = df.groupby(["canal_aquisicao","segmento"]).agg(
        Pedidos=("id","count"),
        Receita=("valor_total","sum"),
        Ticket_Medio=("valor_total","mean"),
        Cancelados=("status", lambda x:(x=="cancelado").sum()),
        Devolvidos=("status", lambda x:(x=="devolvido").sum()),
        Entregues=("status", lambda x:(x=="entregue").sum()),
    ).reset_index()
    tabela["% Cancelado"] = (tabela["Cancelados"]/tabela["Pedidos"]*100).round(2)
    tabela["% Devolvido"] = (tabela["Devolvidos"]/tabela["Pedidos"]*100).round(2)
    tabela["% Entregue"]  = (tabela["Entregues"]/tabela["Pedidos"]*100).round(2)
    tabela["Receita"]     = tabela["Receita"].round(2)
    tabela["Ticket_Medio"]= tabela["Ticket_Medio"].round(2)

    tabela_display = tabela.rename(columns={
        "canal_aquisicao":"Canal","segmento":"Segmento",
        "Pedidos":"Nº Pedidos","Ticket_Medio":"Ticket Médio (R$)",
    })[
        [
        "Canal","Segmento","Nº Pedidos","Receita","Ticket Médio (R$)",
        "% Cancelado","% Devolvido","% Entregue"
    ]]

    st.dataframe(
        tabela_display.style
        .background_gradient(subset=["% Cancelado"], cmap="Reds")
        .background_gradient(subset=["% Entregue"],  cmap="Greens")
        .format({
            "Nº Pedidos":    "{:,}",
            "Receita":       "R$ {:,.2f}",
            "Ticket Médio (R$)": "R$ {:,.2f}",
            "% Cancelado":   "{:.2f}%",
            "% Devolvido":   "{:.2f}%",
            "% Entregue":    "{:.2f}%",
        }),
        use_container_width=True, height=340
    )
    st.markdown("</div>", unsafe_allow_html=True)

    # Top 20 produtos 
    st.markdown(f"""<div class="chart-card" style="margin-top:16px;">
    <div class="chart-subtitle">Top 20 Produtos — Volume, Receita e Margem</div>""",
    unsafe_allow_html=True)

    top20 = agg_prod.head(20)[["nome","categoria","Total_Unidades","Receita_Total","margem_pct"]].copy()
    top20.columns = ["Produto","Categoria","Unidades Vendidas","Receita Total (R$)","Margem Bruta (%)"]
    top20.index = range(1, len(top20)+1)

    st.dataframe(
        top20.style
        .background_gradient(subset=["Unidades Vendidas"], cmap="Purples")
        .background_gradient(subset=["Receita Total (R$)"],  cmap="YlOrBr")
        .background_gradient(subset=["Margem Bruta (%)"],   cmap="Greens")
        .format({
            "Unidades Vendidas": "{:,}",
            "Receita Total (R$)": "R$ {:,.2f}",
            "Margem Bruta (%)": "{:.1f}%",
        }),
        use_container_width=True, height=600
    )
    st.markdown("</div>", unsafe_allow_html=True)