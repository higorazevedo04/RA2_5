.global _start

.data
    array_res: .space 8000
    ptr_res: .word 0

    const_0: .double 0.0
    const_1: .double 1.0
    const_2: .double 10.5
    const_3: .double 2.5
    const_4: .double 100
    const_5: .double 20
    const_6: .double 2
    const_7: .double 3
    const_8: .double 5
    const_9: .double 1
    const_10: .double 10
    const_11: .double 0
    FINAL: .double 0.0
    RESULT: .double 0.0

.text
_start:
    LDR R0, =const_2
    VLDR D0, [R0]
    VPUSH {D0}
    LDR R0, =const_3
    VLDR D0, [R0]
    VPUSH {D0}

    @ operacao +
    VPOP {D1}
    VPOP {D0}
    VADD.F64 D0, D0, D1
    VPUSH {D0}

    @ salva no historico
    VPOP {D0}
    LDR R0, =array_res
    LDR R1, =ptr_res
    LDR R2, [R1]
    ADD R3, R0, R2, LSL #3
    VSTR.F64 D0, [R3]
    ADD R2, R2, #1
    STR R2, [R1]
    VPUSH {D0}
    LDR R0, =const_4
    VLDR D0, [R0]
    VPUSH {D0}
    LDR R0, =const_5
    VLDR D0, [R0]
    VPUSH {D0}

    @ operacao -
    VPOP {D1}
    VPOP {D0}
    VSUB.F64 D0, D0, D1
    VPUSH {D0}

    @ salva no historico
    VPOP {D0}
    LDR R0, =array_res
    LDR R1, =ptr_res
    LDR R2, [R1]
    ADD R3, R0, R2, LSL #3
    VSTR.F64 D0, [R3]
    ADD R2, R2, #1
    STR R2, [R1]
    VPUSH {D0}
    LDR R0, =const_6
    VLDR D0, [R0]
    VPUSH {D0}
    LDR R0, =const_7
    VLDR D0, [R0]
    VPUSH {D0}

    @ operacao ^
    VPOP {D1}
    VPOP {D0}
    VCVT.S32.F64 S1, D1
    VMOV R1, S1
    LDR R2, =const_1
    VLDR D2, [R2]
    B pow_check_0
pow_loop_0:
    VMUL.F64 D2, D2, D0
    SUB R1, R1, #1
pow_check_0:
    CMP R1, #0
    BGT pow_loop_0
    VMOV.F64 D0, D2
    VPUSH {D0}
    LDR R0, =const_8
    VLDR D0, [R0]
    VPUSH {D0}

    @ operacao *
    VPOP {D1}
    VPOP {D0}
    VMUL.F64 D0, D0, D1
    VPUSH {D0}

    @ salva no historico
    VPOP {D0}
    LDR R0, =array_res
    LDR R1, =ptr_res
    LDR R2, [R1]
    ADD R3, R0, R2, LSL #3
    VSTR.F64 D0, [R3]
    ADD R2, R2, #1
    STR R2, [R1]
    VPUSH {D0}
    LDR R0, =const_9
    VLDR D0, [R0]
    VPUSH {D0}

    @ comando RES
    VPOP {D0}
    VCVT.S32.F64 S0, D0
    VMOV R1, S0
    SUB R1, R1, #1
    LDR R0, =array_res
    ADD R2, R0, R1, LSL #3
    VLDR D0, [R2]
    VPUSH {D0}
    LDR R0, =const_6
    VLDR D0, [R0]
    VPUSH {D0}

    @ comando RES
    VPOP {D0}
    VCVT.S32.F64 S0, D0
    VMOV R1, S0
    SUB R1, R1, #1
    LDR R0, =array_res
    ADD R2, R0, R1, LSL #3
    VLDR D0, [R2]
    VPUSH {D0}

    @ operacao +
    VPOP {D1}
    VPOP {D0}
    VADD.F64 D0, D0, D1
    VPUSH {D0}

    @ salva no historico
    VPOP {D0}
    LDR R0, =array_res
    LDR R1, =ptr_res
    LDR R2, [R1]
    ADD R3, R0, R2, LSL #3
    VSTR.F64 D0, [R3]
    ADD R2, R2, #1
    STR R2, [R1]
    VPUSH {D0}
    LDR R0, =const_10
    VLDR D0, [R0]
    VPUSH {D0}
    LDR R0, =const_8
    VLDR D0, [R0]
    VPUSH {D0}

    @ operacao //
    VPOP {D1}
    VPOP {D0}
    VDIV.F64 D0, D0, D1
    VCVT.S32.F64 S0, D0
    VCVT.F64.S32 D0, S0
    VPUSH {D0}
    LDR R0, =const_6
    VLDR D0, [R0]
    VPUSH {D0}

    @ operacao *
    VPOP {D1}
    VPOP {D0}
    VMUL.F64 D0, D0, D1
    VPUSH {D0}

    @ salva no historico
    VPOP {D0}
    LDR R0, =array_res
    LDR R1, =ptr_res
    LDR R2, [R1]
    ADD R3, R0, R2, LSL #3
    VSTR.F64 D0, [R3]
    ADD R2, R2, #1
    STR R2, [R1]
    VPUSH {D0}
    LDR R0, =FINAL
    VLDR D0, [R0]
    VPUSH {D0}

    @ salva no historico
    VPOP {D0}
    LDR R0, =array_res
    LDR R1, =ptr_res
    LDR R2, [R1]
    ADD R3, R0, R2, LSL #3
    VSTR.F64 D0, [R3]
    ADD R2, R2, #1
    STR R2, [R1]
    VPUSH {D0}

    @ if
    LDR R0, =FINAL
    VLDR D0, [R0]
    VPUSH {D0}
    LDR R0, =const_11
    VLDR D0, [R0]
    VPUSH {D0}

    @ operacao >
    VPOP {D1}
    VPOP {D0}
    VCMP.F64 D0, D1
    VMRS APSR_nzcv, FPSCR
    LDR R0, =const_0
    LDRGT R0, =const_1
    VLDR D0, [R0]
    VPUSH {D0}
    VPOP {D0}
    LDR R0, =const_0
    VLDR D1, [R0]
    VCMP.F64 D0, D1
    VMRS APSR_nzcv, FPSCR
    BEQ if_end_0
    LDR R0, =FINAL
    VLDR D0, [R0]
    VPUSH {D0}
    LDR R0, =const_9
    VLDR D0, [R0]
    VPUSH {D0}

    @ operacao +
    VPOP {D1}
    VPOP {D0}
    VADD.F64 D0, D0, D1
    VPUSH {D0}

    @ salva no historico
    VPOP {D0}
    LDR R0, =array_res
    LDR R1, =ptr_res
    LDR R2, [R1]
    ADD R3, R0, R2, LSL #3
    VSTR.F64 D0, [R3]
    ADD R2, R2, #1
    STR R2, [R1]
    VPUSH {D0}
if_end_0:
    LDR R0, =const_6
    VLDR D0, [R0]
    VPUSH {D0}
    LDR R0, =const_7
    VLDR D0, [R0]
    VPUSH {D0}

    @ operacao +
    VPOP {D1}
    VPOP {D0}
    VADD.F64 D0, D0, D1
    VPUSH {D0}

    @ salva no historico
    VPOP {D0}
    LDR R0, =array_res
    LDR R1, =ptr_res
    LDR R2, [R1]
    ADD R3, R0, R2, LSL #3
    VSTR.F64 D0, [R3]
    ADD R2, R2, #1
    STR R2, [R1]
    VPUSH {D0}
    LDR R0, =const_10
    VLDR D0, [R0]
    VPUSH {D0}
    LDR R0, =const_7
    VLDR D0, [R0]
    VPUSH {D0}

    @ operacao %
    VPOP {D1}
    VPOP {D0}
    VMOV.F64 D2, D0
    VDIV.F64 D3, D0, D1
    VCVT.S32.F64 S0, D3
    VCVT.F64.S32 D3, S0
    VMUL.F64 D3, D3, D1
    VSUB.F64 D0, D2, D3
    VPUSH {D0}

    @ salva no historico
    VPOP {D0}
    LDR R0, =array_res
    LDR R1, =ptr_res
    LDR R2, [R1]
    ADD R3, R0, R2, LSL #3
    VSTR.F64 D0, [R3]
    ADD R2, R2, #1
    STR R2, [R1]
    VPUSH {D0}
    LDR R0, =RESULT
    VLDR D0, [R0]
    VPUSH {D0}

    @ salva no historico
    VPOP {D0}
    LDR R0, =array_res
    LDR R1, =ptr_res
    LDR R2, [R1]
    ADD R3, R0, R2, LSL #3
    VSTR.F64 D0, [R3]
    ADD R2, R2, #1
    STR R2, [R1]
    VPUSH {D0}

    @ if
    LDR R0, =RESULT
    VLDR D0, [R0]
    VPUSH {D0}
    LDR R0, =const_8
    VLDR D0, [R0]
    VPUSH {D0}

    @ operacao >
    VPOP {D1}
    VPOP {D0}
    VCMP.F64 D0, D1
    VMRS APSR_nzcv, FPSCR
    LDR R0, =const_0
    LDRGT R0, =const_1
    VLDR D0, [R0]
    VPUSH {D0}
    VPOP {D0}
    LDR R0, =const_0
    VLDR D1, [R0]
    VCMP.F64 D0, D1
    VMRS APSR_nzcv, FPSCR
    BEQ if_end_1
    LDR R0, =RESULT
    VLDR D0, [R0]
    VPUSH {D0}
    LDR R0, =const_9
    VLDR D0, [R0]
    VPUSH {D0}

    @ operacao -
    VPOP {D1}
    VPOP {D0}
    VSUB.F64 D0, D0, D1
    VPUSH {D0}

    @ salva no historico
    VPOP {D0}
    LDR R0, =array_res
    LDR R1, =ptr_res
    LDR R2, [R1]
    ADD R3, R0, R2, LSL #3
    VSTR.F64 D0, [R3]
    ADD R2, R2, #1
    STR R2, [R1]
    VPUSH {D0}
if_end_1:
    MOV R7, #1
    SWI 0
