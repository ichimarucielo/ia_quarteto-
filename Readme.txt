Projeto de conciliacao fiscal
=============================

Visao geral
-----------

Este projeto foi criado para demonstrar o cruzamento entre as notas fiscais
emitidas pela Prefeitura e as notas presentes no Billing.

Neste fluxo, o arquivo/tabela `ZSD008` e a fonte dos dados chamada de
Billing. Portanto, quando o relatorio apresenta `NF Billing`, `Valor Billing`
ou `Saldo Billing`, esses dados vieram do arquivo ZSD008.

O processamento gera dois relatorios Excel:

- `Check_Faturamento.xlsx`: conferencia dos dados da Prefeitura e do SAP,
  incluindo informacoes de excecao.
- `Report_Faturamento.xlsx`: relatorio principal do Billing, com o resumo
  financeiro e a identificacao das notas que nao foram encontradas nos dois
  lados.

Fontes de dados
---------------

O processo utiliza tres fontes:

1. Prefeitura

    Arquivo CSV com as notas fiscais emitidas. Os principais campos usados no
    cruzamento sao:

    - `Numero NF`: numero da nota fiscal da Prefeitura.
    - `Tomador`: cliente associado a nota.
    - `Valor Serviço`: valor da nota.
    - `Nf Ativa`: situacao da nota.

2. FS10N

    Arquivo SAP usado no `Check_Faturamento.xlsx`, principalmente para a
    conferencia de documentos e cancelamentos.

3. ZSD008

    Arquivo usado para montar o Billing do `Report_Faturamento.xlsx`. Os
    principais campos sao:

    - `Nº Nota Fiscal`: numero da nota no Billing.
    - `Razão Social`: cliente associado a nota.
    - `Valor Bruto`: valor registrado no Billing.
    - `Fatura Billing`: identificacao da fatura.
    - `Descrição`: descricao do servico.

Fluxo passo a passo
-------------------

1. Leitura dos arquivos

    O sistema le o CSV da Prefeitura, o arquivo FS10N e a planilha ZSD008.

2. Normalizacao da Prefeitura

    Os campos da Prefeitura sao preparados para comparacao. Valores monetarios
    sao convertidos para numeros e os identificadores sao tratados como texto.

3. Preparacao do Billing

    O sistema seleciona da ZSD008 as colunas necessarias para o relatorio,
    organiza as notas pelo numero da NF e pela descricao do servico.

4. Definicao da chave de cruzamento

    A chave principal da conciliacao e o numero da nota fiscal:

    ```text
    Prefeitura: Numero NF
    Billing:    Nº Nota Fiscal
    ```

    Antes da comparacao, o sistema remove espacos, converte os valores para
    texto e remove o final `.0`. Assim, valores como `12345.0` e `12345`
    podem ser reconhecidos como a mesma NF.

5. Agrupamento dos registros

    Caso uma NF tenha mais de uma linha em qualquer fonte, os registros sao
    agrupados pelo numero da NF.

    - Prefeitura: soma de `Valor Serviço`.
    - Billing: soma de `Valor Bruto`.

6. Cruzamento das NFs

    O sistema compara o conjunto de NFs da Prefeitura com o conjunto de NFs do
    Billing. O resultado pode ser:

    - NF encontrada nos dois lados: considerada localizada.
    - NF somente na Prefeitura: indicada como `PREFEITURA_SEM_BILLING`.
    - NF somente no Billing: indicada como `BILLING_SEM_PREFEITURA`.

7. Calculo da diferenca

    Para uma NF somente na Prefeitura:

    ```text
    Diferenca = Valor Prefeitura - 0
    ```

    Para uma NF somente no Billing:

    ```text
    Diferenca = 0 - Valor Billing
    ```

    O relatorio tambem apresenta uma diferenca geral entre o saldo total da
    Prefeitura e o saldo total do Billing.

8. Geracao dos arquivos

    Ao final, os dados sao organizados em abas Excel e salvos na pasta
    `data/output`.

Abas do Report_Faturamento
--------------------------

`SAP x Prefeitura`

Apresenta os totais gerais:

- saldo da Prefeitura;
- saldo do Billing, originado da ZSD008;
- diferenca entre os saldos;
- quantidade de NFs em cada fonte.

`Notas Emitidas`

Contem as linhas selecionadas da ZSD008 que formam o relatorio do Billing.

`Nao_Conciliadas`

Apresenta as notas que existem somente em uma das fontes. A aba informa:

- status da conciliacao;
- tipo da excecao;
- NF da Prefeitura;
- NF do Billing;
- cliente de cada origem;
- valor de cada origem;
- diferenca calculada;
- motivo da nao conciliacao;
- status da NF na Prefeitura.

`Setup`

Filtra as linhas do Billing cuja `Descrição` contem `SETUP`.

`Contratos Cielo`

Filtra as linhas do Billing cuja `Razão Social` contem `CIELO`.

Como apresentar o resultado
---------------------------

Uma forma simples de explicar o resultado e:

1. A Prefeitura informa quais notas foram emitidas.
2. A ZSD008 informa quais notas foram registradas no Billing.
3. O sistema compara o numero da NF entre as duas fontes.
4. As notas encontradas nos dois lados sao consideradas localizadas.
5. As notas encontradas em apenas um lado aparecem na aba
    `Nao_Conciliadas`.
6. A diferenca financeira mostra o impacto dos documentos que ficaram fora
    do cruzamento.

Observacao importante
---------------------

O cruzamento principal verifica a existencia da NF nas duas fontes. Uma NF
encontrada nos dois lados nao entra na aba `Nao_Conciliadas` apenas por ter
valores diferentes. A diferenca de valores entre NFs presentes nos dois lados
fica refletida no resumo geral e pode ser analisada em uma etapa posterior.

Arquivos de saida
-----------------

Os arquivos sao salvos em `data/output`:

- `Check_Faturamento.xlsx`.
- `Report_Faturamento.xlsx`.

O processamento tambem registra o andamento em
`logs/reconciliation.log`.

Execucao do projeto
-------------------

```text
python main.py --prefeitura <arquivo.csv> --fs10n <arquivo.xlsx> --zsd008 <arquivo.xlsx>
```

Para uma demonstracao, podem ser usados os arquivos organizados nas pastas
`data/raw/prefeitura`, `data/raw/fs10n` e `data/raw/zsd008`.
