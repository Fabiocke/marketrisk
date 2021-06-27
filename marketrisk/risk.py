
import numpy as np

def normal_cdf(x, mu=0,sigma=1):
    import math
    return (1 + math.erf((x - mu) / math.sqrt(2) / sigma)) / 2

def inverse_normal_cdf(p, mu=0, sigma=1, tolerance=0.00001):
    """encontra o inverso mais próximo usando a busca binária"""
    # se não for padrão, computa o padrão e redimensiona
    if mu != 0 or sigma != 1:
        return mu + sigma * inverse_normal_cdf(p, tolerance=tolerance)
    low_z, low_p = -10.0, 0 # normal_cdf(-10) está (muito perto de) 0
    hi_z, hi_p = 10.0, 1 # normal_cdf(10) está (muito perto de) 1
    while hi_z - low_z > tolerance:
        mid_z = (low_z + hi_z) / 2 # considera o ponto do meio e o valor da
        mid_p = normal_cdf(mid_z) # função de distribuição cumulativa lá
        if mid_p < p:
        # o ponto do meio ainda está baixo, procura acima
            low_z, low_p = mid_z, mid_p
        elif mid_p > p:
        # o ponto do meio ainda está alto, procura abaixo
            hi_z, hi_p = mid_z, mid_p
        else:
            break
    return mid_z


class Risk:
    def __init__(self, series, notionals=[]):
        self.series=series
        self.notionals=notionals
        
    # adiciona os volumes para cada serie
    def set_notionals(self, notionals):
        self.notionals=notionals
        
    def correl(self):
        # Gera a matriz de correlação, se alguma série for maior que a outra, considera só os últmos registros da maior
        m=[[np.corrcoef(i[-min(len(i), len(j)):], j[-min(len(i), len(j)):])[0][1] for j in self.series] for i in self.series]
        return m
        
    def ponder(self):
        # Gera a lista de pesos respectivos para cada série
        total = sum(self.notionals)
        if total:
            return [v/total for v in self.notionals]
        
    # Gera o desvio padrão de cada serie
    def std(self, ddof=0, ewma=0):
        if not ewma:
            return [np.std(i, ddof=ddof) for i in self.series]
        else:
            # std ewma
            lam=0.94
            return [sum([i**2*(1-lam)*lam**n for i, n in zip(r, [*reversed(range(len(r)))])])**0.5 for r in self.series]

    
    # Gera a volatilidade da carteira (aa = 1 se for ao ano)
    def vol(self, aa=0, ewma=0):
        m = self.correl()
        p = self.ponder()
        s = self.std(ewma=ewma)
        # matriz de ativos
        l = [sorted([n1,n2]) for n1, _ in enumerate(self.series) for n2,_ in enumerate(self.series) if n1!=n2]
        l = list(map(list, set(map(frozenset, l))))
        
        vol = sum([2*s[n1]*s[n2]*p[n1]*p[n2]*m[n1][n2] for n1, n2 in l]+[po**2*o**2 for po, o in zip(p, s)])**(1/2)
        return vol if not aa else vol*(252**0.5)  
    
    # calcula o value at risk para determinado nível de confiança em determinada quantidade de dias
    def var(self, nc, days=1, ewma=0):
        return self.vol(ewma=ewma)*inverse_normal_cdf(nc)*sum(self.notionals)*(days**0.5)     
    
    
        
        