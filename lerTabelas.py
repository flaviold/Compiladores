from hash import *

tabelaFunc = SymbolTable(2,"tabeladefuncoes.txt")
tabelaIden = SymbolTable(4,"tabeladeidentificadores.txt")
teste = tabelaFunc.consultaS("leia")
print(teste)
