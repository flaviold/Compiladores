#!/usr/bin/python
# -*- coding: utf-8 -*-
from unicodedata import normalize

C = 47
N = 47	

class Bloco:
	def __init__(self):
		self.simbolo = None
		self.colisao = 0


class SymbolTable():

        def __init__(self,caminhoArq):
                self.list=[]      
            
                for i in range(0,C):
                        bloco = Bloco()
                        self.list.append(bloco)

                arquivo = open(caminhoArq, "Ur")
                texto = arquivo.read()
                for linha in texto.split("\n"):
                        self.inserirChave(linha)

		
        def hashT(self,st):
                total = 0
                for i in st:
                        total += ord(i)
                return total%N

        def inicializarBlocos(self):
                self.list = []
                for i in range(C+N):
                        self.list.append(Bloco())
                return self.list

        def inserirChave(self, chave):
                indice = self.hashT(chave)
                if(self.list[indice].simbolo == None):
                        self.list[indice].simbolo = chave
                        self.list[indice].colisao = 0
                        return self.list
                else:
                        if(self.list[indice].colisao == 0):
                                for i in range(N, N+C):
                                        if(self.list[i].simbolo == None):
                                                self.list[i].simbolo = chave
                                                self.list[indice].colisao = i
                                                return self.list
                        else:
                                indiceAux = self.list[indice].colisao
                                anterior = indiceAux
                                cont = 0
                                while((self.list[indiceAux].colisao != 0)and(cont < N+C)):
                                        anterior = indiceAux
                                        indiceAux = self.list[indiceAux].colisao
                                        cont += 1
                                if(self.list[indice].colisao == 0):
                                        for i in range(indiceAux, N+C):
                                                if(self.list[i].simbolo == None):
                                                        self.list[indice].simbolo = chave
                                                        self.list[indice].colisao = 0
                                                        return self.list
                return None

        def consultarChave(self, chave):
                indice = self.hashT(chave)
                if(self.list[indice].simbolo == None):
                        return "Não achou!"
                else:
                        while((self.list[indice].simbolo != chave)and(self.list[indice].colisao != 0)):
                                indice = self.list[indice].colisao
                        if(self.list[indice].simbolo == chave):
                                return self.list[indice].simbolo
                        else:
                                return "Não achou!"


        def imprimirTabela(self):
                for i in range(C+N):
                        if(self.list[i].simbolo != None):
                                print(str(i)+"--->"+self.list[i].simbolo)
                        else:
                                print(str(i)+"--->None")
