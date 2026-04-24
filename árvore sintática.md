# 🌳 Árvore Sintática

> **Compilador RPN — Analisador Sintático LL(1)**
> Responsabilidade: Aluno 7.4 — `gerarArvore()` / `gerarAssembly()`

---

## Arquivo de Teste Utilizado

**Entrada analisada:** Expressão de soma simples em notação RPN

```
( START )
( 3 2 + )
( END )
```

**Tokens gerados pelo Analisador Léxico:**

```
(  START  )  (  3  2  +  )  (  END  )  $
```

**Classificação léxica dos tokens:**

| Token | Categoria |
|-------|-----------|
| `(` | PARENTESE_ESQUERDA |
| `START` | PALAVRA |
| `)` | PARENTESE_DIREITA |
| `(` | PARENTESE_ESQUERDA |
| `3` | NUMERO |
| `2` | NUMERO |
| `+` | OPERADOR |
| `)` | PARENTESE_DIREITA |
| `(` | PARENTESE_ESQUERDA |
| `END` | PALAVRA |
| `)` | PARENTESE_DIREITA |

---

## Árvore de Derivação Concreta (CST)

A **Árvore de Derivação Concreta** (Concrete Syntax Tree) preserva todos os detalhes da gramática, incluindo terminais auxiliares como parênteses.

```
programa
├── [TERMINAL] (
├── [TERMINAL] START
├── [TERMINAL] )
└── laco_principal
    ├── [TERMINAL] (
    └── linha_ou_fim
        ├── conteudo_rpn
        │   ├── valor
        │   │   └── [TERMINAL] 3          ← Operando esquerdo
        │   └── elementos
        │       ├── valor
        │       │   └── [TERMINAL] 2      ← Operando direito
        │       └── acao_final
        │           └── operador
        │               └── [TERMINAL] +  ← Operador
        ├── [TERMINAL] )
        └── laco_principal
            ├── [TERMINAL] (
            └── linha_ou_fim
                ├── [TERMINAL] END
                └── [TERMINAL] )
```

---

## Árvore Sintática Abstrata (AST)

A **Árvore Sintática Abstrata** (Abstract Syntax Tree) remove ruído sintático e representa apenas a estrutura semântica essencial do programa. É a entrada direta do gerador de código.

```
programa_ast
└── instrucoes: [
      operacao
      ├── operador: "+"
      ├── esquerda:
      │   └── numero
      │       └── valor: 3
      └── direita:
          └── numero
              └── valor: 2
    ]
```

---

## Representação em JSON (AST)

```json
{
  "tipo": "programa_ast",
  "instrucoes": [
    {
      "tipo": "operacao",
      "operador": "+",
      "esquerda": {
        "tipo": "numero",
        "valor": 3
      },
      "direita": {
        "tipo": "numero",
        "valor": 2
      }
    }
  ]
}
```

---

## Representação em JSON (CST)

```json
{
  "nome": "programa",
  "filhos": [
    { "terminal": "(" },
    { "terminal": "START" },
    { "terminal": ")" },
    {
      "nome": "laco_principal",
      "filhos": [
        { "terminal": "(" },
        {
          "nome": "linha_ou_fim",
          "filhos": [
            {
              "nome": "conteudo_rpn",
              "filhos": [
                {
                  "nome": "valor",
                  "filhos": [ { "terminal": "3" } ]
                },
                {
                  "nome": "elementos",
                  "filhos": [
                    {
                      "nome": "valor",
                      "filhos": [ { "terminal": "2" } ]
                    },
                    {
                      "nome": "acao_final",
                      "filhos": [
                        {
                          "nome": "operador",
                          "filhos": [ { "terminal": "+" } ]
                        }
                      ]
                    }
                  ]
                }
              ]
            },
            { "terminal": ")" },
            {
              "nome": "laco_principal",
              "filhos": [
                { "terminal": "(" },
                {
                  "nome": "linha_ou_fim",
                  "filhos": [
                    { "terminal": "END" },
                    { "terminal": ")" }
                  ]
                }
              ]
            }
          ]
        }
      ]
    }
  ]
}
```

---

## Segundo Exemplo: Expressão Aninhada

**Entrada:** `( START ) ( ( A B + ) ( C D * ) / ) ( END )`

**AST resultante:**

```
programa_ast
└── instrucoes: [
      operacao "/"
      ├── esquerda:
      │   operacao "+"
      │   ├── esquerda:  variavel "A"
      │   └── direita:   variavel "B"
      └── direita:
          operacao "*"
          ├── esquerda:  variavel "C"
          └── direita:   variavel "D"
    ]
```

Equivalente infixo: `(A + B) / (C * D)`

---

## Terceiro Exemplo: Estrutura de Controle WHILE

**Entrada:** `( START ) ( X 10 < { ( X 1 + ) } WHILE ) ( END )`

**AST resultante:**

```
programa_ast
└── instrucoes: [
      controle "WHILE"
      ├── condicao:
      │   operacao "<"
      │   ├── esquerda:  variavel "X"
      │   └── direita:   numero 10
      └── bloco:
          bloco
          └── instrucoes: [
                operacao "+"
                ├── esquerda:  variavel "X"
                └── direita:   numero 1
              ]
    ]
```

Equivalente em pseudocódigo:
```
while (X < 10) {
    X + 1
}
```

---

## Código Assembly ARMv7 (VFP) Gerado

Para a entrada `( START ) ( 3 2 + ) ( END )`, o gerador de código produz:

```asm
.global _start

.data
    array_res: .space 8000
    ptr_res: .word 0
    const_0: .double 3.0
    const_1: .double 2.0

.text
_start:
    @ Carrega operando esquerdo (3)
    LDR R0, =const_0
    VLDR D0, [R0]
    VPUSH {D0}

    @ Carrega operando direito (2)
    LDR R0, =const_1
    VLDR D0, [R0]
    VPUSH {D0}

    @ Operação: +
    VPOP {D1}    @ Direito
    VPOP {D0}    @ Esquerdo
    VADD.F64 D0, D0, D1
    VPUSH {D0}

    @ Salva resultado no histórico (RES)
    VPOP {D0}
    LDR R0, =array_res
    LDR R1, =ptr_res
    LDR R2, [R1]
    ADD R3, R0, R2, LSL #3
    VSTR.F64 D0, [R3]
    ADD R2, R2, #1
    STR R2, [R1]
    VPUSH {D0}

    MOV R7, #1
    SWI 0
```

> **Resultado esperado em D0:** `5.0` (3 + 2)
