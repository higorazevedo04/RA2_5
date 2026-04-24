# Regras de Produção da Gramática

> **Analisador Sintático LL(1)**

---

## Notação

- **Letras minúsculas** → Não-terminais (ex: `programa`, `valor`)
- **Letras MAIÚSCULAS / símbolos** → Terminais (ex: `START`, `(`, `+`)
- `ε` → Produção vazia (epsilon)
- `|` → Alternativa de produção

---

## Gramática Completa em EBNF

### 1. Estrutura Principal

```
programa        →  ( START ) laco_principal

laco_principal  →  ( linha_ou_fim

linha_ou_fim    →  END ) |  conteudo_rpn ) laco_principal
```

### 2. Instruções e Listas

```
lista_instrucoes  →  instrucao continua_lista

continua_lista    →  instrucao continua_lista |  ε

instrucao         →  ( conteudo_rpn )
```

### 3. Expressões RPN (Notação Polonesa Reversa)

```
conteudo_rpn  →  valor elementos

elementos     →  COMMAND |  valor acao_final |  estrutura_controle

acao_final    →  operador |  estrutura_controle |  COMMAND

valor         →  ID |  NUM |  instrucao
```

### 4. Operadores

```
operador  →  +  |  -  |  *  |  /  |  // |  %  |  ^  |  |  |  >  |  <  |  ==
```

### 5. Estruturas de Controle

```
estrutura_controle  →  bloco_codigo tipo_controle

tipo_controle       →  IF |  WHILE

bloco_codigo        →  { lista_instrucoes }
```

---

## Tabela Resumida das Produções

| Nº | Não-Terminal | Produção |
|----|-------------|----------|
| P01 | `programa` | `( START ) laco_principal` |
| P02 | `laco_principal` | `( linha_ou_fim` |
| P03 | `linha_ou_fim` | `END )` |
| P04 | `linha_ou_fim` | `conteudo_rpn ) laco_principal` |
| P05 | `lista_instrucoes` | `instrucao continua_lista` |
| P06 | `continua_lista` | `instrucao continua_lista` |
| P07 | `continua_lista` | `ε` |
| P08 | `instrucao` | `( conteudo_rpn )` |
| P09 | `conteudo_rpn` | `valor elementos` |
| P10 | `elementos` | `COMMAND` |
| P11 | `elementos` | `valor acao_final` |
| P12 | `elementos` | `estrutura_controle` |
| P13 | `acao_final` | `operador` |
| P14 | `acao_final` | `estrutura_controle` |
| P15 | `acao_final` | `COMMAND` |
| P16 | `estrutura_controle` | `bloco_codigo tipo_controle` |
| P17 | `tipo_controle` | `IF` |
| P18 | `tipo_controle` | `WHILE` |
| P19 | `bloco_codigo` | `{ lista_instrucoes }` |
| P20 | `valor` | `ID` |
| P21 | `valor` | `NUM` |
| P22 | `valor` | `instrucao` |
| P23 | `operador` | `+` |
| P24 | `operador` | `-` |
| P25 | `operador` | `*` |
| P26 | `operador` | `/` |
| P27 | `operador` | `//` |
| P28 | `operador` | `%` |
| P29 | `operador` | `^` |
| P30 | `operador` | `\|` |
| P31 | `operador` | `>` |
| P32 | `operador` | `<` |
| P33 | `operador` | `==` |

---

## Alfabeto Terminal

| Categoria | Tokens |
|-----------|--------|
| **Delimitadores de Programa** | `START`, `END` |
| **Parênteses** | `(`, `)` |
| **Chaves** | `{`, `}` |
| **Operadores Aritméticos** | `+`, `-`, `*`, `/`, `//`, `%`, `^` |
| **Operadores Relacionais** | `>`, `<`, `==` |
| **Operador Bit a Bit** | `\|` |
| **Estruturas de Controle** | `IF`, `WHILE` |
| **Comandos Especiais** | `COMMAND` (`RES`, `MEM`) |
| **Identificadores** | `ID` (nomes de variáveis) |
| **Números** | `NUM` (inteiros e floats) |
| **Fim de Entrada** | `$` |

---

## Características da Linguagem

A linguagem é baseada em **notação pós-fixada (RPN)**. Operandos precedem operadores:

```
( 3 2 + )        → 3 + 2
( A B * )        → A * B
( X 5 > { ... } WHILE )  → while (X > 5) { ... }
```

Comandos especiais operam sobre resultados anteriores:

- **`MEM`** — Armazena um valor em uma variável
- **`RES`** — Recupera um resultado do histórico de execução
