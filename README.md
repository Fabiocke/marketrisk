#Exemplo de calculo do Value at Risk paramétrico de um portfolio de uma carteira composta por:

#Ativos: PETR4, VALE3 e B3SA3

#Tempo: de 01/01/2020 até 01/01/2021

#Para buscar os preços e gerar os retornos:


import marketrisk as mr

portfolio = mr.Stocks(['PETR4', 'MOVI3', 'IBOV'], start='2020-01-01', end='2021-02-20')

retornos = portfolio.get_returns()


#Para calcular o risco:

#O modulo risco recebe os retornos e pode receber os respectivos volumes

risco = mr.Risk(retornos, [1000, 1500, 800])


#Calculo do var paramétrico para 1 dia e 99% de confiança:

var = risco.var(0.99, days=1)


#Calculo do var paramétrico EWMA para 1 dia e 99% de confiança:

var_ewma = risco.var(0.99, days=1, ewma=1)



