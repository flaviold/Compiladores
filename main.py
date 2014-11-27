from hash import *

tabelaFunc = SymbolTable("tabeladefuncoes.txt")
tabelaIden = SymbolTable("tabeladeidentificadores.txt")
compilador = Grafo("grafo.txt",tabelaIden,tabelaFunc)
