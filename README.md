# 👁 OLHO DE DEUS
### Transparência Parlamentar Brasileira

Dashboard de vigilância cidadã sobre gastos públicos, CEAP, votações e proposições — uma versão melhorada do [ceap.escoladados.com](https://ceap.escoladados.com).

---

## Funcionalidades

| Aba | Descrição |
|-----|-----------|
| **Visão Geral** | KPIs, gastos por categoria/partido/UF, evolução mensal, top 20 gastadores |
| **Deputados** | Ranking completo com filtros por partido, UF e categoria |
| **Buscar Deputado** | Perfil individual com foto, alertas de anomalias, fornecedores, evolução mensal |
| **Comparar** | Comparação lado a lado de dois deputados com radar chart |
| **Anomalias IA** | Scanner automático para todos os deputados: Benford, HHI, valores redondos, FDS |
| **Ao Vivo** | Votações e proposições recentes direto da API da Câmara |

---

## Como publicar online (de graça)

### Passo 1 — Criar repositório no GitHub

1. Acesse [github.com](https://github.com) e faça login
2. Clique em **"New repository"**
3. Nome: `olho-de-deus` (ou qualquer outro)
4. Deixe como **Public**
5. Clique em **"Create repository"**

### Passo 2 — Subir os arquivos

Na página do repositório criado, clique em **"uploading an existing file"** e suba:
- `app.py`
- `requirements.txt`

### Passo 3 — Publicar no Streamlit Cloud

1. Acesse [share.streamlit.io](https://share.streamlit.io)
2. Faça login com sua conta do GitHub
3. Clique em **"New app"**
4. Selecione o repositório `olho-de-deus`
5. Main file path: `app.py`
6. Clique em **"Deploy!"**

Pronto! Em alguns minutos você terá um link público tipo:
`https://seuusuario-olho-de-deus-app-xxxxx.streamlit.app`

---

## Fontes de dados

- **CEAP (Cota Parlamentar):** `camara.leg.br/cotas/Ano-{ano}.csv.zip`
- **API REST Câmara:** `dadosabertos.camara.leg.br/api/v2`
  - Deputados, partidos, votações, proposições
- **Licença dos dados:** CC0 — Domínio Público

---

## Técnicas de detecção de anomalias

**Lei de Benford** — Detecta se a distribuição dos primeiros dígitos dos valores foge do padrão logarítmico natural. Auditores fiscais usam há décadas.

**Índice HHI** — Mede concentração de gastos em poucos fornecedores. A mesma métrica do CADE para avaliar monopólios.

**Valores Redondos** — Proporção acima de 30% de valores exatos (múltiplos de R$500/R$1000) é estatisticamente suspeita.

**Gastos em Fim de Semana** — Proporção acima de 15% de notas emitidas em sábados/domingos é atípica para atividade parlamentar legítima.

---

## Licença

Código: MIT  
Dados: CC0 (Domínio Público)
