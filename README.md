# financial-analysis-dashboard

Dashboard acadêmico em Python e Streamlit para análise das demonstrações financeiras
consolidadas da BASF S.A. no Brasil entre 2021 e 2024.

> **Projeto acadêmico independente, desenvolvido para fins educacionais e de portfólio. Não
> representa, não foi patrocinado e não foi validado oficialmente pela BASF.**

Minha contribuição foi auditar as fontes contábeis, reconciliar comparativos e reapresentações,
normalizar a base pública, refatorar o aplicativo monolítico e implementar validações, testes e
documentação reproduzíveis.

O projeto demonstra tratamento e validação de dados contábeis, cálculo reproduzível de
indicadores, visualização interativa e comunicação analítica responsável. Ele não produz
recomendações financeiras, laudos de crédito ou decisões para investidores.

## Problema e objetivo

O material original concentrava dados, interface e regras analíticas em um único arquivo,
dependia de um Excel local e incluía modelos e conclusões que não podiam ser sustentados pelas
variáveis disponíveis. A versão atual separa fonte, transformação, cálculo, validação,
visualização e apresentação.

O dashboard responde a perguntas descritivas:

- como receita, resultados e margens evoluíram no período;
- como o ativo foi financiado por obrigações e patrimônio líquido;
- como os fluxos operacional, de investimento e de financiamento se reconciliam;
- quais indicadores podem ser calculados diretamente dos demonstrativos;
- quais limitações impedem conclusões mais fortes.

## Principais funcionalidades

- navegação por sete páginas analíticas;
- filtro de ano e comparação com o ano anterior;
- alternância entre R$ mil e R$ milhões;
- temas claro e escuro com paleta neutra;
- indicadores recalculados no carregamento, sem confiar na aba original de indicadores;
- validações automáticas da equação patrimonial, DRE, CAPEX, FCF e variação de caixa;
- proveniência por demonstrativo e ano, além de dicionário de dados;
- textos analíticos determinísticos, sem diagnóstico gerado por IA;
- mensagens claras para schema ou arquivos inválidos.

## Tecnologias

- Python 3.11 ou 3.12
- Pandas
- Streamlit
- Plotly
- Pytest
- Ruff
- GitHub Actions

## Arquitetura

```text
financial-analysis-dashboard/
├── app.py
├── src/
│   ├── charts.py
│   ├── config.py
│   ├── data_loader.py
│   ├── financial_metrics.py
│   ├── narratives.py
│   ├── validation.py
│   ├── ui.py
│   └── pages/
│       ├── overview.py
│       ├── income_statement.py
│       ├── balance_sheet.py
│       ├── cash_flow.py
│       ├── indicators.py
│       ├── methodology.py
│       └── sources.py
├── data/
│   ├── processed/
│   │   ├── dre.csv
│   │   ├── balance_sheet.csv
│   │   ├── cash_flow.csv
│   │   ├── indicators.csv
│   │   ├── sources.csv
│   │   └── data_dictionary.csv
│   ├── raw/                 # fontes locais ignoradas pelo Git
│   └── README.md
├── tests/
├── docs/screenshots/
├── SOURCES.md
├── DATA_DICTIONARY.md
├── NOTICE.md
├── SECURITY.md
├── requirements.txt
├── requirements-dev.txt
├── pyproject.toml
└── LICENSE
```

## Origem e período dos dados

Os valores foram conferidos nas demonstrações financeiras consolidadas publicadas para os
exercícios de 2021, 2022, 2023 e 2024. Todos os valores monetários da camada processada estão em
milhares de reais.

Os documentos-fonte e o Excel de trabalho permanecem em `data/raw` apenas para auditoria local e
não são redistribuídos no repositório. O inventário, os nomes normalizados e as notas sobre
comparativos/reapresentações estão em [SOURCES.md](SOURCES.md). Fórmulas, sinais e tratamento de
ausências estão em [DATA_DICTIONARY.md](DATA_DICTIONARY.md).

O aplicativo não depende desses arquivos brutos: um clone contendo somente os CSVs processados
é suficiente. Para substituir a base, crie CSVs com os schemas documentados, preserve uma linha
por exercício e registre a nova proveniência em `sources.csv`; não é necessário recriar os nomes
dos PDFs locais.

## Metodologia dos indicadores

| Indicador | Fórmula |
|---|---|
| Liquidez corrente | Ativo circulante ÷ Passivo circulante |
| Liquidez seca | (Ativo circulante − Estoques) ÷ Passivo circulante |
| Margem bruta | Lucro bruto ÷ Receita líquida |
| Margem operacional | Resultado operacional ÷ Receita líquida |
| Margem líquida | Lucro líquido ÷ Receita líquida |
| ROA | Lucro líquido ÷ Ativo total no encerramento |
| ROE | Lucro líquido ÷ Patrimônio líquido no encerramento |
| Giro do ativo | Receita líquida ÷ Ativo total no encerramento |
| Capital de giro líquido | Ativo circulante − Passivo circulante |
| Endividamento geral | Capital de terceiros ÷ Ativo total |
| Composição do endividamento | Passivo circulante ÷ Capital de terceiros |
| Dívida bruta | Empréstimos + arrendamentos circulantes e não circulantes |
| CAPEX | Aquisição de imobilizado + aquisição de intangível |
| Fluxo de caixa livre | Fluxo operacional − CAPEX |

Percentuais são mantidos internamente como decimais. ROA, ROE e giro do ativo usam saldos de
encerramento para manter a definição consistente nos quatro anos sem introduzir dados de 2020.

## Instalação

Recomenda-se Python 3.11 ou 3.12.

```bash
python -m venv .venv
```

Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements-dev.txt
```

Linux/macOS:

```bash
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements-dev.txt
```

## Execução

```bash
python -m streamlit run app.py
```

O Streamlit abrirá o endereço local informado no terminal, normalmente
`http://localhost:8501`.

## Testes e qualidade

```bash
python -m pytest
python -m ruff check .
python -m ruff format --check .
python -m pip check
```

O `pytest` gera cobertura de `src` e exige pelo menos 85%. O workflow em
`.github/workflows/ci.yml` repete instalação, `pip check`, lint, formatação e testes em Python
3.11.

## Validações contábeis

O aplicativo registra, por ano:

- ativo total versus passivos e patrimônio líquido;
- lucro bruto versus receita e CPV;
- resultado operacional versus linhas operacionais disponíveis;
- lucro antes de IR/CS versus resultado operacional e financeiro;
- lucro líquido versus lucro antes de IR/CS e tributos;
- CAPEX versus aquisições de imobilizado e intangível;
- FCF versus fluxo operacional menos CAPEX;
- fluxos operacional, de investimento e de financiamento versus variação de caixa.

A tolerância é de R$ 1 mil, compatível com o arredondamento das publicações resumidas.

## Decisões de engenharia

- **Altman e Kanitz:** removidos porque a base resumida não contém todas as variáveis exigidas;
  proxies silenciosas produziriam precisão aparente.
- **Markowitz:** removido porque não existe série de retornos da BASF S.A. brasileira e não seria
  correto combinar os demonstrativos com preços da BASF SE.
- **Dados brutos:** PDFs e Excel ficam fora do Git para evitar redistribuição de documentos de
  terceiros; os CSVs mínimos derivados permitem executar o projeto.
- **Reapresentações:** a série usa o comparativo mais recente, com reconciliação numérica entre
  original e reapresentado em `SOURCES.md`.
- **Textos analíticos:** são determinísticos e derivados de regras explícitas; não há geração por
  IA, diagnóstico de crédito ou recomendação de investimento.

## Limitações

- A série contém somente os anos observados de 2021 a 2024.
- Os PDFs resumidos podem apresentar diferenças de R$ 1 mil por arredondamento.
- O fluxo de caixa de 2023 usa o comparativo explicitamente reapresentado em 2024.
- O fluxo de caixa de 2022 usa a coluna comparativa de 2023, que contém reclassificações frente à
  publicação original sem marca explícita de reapresentação no PDF resumido.
- Não há dados suficientes para aplicar Altman ou Kanitz sem proxies inadequadas; esses modelos
  foram removidos.
- A página de Markowitz foi removida. Não se misturam dados contábeis da BASF S.A. brasileira com
  preços de mercado da BASF SE, entidade jurídica distinta.
- O estudo não estabelece causalidade macroeconômica e não oferece recomendação de investimento.

## Screenshots

O primeiro commit não inclui imagens: `docs/screenshots/` contém apenas um `.gitkeep`. Capturas da
instância pública poderão ser adicionadas depois do deploy, sem incorporar documentos-fonte,
caminhos locais ou sessões do navegador.

## Deploy no Streamlit Community Cloud

Use o repositório público, branch `main` e arquivo `app.py`. Selecione Python 3.12 nas configurações
avançadas. O deploy usa `requirements.txt` e `.streamlit/config.toml`; `runtime.txt`,
`packages.txt` e `secrets.toml.example` não são necessários porque não há dependências do sistema
nem segredos.

## Competências demonstradas

Python, Pandas, Streamlit, Plotly, análise financeira, tratamento e validação de dados,
engenharia de software, testes automatizados, documentação técnica e comunicação executiva
responsável.

## Próximos passos

- publicar uma demonstração no Streamlit Community Cloud;
- adicionar screenshots reais após a publicação;
- automatizar a extração de novas demonstrações, mantendo revisão humana da proveniência;
- ampliar testes de regressão visual quando houver um ambiente de CI com navegador.

## Licença

O código e os textos originais do projeto são disponibilizados sob a licença MIT. Os documentos
financeiros de origem não integram a distribuição pública, e nenhuma licença é concedida sobre
marca, logotipo ou conteúdo de terceiros. O escopo aplicável aos CSVs derivados, documentos e
eventuais imagens está detalhado em [NOTICE.md](NOTICE.md).
