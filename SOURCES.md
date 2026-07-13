# Fontes dos dados

Este projeto utiliza exclusivamente demonstrações financeiras públicas consolidadas da BASF S.A.
no Brasil. Os documentos foram usados como fontes contábeis do estudo de caso; sua presença local
não implica autorização para redistribuição.

## Documentos normalizados em `data/raw`

| Exercício | Arquivo local normalizado | Publicação consultada | Uso principal |
|---|---|---|---|
| 2021 | `basf_sa_financial_statements_2021.pdf` | Demonstrações de 2021, publicação no Valor Econômico de 28/04/2022 | DRE, balanço e DFC de 2021 |
| 2022 | `basf_sa_financial_statements_2022.pdf` | Demonstrações resumidas de 2022, publicação de 28/04/2023 | Conferência do período corrente de 2022 |
| 2023 | `basf_sa_financial_statements_2023.pdf` | Demonstrações resumidas de 2023 | DRE, balanço e comparativo de DFC de 2022 |
| 2024 | `basf_sa_financial_statements_2024.pdf` | Demonstrações resumidas de 2024, publicação de 29/04/2025 | 2024 e comparativo/reapresentação de 2023 |

Os arquivos originais tinham nomes gerados por download e incluíam três pares de duplicatas
binárias para 2022, 2023 e 2024. Apenas uma cópia de cada publicação foi preservada localmente.
O PDF integral de 2021 foi mantido; a página avulsa redundante foi removida da pasta de trabalho.

## Critério de seleção do comparativo

- **2021:** valores do período corrente de 2021, confirmados no comparativo da publicação de 2022.
- **2022:** DRE e balanço coincidem entre as publicações de 2022 e 2023. Para a DFC, foi usada a
  coluna comparativa da publicação de 2023, que traz reclassificações frente ao PDF original.
- **2023:** DRE e balanço coincidem com a publicação de 2023. A DFC usa o comparativo da publicação
  de 2024, explicitamente identificado como **reapresentado**.
- **2024:** período corrente da publicação de 2024.

## Reconciliação da DFC de 2022

As duas colunas abaixo são consolidadas, estão em R$ mil e aparecem na página 1 dos respectivos
PDFs. A publicação de 2023 não usa a palavra “reapresentado” para 2022; por isso o projeto trata a
mudança como **comparativo reclassificado**, não como reapresentação formal.

| Conta ou subtotal de 2022 | Publicação de 2022 | Comparativo na publicação de 2023 | Variação | Explicação observável |
|---|---:|---:|---:|---|
| Direito de uso — atividades operacionais | 20.709 | — | -20.709 | A linha deixa de aparecer no bloco operacional. |
| Caixa líquido das atividades operacionais | -298.298 | -319.007 | -20.709 | Efeito integral da retirada acima. |
| Empréstimos concedidos a coligadas | 3.087 em financiamento | 3.087 em investimento | — | Mesma entrada, transferida entre atividades. |
| Pagamento de arrendamento | -103.932 | -83.223 | +20.709 | Valor apresentado no bloco de financiamento é reduzido. |
| Caixa líquido das atividades de investimento | -579.084 | -575.997 | +3.087 | Recebe a entrada de empréstimos concedidos a coligadas. |
| Caixa líquido das atividades de financiamento | 19.854 | 37.476 | +17.622 | Efeito líquido de +20.709 no arrendamento e -3.087 transferidos para investimento. |
| Variação líquida de caixa | -857.528 | -857.528 | 0 | A reclassificação não altera caixa final. |

Foi escolhida a coluna comparativa mais recente porque ela apresenta 2022 na mesma publicação
usada para 2023 e preserva a reconciliação do caixa. A comparabilidade dos totais de caixa é
mantida, mas a comparação por atividade com 2021 deve considerar a mudança de classificação.

## Reconciliação da DFC de 2023

O comparativo de 2023 na publicação de 2024 é identificado expressamente como
**“Reapresentado”** na página 1.

| Conta ou subtotal de 2023 | Publicação de 2023 | Reapresentado na publicação de 2024 | Variação | Explicação observável |
|---|---:|---:|---:|---|
| Provisão para benefícios a funcionários — ajuste | 629 | 16.989 | +16.360 | A reapresentação abre separadamente uma saída de -16.360; efeito operacional líquido zero. |
| Provisão para benefícios a funcionários — variação/pagamento | — | -16.360 | -16.360 | Nova linha no bloco de variações de ativos e passivos. |
| Perdas a valor justo de derivativos — ajuste não caixa | 453.823 | 1.126.360 | +672.537 | Valor do ajuste é ampliado na reapresentação. |
| Perdas a valor justo de derivativos — variação operacional | — | -500.459 | -500.459 | Nova linha no bloco de variações de ativos e passivos. |
| Caixa líquido das atividades operacionais | 706.090 | 878.168 | +172.078 | Efeito líquido das duas linhas de derivativos; benefícios a funcionários se anulam. |
| Liquidação de empréstimos | -13.933.312 em uma linha | -72.175 e -13.861.137 | 0 | O total é separado entre empréstimos e partes relacionadas. |
| Liquidação de instrumentos financeiros derivativos | — | -172.078 | -172.078 | Nova linha classificada em financiamento. |
| Caixa líquido das atividades de investimento | -505.867 | -505.867 | 0 | Sem alteração. |
| Caixa líquido das atividades de financiamento | -545.280 | -717.358 | -172.078 | Compensa o aumento do fluxo operacional. |
| Variação líquida de caixa | -345.057 | -345.057 | 0 | A reapresentação não altera caixa final. |

A versão reapresentada foi escolhida por ser a divulgação posterior explicitamente qualificada
pela própria publicação. A série permanece comparável para variação total de caixa, CAPEX e
fluxo de investimento; há quebra de classificação entre operação e financiamento para 2023, que
deve ser considerada em análises dessas atividades.

## Unidades e escopo

- unidade monetária: milhares de reais (R$ mil);
- entidade: BASF S.A. e controladas, base consolidada;
- períodos: exercícios encerrados em 31 de dezembro de 2021, 2022, 2023 e 2024;
- não há projeções ou números simulados na base processada.

## Diferenças identificadas

1. A equação patrimonial de 2023 apresenta diferença de R$ 1 mil no demonstrativo resumido.
2. O resultado operacional de 2022 difere em R$ 1 mil da soma das linhas operacionais publicadas.
3. O lucro líquido de 2023 difere em R$ 1 mil da soma do lucro antes de IR/CS com o tributo
   publicado.
4. A planilha original tratava CAPEX de forma inconsistente: 2021 incluía imobilizado e intangível,
   enquanto 2022–2024 incluíam apenas imobilizado. A camada processada usa, para todos os anos,
   `aquisição de imobilizado + aquisição de intangível`.

As diferenças de R$ 1 mil são preservadas e tratadas por tolerância de arredondamento; os valores
publicados não foram ajustados para forçar igualdade.

## Rastreabilidade

- `data/processed/sources.csv`: fonte, unidade e observação por ano e demonstrativo;
- `data/processed/data_dictionary.csv`: origem ou fórmula de cada variável;
- `DATA_DICTIONARY.md`: fórmulas, sinais, ausências e limitações de interpretação;
- cada CSV contábil: arquivo-fonte, demonstrativo, unidade e observação na própria linha anual.

## Planilha de trabalho original

O Excel local contém valores estáticos, sem fórmulas ou referências de página por célula. Ele foi
usado como apoio de transcrição, não como fonte autônoma. A aba original de fluxo de caixa também
usava apenas aquisição de imobilizado como CAPEX em 2022–2024, enquanto 2021 incluía intangível.
A camada pública corrige essa inconsistência por regra explícita e rastreia os valores aos PDFs.
Assim, houve digitação manual na planilha de trabalho original, mas nenhum ajuste manual oculto
foi mantido nos CSVs publicados.
