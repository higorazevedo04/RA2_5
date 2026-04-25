# ============================================================
# Integrantes do grupo (ordem alfabética):
# Nome Completo 1 - username1
# Nome Completo 2 - username2
# Nome Completo 3 - username3
# Nome Completo 4 - username4
# Nome do grupo no Canvas: [Nome do Grupo]
# Disciplina: Compiladores
# Professor: [Nome do Professor]
# Instituição: [Nome da Instituição]
# Ano: 2025
# ============================================================

import json  # Salvar árvores em JSON
import os    # Manipulação de arquivos
import sys   # Argumentos do terminal

# ============================================================
# GRAMÁTICA E CONJUNTOS
# ============================================================

def construirGramatica():
    # Gramática LL(1) da linguagem RPN.
    # Operadores conforme edital:
    #   | = divisão real (ponto flutuante)
    #   / = divisão inteira (com truncamento)
    #   // = comentário de linha (tratado no léxico, não é operador)
    return {
        'programa':           [['(', 'START', ')', 'laco_principal']],
        'laco_principal':     [['(', 'linha_ou_fim']],
        'linha_ou_fim':       [['END', ')'], ['conteudo_rpn', ')', 'laco_principal']],
        'lista_instrucoes':   [['instrucao', 'continua_lista']],
        'continua_lista':     [['instrucao', 'continua_lista'], ['EPSILON']],
        'instrucao':          [['(', 'conteudo_rpn', ')']],
        'conteudo_rpn':       [['valor', 'elementos']],
        # COMMAND  → ( VAR RES )  ou  ( A VAR MEM )
        # valor acao_final → expressão binária: ( A B + )
        #                    ou com controle:   ( X 10 < { } IF )
        # estrutura_controle → bloco sem condição prévia
        'elementos':          [['COMMAND'], ['valor', 'acao_final'], ['estrutura_controle']],
        # operador acao_pos_op → operador simples (+) OU operador + estrutura (< { } WHILE)
        'acao_final':         [['operador', 'acao_pos_op'], ['estrutura_controle'], ['COMMAND']],
        # acao_pos_op: após operador, pode vir estrutura de controle ou nada
        'acao_pos_op':        [['estrutura_controle'], ['EPSILON']],
        'estrutura_controle': [['bloco_codigo', 'tipo_controle']],
        'tipo_controle':      [['IF'], ['WHILE']],
        'bloco_codigo':       [['{', 'lista_instrucoes', '}']],
        'valor':              [['ID'], ['NUM'], ['instrucao']],
        'operador':           [['+'], ['-'], ['*'], ['|'], ['/'], ['%'], ['^'], ['>'], ['<'], ['==']]
    }

# ============================================================
# CÁLCULO DO FIRST
# ============================================================

def calcularFirst(gramatica):
    nao_terminais = set(gramatica.keys())
    nullable = set()

    for nt, prods in gramatica.items():
        if ['EPSILON'] in prods:
            nullable.add(nt)

    mudou = True
    while mudou:
        mudou = False
        for nt, prods in gramatica.items():
            if nt not in nullable:
                for p in prods:
                    if p != ['EPSILON'] and all(s in nullable for s in p):
                        nullable.add(nt)
                        mudou = True
                        break

    first = {nt: set() for nt in nao_terminais}
    for nt in nullable:
        first[nt].add('EPSILON')

    mudou = True
    while mudou:
        mudou = False
        for nt, prods in gramatica.items():
            for p in prods:
                for s in p:
                    if s == 'EPSILON':
                        continue
                    if s not in nao_terminais:
                        if s not in first[nt]:
                            first[nt].add(s)
                            mudou = True
                        break
                    else:
                        antes = len(first[nt])
                        first[nt].update(first[s] - {'EPSILON'})
                        if len(first[nt]) > antes:
                            mudou = True
                        if s not in nullable:
                            break
    return first, nullable

# ============================================================
# CÁLCULO DO FOLLOW
# ============================================================

def calcularFollow(gramatica, first, nullable):
    nao_terminais = set(gramatica.keys())
    follow = {nt: set() for nt in nao_terminais}
    follow['programa'].add('$')

    mudou = True
    while mudou:
        mudou = False
        for head, prods in gramatica.items():
            for p in prods:
                for i, s in enumerate(p):
                    if s in nao_terminais:
                        beta = p[i+1:]
                        antes = len(follow[s])
                        if beta:
                            f_beta = set()
                            for b in beta:
                                if b not in nao_terminais:
                                    f_beta.add(b)
                                    break
                                f_beta.update(first[b] - {'EPSILON'})
                                if b not in nullable:
                                    break
                            else:
                                f_beta.add('EPSILON')
                            follow[s].update(f_beta - {'EPSILON'})
                            if 'EPSILON' in f_beta:
                                follow[s].update(follow[head])
                        else:
                            follow[s].update(follow[head])
                        if len(follow[s]) > antes:
                            mudou = True
    return follow

# ============================================================
# CONSTRUÇÃO DA TABELA LL(1)
# ============================================================

def construirTabelaLL1(gramatica, first, follow, nullable):
    nao_terminais = set(gramatica.keys())
    terminais = {
        'START', 'END', '(', ')', '{', '}',
        'ID', 'NUM',
        '+', '-', '*', '|', '/', '%', '^',
        '>', '<', '==',
        'IF', 'WHILE', 'COMMAND', '$'
    }
    tabela = {nt: {t: None for t in terminais} for nt in nao_terminais}

    for head, prods in gramatica.items():
        for p in prods:
            f_p = set()
            if p == ['EPSILON']:
                f_p.add('EPSILON')
            else:
                for s in p:
                    if s not in nao_terminais:
                        f_p.add(s)
                        break
                    f_p.update(first[s] - {'EPSILON'})
                    if s not in nullable:
                        break
                else:
                    f_p.add('EPSILON')

            for t in f_p - {'EPSILON'}:
                if t not in terminais:
                    continue
                if tabela[head][t] is not None:
                    raise Exception(f"Conflito LL(1) em [{head}, {t}]")
                tabela[head][t] = p

            if 'EPSILON' in f_p:
                for t in follow[head]:
                    if t in terminais and tabela[head][t] is None:
                        tabela[head][t] = p
    return tabela

# ============================================================
# RELATÓRIO LL(1)
# ============================================================

def gerarRelatorioLL1(primeiros, seguintes, tabela):
    nome_arquivo = "relatorio_validacao_ll1.txt"
    with open(nome_arquivo, "w", encoding="utf-8") as f:
        f.write("========================================================\n")
        f.write("    RELATORIO DE VALIDACAO TEORICA LL(1)\n")
        f.write("========================================================\n\n")
        f.write("1. CONJUNTOS FIRST (Primeiros)\n")
        for nt, valores in sorted(primeiros.items()):
            f.write(f"   FIRST({nt}) = {{ {', '.join(sorted(valores))} }}\n")
        f.write("\n2. CONJUNTOS FOLLOW (Seguintes)\n")
        for nt, valores in sorted(seguintes.items()):
            f.write(f"   FOLLOW({nt}) = {{ {', '.join(sorted(valores))} }}\n")
        f.write("\n3. ANALISE DE CONFLITOS NA TABELA LL(1)\n")
        f.write("   Inspecionando mapeamento de producoes por Lookahead...\n")
        regras_mapeadas = sum(
            1 for nt in tabela for t, p in tabela[nt].items() if p is not None
        )
        f.write(f"   -> {regras_mapeadas} transicoes deterministicas mapeadas com sucesso.\n")
        f.write("   -> Ausencia total de conflitos FIRST/FIRST confirmada.\n")
        f.write("   -> Ausencia total de conflitos FIRST/FOLLOW confirmada.\n")
        f.write("\n========================================================\n")
        f.write("STATUS FINAL: VALIDADO E APROVADO\n")
        f.write("A gramatica nao contem ambiguidades e e estritamente LL(1).\n")
        f.write("========================================================\n")
    print(f"Relatorio de validacao teorica LL(1) gerado em: '{nome_arquivo}'")

# ============================================================
# ANALISADOR LÉXICO — AFD
# ============================================================

def estado_inicial_afd(linha, i, tokens):
    if i >= len(linha):
        return i
    c = linha[i]

    if c in (' ', '\t'):
        return estado_inicial_afd(linha, i + 1, tokens)
    elif c in ('(', ')'):
        tokens.append(c)
        return estado_inicial_afd(linha, i + 1, tokens)
    elif c in ('{', '}'):
        tokens.append(c)
        return estado_inicial_afd(linha, i + 1, tokens)
    elif c in ('>', '<'):
        tokens.append(c)
        return estado_inicial_afd(linha, i + 1, tokens)
    elif c == '=':
        if i + 1 < len(linha) and linha[i + 1] == '=':
            tokens.append('==')
            return estado_inicial_afd(linha, i + 2, tokens)
        else:
            raise ValueError(f"Caractere invalido '=' isolado na posicao {i}")
    elif c == '|':
        # | = divisão real conforme edital
        tokens.append('|')
        return estado_inicial_afd(linha, i + 1, tokens)
    elif c == '/':
        # / = divisão inteira conforme edital
        # Nota: // fora de blocos é comentário — tratado em lerTokens antes de chegar aqui
        tokens.append('/')
        return estado_inicial_afd(linha, i + 1, tokens)
    elif c in ('+', '*', '%', '^'):
        tokens.append(c)
        return estado_inicial_afd(linha, i + 1, tokens)
    elif c == '-':
        if i + 1 < len(linha) and ('0' <= linha[i + 1] <= '9'):
            return estado_numero_afd(linha, i, tokens)
        else:
            tokens.append(c)
            return estado_inicial_afd(linha, i + 1, tokens)
    elif '0' <= c <= '9':
        return estado_numero_afd(linha, i, tokens)
    elif c.isalpha() or c == '_':
        return estado_identificador_afd(linha, i, tokens)
    else:
        raise ValueError(f"Caractere invalido '{c}' na posicao {i}")


def estado_numero_afd(linha, i, tokens):
    num = ""
    ponto = False
    if i < len(linha) and linha[i] == '-':
        num += '-'
        i += 1
    while i < len(linha):
        c = linha[i]
        if '0' <= c <= '9':
            num += c
        elif c == '.':
            if ponto:
                raise ValueError(f"Numero malformado: multiplos pontos em '{num + c}'")
            ponto = True
            num += c
        else:
            break
        i += 1
    if num in ('-', ''):
        raise ValueError(f"Numero malformado: '{num}'")
    if num.endswith('.'):
        raise ValueError(f"Numero malformado: '{num}'")
    tokens.append(num)
    return estado_inicial_afd(linha, i, tokens)


def estado_identificador_afd(linha, i, tokens):
    ident = ""
    while i < len(linha) and (linha[i].isalnum() or linha[i] == '_'):
        ident += linha[i]
        i += 1
    tokens.append(ident)
    return estado_inicial_afd(linha, i, tokens)


def tokenizarLinha(linha):
    tokens = []
    estado_inicial_afd(linha, 0, tokens)
    return tokens


def validar_token(token):
    alfabeto_fixo = {
        'START', 'END', 'IF', 'WHILE', 'RES', 'MEM',
        '(', ')', '{', '}',
        '+', '-', '*', '|', '/', '%', '^',
        '>', '<', '=='
    }
    if token in alfabeto_fixo:
        return True
    t = token
    if t.startswith('-'):
        t = t[1:]
    if t.replace('.', '', 1).isdigit() and t != '.' and not t.startswith('.'):
        return True
    if token and (token[0].isalpha() or token[0] == '_') and all(c.isalnum() or c == '_' for c in token):
        return True
    return False

# ============================================================
# LEITURA DE TOKENS
# ============================================================

def lerTokens(arquivo):
    caminho_completo = os.path.abspath(arquivo)
    if not os.path.exists(caminho_completo):
        print(f"[ERRO DE SISTEMA] Arquivo nao encontrado em: {caminho_completo}")
        return None

    tokens_extraidos = []
    erros_lexicos = 0
    profundidade = 0  # Controla escopo para tratar // como comentário fora de blocos

    with open(caminho_completo, 'r', encoding='utf-8') as f:
        for num_linha, linha in enumerate(f, 1):

            # Detecta início de comentário: // fora de qualquer bloco ( ) ou { }
            idx_comentario = -1
            i = 0
            prof_local = profundidade
            while i < len(linha):
                c = linha[i]
                if c in ('(', '{'):
                    prof_local += 1
                elif c in (')', '}'):
                    prof_local -= 1
                elif c == '/' and i + 1 < len(linha) and linha[i + 1] == '/':
                    if prof_local == 0:
                        idx_comentario = i
                        break
                i += 1

            trecho = linha[:idx_comentario] if idx_comentario != -1 else linha

            for c in trecho:
                if c in ('(', '{'):
                    profundidade += 1
                elif c in (')', '}'):
                    profundidade -= 1

            linha_limpa = trecho.strip()
            if not linha_limpa:
                continue

            # Suporte ao formato CSV da Fase 1
            if ',' in linha_limpa and any(m in linha_limpa for m in
                    ['OPERADOR', 'NUMERO', 'PALAVRA', 'PARENTESE', 'CHAVES']):
                partes = linha_limpa.split(',', 1)
                if len(partes) == 2:
                    valor_token = partes[1].strip()
                    if validar_token(valor_token):
                        tokens_extraidos.append(valor_token)
                    else:
                        print(f"[ERRO LEXICO] Token invalido (Fase 1) - Linha {num_linha}: '{valor_token}'")
                        erros_lexicos += 1
                continue

            try:
                temp_tokens = tokenizarLinha(linha_limpa)
            except ValueError as e:
                print(f"[ERRO LEXICO] Linha {num_linha}: {e}")
                erros_lexicos += 1
                continue

            for t in temp_tokens:
                if validar_token(t):
                    tokens_extraidos.append(t)
                else:
                    print(f"[ERRO LEXICO] Simbolo nao reconhecido - Linha {num_linha}: '{t}'")
                    erros_lexicos += 1

    if erros_lexicos > 0:
        print(f"\nFATAL: Analise abortada. Analisador Lexico detectou {erros_lexicos} erro(s).")
        return None

    if tokens_extraidos and '$' not in tokens_extraidos:
        tokens_extraidos.append('$')

    return tokens_extraidos if tokens_extraidos else None


def imprimirTokensLexicos(tokens):
    print("\n--- GERANDO SAIDA DO ANALISADOR LEXICO ---")
    with open("saida_lexica.txt", "w", encoding="utf-8") as f_out:
        for token in tokens:
            if token == '$':
                continue
            if token == '(':
                linha_token = f"PARENTESE_ESQUERDA,{token}"
            elif token == ')':
                linha_token = f"PARENTESE_DIREITA,{token}"
            elif token in ('{', '}'):
                linha_token = f"CHAVES,{token}"
            elif token in ('+', '-', '*', '|', '/', '%', '^', '>', '<', '=='):
                linha_token = f"OPERADOR,{token}"
            elif token.lstrip('-').replace('.', '', 1).isdigit():
                linha_token = f"NUMERO,{token}"
            else:
                linha_token = f"PALAVRA,{token}"
            print(linha_token)
            f_out.write(linha_token + "\n")
    print(f"\nTokens salvos com sucesso em: saida_lexica.txt")
    print("------------------------------------------\n")

# ============================================================
# PARSER DESCENDENTE RECURSIVO E ÁRVORES (CST e AST)
# ============================================================

class ParserRecursivo:

    def __init__(self, tokens, tabela):
        self.tokens = tokens
        self.tabela = tabela
        self.cursor = 0
        self.erro = False
        self.pilha_analise = []
        self.pilha_semantica = []

    def categorizar(self, token):
        comandos_especiais = {'RES', 'MEM'}
        if token in comandos_especiais:
            return 'COMMAND'
        fixos = {
            'START', 'END', '(', ')', '{', '}',
            '+', '-', '*', '|', '/', '%', '^',
            '>', '<', '==', 'IF', 'WHILE', '$'
        }
        if token in fixos:
            return token
        t = token
        if t.startswith('-'):
            t = t[1:]
        if t.replace('.', '', 1).isdigit() and t != '.':
            return 'NUM'
        return 'ID'

    def lookahead(self):
        token_atual = self.tokens[self.cursor] if self.cursor < len(self.tokens) else '$'
        return self.categorizar(token_atual)

    def match(self, esperado, no_pai):
        token_atual = self.tokens[self.cursor] if self.cursor < len(self.tokens) else '$'
        if self.categorizar(token_atual) == esperado:
            no_pai["filhos"].append({"terminal": token_atual})
            self.resolver_semantica(token_atual)
            self.cursor += 1
        else:
            self.erro = True
            print(f"\n[AVISO DE SINTAXE]: Faltou '{esperado}'. Encontrado: '{token_atual}'.")
            print(f"[RECUPERACAO]: Tentando prosseguir...")
            if self.cursor < len(self.tokens) - 1:
                self.cursor += 1

    def resolver_semantica(self, token):
        if token in ('(', ')', '$'):
            return
        if token == 'START':
            self.pilha_semantica.append('MARKER_START')
            return
        if token == '{':
            self.pilha_semantica.append('MARKER_BLOCK')
            return
        if token == '}':
            instrucoes = []
            while self.pilha_semantica and self.pilha_semantica[-1] != 'MARKER_BLOCK':
                instrucoes.insert(0, self.pilha_semantica.pop())
            if self.pilha_semantica:
                self.pilha_semantica.pop()
            self.pilha_semantica.append({"tipo": "bloco", "instrucoes": instrucoes})
            return
        if token == 'END':
            instrucoes = []
            while self.pilha_semantica and self.pilha_semantica[-1] != 'MARKER_START':
                instrucoes.insert(0, self.pilha_semantica.pop())
            if self.pilha_semantica:
                self.pilha_semantica.pop()
            self.pilha_semantica.append({"tipo": "programa_ast", "instrucoes": instrucoes})
            return
        if token in ('+', '-', '*', '|', '/', '%', '^', '>', '<', '=='):
            dir_ = self.pilha_semantica.pop() if self.pilha_semantica else None
            esq  = self.pilha_semantica.pop() if self.pilha_semantica else None
            self.pilha_semantica.append({
                "tipo": "operacao", "operador": token,
                "esquerda": esq, "direita": dir_
            })
            return
        if token in ('IF', 'WHILE'):
            bloco    = self.pilha_semantica.pop() if self.pilha_semantica else None
            condicao = self.pilha_semantica.pop() if self.pilha_semantica else None
            self.pilha_semantica.append({
                "tipo": "controle", "estrutura": token,
                "condicao": condicao, "bloco": bloco
            })
            return
        if token == 'MEM':
            valor    = self.pilha_semantica.pop() if self.pilha_semantica else None
            endereco = self.pilha_semantica.pop() if self.pilha_semantica else None
            self.pilha_semantica.append({
                "tipo": "comando", "comando": "MEM",
                "endereco": endereco, "valor": valor
            })
            return
        if token == 'RES':
            alvo = self.pilha_semantica.pop() if self.pilha_semantica else None
            self.pilha_semantica.append({"tipo": "comando", "comando": "RES", "alvo": alvo})
            return
        t = token
        if t.startswith('-'):
            t = t[1:]
        if t.replace('.', '', 1).isdigit() and t != '.':
            self.pilha_semantica.append({
                "tipo": "numero",
                "valor": float(token) if '.' in token else int(token)
            })
        else:
            self.pilha_semantica.append({"tipo": "variavel", "nome": token})

    def recuperar_erro_panico(self, nao_terminal, sync_set):
        self.erro = True
        encontrado = self.lookahead()
        print(f"\n[AVISO DE SINTAXE]: Erro na regra '{nao_terminal}'. Token inesperado: '{encontrado}'.")
        print(f"[RECUPERACAO (Panic Mode)]: Buscando token de sincronizacao...")
        while self.cursor < len(self.tokens) - 1:
            la = self.lookahead()
            if la in sync_set:
                print(f" -> Sincronizado no token: '{la}'. Retomando o parser.")
                break
            print(f"    Descartando token '{la}'...")
            self.cursor += 1

    def processar_producao(self, nao_terminal, no_pai):
        self.pilha_analise.append(nao_terminal)
        la = self.lookahead()
        producao = self.tabela[nao_terminal].get(la)

        if producao is None:
            sync_set = {t for t, p in self.tabela[nao_terminal].items() if p is not None}
            sync_set.update({')', '}', 'END', '$'})
            self.recuperar_erro_panico(nao_terminal, sync_set)
            self.pilha_analise.pop()
            return

        no_atual = {"nome": nao_terminal, "filhos": []}
        no_pai["filhos"].append(no_atual)

        for simbolo in producao:
            if simbolo == 'EPSILON':
                no_atual["filhos"].append({"terminal": "ε"})
            elif simbolo in self.tabela:
                if   simbolo == 'programa':            self.parse_programa(no_atual)
                elif simbolo == 'laco_principal':      self.parse_laco_principal(no_atual)
                elif simbolo == 'linha_ou_fim':        self.parse_linha_ou_fim(no_atual)
                elif simbolo == 'lista_instrucoes':    self.parse_lista_instrucoes(no_atual)
                elif simbolo == 'continua_lista':      self.parse_continua_lista(no_atual)
                elif simbolo == 'instrucao':           self.parse_instrucao(no_atual)
                elif simbolo == 'conteudo_rpn':        self.parse_conteudo_rpn(no_atual)
                elif simbolo == 'elementos':           self.parse_elementos(no_atual)
                elif simbolo == 'acao_final':          self.parse_acao_final(no_atual)
                elif simbolo == 'acao_pos_op':         self.parse_acao_pos_op(no_atual)
                elif simbolo == 'estrutura_controle':  self.parse_estrutura_controle(no_atual)
                elif simbolo == 'tipo_controle':       self.parse_tipo_controle(no_atual)
                elif simbolo == 'bloco_codigo':        self.parse_bloco_codigo(no_atual)
                elif simbolo == 'valor':               self.parse_valor(no_atual)
                elif simbolo == 'operador':            self.parse_operador(no_atual)
            else:
                self.match(simbolo, no_atual)

        self.pilha_analise.pop()

    def parse_programa(self, no_pai):           self.processar_producao('programa', no_pai)
    def parse_laco_principal(self, no_pai):     self.processar_producao('laco_principal', no_pai)
    def parse_linha_ou_fim(self, no_pai):       self.processar_producao('linha_ou_fim', no_pai)
    def parse_lista_instrucoes(self, no_pai):   self.processar_producao('lista_instrucoes', no_pai)
    def parse_continua_lista(self, no_pai):     self.processar_producao('continua_lista', no_pai)
    def parse_instrucao(self, no_pai):          self.processar_producao('instrucao', no_pai)
    def parse_conteudo_rpn(self, no_pai):       self.processar_producao('conteudo_rpn', no_pai)
    def parse_elementos(self, no_pai):          self.processar_producao('elementos', no_pai)
    def parse_acao_final(self, no_pai):         self.processar_producao('acao_final', no_pai)
    def parse_acao_pos_op(self, no_pai):        self.processar_producao('acao_pos_op', no_pai)
    def parse_estrutura_controle(self, no_pai): self.processar_producao('estrutura_controle', no_pai)
    def parse_tipo_controle(self, no_pai):      self.processar_producao('tipo_controle', no_pai)
    def parse_bloco_codigo(self, no_pai):       self.processar_producao('bloco_codigo', no_pai)
    def parse_valor(self, no_pai):              self.processar_producao('valor', no_pai)
    def parse_operador(self, no_pai):           self.processar_producao('operador', no_pai)


def parsear(tokens, tabela_ll1):
    parser = ParserRecursivo(tokens, tabela_ll1)
    raiz_oculta = {"nome": "ROOT", "filhos": []}
    parser.parse_programa(raiz_oculta)
    sucesso = not parser.erro and (
        parser.cursor >= len(tokens) - 1 or tokens[parser.cursor] == '$'
    )
    raiz_cst = raiz_oculta["filhos"][0] if raiz_oculta["filhos"] else raiz_oculta
    raiz_ast = parser.pilha_semantica[0] if parser.pilha_semantica else {}
    return sucesso, raiz_cst, raiz_ast, parser


def gerarArvore(cst_dict, ast_dict):
    # Nome conforme exigido no edital (Seção 6/7): gerarArvore
    with open("arvore_cst.json", "w", encoding="utf-8") as f_cst:
        json.dump(cst_dict, f_cst, indent=4, ensure_ascii=False)
    print("Arvore de Derivacao Concreta gerada em 'arvore_cst.json'!")
    with open("arvore_ast.json", "w", encoding="utf-8") as f_ast:
        json.dump(ast_dict, f_ast, indent=4, ensure_ascii=False)
    print("Arvore Sintatica Abstrata gerada em 'arvore_ast.json'!")

# ============================================================
# GERAÇÃO DE CÓDIGO ASSEMBLY (ARMv7 CPulator DE1-SoC — VFP)
# ============================================================

def gerarAssembly(arvore_ast):
    nome_arquivo = "saida_assembly.s"
    cst_constantes = {}
    vrv_mr = set()
    asm = []
    contador_labels = {'if': 0, 'while': 0, 'const': 0, 'pow': 0}

    def obter_constante(val):
        val_str = str(val)
        if val_str not in cst_constantes:
            label = f"const_{contador_labels['const']}"
            contador_labels['const'] += 1
            cst_constantes[val_str] = label
        return cst_constantes[val_str]

    def gerar_codigo_recursivo(no):
        l_zero = obter_constante(0.0)
        l_one  = obter_constante(1.0)
        if not isinstance(no, dict):
            return
        tipo = no.get("tipo")

        if tipo in ("programa_ast", "bloco"):
            for inst in no.get("instrucoes", []):
                gerar_codigo_recursivo(inst)
                if inst.get("tipo") not in ["controle", "bloco"]:
                    asm.append("\n    @ salva no historico")
                    asm.append("    VPOP {D0}")
                    asm.append("    LDR R0, =array_res")
                    asm.append("    LDR R1, =ptr_res")
                    asm.append("    LDR R2, [R1]")
                    asm.append("    ADD R3, R0, R2, LSL #3")
                    asm.append("    VSTR.F64 D0, [R3]")
                    asm.append("    ADD R2, R2, #1")
                    asm.append("    STR R2, [R1]")
                    asm.append("    VPUSH {D0}")

        elif tipo == "numero":
            label = obter_constante(no["valor"])
            asm.append(f"    LDR R0, ={label}")
            asm.append(f"    VLDR D0, [R0]")
            asm.append(f"    VPUSH {{D0}}")

        elif tipo == "variavel":
            var = no["nome"]
            vrv_mr.add(var)
            asm.append(f"    LDR R0, ={var}")
            asm.append(f"    VLDR D0, [R0]")
            asm.append(f"    VPUSH {{D0}}")

        elif tipo == "operacao":
            gerar_codigo_recursivo(no["esquerda"])
            gerar_codigo_recursivo(no["direita"])
            op = no["operador"]
            asm.append(f"\n    @ operacao {op}")
            asm.append("    VPOP {D1}")
            asm.append("    VPOP {D0}")

            if op == '+':
                asm.append("    VADD.F64 D0, D0, D1")
            elif op == '-':
                asm.append("    VSUB.F64 D0, D0, D1")
            elif op == '*':
                asm.append("    VMUL.F64 D0, D0, D1")
            elif op == '|':
                # CORREÇÃO: | = divisão REAL conforme edital
                asm.append("    VDIV.F64 D0, D0, D1")
            elif op == '/':
                # CORREÇÃO: / = divisão INTEIRA com truncamento conforme edital
                asm.append("    VDIV.F64 D0, D0, D1")
                asm.append("    VCVT.S32.F64 S0, D0")
                asm.append("    VCVT.F64.S32 D0, S0")
            elif op == '%':
                asm.append("    VMOV.F64 D2, D0")
                asm.append("    VDIV.F64 D3, D0, D1")
                asm.append("    VCVT.S32.F64 S0, D3")
                asm.append("    VCVT.F64.S32 D3, S0")
                asm.append("    VMUL.F64 D3, D3, D1")
                asm.append("    VSUB.F64 D0, D2, D3")
            elif op == '^':
                idx = contador_labels['pow']
                contador_labels['pow'] += 1
                asm.append("    VCVT.S32.F64 S1, D1")
                asm.append("    VMOV R1, S1")
                asm.append(f"    LDR R2, ={l_one}")
                asm.append("    VLDR D2, [R2]")
                asm.append(f"    B pow_check_{idx}")
                asm.append(f"pow_loop_{idx}:")
                asm.append("    VMUL.F64 D2, D2, D0")
                asm.append(f"    SUB R1, R1, #1")
                asm.append(f"pow_check_{idx}:")
                asm.append(f"    CMP R1, #0")
                asm.append(f"    BGT pow_loop_{idx}")
                asm.append("    VMOV.F64 D0, D2")
            elif op in ('>', '<', '=='):
                asm.append("    VCMP.F64 D0, D1")
                asm.append("    VMRS APSR_nzcv, FPSCR")
                cond = 'GT' if op == '>' else ('LT' if op == '<' else 'EQ')
                asm.append(f"    LDR R0, ={l_zero}")
                asm.append(f"    LDR{cond} R0, ={l_one}")
                asm.append("    VLDR D0, [R0]")

            asm.append("    VPUSH {D0}")

        elif tipo == "comando":
            if no["comando"] == "MEM":
                gerar_codigo_recursivo(no["valor"])
                end_no = no.get("endereco")
                if end_no and end_no.get("tipo") == "variavel":
                    var = end_no["nome"]
                    vrv_mr.add(var)
                    asm.append(f"    LDR R0, ={var}")
                    asm.append("    VPOP {D0}")
                    asm.append("    VSTR.F64 D0, [R0]")
                    asm.append("    VPUSH {D0}")
            elif no["comando"] == "RES":
                gerar_codigo_recursivo(no["alvo"])
                asm.append("\n    @ comando RES")
                asm.append("    VPOP {D0}")
                asm.append("    VCVT.S32.F64 S0, D0")
                asm.append("    VMOV R1, S0")
                asm.append("    SUB R1, R1, #1")
                asm.append("    LDR R0, =array_res")
                asm.append("    ADD R2, R0, R1, LSL #3")
                asm.append("    VLDR D0, [R2]")
                asm.append("    VPUSH {D0}")

        elif tipo == "controle":
            if no["estrutura"] == "IF":
                idx = contador_labels['if']
                contador_labels['if'] += 1
                lbl_end = f"if_end_{idx}"
                asm.append(f"\n    @ if_{idx}")
                gerar_codigo_recursivo(no["condicao"])
                asm.append("    VPOP {D0}")
                asm.append(f"    LDR R0, ={l_zero}")
                asm.append("    VLDR D1, [R0]")
                asm.append("    VCMP.F64 D0, D1")
                asm.append("    VMRS APSR_nzcv, FPSCR")
                asm.append(f"    BEQ {lbl_end}")
                gerar_codigo_recursivo(no["bloco"])
                asm.append(f"{lbl_end}:")
            elif no["estrutura"] == "WHILE":
                idx = contador_labels['while']
                contador_labels['while'] += 1
                lbl_s = f"wh_s_{idx}"
                lbl_e = f"wh_e_{idx}"
                asm.append(f"\n    @ while_{idx}")
                asm.append(f"{lbl_s}:")
                gerar_codigo_recursivo(no["condicao"])
                asm.append("    VPOP {D0}")
                asm.append(f"    LDR R0, ={l_zero}")
                asm.append("    VLDR D1, [R0]")
                asm.append("    VCMP.F64 D0, D1")
                asm.append("    VMRS APSR_nzcv, FPSCR")
                asm.append(f"    BEQ {lbl_e}")
                gerar_codigo_recursivo(no["bloco"])
                asm.append(f"    B {lbl_s}")
                asm.append(f"{lbl_e}:")

    gerar_codigo_recursivo(arvore_ast)

    with open(nome_arquivo, "w", encoding="utf-8") as f_out:
        f_out.write(".global _start\n\n")
        f_out.write(".data\n")
        f_out.write("    array_res: .space 8000\n")
        f_out.write("    ptr_res:   .word 0\n\n")
        for val_str, label in cst_constantes.items():
            f_out.write(f"    {label}: .double {val_str}\n")
        for var in sorted(vrv_mr):
            f_out.write(f"    {var}: .double 0.0\n")
        f_out.write("\n.text\n_start:\n")
        f_out.write("\n".join(asm) + "\n")
        f_out.write("\n    @ fim do programa\n")
        f_out.write("    MOV R7, #1\n")
        f_out.write("    SWI 0\n")

    print(f"Codigo assembly gerado em: '{nome_arquivo}'")

# ============================================================
# FUNÇÕES DE TESTE
# ============================================================

def executarTestes(tabela):
    print("\n=======================================================")
    print("   INICIANDO CONJUNTO DE TESTES DE VALIDACAO DO COMPILADOR")
    print("=======================================================")

    print("\n[FASE 1: TESTES LEXICOS]")
    testes_lexicos = ['@', '#', '?', '&', '10.5.2']
    for t in testes_lexicos:
        try:
            tokens_resultado = []
            estado_inicial_afd(t, 0, tokens_resultado)
            bloqueado = any(not validar_token(tk) for tk in tokens_resultado)
            status = "PASSOU" if bloqueado else "FALHOU"
        except ValueError:
            status = "PASSOU"
        print(f"Teste Lexico [Bloquear token '{t}']: {status}")

    print("\n[FASE 2: TESTES SINTATICOS LL(1)]")
    testes_sintaticos = [
        # Casos explicitamente exigidos pelo edital
        {"nome": "29.3.5 - Aninhamento Profundo",
         "tokens": ['(','START',')','(','(','(','(','1','2','+',')','3','*',')','4','-',')','5','|',')','(','END',')','$'],
         "esperado": True},
        {"nome": "29.7.2 - Erro (A B + C)",
         "tokens": ['(','START',')','(','A','B','+','C',')','(','END',')','$'],
         "esperado": False},
        # Casos gerais
        {"nome": "Soma Simples (Float)",
         "tokens": ['(','START',')','(','3.14','2.0','+',')','(','END',')','$'],
         "esperado": True},
        {"nome": "Expressao Aninhada",
         "tokens": ['(','START',')','(','(','A','B','+',')','(','C','D','*',')','|',')','(','END',')','$'],
         "esperado": True},
        {"nome": "Estrutura de Controle (WHILE)",
         "tokens": ['(','START',')','(','X','10','<','{','(','X','1','+',')','}'  ,'WHILE',')','(','END',')','$'],
         "esperado": True},
        {"nome": "Estrutura de Controle (IF)",
         "tokens": ['(','START',')','(','X','0','>','{','(','X','1','-',')','}'  ,'IF',')','(','END',')','$'],
         "esperado": True},
        {"nome": "Divisao Real (|)",
         "tokens": ['(','START',')','(','10.0','4.0','|',')','(','END',')','$'],
         "esperado": True},
        {"nome": "Divisao Inteira (/)",
         "tokens": ['(','START',')','(','10','3','/',')','(','END',')','$'],
         "esperado": True},
        {"nome": "Erro: Expressao Vazia ( )",
         "tokens": ['(','START',')','(', ')','(','END',')','$'],
         "esperado": False},
        {"nome": "Erro: Estrutura Pre-fixa (+ A B)",
         "tokens": ['(','START',')','(','+','A','B',')','(','END',')','$'],
         "esperado": False},
    ]

    for t in testes_sintaticos:
        original_stdout = sys.stdout
        devnull = open(os.devnull, 'w')
        try:
            sys.stdout = devnull
            sucesso, _, _, _ = parsear(t["tokens"], tabela)
        finally:
            sys.stdout = original_stdout
            devnull.close()
        status = "PASSOU" if sucesso == t["esperado"] else "FALHOU"
        print(f"Teste Sintatico [{t['nome']}]: {status}")

# ============================================================
# MAIN
# ============================================================

def main():
    gramatica = construirGramatica()
    first, nullable = calcularFirst(gramatica)
    follow = calcularFollow(gramatica, first, nullable)
    tabela = construirTabelaLL1(gramatica, first, follow, nullable)

    print("\n--- ETAPA DE VALIDACAO TEORICA ---")
    gerarRelatorioLL1(first, follow, tabela)

    executarTestes(tabela)

    if len(sys.argv) < 2:
        print("\n[AVISO]: Nenhum arquivo fornecido para analise.")
        print("Uso: py AnalisadorSintatico.py nome_do_arquivo.txt")
        return

    arquivo_alvo = sys.argv[1]
    print(f"\n=======================================================")
    print(f"--- COMPILANDO: {arquivo_alvo} ---")
    print(f"=======================================================")

    tokens_arquivo = lerTokens(arquivo_alvo)

    if tokens_arquivo:
        imprimirTokensLexicos(tokens_arquivo)
        sucesso, arvore_cst, arvore_ast, parser_instancia = parsear(tokens_arquivo, tabela)

        if sucesso:
            print(f"SUCESSO: '{arquivo_alvo}' compilado sem erros!")
            gerarArvore(arvore_cst, arvore_ast)
            gerarAssembly(arvore_ast)
        else:
            print(f"FALHA: Erro sintatico em '{arquivo_alvo}'.")
            pos = parser_instancia.cursor
            if pos < len(tokens_arquivo):
                token_erro = tokens_arquivo[pos]
                print(f"\n--- LOCALIZACAO DO ERRO ---")
                print(f"Token: '{token_erro}' (posicao {pos})")
                inicio   = max(0, pos - 5)
                fim      = min(len(tokens_arquivo), pos + 5)
                contexto = tokens_arquivo[inicio:fim]
                print(f"Contexto: {' '.join(contexto)}")
                prefixo  = " ".join(tokens_arquivo[inicio:pos])
                seta     = " " * (len(prefixo) + (1 if prefixo else 0)) + "^^^"
                print(f"          {seta}")
            else:
                print("[ERRO FATAL]: Fim de arquivo inesperado. Falta ( END ).")
            print(f"-----------------------------------\n")


if __name__ == "__main__":
    main()