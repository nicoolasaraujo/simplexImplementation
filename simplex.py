class Simplex:
  def __init__(self,restricoes=[]):
    self.matriz = self.criaTableau()
    self.penultimaColuna = len(self.matriz[1]) - 1

  def criaTableau(self):
    return [ ['','z', 'x1', 'x2', 's1', 's2', 'sol'],
        ['z',  1, -2,  -3,  0, 0, 0],
        ['s1', 0,  2,   1 , 1, 0, 4],
        ['s2', 0,  1,   2 , 0, 1, 5]  
      ]
  def encontrouOtimo(self):
    aux = list(filter(lambda x: x<0, self.matriz[1][1:self.penultimaColuna]))
    return aux == 0

  def escolheColuna(self, linha= 1):
    menor = self.matriz[linha][1]
    indice = 1
    for i in range(1,self.penultimaColuna):
      if menor > self.matriz[linha][i]:
        menor = self.matriz[linha][i]
        indice = i
    # print(self.matriz[linha][indice])
    return indice
  
  def escolheLinha(self, colunaPivo):
    menor = self.matriz[2][self.penultimaColuna]/self.matriz[2][colunaPivo]     
    indice = 2
    for linha in range(2, len(self.matriz)):
      try:
        temp = self.matriz[linha][self.penultimaColuna]/self.matriz[linha][colunaPivo]
        if temp >=0 and temp < menor:
          menor = temp
          indice = linha
      except ZeroDivisionError as ex:
        pass
      
    return indice

  def atualizaLinhaPivo(self, linha, coluna):
    elementoPivo = self.matriz[linha][coluna]
    for idx_coluna in range(1,self.penultimaColuna+1):
      self.matriz[linha][idx_coluna] = self.matriz[linha][idx_coluna]/elementoPivo
    self.matriz[linha][0] = self.matriz[0][coluna]
    self.novaLinhaPivo = self.matriz[linha][1:]

  def atualizaTableau(self, linhaP, colunaP):
    for linha in range(1, len(self.matriz)):
      if not linhaP == linha:
        print(self.matriz[linha][0])
        tempElemPivo = self.matriz[linha][colunaP] * (-1)  
        tempLp = list(map(lambda x: x * tempElemPivo,self.novaLinhaPivo))
        self.matriz[linha][1:] = list(map(lambda x,y: x+y,tempLp, self.matriz[linha][1:]))
        # print(self.matriz[linha])

  def printaMatriz(self):
    for linha in range(0,len(self.matriz)):
      print(linha)

def main():
  simplex = Simplex()
  # while(not simplex.encontrouOtimo()):
  cp = simplex.escolheColuna()#Acha a coluna pivô
  lp = simplex.escolheLinha(cp)#Acha a linha pivô
  simplex.atualizaLinhaPivo(lp,cp)
  simplex.atualizaTableau(lp, cp)
  print(simplex.matriz)
if __name__ == '__main__':
  main()