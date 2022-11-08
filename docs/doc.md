# Relatório
Autor: João Victor Zucco Marmentini

## Introdução

Esse relatório tem o objetivo de descrever as funcionalidades do projeto desenvolvido para o trabalho 2 de ccomputação gráfica.

## Vídeo

O vídeo a seguir demonstra o funcionamento do trabalho.

https://youtu.be/df2iRpKvtq4

## Inicialização

Todos os personagens são inicializados na função `init()` assim como as curvas e os vizinhos

O jogo inicia pausado e o usuário precisa pressionar a tecla `p` para resumir.

Para iniciar o jogo, execute no terminal:

```bash
python main.py
```

A documentação completa está disponível no repositório no [GitHub](https://github.com/jvzmarmentini/curved-labyrinth).

### Debug

Para iniar o jogo no modo de *debug*, execute no terminal:

```bash
python main.py --debug
```

## Curvas

Existem 40 curvas paramétricas do tipo Bèzier no labirinto, descritas no arquivo `assets/curve/curves.txt`, construídas a partir dos pontos no arquivo `assets/curve/points.txt`. 

A função Lerp que gera cada ponto na curva se da por:

```python
controlPointA = self.vertices[0] * (1-t) + self.vertices[1] * t
controlPointB = self.vertices[1] * (1-t) + self.vertices[2] * t
return controlPointA * (1-t) + controlPointB * t
```

Cada curva possui duas listas de vizinhos, onde estão armazenado as referências para os vizinhos do começo da curva e os vizinhos do fim da curva.

### Tamanho

O tamanho de uma curva Bèzier pode ser aproximado pelo tamanho das retas que compõem a curva. Em nosso caso, como precisamos gerar N retas para desenhar a curva, é necessário apenas calcular o somatório da distância das N retas.

## Personagens

Tanto os jogadores quanto os inimigos compartilham da mesmo classe `Character`, que define todos atributos relacionados ao desenho dos modelos, movimento e curva. 

### Jogador

O modelo do jogador pode ser encontrado em `assets/models/player.txt`. O jogador sempre começa na curva 0 com direção 0 e sua velocidade é uniforme. O jogador possui a habilidade de poder pausar o movimento e inverter sua direção, assim como trocar de curva a partir da metade (t == 0.5)

Para inverter a direção do jogador, pressione a tecla `b`. Para pausar o movimento, pressione a tecla `space`. 

Para trocar a próxima curva, pressione uma das setas (esquerda ou direita).

### Inimigos

O modelo dos inimigos pode ser encontrado em `assets/models/enemy.txt`. Diferente do jogador, os inimigos são inicializados em curvas aleatórias, porém diferente da que o jogador começa, com direção aleatória. Sua velocidade também é escolhida aleatóriamente dentre um intervalo definido préviamente e sempre vai ser menor ou igual a do jogador.

Os inimigos são armazenados em uma lista e atualizados genericamente

### Rotação

Todos personagens acompanham a rotação da curva, como pode ser melhor visualizado no vídeo. Para calcular o ângulo, é necessário seguir os seguintes passos:

+ Calcular a derivada do ponto t em uma curva

```python
der = (p1 - p0) * 2 * (1-t) + (p2 - p1) * 2 * t
```

+ Normalizar a derivada

```python
d = sqrt(der.x ** 2 + der.y ** 2)
norm = Point(der.x / d, der.y / d)
```

+ Calcular o cosseno inverso da componente Y da derivada normalizada
  
```python
np.arccos(norm.y)
```

+ Transformar o ângulo de radianos para graus e inverter conforme a direção

```python
np.rad2deg(angle) + 180 * direction
```

+ Caso a componente da normalização em X seja negativa

```python
if norm.x <= 0:
    angle = 360 - angle
```

## Sobre as trocas de curva

Quando um personagem chega a metade da curva, uma curva vizinha aleatória é escolhida para ser a próxima. Para o jogador, essa curva é destacada com uma cor e espessura diferentes. O jogador também pode trocar a próxima curva, navegando ciclicamente pelas setas pra esqueda e direita.

## Sobre as transformações geométricas

As transformações podem ser realizadas tanto com OpenGL quando pelas funções implementadas pela classe Polygon. Contudo, ao que se refere a Bounding Box, é necessário utilizar as funções da classe Polygon, pois com o OpenGL não é possível receber as vértices transformadas antes do Push, portanto inviabilizando detecção de colisão.

```python
def display(self):
    self.model.rotate(self.angle)
    self.model.translate(self.vector)
    self.model.updateBBox()
    self.model.draw()
    if settings._debugger:
        self.model.bbox.draw()
    self.model.translate(Point() - self.vector)
    self.model.rotate(-self.angle)
```

## Sobre a velocidade

A velocidade dos personagens é calculada da seguinte maneira:

```python
delta = self.velocity * time / self.trail.length
```

Onde `self.velocity` é definido na definição do personagem, `self.trail.length` é o tamanho da curva, calculado a partir da distância de cada reta da curva (ver secção Curva para mais detalhes), e `time` é a diferença de tempo entre o frame atual e o último frame:

```python
et = glutGet(GLUT_ELAPSED_TIME) * .001
et - diffEt
```