import numpy as np

def doublebar(i,j,k,l, Vee):
    return Vee[i,j,k,l] - Vee[i,j,l,k]


def Dir2Mul(p,q,r,s, Vee):
    #Dirac to Mulliken notation
    return Vee[p,r,q,s]
    

def MP2(occ, F, C, VeeMO):
    #Get MO orbital energies
    CT = np.transpose(C)
    eps = np.dot(np.dot(CT, F),C)

    #Calc EMP2
    EMP2 = 0
    for i in range(0, occ):
        for a in range(occ, len(F)):
            for j in range(0, occ):
                for b in range(occ, len(F)):
                    EMP2 += VeeMO[i,a,j,b]*(2*VeeMO[i,a,j,b]-VeeMO[i,b,j,a])/(eps[i, i] + eps[j, j] -eps[a, a] -eps[b, b])

    return EMP2


def MP3(occ, F, C, VeeMOspin):
    # Make the spin MO fock matrix
    Fspin = np.zeros((len(F)*2,len(F)*2))
    Cspin = np.zeros((len(F)*2,len(F)*2))
    for p in range(1,len(F)*2+1):
        for q in range(1,len(F)*2+1):
            Fspin[p-1,q-1] = F[(p+1)//2-1,(q+1)//2-1] * (p%2 == q%2)
            Cspin[p-1,q-1] = C[(p+1)//2-1,(q+1)//2-1] * (p%2 == q%2)
    FMOspin = np.dot(np.transpose(Cspin),np.dot(Fspin,Cspin))

    #Calc EMP3
    Epart1 = 0
    for a in range(0, occ):
        for b in range(0, occ):
            for c in range(0, occ):
                for d in range(0, occ):
                    for r in range(occ, len(Fspin)):
                        for s in range(occ,len(Fspin)):
                            Epart1 += (doublebar(a,b,r,s,VeeMOspin)*doublebar(c,d,a,b,VeeMOspin)*doublebar(r,s,c,d,VeeMOspin))/((FMOspin[a,a]+FMOspin[b,b]-FMOspin[r,r]-FMOspin[s,s])*(FMOspin[c,c]+FMOspin[d,d]-FMOspin[r,r]-FMOspin[s,s]))
    
    Epart2 = 0
    for a in range(0, occ):
        for b in range(0, occ):
            for r in range(occ, len(Fspin)):
                for s in range(occ, len(Fspin)):
                    for t in range(occ, len(Fspin)):
                        for u in range(occ, len(Fspin)):
                            Epart2 += (doublebar(a,b,r,s,VeeMOspin)*doublebar(r,s,t,u,VeeMOspin)*doublebar(t,u,a,b,VeeMOspin))/((FMOspin[a,a]+FMOspin[b,b]-FMOspin[r,r]-FMOspin[s,s])*(FMOspin[a,a]+FMOspin[b,b]-FMOspin[t,t]-FMOspin[u,u]))
    
    Epart3 = 0
    for a in range(0, occ):
        for b in range(0, occ):
            for c in range(0, occ):
                for r in range(occ, len(Fspin)):
                    for s in range(occ, len(Fspin)):
                        for t in range(occ, len(Fspin)):
                            Epart3 += (doublebar(a,b,r,s,VeeMOspin)*doublebar(c,s,t,b,VeeMOspin)*doublebar(r,t,a,c,VeeMOspin))/((FMOspin[a,a]+FMOspin[b,b]-FMOspin[r,r]-FMOspin[s,s])*(FMOspin[a,a]+FMOspin[c,c]-FMOspin[r,r]-FMOspin[t,t]))
    EMP3 = 0.125*Epart1+0.125*Epart2+Epart3
    
    return EMP3
    
    
def DCPT2(occ, F, C, VeeMO):
    #Get MO orbital energies
    CT = np.transpose(C)
    eps = np.dot(np.dot(CT, F),C)
    
    #Calc DCPT2 energy
    Epart1 = 0
    Epart2 = 0
    occ = int(input[0][0]/2)
    for i in range(0, occ):
        for j in range(0, occ):
            for a in range(occ, len(F)):
                for b in range(occ, len(F)):
                    Dabij = eps[a,a] + eps[b,b] - eps[i,i] - eps[j,j]
                    Epart1 += Dabij - (Dabij**2+4*Dir2Mul(i,j,a,b,VeeMO)**2)**0.5
                    Epart2 += Dabij - (Dabij**2+4*(Dir2Mul(i,j,a,b,VeeMO)-Dir2Mul(i,j,b,a,VeeMO))**2)**0.5
    
    EDCPT2 = 0.5*Epart1 + 0.25*Epart2
    
    return EDCPT2
