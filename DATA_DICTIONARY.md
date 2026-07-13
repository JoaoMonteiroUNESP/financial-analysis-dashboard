# Dicionário de dados e metodologia

Este documento descreve a camada pública em `data/processed`. O grão das três tabelas
contábeis e do extrato de indicadores é **uma linha por exercício**, para 2021–2024. Valores
monetários estão em milhares de reais; percentuais e índices são armazenados como números
decimais, sem multiplicação por 100.

## Tratamento comum

- Custos, despesas, tributos e totais de saída de caixa preservam o sinal negativo publicado.
- `Aquisicao_Imobilizado` e `Aquisicao_Intangivel` são os valores absolutos das saídas
  publicadas, para que CAPEX seja expresso como dispêndio positivo.
- O traço publicado para empréstimos não circulantes consolidados de 2024 é armazenado como
  zero; nenhum outro valor ausente é imputado.
- Ausência em coluna obrigatória gera `DataSchemaError`; não há preenchimento por média, zero ou
  período anterior.
- Divisões por denominador zero retornam valor ausente (`NaN`), e não infinito ou zero.
- Diferenças contábeis de até R$ 1 mil são preservadas e tratadas apenas como tolerância de
  validação. Nenhum saldo é ajustado para fechar uma fórmula.

## Variáveis observadas e derivadas

`dre.csv`, `balance_sheet.csv` e `cash_flow.csv` contêm as linhas observadas usadas pelo
dashboard e metadados de origem. As definições linha a linha também estão no arquivo
`data/processed/data_dictionary.csv`.

As únicas transformações monetárias são:

| Variável | Fórmula ou transformação | Unidade | Observação |
|---|---|---|---|
| `Capital_Terceiros` | `Passivo_Circulante + Passivo_Nao_Circulante` | R$ mil | Inclui todas as obrigações, não apenas dívida financeira. |
| `Divida_Bruta` | `Emprestimos_Circulante + Emprestimos_Nao_Circulante + Arrendamentos_Circulante + Arrendamentos_Nao_Circulante` | R$ mil | Não inclui fornecedores, tributos ou provisões. |
| `CAPEX` | `Aquisicao_Imobilizado + Aquisicao_Intangivel` | R$ mil | Ambos os componentes são armazenados como dispêndios positivos nos quatro anos. |
| `Free_Cash_Flow` | `Fluxo_Operacional - CAPEX` | R$ mil | FCF simplificado e pós-juros/impostos conforme a DFC publicada. |

## Indicadores calculados

| Indicador | Fórmula matemática | Colunas utilizadas | Resultado | Sinais e ausências | Limitação de interpretação |
|---|---|---|---|---|---|
| Liquidez corrente | AC ÷ PC | `Ativo_Circulante`, `Passivo_Circulante` | Razão | Saldos preservados; PC zero produz `NaN` | Não avalia prazos nem qualidade dos ativos circulantes. |
| Liquidez seca | (AC − estoques) ÷ PC | `Ativo_Circulante`, `Estoques`, `Passivo_Circulante` | Razão | Estoques são subtraídos; PC zero produz `NaN` | Remove somente estoques e não mede conversibilidade efetiva dos demais ativos. |
| Margem bruta | Lucro bruto ÷ receita líquida | `Lucro_Bruto`, `Receita_Liquida` | Decimal | Resultado negativo permanece negativo; receita zero produz `NaN` | Depende da classificação contábil entre CPV e despesas operacionais. |
| Margem operacional | Resultado operacional ÷ receita líquida | `Resultado_Operacional`, `Receita_Liquida` | Decimal | Resultado negativo permanece negativo; receita zero produz `NaN` | Não separa recorrência das linhas operacionais resumidas. |
| Margem líquida | Lucro líquido ÷ receita líquida | `Lucro_Liquido`, `Receita_Liquida` | Decimal | Prejuízo permanece negativo; receita zero produz `NaN` | Inclui efeitos operacionais, financeiros e tributários. |
| ROA simplificado | Lucro líquido ÷ ativo total final | `Lucro_Liquido`, `Ativo_Total` | Decimal | Prejuízo permanece negativo; ativo zero produz `NaN` | Usa saldo de encerramento, não ativo médio. Pode diferir da definição habitual. |
| ROE simplificado | Lucro líquido ÷ patrimônio líquido final | `Lucro_Liquido`, `Patrimonio_Liquido` | Decimal | Prejuízo permanece negativo; PL zero produz `NaN` | Usa saldo de encerramento, não patrimônio médio. Pode ser afetado por distribuições e movimentos de capital. |
| Giro do ativo simplificado | Receita líquida ÷ ativo total final | `Receita_Liquida`, `Ativo_Total` | Razão | Ativo zero produz `NaN` | Usa saldo final em vez de ativo médio. |
| Capital de giro líquido | AC − PC | `Ativo_Circulante`, `Passivo_Circulante` | R$ mil | Pode ser negativo; ausência é rejeitada no carregamento | Não equivale a caixa disponível. |
| Endividamento geral | (PC + PNC) ÷ ativo total | `Passivo_Circulante`, `Passivo_Nao_Circulante`, `Ativo_Total` | Decimal | Ativo zero produz `NaN` | Mede capital de terceiros total, não apenas dívida financeira. |
| Composição do endividamento | PC ÷ (PC + PNC) | `Passivo_Circulante`, `Passivo_Nao_Circulante` | Decimal | Capital de terceiros zero produz `NaN` | Resume a parcela contábil de curto prazo sem examinar vencimentos individuais. |
| Dívida bruta / ativo | Dívida bruta ÷ ativo total | quatro componentes de dívida e `Ativo_Total` | Decimal | Ativo zero produz `NaN` | Inclui arrendamentos; não considera caixa, portanto não é dívida líquida. |
| Fluxo de caixa livre | FCO − CAPEX | `Fluxo_Operacional`, `Aquisicao_Imobilizado`, `Aquisicao_Intangivel` | R$ mil | FCO negativo e CAPEX positivo são preservados | Definição simplificada; não é fluxo de caixa livre desalavancado nem medida de valuation. |

## Extrato de regressão

`indicators.csv` é um extrato estático dos resultados esperados para os quatro anos. Ele não é
uma publicação da companhia nem uma entrada do cálculo: o aplicativo recalcula os indicadores
em runtime e os testes comparam o resultado com esse extrato. O nome interno utilizado pelo
carregador é `reference_indicators` para evitar confusão com valores publicados.

## Proveniência

`data/processed/sources.csv` registra, por conjunto e exercício, o arquivo, a página/seção, a
unidade, a natureza observada ou calculada, a transformação e as diferenças de arredondamento.
As reapresentações de 2022 e 2023 são reconciliadas numericamente em `SOURCES.md`.
