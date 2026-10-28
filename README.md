# Caçador da Noite

Jogo de ação feito em **Python + pygame** para a GameJam de 2026 da UFF de Rio das Ostras que tinha como tema um único input: nesse caso o **clique do mouse**.
Um caçador armado fica parado no centro da tela enquanto inimigos terrestres e voadores avançam pela esquerda e pela direita. Quem decide o tiro é a **posição do clique**: o quadrante em que você clica define para onde o caçador atira.

A arma tem **alcance curto**: não dá para eliminar os inimigos de longe. É preciso esperar que eles se aproximem e acertar o tiro certo antes que cheguem até você.

## Como funciona

A tela é dividida em quatro quadrantes a partir do personagem:

```
              |
   ar         |         ar
 (esquerda)   |      (direita)
--------------+--------------   <- altura do personagem
   chão       |         chão
 (esquerda)   |      (direita)
              |
```

| Clique em...              | O caçador atira em...              |
|---------------------------|------------------------------------|
| Esquerda, acima da linha  | Inimigo **voador** à esquerda      |
| Esquerda, abaixo da linha | Inimigo **terrestre** à esquerda   |
| Direita, acima da linha   | Inimigo **voador** à direita       |
| Direita, abaixo da linha  | Inimigo **terrestre** à direita    |

O tiro só elimina o inimigo se:

1. o lado do clique for o mesmo lado do inimigo;
2. o tipo do clique (ar ou chão) corresponder ao tipo do inimigo;
3. o inimigo estiver **dentro do alcance** da arma.

O alcance é mostrado por ** um portão de cemitério **. Clicar errado gasta munição, e será necessário parar de atirar por um tempo para recarregar.

## Regras

- Cada inimigo eliminado vale **1 ponto**.
- Se um inimigo alcançar o personagem, é **game over**.
- A velocidade dos inimigos e a quantidade de inimigos simultanea aumenta de acordo com a pontuação, até um limite máximo.
- O **recorde** (maior pontuação) é salvo automaticamente e persiste entre execuções.

## Requisitos

- Python 3.8 ou superior
- [pygame](https://www.pygame.org/)

```bash
pip install pygame
```

## Como executar

```bash
python main.py
```

## Controles

| Ação                  | Input                    |
|-----------------------|--------------------------|
| Atirar                | Botão esquerdo do mouse  |
| Sair                  | `Esc` ou fechar a janela |

## Informações
- Todos as sprites foram feitas usando IA
- Os assets de som são de uma biblioteca de assets gratuíta

## Ideias futuras

- Sprites e animações para o caçador e os inimigos feitas a mão
- Novos tipos de inimigo (resistentes, rápidos, com padrão de movimento próprio)
- Novos mapas com inimigos diferentes
- Combos e multiplicador de pontuação
