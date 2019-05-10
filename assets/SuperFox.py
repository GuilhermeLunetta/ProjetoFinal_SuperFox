#Bibliotecas e importações
import pygame
from os import path

#Diretorio das imagens
img_dir = path.join(path.dirname(__file__), 'img')

#Dados gerais do jogo
WIDTH = 800
HEIGHT = 500
FPS = 60

#Cores
BLACK = (0, 0, 0)

#Gravidade
gravidade = -0.5


#Classe jogador que representa a raposa
class Player(pygame.sprite.Sprite):
    
    #Construtor da classe
    def __init__(self, player_img):
        
        #Construtor da classe pai
        pygame.sprite.Sprite.__init__(self)
        
        #Imagem do player
        self.image = player_img
        
        #Diminuindo o tamanho da imagem
        self.image = pygame.transform.scale(player_img, (70, 58))
        
        #Deixando transparente
        self.image.set_colorkey(BLACK)
        
        #Detalhes sobre posicionamento
        self.rect = self.image.get_rect()
        
        #Posicao
        self.rect.x = 20
        self.rect.bottom = HEIGHT - 80
        
        #Velocidade
        self.speedx = 0
        self.speedy = 0
    
    def update(self):
        self.rect.x += self.speedx
        player.jump()
        
        #Mantém dentro da tela
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.left < 0:
            self.rect.left = 0

        if self.rect.bottom > HEIGHT - 80:
            self.rect.bottom = HEIGHT -80
            self.speedy = 0
        if self.rect.top < 0:
            self.rect.top = 0
            
    #Classe de pulo
    def jump(self):
        self.speedy -= gravidade
        self.rect.y += self.speedy

class Pipes(pygame.sprite.Sprite):
    
    def __init__(self, pipe_img):
        
        pygame.sprite.Sprite.__init__(self)
        
        #imagem
        self.image = pipe_img
        
        self.image = pygame.transform.scale(pipe_img, (50, 80))
        
        self.image.set_colorkey(BLACK)
        
        self.rect = self.image.get_rect()
        
        self.rect.x = 720
        self.rect.y = HEIGHT - 160

class BlocoTijolo(pygame.sprite.Sprite):
    
    def __init__(self, x, y):
        
        pygame.sprite.Sprite.__init__(self)
        
        #Imagem
        brick_img = assets['bloco_tijolo']
        self.image = brick_img
        
        #Diminuindo a imagem
        self.image = pygame.transform.scale(brick_img, (40, 40))
        
        #Imagem transparente
        self.image.set_colorkey(BLACK)
        
        #Posicionamento
        self.rect = self.image.get_rect()
        
        #posicao
        self.rect.x = x
        self.rect.y = y
        
listaPosicaoBlocos=[(100, 250), (140, 250), (180, 250),(260, 250),(220, 110),(260, 110),(340, 110),(380, 110),(380, 250),(420, 250),(460, 250),(500, 250),(540, 250)]

class BlocoAmarelo(pygame.sprite.Sprite):
    
    def __init__(self, x, y):
        
        pygame.sprite.Sprite.__init__(self)
        
        #imagem
        blocoItem_img = assets['bloco_item']
        self.image = blocoItem_img
        
        self.image = pygame.transform.scale(blocoItem_img, (40, 40))
        
        self.image.set_colorkey(BLACK)
        
        self.rect = self.image.get_rect()
        
        #posicao
        self.rect.x = x
        self.rect.y = y
        
listaPosicaoBlocosAmarelos=[(220, 250),(300, 110)]

#função assets (imagens e sons)
def load_assets(img_dir):
    assets = {}
    assets['player_img'] = pygame.image.load(path.join(img_dir, 'fox_static.png')).convert()
    assets['bloco_tijolo'] = pygame.image.load(path.join(img_dir, 'bloco_tijolo.png')).convert()
    assets['bloco_item'] = pygame.image.load(path.join(img_dir, 'bloco_item.png')).convert()
    assets['background'] = pygame.image.load(path.join(img_dir, 'bg_fase1.png')).convert()
    fox_walk = []
    for i in range(1, 3, 1):
        filename = 'fox_walk{}.png'.format(i)
        walk = pygame.image.load(path.join(img_dir, filename)).convert()
        walk = pygame.transform.scale(walk, (70, 58))
        walk.set_colorkey(BLACK)
        fox_walk.append(walk)
    assets['fox_walk'] = fox_walk
    assets['pipe_img'] = pygame.image.load(path.join(img_dir, 'pipes_fase1.png')).convert()
    return assets

#Inicializacao do pygame
pygame.init()
pygame.mixer.init()

#Tamanho da tela
screen = pygame.display.set_mode((WIDTH, HEIGHT))

#Nome do jogo
pygame.display.set_caption("SuperFox by TeamAura")

#Ajuste de velocidade
clock = pygame.time.Clock()

#carrega todos os assets e guarda em um dicionario
assets = load_assets(img_dir)
    
#Carrega o fundo do jogo
background = assets['background']
background = pygame.transform.scale(background, (800, 500))
background_rect = background.get_rect()

#Carrega os sons do jogo

#Cria um player
player = Player(assets['player_img'])

#Cria coisas
pipe = Pipes(assets['pipe_img'])

#Grupos Geral
blocos = pygame.sprite.Group()
pipes = pygame.sprite.Group()

#Grupo sprites
all_sprites = pygame.sprite.Group()
all_sprites.add(player)
all_sprites.add(pipe)

#Cria blocos
for x in range(0, len(listaPosicaoBlocos), 1):
    bloco=BlocoTijolo(listaPosicaoBlocos[x][0], listaPosicaoBlocos[x][1])
    all_sprites.add(bloco)
    blocos.add(bloco)

#Cria blocos amarelos(itens)
for x in range(0, len(listaPosicaoBlocosAmarelos), 1):
    blocoItem=BlocoAmarelo(listaPosicaoBlocosAmarelos[x][0], listaPosicaoBlocosAmarelos[x][1])
    all_sprites.add(blocoItem)
    blocos.add(blocoItem)

#comando para evitar travamentos
try:
    
    #Loop principal
    running = True
    
    while running:
        
        #Ajusta o tick do jogo
        clock.tick(FPS)
        
        #Eventos pygame
        for event in pygame.event.get():
            
            #verifica se foi fechado
            if event.type == pygame.QUIT:
                running = False
                
            #verifica se apertou alguma tecla
            elif event.type == pygame.KEYDOWN:
                #se apertou alguma tecla muda a velocidade
                if event.key == pygame.K_LEFT:
                    player.speedx -= 4
                    
                if event.key == pygame.K_RIGHT:
                    player.speedx += 4
                #Jump
                if event.key == pygame.K_SPACE:
                    player.speedy -= 10
                    
            #verifica se soltou alguma tecla
            elif event.type == pygame.KEYUP:
                #se soltou muda a velocidade
                if event.key == pygame.K_LEFT:
                    player.speedx += 4
                if event.key == pygame.K_RIGHT:
                    player.speedx -= 4
                
        #Atualiza os sprites
        all_sprites.update()
        
        #A cada loop redesenha o fundo e os sprites
        screen.fill(BLACK)
        screen.blit(background, background_rect)
        all_sprites.draw(screen)
        
        #Depois de desenhar tudo inverte o display
        pygame.display.flip()
finally:
    pygame.quit()
        
        
        
        
        