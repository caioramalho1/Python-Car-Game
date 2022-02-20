import pygame

'''
Aqui eu vou fazer algumas funções de utilidade
'''
def scale_image(img,factor):
    """
    Vai ser uma funcao que basicamente irá realizar as mudanças de escalas das imagens, ela recebe uma imagem como param
    e um fator, esse fator será a escala que eu quero alterar a minha imagem. Ex: 2x ou 0.5x, ira dobrar a escala, ou di
    minuila pela metade, respectivamente.
    """
    size = round(img.get_width() * factor), round(img.get_height() * factor ) #estou fazendo o round(Arredondamento) porque eu preciso de int para definir os
    #pixels das imagens, não decimais.

    return pygame.transform.scale(img, size)
    #irá me retornar a imagem transformada baseada no fator que eu enviar no param da funcao

#Agora eu vou precisar de alguma maneira de desenhar a minha imagem apos rotacionar a minha imagem;
def blit_rotate_center(win, image, top_Left, angle):
    """
    O objetivo da funcao é rotacionar a imagem.
    Não é tão facil conseguir rotacionar uma imagem, as imagens na realidade, são retangulos, então se tentar rotacionalas
    normalmente, irão existir muitas distorcoes. Toda imagem no Pygame é um retangulo.  Logo, quando rotaciono a imagem, eu
    rotaciono o retangulo. 
    """
    #essa variavel esta guardando a imagem rotacionada, ela esta baseado no canto superior esquerdo. Ainda não 
    #é esse o objetivo. O objetivo é relacionar baseado no centro da imagem, o segundo código e para eu conseguir mudar 
    #o ponto de mudança para o centro do meu retangulo.
    rotated_image = pygame.transform.rotate(image, angle)
    
    #conseguir mudar  o ponto de mudança para o centro do meu retangulo.
    #Eu primeiro rotacionei a imagem, e a minha imagem foi rotacionada alterando a sua posicao (X,Y) Porém, essa alteracao
    # de posicao do eixo x e eixo y estao baseadas no canto superior esquerdo do retangulo
    # Então agora eu vou criar o meu novo retangulo que vai receber o meu retangulo rotacionado e vai alterar o ponto de
    # referencia desse angulo rotacionado, que antes estava no canto superior esquerdo, para o centro.
    new_rect = rotated_image.get_rect(center=image.get_rect(topleft= top_Left).center)
    #o meu novo retangulo pega o meu retangulo rotacionado, mas faz o centro desse retangulo rotacionado, ser igual
    #ao centro do retangulo da imagem original
    win.blit(rotated_image, new_rect.topleft)
    
def blit_text_center(win, font, text):
    render = font.render(text, 1, (200, 200, 200)) #texto que eu quero renderizar, o antiallising que vai ser sempre 1, e a cor 
    win.blit(render, (win.get_width()/2 - render.get_width() / 2, win.get_height() / 2 - render.get_height() / 2))