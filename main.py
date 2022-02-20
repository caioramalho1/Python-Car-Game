
import pygame
import time
import math
from utilit import scale_image, blit_rotate_center, blit_text_center
pygame.font.init()

GRASS = scale_image(pygame.image.load("imgs/grass.jpg"), 2.5)
TRACK = scale_image(pygame.image.load("imgs/track.png"), 1)


TRACK_BORDER = scale_image(pygame.image.load("imgs/track-border.png"), 1)
TRACK_BORDER_MASK = pygame.mask.from_surface(TRACK_BORDER)

FINISH = pygame.image.load("imgs/finish.png")
FINISH_POSITION = (104, 210)
FINISH_MASK = pygame.mask.from_surface(FINISH)

PURPLE_CAR = scale_image(pygame.image.load("imgs/purple-car.png"), 0.45)
WHITE_CAR = scale_image(pygame.image.load("imgs/white-car.png"), 0.45)

#CRIANDO A MINHA TELA DO PYGAME, EU ENVIO UMA TUPLA COM A ALTURA E LARGURA, NO CASO EU IREI QUERER
#UMA QUE SEJA DO TAMANHO DA MINHA IMAGME DA CORRIDA
WIDTH, HEIGHT = TRACK.get_width(), TRACK.get_height()
WIN = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE) #checar isso em casa
#qUANDO Eu converto as imagens para uma constante no Python, elas se tornam uma superficie, e eu posso pegar o 
#tamanhos da superficie com get_width() e get_height
PATH = [(131, 74), (32, 134), (56, 418), (257, 619), (350, 588), (367, 442), (484, 427), (525, 602), (636, 590), 
(632, 343), (396, 325), (352, 248), (591, 223), (644, 162), (580, 77), (266, 69), (240, 330), (141, 312), (152, 213)]

MAIN_FONT = pygame.font.SysFont("comicsans", 20)

pygame.display.set_caption("Racing Game!") #nome da minha janela do Pygame

FPS = 60

class GameInfo:
    LEVELS = 10
    def __init__(self, level=1) -> None:
        self.level = level
        self.started = False
        self.level_time_start = 0

    def next_level(self):
        self.level += 1
        self.started = False

    def reset(self):
        self.level = 1
        self.started = False
        self.level_time_start = 0
        self.current_position = 0


    def game_over(self):
        if self.level > self.LEVELS:
            return True


    def start_level(self):
        self.started = True
        self.level_time_start = time.time()

    def get_level_time(self):
        if not self.started:
            return 0
        
        return round(time.time() - self.level_time_start, 1)

#Após carregar as minhas imagens para utiliza-las, agora eu quero mostra-las na tela
#O meu loop no pygame vai ser uma constante onde ira acontecer todos os meus eventos, que são, movimentos, colisões, alterações
#de angulação, e assim por diante... Isso vai fazer a minha tela ficar "viva", e assim que eu acabar com esse loop, o jogo acaba
#FPS = 60 #setando essa variavel para definir a velocidade de processamento do meu programa, porque em outro caso, faria 
#com que o jogo rodasse mais rapido para processadores mais potentes;

def draw(win, images, player_car, computer_car, game_info):
    """
    Essa funcao sera criada para poder realizar os desenhos, pro meu loop nao ficar muito grande e com muita informacao
    ela recebe a tela(win) e as imagens como paramatro. Dentro da funcao, eu vou fazer um loop(for) que irá iterar sobre
    uma lista que irá conter tuplas com as imagens e a posicao, e depois de iterar ele vai tirar dois valores, img e pos
    e vai usar a funcao blit nelas.
    """
    for img, pos in images:
        win.blit(img, pos) #metodo que eu uso quando quero mostrar imagens na tela(blit)
    
    level_text = MAIN_FONT.render(f"Level: {game_info.level}", 1, (255, 255, 255))
    win.blit(level_text,(10, HEIGHT - level_text.get_height() - 50))

    time_text = MAIN_FONT.render(f"Time: {game_info.get_level_time()}s", 1, (255, 255, 255))
    win.blit(time_text, (10, HEIGHT - level_text.get_height() - 30))

    vel_text = MAIN_FONT.render(f"VEl: {round(player_car.vel), 1}px/s", 1, (255, 255, 255))
    win.blit(vel_text, (10, HEIGHT - level_text.get_height() - 10))


    player_car.draw(win)
    computer_car.draw(win)

    pygame.display.update() #o metodo update precisa ser passado sempre para que oque eu quero que seja desenhado na
    #tela seja realmente desenhado
    

class AbstractCar:
    """
    Vai ser uma classe "abstrata", porque existem muitas coisas que são comuns aos carros, do player por exemplo, com
    o carro do computador. Então vou cria-la para definir os metodos padrões    
    """

    def __init__(self, max_vel, rotation_vel) -> None:
        self.img = self.IMG
        self.max_vel = max_vel
        self.vel = 0 #comeca com 0 porque quando o carro comeca ele esta parado
        self.rotation_vel = rotation_vel
        self.angle = 0 #o angulo começa em 0 e quando eu rotacionar o meu carro eu rotaciono com o angulo
        self.x, self.y = self.START_POS
        self.acceleration = 0.1 # Sempre que eu apertar na tecla que sera a minha aceleraçao (W) eu vou incrementar a velocidade do carro em 0.1 com esse atributo que eu vou usar no futuro

    def rotate(self, left=False, right=False):
        """
        Caso queira andar para a esquerda basta enviar, left = True e para direita, right = True
        """
        if left:
            self.angle += self.rotation_vel #quando estou indo para a esquera o meu angulo esta diminuindo
        elif right:
            self.angle -= self.rotation_vel #quando esta indo para a direita o meu angulo esta aumentando

    def draw(self, win):
        blit_rotate_center(win, self.img, (self.x, self.y), self.angle)

    def collide(self, mask, x=0, y=0):
        car_mask = pygame.mask.from_surface(self.img)
        offset = (int(self.x - x ), int(self.y - y))
        poi = mask.overlap(car_mask, offset)
        return poi

    def move_foward(self):
        """
        Essa funcao vai aumentar a velocidade do meu carro baseado na aceleracao que eu setei, e a aceleracao só é
        incrementada até o meu max_vel. Não vai fazer nada quando chegar neste limite, somente vai aumentar a velocidade
        """
        self.vel = min(self.vel + self.acceleration, self.max_vel)
        #Se self.vel já esta no maximo, e eu adicionar mais aceleracao, eu não quero ultrapassar o valor self.max_vel
        # Então o que o código diz, se self.vel + self.acceleration for maior que self.max_vel, eu seto a minha velocidade
        #(variavel) para o valor máximo
        self.move()

    def move_backward(self):
        """Metodo para fazer o meu carro se mover para trás"""

        self.vel = max(self.vel - self.acceleration, -self.max_vel/2) #eu quero que a minha maior velocidade negativa seja a metade da velocidade do meu carro
        self.move()

    def move(self):
    #Eu ainda preciso calcular para qual direçao eu vou mover o meu carro, porque se ele esta virado (angulado) para direita
    #ele tem que se mover para direita, certo ?
#        self.x += self.vel #eu vou mover para a direita baseado na minha velocidade OBS. Movimentaçao para 1D
        radians = math.radians(self.angle)
        vertical = math.cos(radians) * self.vel
        horizontal = math.sin(radians) * self.vel

        self.y -= vertical #estou diminuindo porque o calculo vai me dar um valor negativo, assim nos dois casos
        self.x -= horizontal
    
    def reset(self):
        self.x, self.y = self.START_POS
        self.angle = 0 
        self.vel = 0
        


class PlayerCar(AbstractCar):
    IMG = PURPLE_CAR
    START_POS = (130, 150) #140, 150
    
    def reduce_speed(self):
        self.vel = max(self.vel - self.acceleration/2, 0)
        self.move()
    
    def bounce(self):
        self.vel = -self.vel * 0.8
        self.move()

class ComputerCar(AbstractCar):
    IMG = WHITE_CAR
    START_POS = (160, 150)
    def __init__(self, max_vel, rotation_vel, path=[]) -> None:
        super().__init__(max_vel, rotation_vel)
        self.path = path
        self.current_point = 0
        self.vel = max_vel
    
    def draw_points (self, win):
        for point in self.path:
            pygame.draw.circle(win,(255, 0, 0), point, 5)     
    
    def draw(self, win): #estou sobrepondo o metodo draw que esta sendo herdado da abstractcar
        super().draw(win)
#        self.draw_points(win)

    def calculate_angle(self):
        target_x, target_y = self.path[self.current_point]
        x_diff = target_x - self.x
        y_diff = target_y - self.y

        if y_diff == 0:
            desired_radian_angle = math.pi/2 #90 graus
        else: 
            desired_radian_angle = math.atan(x_diff/y_diff)
    
        if target_y > self.y:
            desired_radian_angle += math.pi

        difference_in_angle = self.angle - math.degrees(desired_radian_angle)
        if difference_in_angle >= 180:
            difference_in_angle -= 360

        if difference_in_angle > 0:
            self.angle -= min(self.rotation_vel, abs(difference_in_angle))
        else:
            self.angle += min(self.rotation_vel, abs(difference_in_angle))

    def update_path_point(self):
        target = self.path[self.current_point]
        rect = pygame.Rect(self.x, self.y, self.img.get_width(), self.img.get_height())
        if rect.collidepoint(*target):
            self.current_point += 1 

    def next_level(self, level):
        self.reset()
        self.vel = self.max_vel + (level - 1 ) * 0.1 #isso vai fazer a minha velocidade nucna ser maior do que a velocidade do player
        self.current_point = 0 #vai fazer o meu proximo ponto voltar para o 0 da minha lista de cordenadas
    
    def move(self):

        if self.current_point >= len(self.path):
            return

        self.calculate_angle() #ainda vou escrever mas essa funcao vai calcular o angulo e mover o carro para a direção deste angulo
        self.update_path_point()
        super().move()

def move_player(player_car):
    

    """Vou criar essa funcao para segurar todos  comandos de movimento do player. para que eles não fiquem
        todos dentro do meu loop principal do jogo, para ficar mais facil a vizualização dele
    """
    #vou implementar a ferramenta de realizar acoes quando eu pressiono uma tecla. isso é um evento, então todoo
    #evento que eu posso ter dentro do jogo acontece aqui, eventos de colisao, movimentacao, etc...
    keys = pygame.key.get_pressed()#metodo chamado para verificar se alguma tecla esta sendo apertada
    moved = False
    
    if keys[pygame.K_a]: #estou definindo que a minha tecla sera a letra "a"; e ao mesmo tempo verificando se ela é True, ou seja, #ela sera vertadeira quando eu apertar, ela vem como falsa no default.
        player_car.rotate(left=True)
    if keys[pygame.K_d]:
        player_car.rotate(right=True)
    if keys[pygame.K_w]:
        moved = True
        player_car.move_foward()
    if keys[pygame.K_s]:
        moved = True
        player_car.move_backward()

    if not moved:
        player_car.reduce_speed()

def handle_collision(player_car, computer_car, game_info):
    
    if player_car.collide(TRACK_BORDER_MASK) != None:
        player_car.bounce()
    
    
    computer_finish_pio_collide = computer_car.collide(FINISH_MASK, *FINISH_POSITION)
    if computer_finish_pio_collide != None:
        blit_text_center(WIN, MAIN_FONT, "You LOSE!")
        pygame.display.update()
        pygame.time.wait(4000)
        game_info.reset()
        player_car.reset()
        computer_car.reset()
        pygame.quit()
        
        print("Computer wins!")    
    
    
    player_finish_pio_collide = player_car.collide(FINISH_MASK, *FINISH_POSITION)
    if player_finish_pio_collide != None:
        if player_finish_pio_collide[1] == 0:
            player_car.bounce()
        else:
            game_info.next_level()
            player_car.reset()
            computer_car.next_level(game_info.level)
            print("player wins!")
run = True
clock = pygame.time.Clock()
images = [(GRASS, (0,0)), (TRACK, (0,0)), (FINISH,(FINISH_POSITION)), (TRACK_BORDER, (0,0))]
player_car = PlayerCar(3.0 , 3)
computer_car = ComputerCar(2.5, 2.5, PATH)
game_info = GameInfo()

while run:
    clock.tick(FPS)#ESSE WHILE LOOP NAO PODE RODAR A MAIS DE 60 FRAMES POR SEGUNDO
    
    try:
        draw(WIN, images, player_car, computer_car, game_info)
        
        while not game_info.started:
            blit_text_center(WIN, MAIN_FONT,f"Press any key to start level {game_info.level}!")
            pygame.display.update()
            for event in pygame.event.get():        
                if event.type == pygame.QUIT:
                    pygame.quit()
                    break
            
            if event.type == pygame.KEYDOWN:
                game_info.start_level()

        for event in pygame.event.get(): #isso vai me dar uma lista de todos os eventos e eu posso iterar sobre ela
            #O primeiro evento a ser checado é se o usuario fechou a janela do pygame, se ele precionou o X   
            if event.type == pygame.QUIT:
                run = False
                break
    except pygame.error as error:
        print("fim")
    
    move_player(player_car)
    computer_car.move()
    handle_collision(player_car, computer_car, game_info)

    if game_info.game_over():       
        blit_text_center(WIN, MAIN_FONT, "YOU WON THE GAME")
        pygame.time.wait(4000)
        game_info.reset()    
        player_car.reset()
        computer_car.reset()


pygame.quit()

