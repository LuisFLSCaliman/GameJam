import math
import random

from recorde import carregar_recorde, salvar_recorde


LARGURA, ALTURA = 960, 540
FPS = 60

CHAO_Y = 420
JOGADOR_X = LARGURA // 2
JOGADOR_Y = 380
ALTURA_DIVISAO_TIRO = CHAO_Y - 100
ALCANCE = 230
DISTANCIA_DANO = 30

VELOCIDADE_BASE = 150
VELOCIDADE_POR_MARCO = 5
PONTOS_POR_MARCO_VELOCIDADE = 10
VELOCIDADE_MAX = 420
INIMIGOS_INICIAIS_MAXIMOS = 2
INIMIGOS_POR_MARCO = 1
PONTOS_POR_MARCO_INIMIGOS = 20
INTERVALO_GERACAO_INIMIGO = 2.0
MARGEM_INIMIGO = 24
MULTIPLICADOR_RAPIDO = 2.0
DURACAO_EFEITO_TELEPORTE = 0.55
DURACAO_EXPLOSAO_ROSA = 1.0
DURACAO_GOLPE = 0.15
DURACAO_FLASH_DANO = 0.18
DURACAO_QUEDA_CABECA = 0.08
MUNICOES_POR_CARREGADOR = 8
DURACAO_PRIMEIRA_RECARGA = 1.0
INTERVALO_RECARGA_BALA = 0.4
TAMANHO_INIMIGO_CHAO = (34, 44)
TAMANHO_INIMIGO_RAPIDO = (24, 32)
TAMANHO_INIMIGO_GRANDE = (54, 70)


class Inimigo:
    def __init__(
        self,
        lado,
        tipo,
        velocidade,
        rapido=False,
        grande=False,
        pesado_voador=False,
        teleportador=False,
        rato_magico=False,
        fantasma=False,
        fantasma_explosivo=False,
        espantalho=False,
        zumbi_neon=False,
    ):
        self.lado = lado
        if rato_magico:
            self.tipo = "chao"
        elif pesado_voador or teleportador or fantasma:
            self.tipo = "ar"
        else:
            self.tipo = tipo
        self.rapido = rapido
        self.grande = grande
        self.pesado_voador = pesado_voador
        self.teleportador = teleportador
        self.rato_magico = rato_magico
        self.fantasma = fantasma
        self.fantasma_explosivo = fantasma_explosivo
        self.espantalho = espantalho
        self.zumbi_neon = zumbi_neon
        self.vida_cabeca = 1 if espantalho else 0
        self.cabeca_caida = False
        self.tempo_queda_cabeca = 0.0
        self.tempo_flash_dano = 0.0
        self.teleportou = False
        self.efeitos_teleporte = []
        self.vida_maxima = (
            2 if espantalho else 3 if fantasma else 2 if pesado_voador else 3 if grande else 1
        )
        self.vida = self.vida_maxima
        if grande or fantasma:
            self.velocidade = velocidade * 0.5
        elif pesado_voador:
            self.velocidade = velocidade * 0.75
        else:
            self.velocidade = velocidade * (
                MULTIPLICADOR_RAPIDO if rapido else 1
            )
        self.x = (
            float(MARGEM_INIMIGO)
            if lado == -1
            else float(LARGURA - MARGEM_INIMIGO)
        )
        self.t = random.uniform(0, math.tau)
        self.y = JOGADOR_Y if self.tipo == "chao" else 290

    def atualizar(self, dt):
        self.x += -self.lado * self.velocidade * dt
        if self.tipo == "ar":
            self.t += dt * 5
            amplitude = 13 if self.fantasma else 18
            self.y = 290 + math.sin(self.t) * amplitude
        elif self.rapido:
            self.t += dt * 14
        else:
            self.t += dt * 8
        if self.espantalho and self.cabeca_caida:
            self.tempo_queda_cabeca = min(
                DURACAO_QUEDA_CABECA,
                self.tempo_queda_cabeca + dt,
            )
        self.tempo_flash_dano = max(0.0, self.tempo_flash_dano - dt)
        self.efeitos_teleporte = [
            (x, y, tempo + dt)
            for x, y, tempo in self.efeitos_teleporte
            if tempo + dt < DURACAO_EFEITO_TELEPORTE
        ]
        if (
            self.teleportador
            and not self.teleportou
            and self.no_alcance()
        ):
            saida = (int(self.x), int(self.y))
            self.lado *= -1
            self.x = JOGADOR_X + self.lado * (ALCANCE + 12)
            self.teleportou = True
            chegada = (int(self.x), int(self.y))
            self.efeitos_teleporte.extend(
                ((saida[0], saida[1], 0.0), (chegada[0], chegada[1], 0.0))
            )

    def no_alcance(self):
        return abs(self.x - JOGADOR_X) <= ALCANCE

    def centro(self):
        if self.espantalho:
            if not self.cabeca_caida:
                return int(self.x), 260
            return int(self.x), CHAO_Y - 79
        if self.tipo == "chao":
            if self.grande:
                altura = TAMANHO_INIMIGO_GRANDE[1]
            elif self.rapido:
                altura = TAMANHO_INIMIGO_RAPIDO[1]
            else:
                altura = TAMANHO_INIMIGO_CHAO[1]
            return int(self.x), CHAO_Y - altura // 2
        return int(self.x), int(self.y)

    def chegou(self):
        return abs(self.x - JOGADOR_X) <= DISTANCIA_DANO

    def altura_alvo(self):
        if self.espantalho and not self.cabeca_caida:
            return "ar"
        return self.tipo


def novo_inimigo(pontos, lado=None):
    if lado is None:
        lado = random.choice((-1, 1))
    tipo = random.choice(("chao", "ar"))
    velocidade = min(
        VELOCIDADE_BASE
        + (pontos // PONTOS_POR_MARCO_VELOCIDADE) * VELOCIDADE_POR_MARCO,
        VELOCIDADE_MAX,
    )
    variante = random.choices(
        (
            "normal",
            "rapido",
            "zumbi",
            "zumbi_neon",
            "pesado_voador",
            "teleportador",
            "rato_magico",
            "fantasma",
            "fantasma_explosivo",
            "espantalho",
        ),
        weights=(0.4, 0.2, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05),
    )[0]
    teleportador = variante in ("teleportador", "rato_magico")
    rato_magico = variante == "rato_magico"
    if variante in ("zumbi", "zumbi_neon"):
        tipo = "chao"
    elif teleportador and not rato_magico:
        tipo = "ar"
    elif rato_magico:
        tipo = "chao"
    elif variante == "espantalho":
        tipo = "chao"
    return Inimigo(
        lado,
        tipo,
        velocidade,
        rapido=variante in ("rapido", "teleportador", "rato_magico"),
        grande=variante in ("zumbi", "zumbi_neon"),
        pesado_voador=variante == "pesado_voador",
        teleportador=teleportador,
        rato_magico=rato_magico,
        fantasma=variante in ("fantasma", "fantasma_explosivo"),
        fantasma_explosivo=variante == "fantasma_explosivo",
        espantalho=variante == "espantalho",
        zumbi_neon=variante == "zumbi_neon",
    )


class Jogo:
    def __init__(self):
        self.recorde = carregar_recorde()
        self.pontos = 0
        self.inimigos = [novo_inimigo(self.pontos)]
        self.tempo_geracao_inimigo = 0.0
        self.municao = MUNICOES_POR_CARREGADOR
        self.tempo_sem_tiro = 0.0
        self.primeira_bala_recarga = True
        self.golpe = None
        self.direcao_arma = (1, "ar")
        self.alvo_arma = None
        self.game_over = False
        self.novo_recorde = False
        self.explosao_rosa = 0.0
        self.explosao_verde = 0.0
        self.inimigos_dano_mortais = []

    def reiniciar(self):
        self.pontos = 0
        self.inimigos = [novo_inimigo(self.pontos)]
        self.tempo_geracao_inimigo = 0.0
        self.municao = MUNICOES_POR_CARREGADOR
        self.tempo_sem_tiro = 0.0
        self.primeira_bala_recarga = True
        self.golpe = None
        self.direcao_arma = (1, "ar")
        self.alvo_arma = None
        self.game_over = False
        self.novo_recorde = False
        self.explosao_rosa = 0.0
        self.explosao_verde = 0.0
        self.inimigos_dano_mortais = []

    def clicar(self, posicao):
        if self.game_over:
            self.reiniciar()
            return
        if self.municao == 0:
            return

        mx, my = posicao
        lado = -1 if mx < JOGADOR_X else 1
        vertical = "ar" if my < ALTURA_DIVISAO_TIRO else "chao"
        self.direcao_arma = (lado, vertical)
        candidatos = [
            inimigo
            for inimigo in self.inimigos
            if inimigo.lado == lado
            and inimigo.altura_alvo() == vertical
            and inimigo.no_alcance()
        ]
        alvo_inimigo = min(
            candidatos,
            key=lambda inimigo: abs(inimigo.x - JOGADOR_X),
            default=None,
        )
        alvo = None
        if alvo_inimigo is not None:
            alvo = alvo_inimigo.centro()
        self.alvo_arma = alvo
        acertou = alvo_inimigo is not None
        animar_tiro = (
            alvo_inimigo is not None
            and alvo_inimigo.espantalho
            and not alvo_inimigo.cabeca_caida
        )
        self.golpe = (lado, vertical, DURACAO_GOLPE, acertou, alvo, animar_tiro)
        self.municao -= 1
        self.tempo_sem_tiro = 0.0
        self.primeira_bala_recarga = True

        if alvo_inimigo is not None:
            alvo_inimigo.vida -= 1
            alvo_inimigo.tempo_flash_dano = DURACAO_FLASH_DANO
            if alvo_inimigo.espantalho and not alvo_inimigo.cabeca_caida:
                alvo_inimigo.vida_cabeca -= 1
                if alvo_inimigo.vida_cabeca == 0:
                    alvo_inimigo.cabeca_caida = True
                    alvo_inimigo.tempo_queda_cabeca = 0.0
            if alvo_inimigo.vida == 0:
                self.inimigos_dano_mortais.append(
                    (alvo_inimigo, DURACAO_FLASH_DANO)
                )
                self.inimigos.remove(alvo_inimigo)
                if alvo_inimigo.fantasma_explosivo:
                    self.explosao_rosa = DURACAO_EXPLOSAO_ROSA
                if alvo_inimigo.zumbi_neon:
                    self.explosao_verde = DURACAO_EXPLOSAO_ROSA
                self.pontos += 1
                if self.pontos > self.recorde:
                    self.recorde = self.pontos
                    salvar_recorde(self.recorde)
                    self.novo_recorde = True

    def atualizar(self, dt):
        self.explosao_rosa = max(0.0, self.explosao_rosa - dt)
        self.explosao_verde = max(0.0, self.explosao_verde - dt)
        inimigos_dano_mortais = []
        for inimigo_morto, restante in self.inimigos_dano_mortais:
            restante = max(0.0, restante - dt)
            inimigo_morto.tempo_flash_dano = restante
            if restante > 0:
                inimigos_dano_mortais.append((inimigo_morto, restante))
        self.inimigos_dano_mortais = inimigos_dano_mortais

        if not self.game_over:
            if self.municao < MUNICOES_POR_CARREGADOR:
                self.tempo_sem_tiro += dt
                intervalo_recarga = (
                    DURACAO_PRIMEIRA_RECARGA
                    if self.primeira_bala_recarga
                    else INTERVALO_RECARGA_BALA
                )
                while self.tempo_sem_tiro >= intervalo_recarga:
                    self.municao += 1
                    self.tempo_sem_tiro -= intervalo_recarga
                    self.primeira_bala_recarga = False
                    intervalo_recarga = INTERVALO_RECARGA_BALA
                    if self.municao == MUNICOES_POR_CARREGADOR:
                        self.tempo_sem_tiro = 0.0
                        break
            else:
                self.tempo_sem_tiro = 0.0
            for inimigo in self.inimigos:
                inimigo.atualizar(dt)
            if any(inimigo.chegou() for inimigo in self.inimigos):
                self.game_over = True
            elif len(self.inimigos) < self.limite_inimigos:
                self.tempo_geracao_inimigo += dt
                if self.tempo_geracao_inimigo >= INTERVALO_GERACAO_INIMIGO:
                    contagem_por_lado = {
                        lado: sum(
                            inimigo.lado == lado for inimigo in self.inimigos
                        )
                        for lado in (-1, 1)
                    }
                    menor_contagem = min(contagem_por_lado.values())
                    lados_disponiveis = [
                        lado
                        for lado, quantidade in contagem_por_lado.items()
                        if quantidade == menor_contagem
                    ]
                    self.inimigos.append(
                        novo_inimigo(
                            self.pontos,
                            lado=random.choice(lados_disponiveis),
                        )
                    )
                    self.tempo_geracao_inimigo = 0.0

        if self.golpe:
            lado, vertical, restante, acertou, alvo, animar_tiro = self.golpe
            restante -= dt
            self.golpe = (
                (lado, vertical, restante, acertou, alvo, animar_tiro)
                if restante > 0
                else None
            )

    @property
    def limite_inimigos(self):
        return (
            INIMIGOS_INICIAIS_MAXIMOS
            + self.pontos // PONTOS_POR_MARCO_INIMIGOS
            * INIMIGOS_POR_MARCO
        )
