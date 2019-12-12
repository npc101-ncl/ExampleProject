model_string = """
model myTest

    compartment cytoplasm = 1
    var S in cytoplasm
    var E in cytoplasm
    var I in cytoplasm
    var P in cytoplasm
    var ES in cytoplasm
    var EI in cytoplasm

    R1: E+S->ES; k_es*E*S;
    R2: E+I->EI; k_ei*E*I;
    R3: ES->E+S; k_res*ES;
    R4: EI->E+I; k_rei*EI;
    R5: ES->E+P; k_cat*ES;
    R6: ->I; k_Igen/(1+k_Pinh*P);
    R7: I->; k_Ideg*I;
    R8: P->; k_Pdeg*P;
    R9: S->; k_Sdeg*S;
    R10: ->S; k_Sinp*ProS;
    
    S=10
    E=0
    I=20
    P=0
    ES=0
    EI=1
    
    k_es=1
    k_ei=1
    k_res=1
    k_rei=1
    k_cat=0.1
    k_Igen=10
    k_Pinh=10
    k_Ideg=1
    k_Pdeg=0.1
    k_Sdeg=1
    k_Sinp=1

    ProS := piecewise(0.1, time > 55 ,20, time > 45, 0.1)
    
end
"""

model_string_ex="""
model exercise
    compartment cytoplasm = 1
    var _N in cytoplasm
    var _G in cytoplasm
    var _D in cytoplasm
    var _K in cytoplasm
    var Np in cytoplasm
    var Gp in cytoplasm
    var Dp in cytoplasm
    var Kp in cytoplasm
    
    RpN: _N->Np; _k_Np*_N*S
    RdN: Np->_N; _k_Nd*Np*Dp
    RpG: _G->Gp; _k_Gp*_G*Np
    RdG: Gp->_G; _k_Gd*Gp*I1
    RpD: _D->Dp; _k_Dp*_D*Gp
    RdD: Dp->_D; _k_Dd*Dp*I2
    RpK: _K->Kp; (_k_KpN*Np+_k_KpG*Gp)*_K
    RdK: Kp->_K; _k_Kd*Kp
    
    _N=36
    Np=0
    _G=10
    Gp=0
    _D=10
    Dp=0
    _K=48
    Kp=0
    
    _k_Np=0.1
    _k_Nd=0.1
    _k_Gp=0.1
    _k_Gd=0.1
    _k_Dp=0.1
    _k_Dd=0.1
    _k_KpN=0.1
    _k_KpG=0.1
    _k_Kd=0.1
    
    S=0
    I1=0
    I2=0
    
end
"""