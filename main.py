from pathlib import Path
import sys

import pygame

from desenho import (
    MENU_CONFIGURACOES_RECT,
    MENU_JOGAR_RECT,
    MENU_TUTORIAL_RECT,
    MENU_VOLTAR_RECT,
    GAME_OVER_MENU_RECT,
    GAME_OVER_RETRY_RECT,
    VOLUME_EFEITOS_RECT,
    VOLUME_MUSICA_RECT,
    desenhar_jogo,
    desenhar_menu,
)
from mecanicas import ALTURA, FPS, LARGURA, Jogo


def tocar_musica(nome_arquivo, volume):
    caminho = Path(__file__).resolve().parent / "assets" / nome_arquivo
    pygame.mixer.music.load(caminho)
    pygame.mixer.music.set_volume(volume)
    pygame.mixer.music.play(-1)


def botao_clicado(retangulo, posicao, som_botao):
    if not retangulo.collidepoint(posicao):
        return False
    som_botao.play()
    return True


def main():
    pygame.init()
    pygame.mixer.init()
    som_tiro = pygame.mixer.Sound(
        Path(__file__).resolve().parent / "assets" / "som_tiro.mp3"
    )
    som_recarga = pygame.mixer.Sound(
        Path(__file__).resolve().parent / "assets" / "som_recarga.mp3"
    )
    som_botao = pygame.mixer.Sound(
        Path(__file__).resolve().parent / "assets" / "som_botao.mp3"
    )
    som_sem_municao = pygame.mixer.Sound(
        Path(__file__).resolve().parent / "assets" / "som_sem_municao.mp3"
    )
    volume_musica = 0.7
    volume_efeitos = 0.8
    som_tiro.set_volume(volume_efeitos)
    som_recarga.set_volume(volume_efeitos)
    som_botao.set_volume(volume_efeitos)
    som_sem_municao.set_volume(volume_efeitos)
    tocar_musica("musica_menu.mp3", volume_musica)
    tela = pygame.display.set_mode(
        (LARGURA, ALTURA),
        pygame.FULLSCREEN | pygame.SCALED,
    )
    pygame.display.set_caption("NightHunter")
    relogio = pygame.time.Clock()
    fonte = pygame.font.SysFont("arial", 26, bold=True)
    fonte_grande = pygame.font.SysFont("arial", 56, bold=True)
    fonte_hud = pygame.font.SysFont("Chiller", 34, bold=True)
    fonte_menu_titulo = pygame.font.SysFont("Chiller", 64, bold=True)
    fonte_menu_botao = pygame.font.SysFont("Georgia", 28, bold=True)
    fonte_fim_titulo = pygame.font.SysFont("Chiller", 58, bold=True)
    fonte_tutorial = pygame.font.SysFont("arial", 20)
    jogo = Jogo()
    musica_parada = False
    estado_tela = "menu"
    controle_volume_ativo = None

    def ajustar_volume(controle, posicao_x):
        nonlocal volume_musica, volume_efeitos
        area_controle = (
            VOLUME_MUSICA_RECT
            if controle == "musica"
            else VOLUME_EFEITOS_RECT
        )
        inicio = area_controle.x + 18
        fim = area_controle.right - 18
        volume = max(0.0, min(1.0, (posicao_x - inicio) / (fim - inicio)))
        if controle == "musica":
            volume_musica = volume
            pygame.mixer.music.set_volume(volume_musica)
        else:
            volume_efeitos = volume
            som_tiro.set_volume(volume_efeitos)
            som_recarga.set_volume(volume_efeitos)
            som_botao.set_volume(volume_efeitos)
            som_sem_municao.set_volume(volume_efeitos)

    while True:
        dt = relogio.tick(FPS) / 1000.0

        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if ev.type == pygame.KEYDOWN and ev.key == pygame.K_ESCAPE:
                if estado_tela in ("configuracoes", "tutorial"):
                    estado_tela = "menu"
                else:
                    pygame.quit()
                    sys.exit()

            if ev.type == pygame.MOUSEBUTTONDOWN and ev.button == 1:
                if estado_tela == "menu":
                    if botao_clicado(MENU_JOGAR_RECT, ev.pos, som_botao):
                        jogo.reiniciar()
                        estado_tela = "jogo"
                        tocar_musica("musica_fundo.mp3", volume_musica)
                    elif botao_clicado(MENU_CONFIGURACOES_RECT, ev.pos, som_botao):
                        estado_tela = "configuracoes"
                    elif botao_clicado(MENU_TUTORIAL_RECT, ev.pos, som_botao):
                        estado_tela = "tutorial"
                elif estado_tela in ("configuracoes", "tutorial"):
                    if botao_clicado(MENU_VOLTAR_RECT, ev.pos, som_botao):
                        estado_tela = "menu"
                    elif estado_tela == "configuracoes":
                        if VOLUME_MUSICA_RECT.collidepoint(ev.pos):
                            controle_volume_ativo = "musica"
                            ajustar_volume(controle_volume_ativo, ev.pos[0])
                        elif VOLUME_EFEITOS_RECT.collidepoint(ev.pos):
                            controle_volume_ativo = "efeitos"
                            ajustar_volume(controle_volume_ativo, ev.pos[0])
                elif estado_tela == "jogo":
                    if jogo.game_over:
                        if botao_clicado(GAME_OVER_MENU_RECT, ev.pos, som_botao):
                            estado_tela = "menu"
                            tocar_musica("musica_menu.mp3", volume_musica)
                            musica_parada = False
                        elif botao_clicado(
                            GAME_OVER_RETRY_RECT,
                            ev.pos,
                            som_botao,
                        ):
                            jogo.reiniciar()
                            musica_parada = False
                            tocar_musica("musica_fundo.mp3", volume_musica)
                    else:
                        if jogo.municao == 0:
                            som_sem_municao.play()
                        else:
                            municao_antes = jogo.municao
                            jogo.clicar(ev.pos)
                            if jogo.municao < municao_antes:
                                som_tiro.play()

            if ev.type == pygame.MOUSEBUTTONUP and ev.button == 1:
                controle_volume_ativo = None

            if ev.type == pygame.MOUSEMOTION and controle_volume_ativo:
                ajustar_volume(controle_volume_ativo, ev.pos[0])

        if estado_tela == "jogo":
            municao_antes = jogo.municao
            jogo.atualizar(dt)
            balas_carregadas = jogo.municao - municao_antes
            for _ in range(balas_carregadas):
                som_recarga.play()
            if jogo.game_over and not musica_parada:
                pygame.mixer.music.stop()
                musica_parada = True
            elif not jogo.game_over and musica_parada:
                pygame.mixer.music.play(-1)
                musica_parada = False
            desenhar_jogo(
                tela,
                fonte,
                fonte_grande,
                jogo,
                fonte_hud,
                fonte_fim_titulo,
            )
        else:
            desenhar_menu(
                tela,
                fonte,
                fonte_menu_titulo,
                fonte_menu_botao,
                estado_tela,
                pygame.mouse.get_pos(),
                volume_musica,
                volume_efeitos,
                fonte_tutorial,
            )
        pygame.display.flip()


if __name__ == "__main__":
    main()
