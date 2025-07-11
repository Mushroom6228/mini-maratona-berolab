<<<<<<< HEAD
import pygame # Importa a biblioteca Pygame, essencial para o desenvolvimento de jogos.
import os # Importa o módulo os para interagir com o sistema operacional (caminhos de arquivo).
# Importa constantes como largura/altura da tela, cores, som de ponto e FPS.
from dino_runner.utils.constants import SCREEN_WIDTH, SCREEN_HEIGHT, BLACK, WHITE, POINT_SOUND, FPS
# Importa a função para gerenciar caminhos de recursos.
from dino_runner.utils.resource_manager import resource_path

class Score:
    def __init__(self):
        self.points = 0 # Pontuação exibida para o jogador (valor inteiro).
        self.float_points = 0.0 # Pontuação real em ponto flutuante para um incremento mais suave.
        # Define o caminho para o arquivo da fonte usando resource_path.
        font_path = resource_path('dino_runner/assets/Font/joystix monospace.otf')
        try:
            self.font = pygame.font.Font(font_path, 20) # Tenta carregar a fonte personalizada com tamanho 20.
        except FileNotFoundError: # Se o arquivo da fonte não for encontrado.
            self.font = pygame.font.Font(None, 20) # Usa a fonte padrão do Pygame como fallback.
        except pygame.error: # Se ocorrer um erro específico do Pygame ao carregar a fonte.
            self.font = pygame.font.Font(None, 20) # Usa a fonte padrão do Pygame como fallback.
        self.color_day = BLACK # Define a cor da pontuação para o dia (preto).
        self.color_night = WHITE # Define a cor da pontuação para a noite (branco).
        self.last_point_sound_played_at_multiple = 0 # Controla quando o som de 100 pontos foi tocado pela última vez.
        self.blink_active = False # Flag para indicar se a animação de piscar está ativa.
        self.blink_timer = 0 # Temporizador para controlar a duração total do piscar.
        self.current_alpha = 255 # Valor de opacidade atual da pontuação (0 = transparente, 255 = opaco).
        self.blink_duration = 1000 # Duração total da animação de piscar em milissegundos (1 segundo).
        self.blink_interval = 100 # Intervalo de tempo em milissegundos para alternar a visibilidade durante o piscar.
        self.show_score_for_blink = True # Flag que controla a visibilidade da pontuação durante a animação de piscar.
        self.points_per_second = 100 / 10 # Define quantos pontos são ganhos por segundo (100 pontos a cada 10 segundos = 10 pontos/segundo).
        self.points_per_frame = self.points_per_second / FPS # Calcula quantos pontos são adicionados a cada quadro do jogo.
        # Define o caminho para o arquivo de som da pontuação.
        score_sound_path = resource_path('dino_runner/assets/Other/score.wav')
        if os.path.exists(score_sound_path): # Verifica se o arquivo de som da pontuação existe.
            self.score_sound = pygame.mixer.Sound(score_sound_path) # Carrega o som da pontuação.
            self.score_sound.set_volume(0.7) # Define o volume do som da pontuação para 70%.
        else:
            self.score_sound = None # Se o arquivo não existir, define o som como None.

    def update(self, is_night=False): # Método para atualizar a pontuação a cada quadro.
        current_time = pygame.time.get_ticks() # Obtém o tempo atual em milissegundos.
        self.float_points += self.points_per_frame # Incrementa a pontuação em ponto flutuante suavemente.
        new_integer_points = int(self.float_points) # Converte a pontuação para um inteiro para exibição.
        if new_integer_points > self.points: # Se a pontuação inteira mudou (aumentou).
            old_points_multiple = (self.points // 100) * 100 # Calcula o último múltiplo de 100 da pontuação.
            self.points = new_integer_points # Atualiza a pontuação exibida.
            current_points_multiple = (self.points // 100) * 100 # Calcula o múltiplo de 100 atual da pontuação.
            # Verifica se a pontuação cruzou um novo múltiplo de 100 e não é zero.
            if current_points_multiple > old_points_multiple and current_points_multiple > 0:
                if self.score_sound: # Se o som da pontuação estiver carregado.
                    self.score_sound.play() # Toca o som.
                self.blink_active = True # Ativa a animação de piscar.
                self.blink_timer = current_time # Inicia o temporizador do piscar.
                self.show_score_for_blink = False # Esconde a pontuação para iniciar o piscar.
                self.last_point_sound_played_at_multiple = current_time # Reinicia o temporizador para o intervalo de piscar.
        # Lógica para a animação de piscar.
        if self.blink_active:
            elapsed_time = current_time - self.blink_timer # Calcula o tempo decorrido desde o início do piscar.
            if elapsed_time > self.blink_duration: # Se a duração total do piscar terminou.
                self.blink_active = False # Desativa a animação de piscar.
                self.show_score_for_blink = True # Garante que a pontuação esteja visível após o piscar.
                self.current_alpha = 255 # Restaura a opacidade total.
            # Se o tempo decorrido desde a última alternância de visibilidade for maior que o intervalo de piscar.
            elif current_time - self.last_point_sound_played_at_multiple > self.blink_interval:
                self.show_score_for_blink = not self.show_score_for_blink # Alterna a visibilidade da pontuação.
                self.last_point_sound_played_at_multiple = current_time # Atualiza o tempo da última alternância.
        else:
            self.show_score_for_blink = True # Garante que a pontuação esteja visível se não estiver piscando.
            self.current_alpha = 255 # Garante opacidade total.

    def draw(self, screen, is_night=False): # Método para desenhar a pontuação na tela.
        current_color = self.color_night if is_night else self.color_day # Define a cor da pontuação com base no ciclo dia/noite.
        if self.show_score_for_blink: # Só desenha a pontuação se ela deve estar visível.
            # Renderiza o texto da pontuação com a cor atual.
            text_surface = self.font.render(f'Score: {self.points}', True, current_color)
            self.text_rect = text_surface.get_rect() # Obtém o retângulo que envolve a superfície do texto.
            self.text_rect.x = SCREEN_WIDTH - 200 # Define a posição X do retângulo (mais à direita).
            self.text_rect.y = 38 # Define a posição Y do retângulo (um pouco para baixo).
            screen.blit(text_surface, self.text_rect) # Desenha a superfície do texto na tela na posição definida.

    def reset(self): # Método para resetar a pontuação para um novo jogo.
        self.points = 0 # Reseta a pontuação exibida para zero.
        self.float_points = 0.0 # Reseta a pontuação em ponto flutuante para zero.
        self.last_point_sound_played_at_multiple = 0 # Reseta o controle do som de 100 pontos.
        self.blink_active = False # Desativa a animação de piscar.
        self.current_alpha = 255 # Garante que a pontuação esteja totalmente visível.
        self.show_score_for_blink = True # Garante que a pontuação esteja visível.
=======
# dino_runner/components/score.py
import pygame
from dino_runner.utils.constants import SCREEN_WIDTH, SCREEN_HEIGHT, BLACK, WHITE, POINT_SOUND, FPS
from dino_runner.utils.resource_manager import resource_path # Import resource_path

class Score:
    def __init__(self):
        self.points = 0 # Pontuação exibida (inteiro)
        self.float_points = 0.0 # Pontuação real em ponto flutuante para suavidade
        
        # O caminho da fonte agora usa resource_path
        font_path = resource_path('dino_runner/assets/Font/joystix monospace.otf')
        
        # Tenta carregar a fonte. Se falhar, usa a fonte padrão do Pygame.
        try:
            self.font = pygame.font.Font(font_path, 20) # Font size adjusted to 20 (same as high score)
        except FileNotFoundError:
            print(f"Warning: Font '{font_path}' not found. Using Pygame's default font for score.")
            self.font = pygame.font.Font(None, 20) # Fallback to default font
        except pygame.error as e:
            print(f"Error loading font '{font_path}': {e}. Using Pygame's default font for score.")
            font = pygame.font.Font(None, 20) # Fallback to default font
            self.font = font # Assign fallback font
            
        self.color_day = BLACK # Black for day (imported from constants)
        self.color_night = WHITE # White for night (imported from constants)
        
        self.last_point_sound_played_at_multiple = 0 # Para controlar o som de 100 pontos

        # Atributos para o efeito de piscar
        self.blink_active = False
        self.blink_timer = 0
        self.current_alpha = 255 # Começa totalmente opaco
        self.blink_duration = 1000 # Duração total do piscar (ms) - ALTERADO para 1 segundo
        self.blink_interval = 100 # Intervalo de piscar (ms) - 100ms para piscar várias vezes
        self.show_score_for_blink = True # Controla a visibilidade durante o piscar

        # Configuração da velocidade de crescimento: 100 pontos a cada 10 segundos
        self.points_per_second = 100 / 10 # 10 pontos por segundo
        self.points_per_frame = self.points_per_second / FPS # Pontos a serem adicionados a cada frame

    def update(self, is_night=False): # Removido game_speed, pois a pontuação é baseada em tempo
        current_time = pygame.time.get_ticks()

        # Incrementa os pontos em ponto flutuante suavemente
        self.float_points += self.points_per_frame
        
        # Converte para inteiro para exibição, mas só atualiza se o valor inteiro mudou
        new_integer_points = int(self.float_points)
        if new_integer_points > self.points:
            old_points_multiple = (self.points // 100) * 100 # Múltiplo de 100 anterior
            self.points = new_integer_points # Atualiza a pontuação exibida
            
            # Lógica para tocar o som e iniciar o piscar a cada 100 pontos
            current_points_multiple = (self.points // 100) * 100 # Múltiplo de 100 atual
            if current_points_multiple > old_points_multiple and current_points_multiple > 0:
                if POINT_SOUND:
                    POINT_SOUND.play()
                self.blink_active = True
                self.blink_timer = current_time
                self.show_score_for_blink = False # Começa o piscar escondendo a pontuação
                self.last_point_sound_played_at_multiple = current_time # Reinicia o timer para o piscar

        # Lógica do piscar
        if self.blink_active:
            elapsed_time = current_time - self.blink_timer
            if elapsed_time > self.blink_duration:
                self.blink_active = False
                self.show_score_for_blink = True # Garante que esteja visível após o piscar
                self.current_alpha = 255 # Volta para totalmente opaco
            elif current_time - self.last_point_sound_played_at_multiple > self.blink_interval: # Reutilizando last_point_sound_played_at_multiple para o intervalo de piscar
                self.show_score_for_blink = not self.show_score_for_blink # Alterna visibilidade
                self.last_point_sound_played_at_multiple = current_time # Atualiza o último tempo de piscar
        else:
            self.show_score_for_blink = True # Garante que esteja visível se não estiver piscando
            self.current_alpha = 255 # Garante opacidade total

    def draw(self, screen, is_night=False):
        current_color = self.color_night if is_night else self.color_day
        
        if self.show_score_for_blink: # Só desenha se deve estar visível
            # Renderiza o texto com a cor atual
            text_surface = self.font.render(f'Score: {self.points}', True, current_color)
            
            # Aplica a opacidade se estiver piscando, caso contrário, mantém totalmente opaco
            # Nota: current_alpha é usado para o efeito de fade-in/fade-out se você quisesse.
            # Para piscar on/off, show_score_for_blink é mais direto.
            # Se quiser um fade, precisaria ajustar current_alpha com base no tempo dentro de cada ciclo de blink_interval.
            # Por enquanto, usaremos apenas show_score_for_blink para on/off.
            
            self.text_rect = text_surface.get_rect()
            # Ajusta a posição para ficar bem mais à direita e um pouco para baixo
            self.text_rect.x = SCREEN_WIDTH - 200 # Posição X
            self.text_rect.y = 38 # Posição Y
            screen.blit(text_surface, self.text_rect)

    def reset(self):
        self.points = 0
        self.float_points = 0.0 # Reseta também os pontos em ponto flutuante
        self.last_point_sound_played_at_multiple = 0 # Reset 100-point sound control
        self.blink_active = False
        self.current_alpha = 255 # Garante que a pontuação esteja visível ao resetar
        self.show_score_for_blink = True # Garante que a pontuação esteja visível ao resetar
>>>>>>> be73f1d8742b9414b87a1ef857da4e48644b5e82
