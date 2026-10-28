import math

import pygame
import pygame.gfxdraw

from mecanicas import (
    ALCANCE,
    ALTURA,
    CHAO_Y,
    DURACAO_EFEITO_TELEPORTE,
    DURACAO_EXPLOSAO_ROSA,
    DURACAO_FLASH_DANO,
    DURACAO_GOLPE,
    DURACAO_QUEDA_CABECA,
    JOGADOR_X,
    JOGADOR_Y,
    LARGURA,
    MARGEM_INIMIGO,
    MUNICOES_POR_CARREGADOR,
    TAMANHO_INIMIGO_CHAO,
    TAMANHO_INIMIGO_GRANDE,
    TAMANHO_INIMIGO_RAPIDO,
    Inimigo,
)


COR_FUNDO = (42, 24, 66)
COR_CHAO = (0, 0, 0)
COR_JOGADOR = (90, 200, 255)
COR_ALCANCE = (255, 220, 90)
COR_TEXTO = (235, 235, 245)
COR_INIMIGO_CHAO = (230, 90, 90)
COR_INIMIGO_AR = (190, 110, 240)
COR_VARIANTE_CHAO = (65, 155, 255)
COR_VARIANTE_AR = (255, 220, 70)
COR_INIMIGO_GRANDE = (190, 160, 110)
COR_PESADO_VOADOR = (255, 145, 75)
COR_SILHUETA_CEMITERIO = (9, 7, 15)
COR_METAL_CERCA = (76, 79, 94)
COR_METAL_DETALHE = (116, 120, 137)
COR_MANA_MORCEGO = (64, 158, 255)
MENU_JOGAR_RECT = pygame.Rect(350, 235, 260, 56)
MENU_CONFIGURACOES_RECT = pygame.Rect(350, 307, 260, 56)
MENU_TUTORIAL_RECT = pygame.Rect(350, 379, 260, 56)
MENU_VOLTAR_RECT = pygame.Rect(24, 22, 104, 44)
GAME_OVER_MENU_RECT = pygame.Rect(350, 330, 260, 54)
GAME_OVER_RETRY_RECT = pygame.Rect(350, 399, 260, 54)
VOLUME_MUSICA_RECT = pygame.Rect(300, 228, 360, 40)
VOLUME_EFEITOS_RECT = pygame.Rect(300, 318, 360, 40)


def _desenhar_sobreposicao(tela):
    sobreposicao = pygame.Surface((LARGURA, ALTURA), pygame.SRCALPHA)
    sobreposicao.fill((8, 6, 14, 190))
    tela.blit(sobreposicao, (0, 0))


def _desenhar_botao(tela, fonte, retangulo, texto, mouse_pos):
    cor = (81, 65, 92) if retangulo.collidepoint(mouse_pos) else (43, 37, 55)
    pygame.draw.rect(tela, (119, 105, 132), retangulo.inflate(4, 4), border_radius=8)
    pygame.draw.rect(tela, cor, retangulo, border_radius=7)
    pygame.draw.rect(tela, (145, 128, 150), retangulo, 2, border_radius=7)
    superficie = fonte.render(texto, True, (224, 218, 228))
    tela.blit(superficie, superficie.get_rect(center=retangulo.center))


def desenhar_menu(
    tela,
    fonte,
    fonte_titulo,
    fonte_botao,
    estado,
    mouse_pos,
    volume_musica,
    volume_efeitos,
    fonte_tutorial,
):
    desenhar_cenario(tela)
    _desenhar_sobreposicao(tela)

    if estado == "menu":
        titulo = fonte_titulo.render("CAÇADOR DA NOITE", True, (202, 195, 211))
        tela.blit(titulo, titulo.get_rect(center=(LARGURA // 2, 148)))
        subtitulo = fonte.render("Uma noite no cemitério", True, (145, 137, 154))
        tela.blit(subtitulo, subtitulo.get_rect(center=(LARGURA // 2, 194)))
        for retangulo, texto in (
            (MENU_JOGAR_RECT, "Jogar"),
            (MENU_CONFIGURACOES_RECT, "Configurações"),
            (MENU_TUTORIAL_RECT, "Tutorial"),
        ):
            _desenhar_botao(tela, fonte_botao, retangulo, texto, mouse_pos)
        return

    pygame.draw.rect(
        tela,
        (24, 21, 33),
        (72, 88, LARGURA - 144, ALTURA - 128),
        border_radius=12,
    )
    pygame.draw.rect(
        tela,
        (102, 91, 116),
        (72, 88, LARGURA - 144, ALTURA - 128),
        2,
        border_radius=12,
    )
    _desenhar_botao(
        tela,
        fonte_botao,
        MENU_VOLTAR_RECT,
        "Voltar",
        mouse_pos,
    )

    titulo_texto = "Configurações" if estado == "configuracoes" else "Tutorial"
    titulo = fonte_titulo.render(titulo_texto, True, (202, 195, 211))
    tela.blit(titulo, titulo.get_rect(center=(LARGURA // 2, 128)))

    if estado == "configuracoes":
        _desenhar_controle_volume(
            tela, fonte, "Música", VOLUME_MUSICA_RECT, volume_musica
        )
        _desenhar_controle_volume(
            tela, fonte, "Efeitos sonoros", VOLUME_EFEITOS_RECT, volume_efeitos
        )
        dica = fonte.render(
            "Ajuste o volume arrastando os controles.",
            True,
            (155, 148, 166),
        )
        tela.blit(dica, dica.get_rect(center=(LARGURA // 2, 408)))
    elif estado == "tutorial":
        _desenhar_tutorial(tela, fonte_tutorial, fonte_botao)


def _desenhar_controle_volume(tela, fonte, rotulo, retangulo, volume):
    texto = fonte.render(rotulo, True, (211, 205, 218))
    tela.blit(texto, (retangulo.x, retangulo.y - 28))
    inicio = retangulo.x + 18
    fim = retangulo.right - 18
    centro_y = retangulo.centery
    pygame.draw.line(tela, (76, 70, 88), (inicio, centro_y), (fim, centro_y), 10)
    pygame.draw.line(
        tela,
        (172, 164, 184),
        (inicio, centro_y),
        (round(inicio + (fim - inicio) * volume), centro_y),
        6,
    )
    pygame.draw.circle(
        tela,
        (211, 205, 218),
        (round(inicio + (fim - inicio) * volume), centro_y),
        12,
    )
    pygame.draw.circle(
        tela,
        (85, 76, 99),
        (round(inicio + (fim - inicio) * volume), centro_y),
        12,
        2,
    )
    valor = fonte.render(f"{round(volume * 100)}%", True, (155, 148, 166))
    tela.blit(valor, (retangulo.right + 12, retangulo.y + 8))


def _desenhar_tutorial(tela, fonte, fonte_botao):
    pygame.draw.line(tela, (78, 70, 90), (104, 163), (856, 163), 1)

    instrucoes = (
        "Inimigos atacam por quatro direções: dos dois lados, pelo chão ou pelo ar.",
        "Clique no lado e na altura do inimigo para disparar na direção certa.",
        "A arma tem alcance limitado. Espere o inimigo se aproximar para acertar.",
        "Inimigos especiais são traiçoeiros. Você tem 8 balas; recarrega sem disparar.",
    )
    retangulo_cartao = pygame.Rect(104, 181, 444, 54)
    for indice, instrucao in enumerate(instrucoes, start=1):
        pygame.draw.rect(
            tela,
            (34, 30, 44),
            retangulo_cartao,
            border_radius=7,
        )
        pygame.draw.circle(
            tela,
            (88, 76, 101),
            (retangulo_cartao.x + 22, retangulo_cartao.centery),
            14,
        )
        numero = fonte.render(str(indice), True, (225, 216, 231))
        tela.blit(
            numero,
            numero.get_rect(
                center=(retangulo_cartao.x + 22, retangulo_cartao.centery)
            ),
        )
        linhas = _quebrar_texto(instrucao, fonte, 385)
        altura_linha = fonte.get_linesize()
        inicio_y = retangulo_cartao.centery - len(linhas) * altura_linha // 2
        for linha_indice, linha in enumerate(linhas):
            superficie = fonte.render(linha, True, (210, 205, 216))
            tela.blit(
                superficie,
                (retangulo_cartao.x + 48, inicio_y + linha_indice * altura_linha),
            )
        retangulo_cartao.y += 62

    painel_diagrama = pygame.Rect(575, 181, 281, 301)
    pygame.draw.rect(tela, (31, 28, 41), painel_diagrama, border_radius=9)
    pygame.draw.rect(tela, (76, 68, 87), painel_diagrama, 1, border_radius=9)
    legenda = fonte.render("Fique atento aos lados", True, (183, 174, 193))
    tela.blit(
        legenda,
        legenda.get_rect(center=(painel_diagrama.centerx, 208)),
    )

    centro = (painel_diagrama.centerx, 330)
    pygame.draw.circle(tela, (104, 91, 119), centro, 34, 2)
    pygame.draw.circle(tela, (190, 181, 202), (centro[0], centro[1] - 13), 8)
    pygame.draw.line(
        tela,
        (190, 181, 202),
        (centro[0], centro[1] - 3),
        (centro[0], centro[1] + 20),
        4,
    )
    pygame.draw.line(
        tela,
        (190, 181, 202),
        (centro[0] - 13, centro[1] + 5),
        (centro[0] + 13, centro[1] + 5),
        3,
    )
    pygame.draw.line(
        tela,
        (190, 181, 202),
        (centro[0], centro[1] + 19),
        (centro[0] - 9, centro[1] + 32),
        3,
    )
    pygame.draw.line(
        tela,
        (190, 181, 202),
        (centro[0], centro[1] + 19),
        (centro[0] + 9, centro[1] + 32),
        3,
    )
    _desenhar_seta(tela, (centro[0] - 78, centro[1] - 58), (centro[0] - 31, centro[1] - 27))
    _desenhar_seta(
        tela,
        (centro[0] + 78, centro[1] - 58),
        (centro[0] + 31, centro[1] - 27),
    )
    _desenhar_seta(
        tela,
        (centro[0] - 78, centro[1] + 58),
        (centro[0] - 31, centro[1] + 27),
    )
    _desenhar_seta(
        tela,
        (centro[0] + 78, centro[1] + 58),
        (centro[0] + 31, centro[1] + 27),
    )
    legenda_direcoes = fonte.render("Esquerda • Direita • Ar • Chão", True, (159, 151, 172))
    tela.blit(
        legenda_direcoes,
        legenda_direcoes.get_rect(center=(painel_diagrama.centerx, 445)),
    )


def _desenhar_seta(tela, inicio, fim):
    cor = (188, 174, 202)
    pygame.draw.line(tela, cor, inicio, fim, 3)
    angulo = math.atan2(fim[1] - inicio[1], fim[0] - inicio[0])
    for desvio in (-0.55, 0.55):
        ponta = (
            round(fim[0] - 10 * math.cos(angulo + desvio)),
            round(fim[1] - 10 * math.sin(angulo + desvio)),
        )
        pygame.draw.line(tela, cor, fim, ponta, 3)


def _quebrar_texto(texto, fonte, largura_maxima):
    linhas = []
    linha_atual = ""
    for palavra in texto.split():
        candidata = f"{linha_atual} {palavra}".strip()
        if linha_atual and fonte.size(candidata)[0] > largura_maxima:
            linhas.append(linha_atual)
            linha_atual = palavra
        else:
            linha_atual = candidata
    if linha_atual:
        linhas.append(linha_atual)
    return linhas


def _desenhar_lapide(tela, x, y, largura, altura, formato):
    cor = COR_SILHUETA_CEMITERIO
    if formato == "cruz":
        haste = max(6, largura // 4)
        cruz_altura = altura // 2
        pygame.draw.rect(
            tela,
            cor,
            (x + (largura - haste) // 2, y, haste, cruz_altura),
        )
        pygame.draw.rect(
            tela,
            cor,
            (x, y + cruz_altura // 3, largura, max(6, largura // 5)),
        )
        pygame.draw.rect(
            tela,
            cor,
            (x + 4, y + cruz_altura, largura - 8, altura - cruz_altura),
        )
    elif formato == "gótica":
        pygame.draw.polygon(
            tela,
            cor,
            [
                (x + largura // 2, y),
                (x + largura, y + 12),
                (x + largura - 4, y + altura),
                (x + 4, y + altura),
                (x, y + 12),
            ],
        )
    elif formato == "pontuda":
        pygame.draw.polygon(
            tela,
            cor,
            [
                (x + largura // 2, y),
                (x + largura, y + largura // 2),
                (x + largura - 4, y + altura),
                (x + 4, y + altura),
                (x, y + largura // 2),
            ],
        )
    elif formato == "chanfrada":
        pygame.draw.polygon(
            tela,
            cor,
            [
                (x + 5, y),
                (x + largura - 5, y),
                (x + largura, y + 8),
                (x + largura - 4, y + altura),
                (x + 4, y + altura),
                (x, y + 8),
            ],
        )
    elif formato == "ombros":
        pygame.draw.polygon(
            tela,
            cor,
            [
                (x + 7, y),
                (x + largura - 7, y),
                (x + largura - 4, y + 9),
                (x + largura, y + 13),
                (x + largura - 4, y + altura),
                (x + 4, y + altura),
                (x, y + 13),
                (x + 4, y + 9),
            ],
        )
    else:
        raio = largura // 2
        pygame.draw.rect(
            tela,
            cor,
            (x, y + raio, largura, altura - raio),
        )
        pygame.draw.circle(tela, cor, (x + raio, y + raio), raio)


def _desenhar_arvore_seca(tela):
    galhos = (
        ((88, CHAO_Y), (78, 325), 24),
        ((78, 325), (91, 250), 19),
        ((91, 250), (72, 179), 14),
        ((72, 179), (38, 133), 8),
        ((72, 190), (111, 143), 9),
        ((83, 285), (43, 232), 13),
        ((43, 232), (27, 174), 8),
        ((48, 238), (12, 214), 7),
        ((86, 270), (143, 217), 13),
        ((143, 217), (164, 157), 8),
        ((138, 220), (193, 195), 7),
        ((80, 326), (145, 293), 13),
        ((145, 293), (181, 244), 8),
        ((80, 306), (36, 290), 10),
        ((36, 290), (14, 255), 6),
        ((92, 250), (123, 204), 8),
        ((123, 204), (117, 163), 5),
        ((47, 231), (57, 191), 5),
    )
    for inicio, fim, largura in galhos:
        pygame.draw.line(
            tela,
            COR_SILHUETA_CEMITERIO,
            inicio,
            fim,
            largura,
        )


def _desenhar_cerca_e_portao(tela):
    esquerda = JOGADOR_X - ALCANCE
    direita = JOGADOR_X + ALCANCE
    topo = CHAO_Y - 42
    meio = CHAO_Y - 21
    base = CHAO_Y + 10

    for x_inicio, x_fim in ((0, esquerda), (direita, LARGURA)):
        pygame.draw.line(
            tela,
            COR_METAL_CERCA,
            (x_inicio, topo),
            (x_fim, topo),
            4,
        )
        pygame.draw.line(
            tela,
            COR_METAL_CERCA,
            (x_inicio, meio),
            (x_fim, meio),
            4,
        )
        for x in range(x_inicio + 12, x_fim, 24):
            pygame.draw.line(
                tela,
                COR_METAL_CERCA,
                (x, base),
                (x, topo - 2),
                4,
            )
            pygame.draw.polygon(
                tela,
                COR_METAL_DETALHE,
                [(x - 4, topo + 2), (x, topo - 8), (x + 4, topo + 2)],
            )
        for x in range(x_inicio + 48, x_fim, 96):
            pygame.draw.circle(tela, COR_METAL_DETALHE, (x, (topo + meio) // 2), 5, 2)

    arco = []
    for indice in range(41):
        t = indice / 40
        x = esquerda + (direita - esquerda) * t
        y = (CHAO_Y - 78) - math.sin(math.pi * t) * 112
        arco.append((round(x), round(y)))
    pygame.draw.lines(tela, COR_METAL_CERCA, False, arco, 8)
    arco_detalhe = [(x, y + 9) for x, y in arco]
    pygame.draw.lines(tela, COR_METAL_DETALHE, False, arco_detalhe, 2)
    topo_arco_x, topo_arco_y = arco[len(arco) // 2]

    for x in (esquerda, direita):
        topo_poste = CHAO_Y - 78
        poste = pygame.Rect(x - 9, topo_poste, 18, base - topo_poste + 1)
        pygame.draw.rect(tela, COR_METAL_CERCA, poste, border_radius=3)
        pygame.draw.rect(tela, COR_METAL_DETALHE, poste.inflate(-8, -8), 2)
        pygame.draw.rect(tela, COR_METAL_DETALHE, (x - 13, CHAO_Y - 82, 26, 7))
        pygame.draw.circle(tela, COR_METAL_CERCA, (x, CHAO_Y - 91), 9)
        pygame.draw.circle(tela, COR_METAL_DETALHE, (x, CHAO_Y - 91), 4)
        pygame.draw.line(
            tela,
            COR_METAL_DETALHE,
            (x - 5, CHAO_Y - 20),
            (x + 5, CHAO_Y - 20),
            2,
        )

    pygame.draw.line(
        tela,
        COR_METAL_DETALHE,
        (topo_arco_x, topo_arco_y - 2),
        (topo_arco_x, topo_arco_y - 10),
        3,
    )
    pygame.draw.circle(
        tela,
        COR_METAL_DETALHE,
        (topo_arco_x, topo_arco_y - 10),
        7,
    )
    pygame.draw.polygon(
        tela,
        COR_METAL_CERCA,
        [
            (topo_arco_x - 7, topo_arco_y - 13),
            (topo_arco_x, topo_arco_y - 27),
            (topo_arco_x + 7, topo_arco_y - 13),
        ],
    )

def desenhar_cenario(tela):
    tela.fill(COR_FUNDO)

    estrelas = (
        (72, 66), (170, 120), (290, 52), (410, 95), (545, 58),
        (640, 142), (870, 70), (910, 180), (340, 175), (110, 220),
    )
    for x, y in estrelas:
        pygame.draw.circle(tela, (218, 198, 245), (x, y), 2)

    brilho = pygame.Surface((220, 220), pygame.SRCALPHA)
    pygame.draw.circle(brilho, (198, 174, 255, 5), (110, 110), 106)
    pygame.draw.circle(brilho, (255, 222, 174, 9), (110, 110), 96)
    pygame.draw.circle(brilho, (255, 238, 170, 18), (110, 110), 86)
    pygame.draw.circle(brilho, (255, 238, 170, 32), (110, 110), 66)
    pygame.draw.circle(brilho, (255, 238, 190, 55), (110, 110), 48)
    tela.blit(brilho, (680, -5))
    pygame.draw.circle(tela, (255, 246, 202), (790, 105), 37)
    pygame.draw.circle(tela, (255, 255, 235), (790, 105), 29)

    pygame.draw.rect(tela, COR_CHAO, (0, CHAO_Y, LARGURA, ALTURA - CHAO_Y))
    pygame.draw.polygon(
        tela,
        COR_SILHUETA_CEMITERIO,
        [
            (520, CHAO_Y),
            (565, 389),
            (620, 365),
            (685, 345),
            (750, 336),
            (815, 338),
            (870, 351),
            (925, 378),
            (LARGURA, 398),
            (LARGURA, CHAO_Y),
        ],
    )

    lapides = (
        (55, 354, 36, 66, "arredondada"),
        (135, 375, 28, 45, "pontuda"),
        (235, 345, 42, 75, "cruz"),
        (335, 380, 30, 40, "chanfrada"),
        (615, 324, 34, 50, "ombros"),
        (715, 278, 42, 70, "gótica"),
        (825, 309, 30, 42, "arredondada"),
        (900, 312, 38, 64, "cruz"),
    )
    for lapide in lapides:
        _desenhar_lapide(tela, *lapide)

    _desenhar_arvore_seca(tela)


def desenhar_jogador(tela, direcao_arma, alvo_arma=None):
    cx = JOGADOR_X
    pygame.draw.line(tela, (19, 20, 27), (cx - 7, CHAO_Y - 15), (cx - 9, CHAO_Y), 8)
    pygame.draw.line(tela, (19, 20, 27), (cx + 7, CHAO_Y - 15), (cx + 9, CHAO_Y), 8)
    pygame.draw.ellipse(tela, (10, 11, 17), (cx - 17, CHAO_Y - 53, 34, 41))
    pygame.draw.polygon(
        tela,
        (18, 19, 26),
        (
            (cx - 15, CHAO_Y - 49),
            (cx - 9, CHAO_Y - 55),
            (cx + 9, CHAO_Y - 55),
            (cx + 15, CHAO_Y - 49),
            (cx + 19, CHAO_Y - 10),
            (cx + 13, CHAO_Y - 2),
            (cx - 13, CHAO_Y - 2),
            (cx - 19, CHAO_Y - 10),
        ),
    )
    pygame.draw.polygon(
        tela,
        (82, 72, 68),
        ((cx - 9, CHAO_Y - 48), (cx, CHAO_Y - 38), (cx - 4, CHAO_Y - 8), (cx - 13, CHAO_Y - 5)),
    )
    pygame.draw.line(tela, (115, 91, 67), (cx, CHAO_Y - 47), (cx, CHAO_Y - 5), 2)

    pygame.draw.ellipse(tela, (197, 155, 124), (cx - 9, CHAO_Y - 72, 18, 23))
    pygame.draw.polygon(
        tela,
        (37, 29, 27),
        (
            (cx - 10, CHAO_Y - 65),
            (cx - 8, CHAO_Y - 76),
            (cx + 7, CHAO_Y - 77),
            (cx + 11, CHAO_Y - 66),
            (cx + 8, CHAO_Y - 60),
            (cx + 6, CHAO_Y - 69),
            (cx - 5, CHAO_Y - 67),
            (cx - 8, CHAO_Y - 59),
        ),
    )
    pygame.draw.polygon(
        tela,
        (10, 11, 17),
        (
            (cx - 22, CHAO_Y - 72),
            (cx - 12, CHAO_Y - 75),
            (cx - 7, CHAO_Y - 79),
            (cx + 7, CHAO_Y - 79),
            (cx + 14, CHAO_Y - 74),
            (cx + 23, CHAO_Y - 72),
            (cx + 13, CHAO_Y - 69),
            (cx - 15, CHAO_Y - 69),
        ),
    )
    pygame.draw.polygon(
        tela,
        (25, 26, 34),
        (
            (cx - 9, CHAO_Y - 78),
            (cx - 7, CHAO_Y - 88),
            (cx + 5, CHAO_Y - 91),
            (cx + 11, CHAO_Y - 78),
        ),
    )
    pygame.draw.line(tela, (133, 103, 70), (cx - 11, CHAO_Y - 73), (cx + 12, CHAO_Y - 73), 2)

    altura_oculos = CHAO_Y - 62
    for x_oculo in (cx - 9, cx + 1):
        pygame.draw.rect(
            tela,
            (18, 19, 26),
            (x_oculo, altura_oculos - 3, 8, 6),
            border_radius=2,
        )
        pygame.draw.rect(
            tela,
            (103, 125, 137),
            (x_oculo + 1, altura_oculos - 2, 6, 4),
            border_radius=1,
        )
    pygame.draw.line(
        tela,
        (18, 19, 26),
        (cx - 1, altura_oculos),
        (cx + 1, altura_oculos),
        2,
    )

    pygame.draw.line(tela, (167, 142, 116), (cx - 3, CHAO_Y - 49), (cx, CHAO_Y - 41), 2)
    pygame.draw.line(tela, (167, 142, 116), (cx, CHAO_Y - 41), (cx + 3, CHAO_Y - 49), 2)
    pygame.draw.line(tela, (210, 185, 140), (cx, CHAO_Y - 42), (cx, CHAO_Y - 31), 2)
    pygame.draw.line(tela, (210, 185, 140), (cx - 4, CHAO_Y - 37), (cx + 4, CHAO_Y - 37), 2)

    lado, vertical = direcao_arma
    inicio_tiro, fim_tiro = _linha_tiro(lado, vertical, alvo_arma)
    dx_tiro = fim_tiro[0] - inicio_tiro[0]
    dy_tiro = fim_tiro[1] - inicio_tiro[1]
    comprimento_tiro = math.hypot(dx_tiro, dy_tiro)
    if comprimento_tiro == 0:
        dx_tiro, dy_tiro = _vetor_tiro(lado, vertical)
        comprimento_tiro = math.hypot(dx_tiro, dy_tiro)
    direcao_tiro = (
        dx_tiro / comprimento_tiro,
        dy_tiro / comprimento_tiro,
    )
    boca = (float(inicio_tiro[0]), float(inicio_tiro[1]))
    base_cano = (
        boca[0] - direcao_tiro[0] * 30,
        boca[1] - direcao_tiro[1] * 30,
    )
    ombro = (JOGADOR_X + lado * 4, JOGADOR_Y + 5)
    normal = (-direcao_tiro[1], direcao_tiro[0])
    if normal[1] < 0 or (normal[1] == 0 and normal[0] * lado > 0):
        normal = (-normal[0], -normal[1])
    cabo = (
        base_cano[0] + normal[0] * 9,
        base_cano[1] + normal[1] * 9,
    )

    pygame.draw.line(
        tela,
        (225, 175, 145),
        ombro,
        (int(cabo[0]), int(cabo[1])),
        5,
    )
    pygame.draw.line(
        tela,
        (42, 44, 58),
        (int(base_cano[0]), int(base_cano[1])),
        (int(boca[0]), int(boca[1])),
        8,
    )
    pygame.draw.line(
        tela,
        (125, 130, 150),
        (int(base_cano[0]), int(base_cano[1])),
        (int(boca[0]), int(boca[1])),
        3,
    )
    pygame.draw.line(
        tela,
        (105, 70, 48),
        (int(cabo[0]), int(cabo[1])),
        (int(base_cano[0]), int(base_cano[1])),
        5,
    )


def _vetor_tiro(lado, vertical):
    return lado * (ALCANCE - 15), -90 if vertical == "ar" else 10


def _linha_tiro(lado, vertical, alvo=None):
    inicio = (JOGADOR_X + lado * 15, JOGADOR_Y)
    if alvo is not None:
        return inicio, alvo
    dx, dy = _vetor_tiro(lado, vertical)
    return inicio, (inicio[0] + dx, inicio[1] + dy)


def desenhar_golpe(tela, golpe):
    lado, vertical, restante, acertou, alvo, animar_tiro = golpe
    progresso = min(1.0, max(0.0, 1 - restante / DURACAO_GOLPE))
    alfa = max(0.0, restante / DURACAO_GOLPE)
    cor = (255, 255, 255) if acertou else (150, 150, 170)
    inicio, fim = _linha_tiro(lado, vertical, alvo)
    if animar_tiro and alvo is not None:
        fim = (
            round(inicio[0] + (fim[0] - inicio[0]) * progresso),
            round(inicio[1] + (fim[1] - inicio[1]) * progresso),
        )
    largura = max(1, int(6 * alfa))
    pygame.draw.line(tela, cor, inicio, fim, largura)
    if animar_tiro and alvo is not None:
        pygame.draw.circle(tela, cor, fim, 3)


def _desenhar_ceifador(tela, inimigo: Inimigo):
    cx = int(inimigo.x)
    base = CHAO_Y
    sentido = -inimigo.lado
    fase = inimigo.t * 2
    passo = math.sin(fase) * 2
    balanco = math.sin(fase) * 0.08

    def ponto(local_x, local_y):
        return (round(cx + sentido * local_x), round(base + local_y))

    def ponto_foice(local_x, local_y):
        eixo_x, eixo_y = 6, -13
        dx, dy = local_x - eixo_x, local_y - eixo_y
        x = eixo_x + dx * math.cos(balanco) - dy * math.sin(balanco)
        y = eixo_y + dx * math.sin(balanco) + dy * math.cos(balanco)
        return ponto(x, y)

    cabo = (ponto_foice(6, -13), ponto_foice(23, -48))
    pygame.draw.line(tela, (22, 21, 24), *cabo, 6)
    pygame.draw.line(tela, (238, 158, 42), *cabo, 3)

    contorno_lamina = tuple(
        ponto_foice(x, y)
        for x, y in (
            (21, -48), (28, -44), (35, -37), (40, -28),
            (44, -18), (45, -8), (43, 0), (40, 4), (38, 0),
            (36, -10), (33, -21), (29, -31), (24, -40),
        )
    )
    lamina = tuple(
        ponto_foice(x, y)
        for x, y in (
            (24, -44), (29, -41), (35, -34), (39, -26),
            (42, -17), (43, -9), (41, -2), (39, -12),
            (36, -22), (32, -32), (27, -40),
        )
    )
    pygame.gfxdraw.filled_polygon(tela, contorno_lamina, (20, 22, 25))
    pygame.gfxdraw.aapolygon(tela, contorno_lamina, (20, 22, 25))
    pygame.gfxdraw.filled_polygon(tela, lamina, (76, 91, 99))
    pygame.gfxdraw.aapolygon(tela, lamina, (76, 91, 99))

    manto = (
        ponto(0, -43),
        ponto(11, -35),
        ponto(10, -20),
        ponto(17, -2 + passo),
        ponto(7, -5 - passo),
        ponto(0, -2 + passo),
        ponto(-7, -5 - passo),
        ponto(-17, -2 + passo),
        ponto(-10, -20),
        ponto(-11, -35),
    )
    pygame.draw.polygon(tela, (20, 17, 29), manto)
    pygame.draw.lines(
        tela,
        (61, 54, 72),
        False,
        (ponto(-10, -19), ponto(-7, -9), ponto(0, -5), ponto(7, -9), ponto(10, -19)),
        2,
    )
    pygame.draw.ellipse(tela, (9, 8, 15), (cx - 9, base - 39, 18, 19))
    pygame.draw.polygon(
        tela,
        (9, 8, 15),
        (ponto(-9, -31), ponto(0, -43), ponto(9, -31)),
    )
    for olho_x in (-4, 4):
        olho = ponto(olho_x, -29)
        pygame.draw.circle(tela, (255, 75, 58), olho, 2)
        pygame.draw.circle(tela, (255, 190, 110), olho, 1)


def _desenhar_fantasma(tela, inimigo: Inimigo):
    cx, cy = int(inimigo.x), int(inimigo.y)
    onda = math.sin(inimigo.t * 2.4)
    onda_lateral = math.sin(inimigo.t * 2.4 + math.pi / 2)

    def curva(p0, p1, p2, p3):
        pontos = []
        for indice in range(1, 9):
            t = indice / 8
            u = 1 - t
            x = u**3 * p0[0] + 3 * u**2 * t * p1[0] + 3 * u * t**2 * p2[0] + t**3 * p3[0]
            y = u**3 * p0[1] + 3 * u**2 * t * p1[1] + 3 * u * t**2 * p2[1] + t**3 * p3[1]
            pontos.append((round(cx + x), round(cy + y)))
        return pontos

    segmentos = (
        ((0, -35), (-10, -35), (-17, -29), (-18, -17)),
        ((-18, -17), (-20, -5), (-18, 6), (-21, 13)),
        ((-21, 13), (-24, 18 + onda * 2), (-28, 20 + onda * 2), (-27, 22 + onda)),
        ((-27, 22 + onda), (-25, 26 + onda), (-18, 25 - onda), (-15, 21 - onda)),
        ((-15, 21 - onda), (-14, 29 - onda), (-8, 34 + onda), (-4, 29 + onda)),
        ((-4, 29 + onda), (0, 25 + onda), (1, 27 - onda), (4, 31 - onda)),
        ((4, 31 - onda), (8, 35 - onda), (13, 29 + onda_lateral), (14, 23 + onda_lateral)),
        ((14, 23 + onda_lateral), (20, 26 + onda_lateral), (27, 24 + onda_lateral), (27, 20 + onda_lateral)),
        ((27, 20 + onda_lateral), (27, 16 + onda_lateral), (21, 9), (19, 1)),
        ((19, 1), (16, -10), (16, -24), (9, -31)),
        ((9, -31), (4, -36), (-4, -37), (0, -35)),
    )
    corpo = []
    for segmento in segmentos:
        corpo.extend(curva(*segmento))

    pygame.gfxdraw.filled_polygon(tela, corpo, (250, 249, 255))
    pygame.gfxdraw.aapolygon(tela, corpo, (18, 17, 24))

    pygame.draw.lines(
        tela,
        (196, 194, 205),
        False,
        ((cx - 14, cy - 5), (cx - 13, cy + 4), (cx - 12, cy + 16 + onda)),
        2,
    )
    pygame.draw.lines(
        tela,
        (196, 194, 205),
        False,
        ((cx + 14, cy - 3), (cx + 17, cy + 7), (cx + 24, cy + 14 + onda_lateral)),
        2,
    )
    pygame.draw.lines(
        tela,
        (196, 194, 205),
        False,
        ((cx - 4, cy + 9), (cx - 3, cy + 17), (cx + 2, cy + 26 - onda)),
        2,
    )

    olho = (255, 105, 190) if inimigo.fantasma_explosivo else (8, 8, 13)
    for olho_x in (cx - 7, cx + 8):
        pygame.draw.ellipse(tela, olho, (olho_x - 4, cy - 19, 8, 15))
        if inimigo.fantasma_explosivo:
            pygame.draw.circle(tela, (255, 218, 243), (olho_x - 2, cy - 14), 2)


def _desenhar_espantalho(tela, inimigo: Inimigo):
    cx = int(inimigo.x)
    base = CHAO_Y
    movimento = math.sin(inimigo.t * 2) * 2
    cor_palha = (184, 127, 55)
    cor_palha_clara = (224, 177, 91)
    cor_madeira = (82, 49, 35)

    topo_poste = base - 28 if inimigo.cabeca_caida else base - 140
    pygame.draw.line(tela, cor_madeira, (cx, topo_poste), (cx, base - 5), 7)
    pygame.draw.line(tela, cor_palha, (cx - 29, base - 88), (cx + 29, base - 88), 7)
    pygame.draw.line(tela, cor_palha_clara, (cx - 42, base - 94), (cx - 25, base - 82), 3)
    pygame.draw.line(tela, cor_palha_clara, (cx + 25, base - 82), (cx + 42, base - 94), 3)
    pygame.draw.line(tela, cor_palha, (cx - 2, base - 9), (cx - 13, base), 5)
    pygame.draw.line(tela, cor_palha, (cx + 2, base - 9), (cx + 13, base), 5)
    pygame.draw.polygon(
        tela,
        (77, 42, 37),
        (
            (cx - 9, base - 88 + round(movimento)),
            (cx + 9, base - 88 - round(movimento)),
            (cx + 8, base - 36),
            (cx - 8, base - 36),
        ),
    )
    pygame.draw.line(tela, cor_palha_clara, (cx - 7, base - 80), (cx + 6, base - 48), 2)
    pygame.draw.line(tela, cor_palha, (cx + 7, base - 79), (cx - 5, base - 47), 2)
    for lado in (-1, 1):
        x = cx + lado * 34
        pygame.draw.line(tela, cor_palha, (x, base - 92), (x + lado * 8, base - 82), 2)
        pygame.draw.line(tela, cor_palha_clara, (x - 3, base - 93), (x - 5, base - 82), 2)
        pygame.draw.line(tela, cor_palha, (x + 3, base - 93), (x + 6, base - 83), 2)

    if inimigo.cabeca_caida:
        progresso = min(
            1.0,
            inimigo.tempo_queda_cabeca / DURACAO_QUEDA_CABECA,
        )
        cabeca_y = round(260 + (base - 79 - 260) * progresso)
        cabeca_x = cx
    else:
        cabeca_y = 260
        cabeca_x = cx
    pygame.draw.ellipse(
        tela,
        (105, 48, 14),
        (cabeca_x - 21, cabeca_y - 20, 42, 40),
    )
    pygame.draw.ellipse(
        tela,
        (232, 111, 21),
        (cabeca_x - 18, cabeca_y - 20, 36, 36),
    )
    for offset in (-11, 0, 11):
        pygame.draw.arc(
            tela,
            (190, 77, 17),
            (cabeca_x + offset - 7, cabeca_y - 16, 14, 31),
            0.2,
            2.9,
            2,
        )
    pygame.draw.polygon(
        tela,
        (255, 221, 78),
        (
            (cabeca_x - 13, cabeca_y - 6),
            (cabeca_x - 4, cabeca_y - 2),
            (cabeca_x - 12, cabeca_y + 1),
        ),
    )
    pygame.draw.polygon(
        tela,
        (255, 221, 78),
        (
            (cabeca_x + 13, cabeca_y - 6),
            (cabeca_x + 4, cabeca_y - 2),
            (cabeca_x + 12, cabeca_y + 1),
        ),
    )
    pygame.draw.polygon(
        tela,
        (68, 34, 24),
        (
            (cabeca_x - 11, cabeca_y + 7),
            (cabeca_x - 6, cabeca_y + 12),
            (cabeca_x - 2, cabeca_y + 8),
            (cabeca_x + 2, cabeca_y + 13),
            (cabeca_x + 7, cabeca_y + 7),
            (cabeca_x + 12, cabeca_y + 8),
            (cabeca_x + 9, cabeca_y + 17),
            (cabeca_x - 8, cabeca_y + 17),
        ),
    )


def _desenhar_zumbi(tela, inimigo: Inimigo):
    cx = int(inimigo.x)
    base = CHAO_Y
    sentido = -inimigo.lado
    pele = (111, 130, 75)
    pele_clara = (147, 161, 91)
    roupa = (65, 47, 53)
    roupa_clara = (91, 63, 66)
    fase = inimigo.t * 2
    passo = math.sin(fase) * 6
    braco = math.sin(fase + math.pi) * 6
    balanco = round(abs(math.sin(fase)) * 2)

    pygame.draw.line(
        tela,
        (39, 35, 38),
        (cx - 12, base - 18 - balanco),
        (cx - 15 + round(passo), base),
        7,
    )
    pygame.draw.line(
        tela,
        (39, 35, 38),
        (cx + 11, base - 18 - balanco),
        (cx + 16 - round(passo), base),
        7,
    )
    pygame.draw.line(
        tela,
        pele,
        (cx - 17, base - 48 - balanco),
        (cx - 27 + round(braco), base - 25),
        9,
    )
    pygame.draw.line(
        tela,
        pele,
        (cx + 17, base - 48 - balanco),
        (cx + 26 - round(braco), base - 26),
        9,
    )
    pygame.draw.ellipse(tela, roupa, (cx - 26, base - 52 - balanco, 52, 43))
    pygame.draw.ellipse(tela, roupa_clara, (cx - 22, base - 48 - balanco, 44, 34), 2)
    pygame.draw.line(
        tela,
        (145, 128, 104),
        (cx, base - 49 - balanco),
        (cx + sentido * 5, base - 19),
        3,
    )
    pygame.draw.circle(tela, (36, 34, 34), (cx + sentido * 5, base - 38 - balanco), 2)
    pygame.draw.circle(tela, (36, 34, 34), (cx + sentido * 4, base - 29 - balanco), 2)

    pygame.draw.ellipse(tela, pele, (cx - 18, base - 72 - balanco, 36, 31))
    pygame.draw.arc(tela, pele_clara, (cx - 16, base - 70 - balanco, 32, 27), 0.2, 2.8, 2)
    pygame.draw.ellipse(tela, (67, 45, 37), (cx - 19, base - 75 - balanco, 38, 13))
    pygame.draw.ellipse(tela, (38, 34, 32), (cx - 16, base - 81 - balanco, 32, 12))

    olho = (111, 255, 24) if inimigo.zumbi_neon else (182, 33, 38)
    brilho = (209, 255, 125) if inimigo.zumbi_neon else (255, 101, 72)
    for olho_x in (cx - 7, cx + 7):
        pygame.draw.ellipse(tela, olho, (olho_x - 3, base - 62 - balanco, 6, 8))
        pygame.draw.circle(tela, brilho, (olho_x - 1, base - 60 - balanco), 1)
    pygame.draw.line(
        tela,
        (49, 37, 34),
        (cx - 6, base - 48 - balanco),
        (cx + 7, base - 48 - balanco),
        3,
    )
    pygame.draw.line(
        tela,
        (230, 215, 177),
        (cx - 4, base - 46 - balanco),
        (cx + 5, base - 46 - balanco),
        1,
    )


def desenhar_inimigo(tela, inimigo: Inimigo):
    if inimigo.tempo_flash_dano <= 0:
        _desenhar_inimigo(tela, inimigo)
        return

    camada = pygame.Surface(tela.get_size(), pygame.SRCALPHA)
    _desenhar_inimigo(camada, inimigo)
    intensidade = inimigo.tempo_flash_dano / DURACAO_FLASH_DANO
    canal = round(255 - 190 * intensidade)
    camada.fill((255, canal, canal, 255), special_flags=pygame.BLEND_RGBA_MULT)
    tela.blit(camada, (0, 0))


def _desenhar_inimigo(tela, inimigo: Inimigo):
    if inimigo.teleportador:
        for x, y, tempo in inimigo.efeitos_teleporte:
            progresso = tempo / DURACAO_EFEITO_TELEPORTE
            brilho = pygame.Surface((96, 96), pygame.SRCALPHA)
            for indice in range(3):
                fase = progresso - indice * 0.22
                if 0 <= fase <= 1:
                    raio = 5 + round(fase * 34)
                    alpha = round(220 * (1 - fase))
                    pygame.draw.circle(
                        brilho,
                        (*COR_MANA_MORCEGO, alpha),
                        (48, 48),
                        raio,
                        max(1, round(4 * (1 - fase))),
                    )
            tela.blit(brilho, (x - 48, y - 48))

    if inimigo.pesado_voador:
        cor_chao = COR_PESADO_VOADOR
    elif inimigo.grande:
        cor_chao = COR_INIMIGO_GRANDE
    else:
        cor_chao = COR_VARIANTE_CHAO if inimigo.rapido else COR_INIMIGO_CHAO

    if inimigo.tipo == "chao":
        if inimigo.grande:
            tamanho = TAMANHO_INIMIGO_GRANDE
        elif inimigo.rapido:
            tamanho = TAMANHO_INIMIGO_RAPIDO
        else:
            tamanho = TAMANHO_INIMIGO_CHAO
        if inimigo.espantalho:
            _desenhar_espantalho(tela, inimigo)
            return
        if inimigo.grande:
            _desenhar_zumbi(tela, inimigo)
            return
        if inimigo.rapido:
            _desenhar_rato(tela, inimigo)
            return
        if not inimigo.grande:
            _desenhar_ceifador(tela, inimigo)
            return
        rect = pygame.Rect(0, 0, *tamanho)
        rect.midbottom = (int(inimigo.x), CHAO_Y)
        pygame.draw.rect(
            tela,
            cor_chao,
            rect,
            border_radius=9 if inimigo.grande else 5,
        )
    else:
        cx, cy = int(inimigo.x), int(inimigo.y)
        if inimigo.fantasma:
            _desenhar_fantasma(tela, inimigo)
        else:
            if inimigo.pesado_voador:
                largura_asa, altura_asa, raio = 30, 12, 15
            elif inimigo.rapido:
                largura_asa, altura_asa, raio = 17, 7, 9
            else:
                largura_asa, altura_asa, raio = 24, 10, 12
            if inimigo.pesado_voador:
                cor_morcego = (74, 43, 29)
            elif inimigo.teleportador:
                cor_morcego = (245, 242, 255)
            else:
                cor_morcego = (245, 242, 255) if inimigo.rapido else (4, 3, 8)
            flap = math.sin(inimigo.t * 2) * altura_asa
            ponta_y = cy + flap
            silhueta = [
                (cx - 3, cy - 2),
                (cx - largura_asa, ponta_y - altura_asa),
                (cx - largura_asa * 3 // 4, cy - altura_asa // 3),
                (cx - largura_asa // 2, cy + altura_asa // 2),
                (cx - largura_asa // 3, cy + altura_asa // 4),
                (cx, cy + raio // 2),
                (cx + largura_asa // 3, cy + altura_asa // 4),
                (cx + largura_asa // 2, cy + altura_asa // 2),
                (cx + largura_asa * 3 // 4, cy - altura_asa // 3),
                (cx + largura_asa, ponta_y - altura_asa),
                (cx + 3, cy - 2),
                (cx + raio // 2, cy - raio),
                (cx, cy - raio + 2),
                (cx - raio // 2, cy - raio),
            ]
            if inimigo.teleportador:
                pygame.draw.polygon(tela, COR_MANA_MORCEGO, silhueta, 3)
            pygame.draw.polygon(tela, cor_morcego, silhueta)
            corpo_morcego = pygame.Rect(
                cx - raio // 2,
                cy - raio // 2,
                raio,
                raio * 2,
            )
            if inimigo.teleportador:
                pygame.draw.ellipse(tela, COR_MANA_MORCEGO, corpo_morcego, 2)
            pygame.draw.ellipse(
                tela,
                cor_morcego,
                corpo_morcego,
            )
            cabeca = (cx, cy - raio // 2)
            raio_cabeca = max(3, raio // 2)
            if inimigo.teleportador:
                pygame.draw.circle(tela, COR_MANA_MORCEGO, cabeca, raio_cabeca + 1, 2)
            pygame.draw.circle(tela, cor_morcego, cabeca, raio_cabeca)
            olho = (255, 70, 90) if not inimigo.rapido else (90, 30, 45)
            pygame.draw.circle(tela, olho, (cx - 2, cy - raio // 2), 1)
            pygame.draw.circle(tela, olho, (cx + 2, cy - raio // 2), 1)

def _desenhar_rato(tela, inimigo: Inimigo):
    cx = int(inimigo.x)
    base = CHAO_Y - 3
    sentido = -inimigo.lado
    cor_corpo = (5, 5, 9)

    def ponto(local_x, local_y):
        return (cx + sentido * local_x, base + local_y)

    fase = inimigo.t * 2
    balanco_frente = math.sin(fase) * 4
    balanco_traseira = math.sin(fase + math.pi) * 4
    patas = (
        (7, balanco_frente),
        (10, -balanco_frente),
        (-10, balanco_traseira),
        (-7, -balanco_traseira),
    )
    for local_x, balanco in patas:
        inicio = ponto(local_x, -8)
        joelho = ponto(local_x + balanco, -3)
        pe = ponto(local_x + balanco + 3, -1)
        pygame.draw.lines(tela, cor_corpo, False, (inicio, joelho, pe), 3)

    cauda = (ponto(-12, -10), ponto(-19, -13), ponto(-25, -10), ponto(-30, -15))
    pygame.draw.lines(tela, cor_corpo, False, cauda, 2)

    corpo = pygame.Rect(cx - 15, base - 25, 30, 20)
    cabeca = ponto(13, -20)
    focinho = ponto(22, -17)

    pygame.draw.ellipse(tela, cor_corpo, corpo)
    pygame.draw.circle(tela, cor_corpo, cabeca, 8)
    pygame.draw.polygon(
        tela,
        cor_corpo,
        [ponto(8, -25), ponto(10, -35), ponto(16, -27)],
    )
    pygame.draw.polygon(
        tela,
        cor_corpo,
        [ponto(14, -26), ponto(19, -34), ponto(21, -24)],
    )
    pygame.draw.polygon(
        tela,
        cor_corpo,
        [ponto(18, -22), ponto(27, -18), ponto(19, -14)],
    )

    olho = ponto(16, -22)
    if inimigo.rato_magico:
        pygame.draw.circle(tela, (110, 210, 255), olho, 4)
        pygame.draw.circle(tela, (35, 145, 255), olho, 3)
        pygame.draw.circle(tela, (8, 45, 115), olho, 1)
        cor_nariz = (115, 190, 255)
    else:
        pygame.draw.circle(tela, (255, 110, 125), olho, 4)
        pygame.draw.circle(tela, (255, 35, 55), olho, 3)
        pygame.draw.circle(tela, (100, 8, 24), olho, 1)
        cor_nariz = (255, 140, 155)
    pygame.draw.circle(tela, cor_nariz, focinho, 2)


def desenhar_jogo(tela, fonte, fonte_grande, jogo, fonte_hud, fonte_fim_titulo):
    desenhar_cenario(tela)
    desenhar_jogador(tela, jogo.direcao_arma, jogo.alvo_arma)
    if not jogo.game_over:
        for inimigo in jogo.inimigos:
            desenhar_inimigo(tela, inimigo)
    for inimigo_morto, _ in jogo.inimigos_dano_mortais:
        desenhar_inimigo(tela, inimigo_morto)
    _desenhar_cerca_e_portao(tela)
    if jogo.golpe:
        desenhar_golpe(tela, jogo.golpe)

    textos_hud = (
        (f"Pontos: {jogo.pontos}", (190, 195, 205), ALTURA - 72),
        (f"Recorde: {jogo.recorde}", (170, 160, 180), ALTURA - 42),
    )
    for texto, cor, y in textos_hud:
        superficie_texto = fonte_hud.render(texto, True, cor)
        tela.blit(
            fonte_hud.render(texto, True, (12, 10, 18)),
            (18, y + 2),
        )
        tela.blit(superficie_texto, (16, y))

    largura_bala = 10
    altura_bala = 22
    espacamento_balas = 6
    largura_municao = (
        MUNICOES_POR_CARREGADOR * (largura_bala + espacamento_balas)
        - espacamento_balas
    )
    inicio_municao_x = LARGURA - largura_municao - 20
    y_bala = ALTURA - altura_bala - 16
    for indice in range(MUNICOES_POR_CARREGADOR):
        x_bala = inicio_municao_x + indice * (largura_bala + espacamento_balas)
        forma_bala = (
            (x_bala + largura_bala // 2, y_bala),
            (x_bala + largura_bala - 1, y_bala + 6),
            (x_bala + largura_bala - 1, y_bala + altura_bala - 2),
            (x_bala + 1, y_bala + altura_bala - 2),
            (x_bala + 1, y_bala + 6),
        )
        if indice < jogo.municao:
            pygame.draw.polygon(tela, (95, 101, 112), forma_bala)
            pygame.draw.rect(
                tela,
                (190, 198, 208),
                (x_bala + 2, y_bala + 6, largura_bala - 4, altura_bala - 9),
            )
            pygame.draw.line(
                tela,
                (235, 239, 244),
                (x_bala + 3, y_bala + 7),
                (x_bala + 3, y_bala + altura_bala - 5),
                1,
            )
            pygame.draw.line(
                tela,
                (125, 132, 143),
                (x_bala + 1, y_bala + altura_bala - 4),
                (x_bala + largura_bala - 2, y_bala + altura_bala - 4),
                2,
            )
        else:
            pygame.draw.polygon(tela, (95, 101, 112), forma_bala, 1)
            pygame.draw.rect(
                tela,
                (95, 101, 112),
                (x_bala + 2, y_bala + 7, largura_bala - 4, altura_bala - 10),
                1,
            )

    if not jogo.game_over and jogo.pontos == 0 and any(
        inimigo.x
        in (float(MARGEM_INIMIGO), float(LARGURA - MARGEM_INIMIGO))
        for inimigo in jogo.inimigos
    ):
        dica = fonte.render(
            "Clique no lado e na altura do inimigo (chão ou ar)",
            True,
            COR_TEXTO,
        )
        tela.blit(dica, dica.get_rect(center=(LARGURA // 2, 110)))

    if jogo.explosao_rosa > 0:
        flash_rosa = pygame.Surface((LARGURA, ALTURA), pygame.SRCALPHA)
        alfa = round(190 * jogo.explosao_rosa / DURACAO_EXPLOSAO_ROSA)
        flash_rosa.fill((255, 75, 180, alfa))
        tela.blit(flash_rosa, (0, 0))
    if jogo.explosao_verde > 0:
        flash_verde = pygame.Surface((LARGURA, ALTURA), pygame.SRCALPHA)
        alfa = round(190 * jogo.explosao_verde / DURACAO_EXPLOSAO_ROSA)
        flash_verde.fill((173, 255, 0, alfa))
        tela.blit(flash_verde, (0, 0))
    if jogo.game_over:
        _desenhar_tela_fim_de_jogo(tela, fonte, fonte_fim_titulo, jogo)


def _desenhar_tela_fim_de_jogo(tela, fonte, fonte_titulo, jogo):
    sobreposicao = pygame.Surface((LARGURA, ALTURA), pygame.SRCALPHA)
    sobreposicao.fill((5, 4, 10, 205))
    tela.blit(sobreposicao, (0, 0))

    painel = pygame.Rect(220, 82, 520, 390)
    pygame.draw.rect(tela, (24, 20, 33), painel, border_radius=14)
    pygame.draw.rect(tela, (115, 98, 125), painel, 2, border_radius=14)

    titulo = fonte_titulo.render("FIM DE JOGO", True, (211, 194, 205))
    tela.blit(titulo, titulo.get_rect(center=(LARGURA // 2, 148)))

    pontuacao = fonte.render(f"Pontuação atingida: {jogo.pontos}", True, COR_TEXTO)
    tela.blit(pontuacao, pontuacao.get_rect(center=(LARGURA // 2, 220)))
    texto_recorde = (
        "Novo recorde!"
        if jogo.novo_recorde
        else f"Recorde não superado — recorde atual: {jogo.recorde}"
    )
    cor_recorde = (218, 194, 135) if jogo.novo_recorde else (166, 157, 176)
    recorde = fonte.render(texto_recorde, True, cor_recorde)
    tela.blit(recorde, recorde.get_rect(center=(LARGURA // 2, 265)))

    mouse_pos = pygame.mouse.get_pos()
    _desenhar_botao(
        tela,
        fonte,
        GAME_OVER_MENU_RECT,
        "Voltar ao menu",
        mouse_pos,
    )
    _desenhar_botao(
        tela,
        fonte,
        GAME_OVER_RETRY_RECT,
        "Tentar novamente",
        mouse_pos,
    )
