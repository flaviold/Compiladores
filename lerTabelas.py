from hash import *

tabelaFunc = SymbolTable("tabeladefuncoes.txt")
tabelaIden = SymbolTable("tabeladeidentificadores.txt")
teste = tabelaFunc.consultarChave("imprimir")
print(teste)
tabelaFunc.imprimirTabela()
