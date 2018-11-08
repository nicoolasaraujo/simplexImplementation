'''
# Simplex
##Execução
```
python3 simplex.py tst.txt
```
## O arquivo passado(tst.txt) como argumento deve possuir a seguinte formatação:
1. Na primeira linha deve-se inserir a quantidade de variáveis de decisão seguida pela quantidade de restrições 
2. Nas linhas que se seguem serão inseridas em ordem todas as restrições, incluindo a Z
**Obs.: Os valores devem ser separados por vírgula**

```
2,2
1,-2,-3,0,0,0
0,2,1,1,0,4
0,1,2,0,1,5 
```

**No exemplo acima foram utilizadas duas restrições e duas variáveis de decisão gerando o ótimo de z=8** 
'''

import os
import sys

class Simplex:
  def __init__(self,restricoes):
    self.matriz = self.criaTableau(restricoes) # matriz com os dados do simplex
    self.ultimaColuna = len(self.matriz[1]) - 1 # idice para facilitar acesso a última coluna do simplex
    
    
  def criaTableau(self,restricoes):
    linhaCab = ['', 'z'] # linha de cabeçalho que identificará quais a variáveis utilizadas
    tableau = []
    primeiraLinha = restricoes.readline()
    primeiraLinha = primeiraLinha.split(',')
    self.qtdVariaveis = int(primeiraLinha[0]) # quantidade de variáveis de decisão
    self.qtdRestricoes = int(primeiraLinha[1]) # quantidade de restrições

    for i in range(1,self.qtdVariaveis+1):
      linhaCab +=  ['x{}'.format(i)]

    for i in range(1,self.qtdRestricoes+1):
      linhaCab += ['s{}'.format(i)]
    linhaCab += ['sol']

    for i in range(0, self.qtdRestricoes+1):
      tempLinha = restricoes.readline()
      tempLinha = tempLinha.replace('\n','')
      if i == 0: #cria a linha z 
         tempZ = list(map(lambda x: int(x), tempLinha.split(',')))
         tempZ = list(map(lambda x: int(x), tempLinha.split(',')))
         self.funcObjetivo = [] # Lista com as restrições de z
         for idx, data in enumerate(tempZ[1:1+self.qtdVariaveis]):
           self.funcObjetivo.append('x' + str(idx+1) +' = '+ str(data*(-1)))
         tableau.append(['z']+ tempZ)
      else: #cria as demais linhas
        tableau.append(['s{}'.format(i)]+ list(map(lambda x: int(x), tempLinha.split(','))))

    tableau.insert(0,linhaCab)
    return tableau
  
  def encontrouOtimo(self):
    '''
      Verifica se encontrou o ótimo

      @return: True - Não existe nenhum valor menor que 0 nas restrições ; False - Existem valor zerados
   '''
    for id, aux in enumerate(self.matriz[1][1:-2]):
      if aux < 0:
        return False
    return True

  def escolheColuna(self, linha= 1):
    '''
      Escolhe a coluna pivô

      @return: Indice da coluna pivô
    '''
    menor = self.matriz[linha][1]
    indice = 1
    for i in range(1,self.ultimaColuna):
      if menor > self.matriz[linha][i]:
        menor = self.matriz[linha][i]
        indice = i
    return indice
  
  def escolheLinha(self, colunaPivo):
    '''
      Escolhe a linha pivô buscando o menor valor positivo entre as divisões da solução de cada linha pelo elemento posicionado a posição pivô

      @param colunaPivo: Indice da coluna pivô
      
      @return: Indice da linha pivô
    '''
    menor = self.matriz[2][self.ultimaColuna]/self.matriz[2][colunaPivo]     
    indice = 2
    for linha in range(2, len(self.matriz)):
      temp = self.matriz[linha][self.ultimaColuna]/self.matriz[linha][colunaPivo]
      if temp >=0 and temp < menor:
        menor = temp
        indice = linha
    return indice

  def atualizaLinhaPivo(self, linha, coluna):
    '''
      Atualiza a linha pivô dividindo-a pelo elemento pivo dado pelos indicies passados como parâmetro

      @param linha: Indice linha pivô

      @param coluna: Indice coluna pivô
    '''
    print('---------------------------Método - atualizaLinhaPivo---------------------------')
    elementoPivo = self.matriz[linha][coluna]
    print('Elemento Pivo = {}'.format(elementoPivo))
    for idx_coluna in range(1,self.ultimaColuna+1):
      self.matriz[linha][idx_coluna] = self.matriz[linha][idx_coluna]/elementoPivo
    self.matriz[linha][0] = self.matriz[0][coluna]
    self.novaLinhaPivo = self.matriz[linha][1:]
    print('Nova linha pivo = ', end="")
    print(self.novaLinhaPivo)
    self.printaMatriz()

  def atualizaTableau(self, linhaP, colunaP):
    '''
      Atualiza o simplex, percorre todas as linhas(exceto a pivô) multiplicando a linha pivô pelo oposto do elemento na coluna pivô de cada linha e depois soma a linha pivô com cada linha
    '''
    print('---------------------------Método - atualizaTableau---------------------------')
    for linha in range(1, len(self.matriz)):
      if not linhaP == linha:
        print('Linha = {}'.format(self.matriz[linha][0]))
        tempElemPivo = self.matriz[linha][colunaP] * (-1)  
        print('Elemento Pivo_temp = {}'.format(tempElemPivo))
        tempLp = list(map(lambda x: x * tempElemPivo,self.novaLinhaPivo))
        print('Nova linha pivo_temp = ', end="")
        print(tempLp)
        print('Vai somar com - ', end="")
        print(self.matriz[linha][1:])
        self.matriz[linha][1:] = list(map(lambda x,y: x+y,tempLp, self.matriz[linha][1:]))
        print('\n')

  def printaMatriz(self):
    '''
      Apresenta os valores do simplex
    '''
    for id, linha in enumerate(self.matriz):
      print(linha)
  
  def apresentaSolucao(self):
    '''
      Apresenta a solução do simplex
    '''
    print('\n--------------------------Resultado--------------------------\n')
    self.printaMatriz()
    print('\nFunção objetivo - {}'.format(self.funcObjetivo))
    print('z = {}'.format(self.matriz[1][-1]))
    for i in range(1, self.qtdVariaveis+1): #percorre a quantidade de variáveis passadas como argumento buscando pelos valor de xn
      variavel = 'x' + str(i)
      encontrouVariavel = False
      for linha in range(2, len(self.matriz)):
        if variavel == self.matriz[linha][0]:
          encontrouVariavel = True
          print('{} = {}'.format(variavel, self.matriz[linha][self.ultimaColuna])) # apresenta o valor da solução caso tenha encontrado a variável
          break
      if (not encontrouVariavel):
          print('{} = 0'.format(variavel)) # se não encontrou a variável possui valor 0


def main():
  NOME_ARQUIVO = sys.argv[1]
  with open(NOME_ARQUIVO, 'r') as restricoes:
    simplex = Simplex(restricoes)
    while(not simplex.encontrouOtimo()):
      cp = simplex.escolheColuna() #Acha a coluna pivô
      lp = simplex.escolheLinha(cp) #Acha a linha pivô
      simplex.atualizaLinhaPivo(lp,cp) # Atualiza a linha pivô
      simplex.atualizaTableau(lp, cp) # Atualiza o tableau
    simplex.apresentaSolucao() # Apresenta a solução do simplex

if __name__ == '__main__':
  main()