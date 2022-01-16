from callstats import CallRecorder

@CallRecorder
def sac_a_dos(ens, somme):
    if (somme == 0):
        return []
    if (somme < 0):
        return None
    if len(ens) == 0:
        return None
    res = sac_a_dos(ens[1:], somme - ens[0])
    if res is not None:
        res.append(ens[0])
        return res
    else:
        return sac_a_dos(ens[1:],somme)
    
call = sac_a_dos([2, 9, 10], 12)
print(call.trace())
