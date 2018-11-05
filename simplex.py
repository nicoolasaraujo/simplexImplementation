import os

class Simplex:
  def __init__(self,restricoes=[]):
    super()
    self.matriz = self.criaTableau()
    self.penultimaColuna = len(self.matriz[1]) - 1
    os.execvpe

  def criaTableau(self):
    cabSimplex = ['', 'z']
    tableau = []
    qtdDecisao = int(input('Quantidade da variáveis de decisão: '))
    qtdRestricoes = int(input ('Quantidade restrições: '))
    for i in range(1,qtdDecisao+1):
      cabSimplex.append('x{}'.format(i))
    for i in range(1, qtdRestricoes+1):
      cabSimplex.append('s{}'.format(i))
    cabSimplex.append('sol')
    tableau.append(cabSimplex)

    for i in range(0,qtdRestricoes+1):
      nomeLinha = 'z' if i == 0 else 's'+str(i)
      restricoes = input('Digite os valores da linha {} separados por ; : '.format(nomeLinha)).strip()
      linha_temp = [nomeLinha]
      linha_temp = linha_temp + list(map(lambda x: int(x), restricoes.split(';') ))
      tableau.append(linha_temp)
    
    return tableau

  
  def encontrouOtimo(self):
    '''
      Verifica se encontrou o ótimo

      @return: True - Não existe nenhum valor menor que 0 nas restrições ; False - Existem valor zerados
   '''
    for id, aux in enumerate(self.matriz[1][1:-2]):
      print(aux)
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
    for i in range(1,self.penultimaColuna):
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
    menor = self.matriz[2][self.penultimaColuna]/self.matriz[2][colunaPivo]     
    indice = 2
    for linha in range(2, len(self.matriz)):
      temp = self.matriz[linha][self.penultimaColuna]/self.matriz[linha][colunaPivo]
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
    print('Elemento Pivo - {}'.format(elementoPivo))
    for idx_coluna in range(1,self.penultimaColuna+1):
      self.matriz[linha][idx_coluna] = self.matriz[linha][idx_coluna]/elementoPivo
    self.matriz[linha][0] = self.matriz[0][coluna]
    self.novaLinhaPivo = self.matriz[linha][1:]
    print('Nova linha pivo - ', end="")
    print(self.novaLinhaPivo)
    self.printaMatriz()
    input('Pressiona enter para continuar')

  def atualizaTableau(self, linhaP, colunaP):
    '''
      Atualiza o simples, percorre todas as linhas(exceto a pivô) multiplicando a linha pivô pelo oposto do elemento na coluna pivô de cada linha e depois soma a linha pivô com cada linha
    '''
    print('---------------------------Método - atualizaTableau---------------------------')
    for linha in range(1, len(self.matriz)):
      if not linhaP == linha:
        print('Linha - {}'.format(self.matriz[linha][0]))
        tempElemPivo = self.matriz[linha][colunaP] * (-1)  
        print('Elemento Pivo_temp - {}'.format(tempElemPivo))
        tempLp = list(map(lambda x: x * tempElemPivo,self.novaLinhaPivo))
        print('Nova linha pivo_temp - ', end="")
        print(tempLp)
        print('Vai somar com - ', end="")
        print(self.matriz[linha][1:])
        self.matriz[linha][1:] = list(map(lambda x,y: x+y,tempLp, self.matriz[linha][1:]))
        self.printaMatriz()
        # print(self.matriz[linha])
        input('Pressiona enter para continuar')

  def printaMatriz(self):
    '''
      Apresenta os valore do simplex
    '''
    for linha in enumerate(self.matriz):
      print(linha)

  

def main():
  simplex = Simplex()
  simplex.printaMatriz()
  while(not simplex.encontrouOtimo()):
    cp = simplex.escolheColuna()#Acha a coluna pivô
    lp = simplex.escolheLinha(cp)#Acha a linha pivô
    simplex.atualizaLinhaPivo(lp,cp)
    simplex.atualizaTableau(lp, cp)
    simplex.printaMatriz()
  print(simplex.matriz[1][-1])
  
    

if __name__ == '__main__':
  main()