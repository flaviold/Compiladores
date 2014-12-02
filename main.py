from hash import *
from navegaGrafo import *

tabelaFunc = SymbolTable("tabeladefuncoes.txt")
tabelaIden = SymbolTable("tabeladeidentificadores.txt")
compilador = Grafo("grafo.txt",tabelaIden,tabelaFunc)
programa, compilar = compilador.lexico("teste.txt")

result = compilador.verificaPrograma(compilar)

print(result)