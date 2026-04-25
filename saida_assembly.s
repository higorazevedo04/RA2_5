.global _start

.data
    @ --- Gerenciamento de Memória Dinâmica ---
    array_res: .space 8000   @ Buffer para histórico de 1000 resultados (RES)
    ptr_res: .word 0         @ Ponteiro do índice de execução

    @ --- Pool de Constantes e Variáveis ---
    const_0: .double 0.0
    const_1: .double 1.0
    const_2: .double 1
    const_3: .double 2
    CONTADOR: .double 0.0
    LIMITE: .double 0.0
    PARIDADE: .double 0.0

.text
_start:
    LDR R0, =CONTADOR
    VLDR D0, [R0]
    VPUSH {D0}

    @ --- Salva estado no histórico para o comando RES ---
    VPOP {D0}
    LDR R0, =array_res
    LDR R1, =ptr_res
    LDR R2, [R1]             @ Carrega índice atual
    ADD R3, R0, R2, LSL #3   @ Endereço = array_res + (índice * 8 bytes)
    VSTR.F64 D0, [R3]        @ Salva o Double na memória
    ADD R2, R2, #1
    STR R2, [R1]             @ Incrementa o ponteiro
    VPUSH {D0}               @ Re-empilha o resultado
    @ -----------------------------------------------------

    LDR R0, =LIMITE
    VLDR D0, [R0]
    VPUSH {D0}

    @ --- Salva estado no histórico para o comando RES ---
    VPOP {D0}
    LDR R0, =array_res
    LDR R1, =ptr_res
    LDR R2, [R1]             @ Carrega índice atual
    ADD R3, R0, R2, LSL #3   @ Endereço = array_res + (índice * 8 bytes)
    VSTR.F64 D0, [R3]        @ Salva o Double na memória
    ADD R2, R2, #1
    STR R2, [R1]             @ Incrementa o ponteiro
    VPUSH {D0}               @ Re-empilha o resultado
    @ -----------------------------------------------------


    @ --- INICIO LACO WHILE ---
wh_s_0:
    LDR R0, =CONTADOR
    VLDR D0, [R0]
    VPUSH {D0}
    LDR R0, =LIMITE
    VLDR D0, [R0]
    VPUSH {D0}

    @ --- Operação: < ---
    VPOP {D1}  @ Direito
    VPOP {D0}  @ Esquerdo
    VCMP.F64 D0, D1
    VMRS APSR_nzcv, FPSCR
    LDR R0, =const_0
    LDRLT R0, =const_1
    VLDR D0, [R0]
    VPUSH {D0}
    VPOP {D0}
    LDR R0, =const_0
    VLDR D1, [R0]
    VCMP.F64 D0, D1
    VMRS APSR_nzcv, FPSCR
    BEQ wh_e_0
    LDR R0, =CONTADOR
    VLDR D0, [R0]
    VPUSH {D0}
    LDR R0, =const_2
    VLDR D0, [R0]
    VPUSH {D0}

    @ --- Operação: + ---
    VPOP {D1}  @ Direito
    VPOP {D0}  @ Esquerdo
    VADD.F64 D0, D0, D1
    VPUSH {D0}

    @ --- Salva estado no histórico para o comando RES ---
    VPOP {D0}
    LDR R0, =array_res
    LDR R1, =ptr_res
    LDR R2, [R1]             @ Carrega índice atual
    ADD R3, R0, R2, LSL #3   @ Endereço = array_res + (índice * 8 bytes)
    VSTR.F64 D0, [R3]        @ Salva o Double na memória
    ADD R2, R2, #1
    STR R2, [R1]             @ Incrementa o ponteiro
    VPUSH {D0}               @ Re-empilha o resultado
    @ -----------------------------------------------------

    LDR R0, =CONTADOR
    VLDR D0, [R0]
    VPUSH {D0}

    @ --- Salva estado no histórico para o comando RES ---
    VPOP {D0}
    LDR R0, =array_res
    LDR R1, =ptr_res
    LDR R2, [R1]             @ Carrega índice atual
    ADD R3, R0, R2, LSL #3   @ Endereço = array_res + (índice * 8 bytes)
    VSTR.F64 D0, [R3]        @ Salva o Double na memória
    ADD R2, R2, #1
    STR R2, [R1]             @ Incrementa o ponteiro
    VPUSH {D0}               @ Re-empilha o resultado
    @ -----------------------------------------------------

    LDR R0, =CONTADOR
    VLDR D0, [R0]
    VPUSH {D0}
    LDR R0, =const_3
    VLDR D0, [R0]
    VPUSH {D0}

    @ --- Operação: % ---
    VPOP {D1}  @ Direito
    VPOP {D0}  @ Esquerdo
    VMOV.F64 D2, D0          @ D2 = A
    VDIV.F64 D3, D0, D1      @ D3 = A / B
    VCVT.S32.F64 S0, D3
    VCVT.F64.S32 D3, S0      @ D3 = A // B
    VMUL.F64 D3, D3, D1      @ D3 = (A // B) * B
    VSUB.F64 D0, D2, D3      @ D0 = A - ((A // B) * B)
    VPUSH {D0}

    @ --- Salva estado no histórico para o comando RES ---
    VPOP {D0}
    LDR R0, =array_res
    LDR R1, =ptr_res
    LDR R2, [R1]             @ Carrega índice atual
    ADD R3, R0, R2, LSL #3   @ Endereço = array_res + (índice * 8 bytes)
    VSTR.F64 D0, [R3]        @ Salva o Double na memória
    ADD R2, R2, #1
    STR R2, [R1]             @ Incrementa o ponteiro
    VPUSH {D0}               @ Re-empilha o resultado
    @ -----------------------------------------------------

    LDR R0, =PARIDADE
    VLDR D0, [R0]
    VPUSH {D0}

    @ --- Salva estado no histórico para o comando RES ---
    VPOP {D0}
    LDR R0, =array_res
    LDR R1, =ptr_res
    LDR R2, [R1]             @ Carrega índice atual
    ADD R3, R0, R2, LSL #3   @ Endereço = array_res + (índice * 8 bytes)
    VSTR.F64 D0, [R3]        @ Salva o Double na memória
    ADD R2, R2, #1
    STR R2, [R1]             @ Incrementa o ponteiro
    VPUSH {D0}               @ Re-empilha o resultado
    @ -----------------------------------------------------

    B wh_s_0
wh_e_0:
    @ --- FIM LACO WHILE ---

    LDR R0, =const_2
    VLDR D0, [R0]
    VPUSH {D0}

    @ --- Comando RES (Resgatar Histórico) ---
    VPOP {D0}                @ Carrega N (Float)
    VCVT.S32.F64 S0, D0
    VMOV R1, S0              @ R1 = Inteiro N
    SUB R1, R1, #1           @ Converte para 0-based
    LDR R0, =array_res
    ADD R2, R0, R1, LSL #3   @ Endereço = array_res + (N * 8 bytes)
    VLDR D0, [R2]            @ Carrega do histórico
    VPUSH {D0}

    @ --- Salva estado no histórico para o comando RES ---
    VPOP {D0}
    LDR R0, =array_res
    LDR R1, =ptr_res
    LDR R2, [R1]             @ Carrega índice atual
    ADD R3, R0, R2, LSL #3   @ Endereço = array_res + (índice * 8 bytes)
    VSTR.F64 D0, [R3]        @ Salva o Double na memória
    ADD R2, R2, #1
    STR R2, [R1]             @ Incrementa o ponteiro
    VPUSH {D0}               @ Re-empilha o resultado
    @ -----------------------------------------------------

    MOV R7, #1
    SWI 0
