# UFES
# Gilberto Ewald Filho, Mauricio Carvalho de Oliveira
# Compiladores - 2014/1

from hash import *
import sys, re, os

class ItemLex():
	def __init__(self, palavra, tipo):
		self.palavra = palavra
		self.tipo = tipo
		self.noLista = None

class Automato():
	def __init__(self, caminhoArq):
		self.estados = []
		a = open(caminhoArq, "Ur")
		#expReg = re.compile("[\W]+ | [\w]+")
		linha = a.readline()
		while(len(linha) > 0):
			if(linha[0] == '#'):
				#comentario... nada a fazer
				linha = a.readline()
				continue
			elif(linha == "Estados:\n"):
				linha = a.readline()
				while(len(linha) > 0 and linha[0] == '\t'):
                    #Armazenando os estados na lista de estados
					self.estados.append(Estado(linha[1:-1]))
					
					linha = a.readline()
			
			elif(linha == "Transicoes:\n"):
				linha = a.readline()
				while(len(linha) > 0 and linha[0] == '\t'):
                    #Quebrando a linha
					args = linha.split()
					#Estado anterior de ler o caracter
					estado1 = self.getEstado(args[0])
					#Estado apos ler o caracter
					estado2 = self.getEstado(args[2])
					#Listas de transicoes do estado1, primeiro elemento a expReg e o outro estado
					estado1.addTransicao(args[1], estado2)
					#Pegando o proximo
					linha = a.readline()
			linha = a.readline()
	
	def getEstado(self, nome):
		for estado in self.estados:
			if(estado.nome == nome):
				return estado
		return 0

	
	def checa(self, palavra):
		print("checando ", palavra)
		#Pegando o estado start, e a sua lista de transicoes, e cada elemento tem a exprReg e o proximo estado
		estado = self.getEstado("start")
		for carac in palavra:                        
			for trans in estado.transicoes:
				#print(trans.conjValido)
				#expReg = re.compile(trans.conjValido)
				if(re.match(trans.conjValido, carac)):
					#print(
					estado = trans.proxEstado
					#print (carac)
					#print("caractere:", carac, "; vai pro estado:", estado.nome)
					break
			else:
				#print("ERRO - caractere nao reconhecido pelo estado... abortando!\n")
				return
		print("Estado final: ", estado.nome)
		return palavra

					


		
	def analiseLexica(self,nomePrograma):
		if(not os.path.exists(nomePrograma)):
			input("Arquivo inexistente. Pressione qualquer tecla para continuar...\n")
			return 1
		listaItensLex = []
		listaItensLexDois = []
		arquivo = open(nomePrograma,"Ur")
		tabelaPalavrasReservadas = SymbolTable(47,"simbolos.txt")
		tabelaProcedimentos = SymbolTable(47,"tabelaProcedimentos.txt")
		listaLeitura=[]
		palavrasArquivo = arquivo.read()
		estado = self.getEstado("start")
		#caracter anterior quando a lista para de dar append
		anterior='0'
		anterior = palavrasArquivo[0]
		aux = 0
		count = 0
		i=0
		while (i < len(palavrasArquivo)):                            
			if(aux):
				i=i-1
				aux=0

			for trans in estado.transicoes:
				estadoAnterior = estado
				if(re.match(trans.conjValido, palavrasArquivo[i])):
					estado = trans.proxEstado
					listaLeitura.append(palavrasArquivo[i])
					carac = palavrasArquivo[i]
					if(estado.nome=="start"):
						listaLeitura=[]
					#print(carac)
					#print("caractere:", carac, "; vai pro estado:", estado.nome)
					if (estado.nome == "estadofinal"):
						listaLeitura = listaLeitura[:-1]
						if(tabelaPalavrasReservadas.consultaS(''.join(listaLeitura))):
							#print(tabelaPalavrasReservadas.consultaS(''.join(listaLeitura)) + ":",''.join(listaLeitura))
							listaItensLexDois.append(ItemLex(''.join(listaLeitura),tabelaPalavrasReservadas.consultaS(''.join(listaLeitura))))							

						else:
							if(estadoAnterior.nome == "simboloespecial" or estadoAnterior.nome == "operadorrelacional" or estadoAnterior.nome == "operadoraritmetico"):
								#print('O valor do operador eh  = '+''.join(listaLeitura));
								listaItensLexDois.append(ItemLex(''.join(listaLeitura),''.join(listaLeitura)))

								
                                                        
							elif(estadoAnterior.nome == "float" or estadoAnterior.nome == "int"):
								#print("numb "+ ":",''.join(listaLeitura))
								listaItensLexDois.append( ItemLex(''.join(listaLeitura), "numb"))

							elif(tabelaProcedimentos.consultaS(''.join(listaLeitura))):
                                                                #print("Procedimento "+ ":",''.join(listaLeitura))
                                                                #Eh um procedimento
                                                                listaItensLexDois.append(ItemLex(''.join(listaLeitura),tabelaProcedimentos.consultaS(''.join(listaLeitura))))


							#Nao eh procedimento, nem palavra reservada e nem um numero, (so pode ser apenas um identificador(de variavel))								
							else:														
								#print(estadoAnterior.nome+"**:**",''.join(listaLeitura))
								#print("*So pode ser um identificador de variavel ou literal final*\n");
								if(estadoAnterior.nome == "literalfinal"):
									listaItensLexDois.append( ItemLex(''.join(listaLeitura), "identificador"))
								#Eh um identificador		
								else:
									listaItensLexDois.append(ItemLex(''.join(listaLeitura), estadoAnterior.nome))
								#print(estadoAnterior.nome)
						listaItensLex.append( ItemLex(listaLeitura, estadoAnterior.nome) )
													
						#listaItensLexDois.append()
						listaLeitura = []
						aux=1
						#Voltando para o estado inicial
						estado = self.getEstado("start")                            
						
					break            
			else:
				print("ERRO - caractere nao reconhecido pelo estado... abortando!\n")
				return 2
			i = i+1
		return listaItensLexDois #listaItensLex
		
class Estado():
	def __init__(self, nome):
		self.nome = nome
		self.transicoes = []
	
	def addTransicao(self, conjValido, proxEstado):
		self.transicoes.append(Transicao(conjValido, proxEstado))

class Transicao():
	def __init__(self, conjValido, proxEstado):
		self.conjValido = conjValido
		self.proxEstado = proxEstado


