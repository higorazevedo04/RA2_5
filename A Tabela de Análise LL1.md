# Tabela de Análise LL(1)

> **Analisador Sintático LL(1)**
---

## Como ler a tabela

Cada célula `[Não-Terminal, Terminal]` contém a **produção a ser aplicada** quando o parser está tentando expandir o não-terminal e o próximo token (lookahead) é aquele terminal.

- **Célula vazia** → Erro sintático (combinação inválida)
- **`ε`** → Aplicar a produção vazia (epsilon)
- Os símbolos são separados por espaços na produção

---

## Tabela Completa LL(1)

> **Legenda de terminais:** `(` `)` `{` `}` `START` `END` `ID` `NUM` `+` `-` `*` `/` `//` `%` `^` `|` `>` `<` `==` `IF` `WHILE` `COMMAND` `$`

---

### `programa`

| Terminal | Produção |
|----------|----------|
| `(` | `( START ) laco_principal` |

---

### `laco_principal`

| Terminal | Produção |
|----------|----------|
| `(` | `( linha_ou_fim` |

---

### `linha_ou_fim`

| Terminal | Produção |
|----------|----------|
| `END` | `END )` |
| `(` | `conteudo_rpn ) laco_principal` |
| `ID` | `conteudo_rpn ) laco_principal` |
| `NUM` | `conteudo_rpn ) laco_principal` |

---

### `lista_instrucoes`

| Terminal | Produção |
|----------|----------|
| `(` | `instrucao continua_lista` |

---

### `continua_lista`

| Terminal | Produção |
|----------|----------|
| `(` | `instrucao continua_lista` |
| `}` | `ε` |

---

### `instrucao`

| Terminal | Produção |
|----------|----------|
| `(` | `( conteudo_rpn )` |

---

### `conteudo_rpn`

| Terminal | Produção |
|----------|----------|
| `(` | `valor elementos` |
| `ID` | `valor elementos` |
| `NUM` | `valor elementos` |

---

### `elementos`

| Terminal | Produção |
|----------|----------|
| `(` | `valor acao_final` |
| `ID` | `valor acao_final` |
| `NUM` | `valor acao_final` |
| `COMMAND` | `COMMAND` |
| `{` | `estrutura_controle` |

---

### `acao_final`

| Terminal | Produção |
|----------|----------|
| `+` | `operador` |
| `-` | `operador` |
| `*` | `operador` |
| `/` | `operador` |
| `//` | `operador` |
| `%` | `operador` |
| `^` | `operador` |
| `\|` | `operador` |
| `>` | `operador` |
| `<` | `operador` |
| `==` | `operador` |
| `COMMAND` | `COMMAND` |
| `{` | `estrutura_controle` |

---

### `estrutura_controle`

| Terminal | Produção |
|----------|----------|
| `{` | `bloco_codigo tipo_controle` |

---

### `bloco_codigo`

| Terminal | Produção |
|----------|----------|
| `{` | `{ lista_instrucoes }` |

---

### `tipo_controle`

| Terminal | Produção |
|----------|----------|
| `IF` | `IF` |
| `WHILE` | `WHILE` |

---

### `valor`

| Terminal | Produção |
|----------|----------|
| `(` | `instrucao` |
| `ID` | `ID` |
| `NUM` | `NUM` |

---

### `operador`

| Terminal | Produção |
|----------|----------|
| `+` | `+` |
| `-` | `-` |
| `*` | `*` |
| `/` | `/` |
| `//` | `//` |
| `%` | `%` |
| `^` | `^` |
| `\|` | `\|` |
| `>` | `>` |
| `<` | `<` |
| `==` | `==` |

---

## Tabela Consolidada (Visão Matricial Compacta)

> Mostrando apenas os não-terminais mais relevantes e seus lookaheads ativos.

| Não-Terminal ↓ / Terminal → | `(` | `)` | `{` | `}` | `END` | `ID` | `NUM` | `IF` | `WHILE` | `COMMAND` | `+`…`==` |
|-----------------------------|-----|-----|-----|-----|-------|------|-------|------|---------|-----------|----------|
| `programa` | P01 | — | — | — | — | — | — | — | — | — | — |
| `laco_principal` | P02 | — | — | — | — | — | — | — | — | — | — |
| `linha_ou_fim` | P04 | — | — | — | P03 | P04 | P04 | — | — | — | — |
| `lista_instrucoes` | P05 | — | — | — | — | — | — | — | — | — | — |
| `continua_lista` | P06 | — | — | P07(ε) | — | — | — | — | — | — | — |
| `instrucao` | P08 | — | — | — | — | — | — | — | — | — | — |
| `conteudo_rpn` | P09 | — | — | — | — | P09 | P09 | — | — | — | — |
| `elementos` | P11 | — | P12 | — | — | P11 | P11 | — | — | P10 | — |
| `acao_final` | — | — | P14 | — | — | — | — | — | — | P15 | P13 |
| `estrutura_controle` | — | — | P16 | — | — | — | — | — | — | — | — |
| `bloco_codigo` | — | — | P19 | — | — | — | — | — | — | — | — |
| `tipo_controle` | — | — | — | — | — | — | — | P17 | P18 | — | — |
| `valor` | P22 | — | — | — | — | P20 | P21 | — | — | — | — |
| `operador` | — | — | — | — | — | — | — | — | — | — | P23…P33 |


---

## Validação: Determinismo da Tabela

Condições verificadas para garantir que a tabela é **livre de conflitos**:

| Verificação | Resultado |
|-------------|-----------|
| Nenhuma célula contém mais de uma produção |  Confirmado |
| Conflitos FIRST/FIRST |  Ausentes — cada lookahead mapeia para no máximo 1 produção |
| Conflitos FIRST/FOLLOW (para `continua_lista → ε`) | ✅ Ausentes — `FIRST(instrucao) ∩ FOLLOW(continua_lista) = {(} ∩ {} = ∅` |
| Total de transições determinísticas mapeadas | **44 entradas** |

> **Conclusão:** A tabela é **estritamente determinística** e confirma que a gramática é **LL(1)**.
