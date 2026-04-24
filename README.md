# Nome do Projeto

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
