# Camada de dados

## `processed/`

ContÃ©m os dados pÃºblicos consolidados usados pelo aplicativo:

- `dre.csv`: demonstraÃ§Ã£o do resultado;
- `balance_sheet.csv`: balanÃ§o patrimonial e componentes de dÃ­vida bruta;
- `cash_flow.csv`: fluxos de caixa e CAPEX normalizado;
- `indicators.csv`: extrato de indicadores derivados para teste de regressÃ£o;
- `sources.csv`: proveniÃªncia por ano e demonstrativo;
- `data_dictionary.csv`: descriÃ§Ã£o e fÃ³rmula/origem das variÃ¡veis.

O aplicativo recalcula os indicadores em runtime. O arquivo `indicators.csv` nÃ£o Ã© tratado como
fonte contÃ¡bil; ele existe para tornar o resultado esperado auditÃ¡vel e permitir testes de
regressÃ£o.

## `raw/`

ContÃ©m localmente os PDFs pÃºblicos e o Excel original renomeados. Todo o conteÃºdo de `raw/`, com
exceÃ§Ã£o de `.gitkeep`, Ã© ignorado pelo Git para evitar redistribuiÃ§Ã£o desnecessÃ¡ria. Consulte
`SOURCES.md` para o inventÃ¡rio dos documentos.

## ConvenÃ§Ãµes

- valores monetÃ¡rios em R$ mil;
- custos, despesas, tributos e saÃ­das de caixa mantÃªm o sinal contÃ¡bil, exceto as colunas de
  aquisiÃ§Ã£o usadas no CAPEX, armazenadas como valores positivos;
- percentuais armazenados como decimais;
- uma linha por ano em cada conjunto contÃ¡bil;
- anos permitidos: 2021, 2022, 2023 e 2024.
