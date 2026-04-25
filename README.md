# Analisador Sintatico

- Integrante: Higor Leonardo da Silva Azevedo
- Instituição: Pontifícia Universidade Católica do Paraná (PUCPR)
- Curso: Engenharia de Computação
- Disciplina: Linguagens Formais e Compiladores
- Professor: Frank de Alcantara

Este projeto consiste em um compilador completo que traduz uma linguagem baseada em Notação Polonesa Reversa (RPN) para código Assembly ARMv7, focado em operações de ponto flutuante via coprocessador VFP. O sistema realiza desde a análise léxica robusta até a geração de código otimizada para o simulador CPUlator (DE1-SoC).

Tecnologias Utilizadas
Linguagem: Python 
Target: Assembly ARMv7 (Precisão dupla/Double Precision)
Simulação: Recomendado o uso do Cpulator (ARMv7 System).

Como Executar
1. Abra o terminal na pasta do projeto.
2. Execute o analisador passando um arquivo de texto como argumento:
   ```text
       py analigador.py teste.txt
   ```
3. Artefatos Gerados:
- saida_lexica.txt: Lista de tokens categorizados.
- arvore_cst.json: Árvore de Derivação Concreta (Sintaxe).
- arvore_ast.json: Árvore Sintática Abstrata (Semântica).
- saida_assembly.s: Código fonte ARMv7 pronto para o CPUlator.
- relatorio_validacao_ll1.txt: Relatório técnico de conjuntos FIRST/FOLLOW.

O Analisador utliza grámatica LL(1). Todas as instruções devem estar contidas em blocos delimitados

Estrutura Geral
Todo programa deve iniciar com ( START ) e terminar com ( END )

Operadores Suportados
- Aritméticos: +, -, *, /, // (divisão inteira), % (módulo).
- Lógicos/Comparação: >, <, ==, | (OR bitwise).
- Especiais: ^ (potência), MEM (armazenamento), RES (resgate de histórico).

Exemplo
 ```text
( START )
( 3.1415 raio 2 ^ * ) // Calcula PI * raio²
( 100 AREA MEM )      // Armazena resultado na variável AREA
( END )
```
Laço de Repetição (Incremento de Variável)
 ```text
( START )
( X 10 < {
    ( X 1 + )        // Incrementa X em 1
    ( 0 X MEM )      // Salva novo valor em X
} WHILE )
( END )
  ```

Detalhes importantes
O gerador de código foi otimizado para o CPUlator, garantindo:
Aderência à FPU: Uso estrito de registradores Dx e Sx.
Segurança de Pilha: Todas as operações, inclusive as não nativas (%, ^), garantem o balanço da pilha VFP.
Histórico Dinâmico: O comando RES acessa um buffer de memória real (array_res) populado em tempo de execução.
