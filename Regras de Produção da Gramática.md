# Regras de Produção da Gramática
> **Analisador Sintático LL(1) — Linguagem RPN**

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
linha_ou_fim    →  END )
                |  conteudo_rpn ) laco_principal
```

### 2. Instruções e Listas

```
lista_instrucoes  →  instrucao continua_lista
continua_lista    →  instrucao continua_lista
                  |  ε
instrucao         →  ( conteudo_rpn )
```

### 3. Expressões RPN (Notação Polonesa Reversa)

```
conteudo_rpn  →  valor elementos
elementos     →  valor elementos
              |  operador elementos
              |  COMMAND elementos
              |  estrutura_controle elementos
              |  ε
valor         →  ID
              |  NUM
              |  instrucao
```

> **Nota sobre `elementos`:** A produção é recursiva à direita e aceita
> qualquer sequência de valores, operadores, comandos e estruturas de controle.
> Isso permite expressões RPN de comprimento arbitrário sem conflitos LL(1).
> O `ε` encerra a sequência quando o próximo token for `)` (fim de instrução).

### 4. Operadores

```
operador  →  +  |  -  |  *  |  /  |  //  |  %  |  ^  |  |  |  >  |  <  |  ==
```

### 5. Estruturas de Controle

```
estrutura_controle  →  bloco_codigo tipo_controle
tipo_controle       →  IF
                    |  WHILE
bloco_codigo        →  { lista_instrucoes }
```

---

## Tabela Resumida das Produções

| Nº  | Não-Terminal          | Produção                                         |
|-----|-----------------------|--------------------------------------------------|
| P01 | `programa`            | `( START ) laco_principal`                       |
| P02 | `laco_principal`      | `( linha_ou_fim`                                 |
| P03 | `linha_ou_fim`        | `END )`                                          |
| P04 | `linha_ou_fim`        | `conteudo_rpn ) laco_principal`                  |
| P05 | `lista_instrucoes`    | `instrucao continua_lista`                       |
| P06 | `continua_lista`      | `instrucao continua_lista`                       |
| P07 | `continua_lista`      | `ε`                                              |
| P08 | `instrucao`           | `( conteudo_rpn )`                               |
| P09 | `conteudo_rpn`        | `valor elementos`                                |
| P10 | `elementos`           | `valor elementos`                                |
| P11 | `elementos`           | `operador elementos`                             |
| P12 | `elementos`           | `COMMAND elementos`                              |
| P13 | `elementos`           | `estrutura_controle elementos`                   |
| P14 | `elementos`           | `ε`                                              |
| P15 | `acao_final`          | `operador`                                       |
| P16 | `acao_final`          | `estrutura_controle`                             |
| P17 | `acao_final`          | `COMMAND`                                        |
| P18 | `estrutura_controle`  | `bloco_codigo tipo_controle`                     |
| P19 | `tipo_controle`       | `IF`                                             |
| P20 | `tipo_controle`       | `WHILE`                                          |
| P21 | `bloco_codigo`        | `{ lista_instrucoes }`                           |
| P22 | `valor`               | `ID`                                             |
| P23 | `valor`               | `NUM`                                            |
| P24 | `valor`               | `instrucao`                                      |
| P25 | `operador`            | `+`                                              |
| P26 | `operador`            | `-`                                              |
| P27 | `operador`            | `*`                                              |
| P28 | `operador`            | `/`                                              |
| P29 | `operador`            | `//`                                             |
| P30 | `operador`            | `%`                                              |
| P31 | `operador`            | `^`                                              |
| P32 | `operador`            | `\|`                                             |
| P33 | `operador`            | `>`                                              |
| P34 | `operador`            | `<`                                              |
| P35 | `operador`            | `==`                                             |

---

## Alfabeto Terminal

| Categoria                   | Tokens                                        |
|-----------------------------|-----------------------------------------------|
| **Delimitadores de Programa** | `START`, `END`                              |
| **Parênteses**              | `(`, `)`                                      |
| **Chaves**                  | `{`, `}`                                      |
| **Operadores Aritméticos**  | `+`, `-`, `*`, `/`, `//`, `%`, `^`           |
| **Operadores Relacionais**  | `>`, `<`, `==`                               |
| **Operador Bit a Bit**      | `\|`                                          |
| **Estruturas de Controle**  | `IF`, `WHILE`                                |
| **Comandos Especiais**      | `COMMAND` → `RES`, `MEM`                    |
| **Identificadores**         | `ID` (nomes de variáveis, ex: `X`, `total`)  |
| **Números**                 | `NUM` (inteiros e floats, ex: `3`, `3.14`, `-2`) |
| **Fim de Entrada**          | `$`                                          |

---

## Características da Linguagem

A linguagem é baseada em **notação pós-fixada (RPN)**. Operandos sempre precedem seus operadores:

```
( 3 2 + )                    →  3 + 2          =  5
( A B * )                    →  A × B
( 10 3 % )                   →  10 mod 3       =  1
( 2 8 ^ )                    →  2⁸             =  256
( X 5 > { ... } IF )         →  if (X > 5) { ... }
( X 0 > { ... } WHILE )      →  while (X > 0) { ... }
```

Comandos especiais operam sobre o histórico de resultados e a memória:

- **`MEM`** — Armazena um valor em uma variável: `( ADDR VAL MEM )` → `ADDR = VAL`
- **`RES`** — Recupera o resultado da linha N do histórico: `( N RES )` → empilha resultado[N]

---

## Estrutura Completa de um Programa

Todo programa deve obedecer ao seguinte padrão:

```
( START )
( <instrução_1> )
( <instrução_2> )
...
( END )
```

### Exemplos completos

**Expressão aritmética simples:**
```
( START )
( 3.14 2.0 + )
( END )
```

**Expressão aninhada:**
```
( START )
( ( A B + ) ( C D * ) / )
( END )
```

**Estrutura de decisão (IF):**
```
( START )
( X 10 > { ( X 1 - ) } IF )
( END )
```

**Estrutura de repetição (WHILE):**
```
( START )
( X 0 > { ( X 1 - ) } WHILE )
( END )
```

**Armazenar e recuperar:**
```
( START )
( 42.0 )
( resultado 1 RES MEM )
( END )
```

---

## Análise Léxica — AFD (Autômato Finito Determinístico)

O analisador léxico desta implementação usa um **AFD recursivo** com três estados:

| Estado                    | Responsabilidade                                               |
|---------------------------|----------------------------------------------------------------|
| `estado_inicial_afd`      | Despacha para o estado correto conforme o 1º caractere        |
| `estado_numero_afd`       | Lê dígitos, ponto decimal e sinal negativo                    |
| `estado_identificador_afd`| Lê letras, dígitos e `_` (após iniciar com letra ou `_`)     |

**Regras de reconhecimento de tokens:**

| Tipo      | Regra                                                                 |
|-----------|-----------------------------------------------------------------------|
| `NUM`     | `[0-9]+` ou `[0-9]+.[0-9]+` ou `-[0-9]+` ou `-[0-9]+.[0-9]+`       |
| `ID`      | `[a-zA-Z_][a-zA-Z0-9_]*`                                            |
| `//`      | Reconhecido antes de `/` — dois `/` consecutivos = divisão inteira   |
| `==`      | Reconhecido antes de `=` — dois `=` consecutivos = igualdade        |
| Comentário| `//` fora de qualquer bloco `()` ou `{}` — ignorado até fim da linha |

---

## Tokens Inválidos (rejeitados pelo léxico)

Os seguintes padrões causam **erro léxico** e abortam a compilação:

| Entrada      | Motivo do erro                        |
|--------------|---------------------------------------|
| `@`, `#`, `?`, `&` | Símbolo fora do alfabeto        |
| `10.5.2`     | Número com múltiplos pontos decimais  |
| `=`          | `=` isolado não é operador válido     |
| `.5`         | Número não pode começar com ponto     |
| `5.`         | Número não pode terminar com ponto    |
