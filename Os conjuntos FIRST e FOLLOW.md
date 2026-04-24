# Conjuntos FIRST e FOLLOW

> ** Analisador Sintático LL(1)**
---

## O que são FIRST e FOLLOW?

| Conjunto | Definição |
|----------|-----------|
| **FIRST(A)** | Conjunto de terminais que podem aparecer como **primeiro símbolo** de qualquer cadeia derivada a partir de `A`. Se `A` pode derivar `ε`, então `ε ∈ FIRST(A)`. |
| **FOLLOW(A)** | Conjunto de terminais que podem aparecer **imediatamente após** `A` em alguma forma sentencial. O marcador `$` (fim de entrada) é incluído para o símbolo inicial. |

---

## Conjuntos FIRST

| Não-Terminal | FIRST |
|-------------|-------|
| `programa` | `{` **`(`** `}` |
| `laco_principal` | `{` **`(`** `}` |
| `linha_ou_fim` | `{` **`(`**, **`END`**, **`ID`**, **`NUM`** `}` |
| `lista_instrucoes` | `{` **`(`** `}` |
| `continua_lista` | `{` **`(`**, **`ε`** `}` |
| `instrucao` | `{` **`(`** `}` |
| `conteudo_rpn` | `{` **`(`**, **`ID`**, **`NUM`** `}` |
| `elementos` | `{` **`(`**, **`COMMAND`**, **`ID`**, **`NUM`**, **`{`** `}` |
| `acao_final` | `{` **`%`**, **`*`**, **`+`**, **`-`**, **`/`**, **`//`**, **`<`**, **`==`**, **`>`**, **`COMMAND`**, **`^`**, **`{`**, **`\|`** `}` |
| `estrutura_controle` | `{` **`{`** `}` |
| `bloco_codigo` | `{` **`{`** `}` |
| `tipo_controle` | `{` **`IF`**, **`WHILE`** `}` |
| `valor` | `{` **`(`**, **`ID`**, **`NUM`** `}` |
| `operador` | `{` **`%`**, **`*`**, **`+`**, **`-`**, **`/`**, **`//`**, **`<`**, **`==`**, **`>`**, **`^`**, **`\|`** `}` |

---

## Conjuntos FOLLOW

| Não-Terminal | FOLLOW |
|-------------|--------|
| `programa` | `{` **`$`** `}` |
| `laco_principal` | `{` **`$`** `}` |
| `linha_ou_fim` | `{` **`$`** `}` |
| `lista_instrucoes` | `{` **`}`** `}` |
| `continua_lista` | `{` **`}`** `}` |
| `instrucao` | `{` **`%`**, **`(`**, **`*`**, **`+`**, **`-`**, **`/`**, **`//`**, **`<`**, **`==`**, **`>`**, **`COMMAND`**, **`ID`**, **`NUM`**, **`^`**, **`{`**, **`\|`**, **`}`** `}` |
| `conteudo_rpn` | `{` **`)`** `}` |
| `elementos` | `{` **`)`** `}` |
| `acao_final` | `{` **`)`** `}` |
| `estrutura_controle` | `{` **`)`** `}` |
| `bloco_codigo` | `{` **`IF`**, **`WHILE`** `}` |
| `tipo_controle` | `{` **`)`** `}` |
| `valor` | `{` **`%`**, **`(`**, **`*`**, **`+`**, **`-`**, **`/`**, **`//`**, **`<`**, **`==`**, **`>`**, **`COMMAND`**, **`ID`**, **`NUM`**, **`^`**, **`{`**, **`\|`** `}` |
| `operador` | `{` **`)`** `}` |

---

## Não-terminais Anuláveis (Nullable)

Um não-terminal é **anulável** se pode derivar a cadeia vazia `ε`.

| Não-Terminal | Anulável? | Justificativa |
|-------------|-----------|--------------|
| `continua_lista` | **Sim** | Possui a produção `continua_lista → ε` diretamente |
| Todos os demais | Não | Não possuem caminho para derivar `ε` |

---

## Derivação dos Conjuntos 

### Exemplos de cálculo do FIRST

**`FIRST(valor)`**
- `valor → ID` → adiciona **`ID`**
- `valor → NUM` → adiciona **`NUM`**
- `valor → instrucao` e `FIRST(instrucao) = {(}` → adiciona **`(`**
- **Resultado:** `{ (, ID, NUM }`

**`FIRST(elementos)`**
- `elementos → COMMAND` → adiciona **`COMMAND`**
- `elementos → valor acao_final` e `FIRST(valor) = {(, ID, NUM}` → adiciona todos
- `elementos → estrutura_controle` e `FIRST(estrutura_controle) = {{` → adiciona **`{`**
- **Resultado:** `{ (, COMMAND, ID, NUM, { }`

**`FIRST(linha_ou_fim)`**
- `linha_ou_fim → END )` → adiciona **`END`**
- `linha_ou_fim → conteudo_rpn ) laco_principal` e `FIRST(conteudo_rpn) = {(, ID, NUM}` → adiciona todos
- **Resultado:** `{ (, END, ID, NUM }`

### Exemplos de cálculo do FOLLOW

**`FOLLOW(conteudo_rpn)`**
- Aparece em `instrucao → ( conteudo_rpn )` → o que segue é `)` → adiciona **`)`**
- Aparece em `linha_ou_fim → conteudo_rpn ) laco_principal` → o que segue é `)` → adiciona **`)`**
- **Resultado:** `{ ) }`

**`FOLLOW(bloco_codigo)`**
- Aparece em `estrutura_controle → bloco_codigo tipo_controle` → `FIRST(tipo_controle) = {IF, WHILE}`
- Nenhum anulável após → **Resultado:** `{ IF, WHILE }`

**`FOLLOW(programa)`**
- É o símbolo inicial → adiciona **`$`**
- **Resultado:** `{ $ }`

---

## Verificação LL(1): Ausência de Conflitos

Para cada não-terminal `A` com produções `A → α` e `A → β`:

| Condição | Status |
|----------|--------|
| `FIRST(α) ∩ FIRST(β) = ∅` para todas as alternativas | ✅ Sem conflito FIRST/FIRST |
| Se `ε ∈ FIRST(α)`, então `FIRST(β) ∩ FOLLOW(A) = ∅` | ✅ Sem conflito FIRST/FOLLOW |

> **Conclusão:** A gramática é **estritamente LL(1)** — sem ambiguidades e com parsing determinístico.
