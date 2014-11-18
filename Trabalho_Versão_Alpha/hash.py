#Definindo a classe que representa o simbolo
class Symbol():

    def __init__(self, symbol, typ):

        self.symbol = symbol

        self.type = typ

        self.collision = 0

#Definindo a classe que representa a tabela de simbolos
class SymbolTable():

    #the self variable represents the instance of the object itself
    #The __init__ method is roughly what represents a constructor in Python.


    #Feito o inicializa
    def __init__(self, m,caminhoArq):
        #Representando o tamanho da tabela primaria
        self.m = m
        #Iniciando a lista como vazia
        self.list=[]
        #Atributo proxima colisao(entrada para a tabela de colisao = m)
        self.nextcollision = m        
            
        #Botando Zero na lista toda
        for i in range(0,m):
            #CRIEI UM OBJETO SIMBOLO ANTES, PQ NAO ESTAVA DANDO
            #PARA ACHAR UM OBJETO QUE NAO HAVIA SIDO INSERIDO NA TABELA ANTES
            symbol = Symbol(0,0)
            self.list.append(symbol)


        #Abrindo o arquivo
        arquivo = open(caminhoArq, "Ur")
        #Lendo a linha
        linha = arquivo.readline()
        while(linha):
            #Separando por espacos
            cols = linha.split()
            #Inserindo na tabelaHash
            if (len(cols)!=0):
                self.insereS(cols[0],cols[1])
            linha = arquivo.readline()

    
    def funcaoHash(self, symbol):
        intLength = len(symbol)
        
        total=0
        #Aqui faz toda a conta para calcular o valor Hash, apenas soma os caracteres
        for i in range(0, intLength):
            total = total + ord(symbol[i])

        #print (total)
        return total%self.m

    def insereS(self, symbol, typ):
        
        #Pegando o valor Hash
        index = self.funcaoHash(symbol)
        
        #print(symbol)
        #print(index)
        #print(self.list[index].symbol)
        #Inserindo
        #Primeiro caso: Se a entrada de indice r estiver vazia...
        if(self.list[index].symbol == 0):
            #Simplesmente insere o simbolo na posicao mapeada pela funcaoHash

            self.list[index] = Symbol(symbol, typ)
        #Caso 2: Se a entrada de indice r nao estiver vazia
        else:
            #Caso 2.1: O campo colisao igual a zero 
            if(self.list[index].collision == 0):
                #O campo colisao ira receber o indice de colisao na tabela de colisao
                self.list[index].collision = self.nextcollision
                self.list.append(Symbol(symbol,typ))

            #Caso 2.2: O campo colisao e diferente de zero
            else:
                #Pegando o indice para percorrer na cadeia de colisoes
                chain = index
                while(self.list[chain].collision !=0):
                    chain = self.list[chain].collision

                self.list[chain].collision = self.nextcollision
                self.list.append(Symbol(symbol,typ))
            #Incrementando o atributo proximaColisao, para que caso haja colisao o elemento seja inserido na proximaColisao correta    
            self.nextcollision +=1

    def consultaS(self,symbol):
        index = self.funcaoHash(symbol)
        result = self.list[index]
        if(result.symbol==0):
            return 0
        #O campo colisao igual a zero
        if(result.collision==0 and (result.symbol==symbol)):
            return result.type
        
        #Iremos percorrer ate achar o simbolo
        else:
            while(result.collision != 0):
                if(result.symbol == symbol):
                    return result.type
                result = self.list[result.collision]
            if(result.symbol == symbol):
                return result.type
            else:
                return 0

