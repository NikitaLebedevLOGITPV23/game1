import pygame, sys, random 
pygame.init()

pygame.init()
screen = pygame.display.set_mode((576,1024))
clock = pygame.time.Clock()
game_font =pygame.font.SysFont(None, 55)

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

gravity=0.5
bird_movement=0
game_active=True
score=0
high_score=0

background_image=pygame.image.load("background.png").convert()
floor_image=pygame.image.load("base.png").convert()
floor_x_pos=0
pipe_image=pygame.image.load("pipe.png")
pipe_list=[]
bird_down=pygame.image.load("bluebirdDown.png").convert_alpha()
bird_mid=pygame.image.load("bluebirdMid.png").convert_alpha()
bird_up=pygame.image.load("bluebirdUp.png").convert_alpha()
bird_frames=[bird_down,bird_mid,bird_up]
bird_index = 0
bird_surface=bird_frames[bird_index]
bird_rect=bird_surface.get_rect(center = (100,512))
BIRDFLAP=pygame.USEREVENT + 1
pygame.time.set_timer(BIRDFLAP,200)

SpawnPipe=pygame.USEREVENT
pygame.time.set_timer(SpawnPipe,1200)
pipe_height=[400,600,800]


def draw_floor():
	screen.blit(floor_image,(floor_x_pos,900))
	screen.blit(floor_image,(floor_x_pos + 576,900))

def create_pipe():
	random_pipe_pos=random.choice(pipe_height)
	bottom_pipe=pipe_image.get_rect(midtop=(700,random_pipe_pos))
	top_pipe=pipe_image.get_rect(midbottom=(700,random_pipe_pos - 300))
	return bottom_pipe,top_pipe

def move_pipes(pipes):
	for pipe in pipes:
		pipe.centerx-=5
	return pipes

def draw_pipes(pipes):
	for pipe in pipes:
		if pipe.bottom>=1024:
			screen.blit(pipe_image,pipe)
		else:
			flip_pipe=pygame.transform.flip(pipe_image,False,True)
			screen.blit(flip_pipe,pipe)

def remove_pipes(pipes):
	for pipe in pipes:
		if pipe.centerx==-600:
			pipes.remove(pipe)
	return pipes

def check_collision(pipes):
	for pipe in pipes:
		if bird_rect.colliderect(pipe):
			return False
	if bird_rect.top<=-100 or bird_rect.bottom>=900:
		return False

	return True

def rotate_bird(bird):
	new_bird=pygame.transform.rotozoom(bird,-bird_movement * 3,1)
	return new_bird

def bird_animation():
	new_bird=bird_frames[bird_index]
	new_bird_rect=new_bird.get_rect(center=(100,bird_rect.centery))
	return new_bird,new_bird_rect

def score_display(game_state):
	if game_state=="main_game":
		score_surface=game_font.render(str(int(score)),True,(BLACK))
		score_rect=score_surface.get_rect(center = (288,100))
		screen.blit(score_surface,score_rect)
	if game_state=="game_over":
		score_surface=game_font.render(f"Skoor: {int(score)}" ,True,(BLACK))
		score_rect=score_surface.get_rect(center = (288,100))
		screen.blit(score_surface,score_rect)

		high_score_surface=game_font.render(f"Skoori: {int(high_score)}",True,(BLACK))
		high_score_rect=high_score_surface.get_rect(center = (288,850))
		screen.blit(high_score_surface,high_score_rect)

game_over_surface=pygame.image.load("message.png").convert_alpha()
game_over_rect=game_over_surface.get_rect(center=(288, 430))

def update_score(score,high_score):
	if score>high_score:
		high_score=score
	return high_score

while True:
	for event in pygame.event.get():
		if event.type==pygame.QUIT:
			pygame.quit()
			sys.exit()
		if event.type==pygame.KEYDOWN:
			if event.key==pygame.K_SPACE and game_active:
				bird_movement=0
				bird_movement-=12
			if event.key==pygame.K_SPACE and game_active == False:
				game_active=True
				pipe_list.clear()
				bird_rect.center=(100,512)
				bird_movement=0
				score=0

		if event.type==SpawnPipe:
			pipe_list.extend(create_pipe())

		if event.type==BIRDFLAP:
			if bird_index<2:
				bird_index+ 1
			else:
				bird_index=0

			bird_surface,bird_rect=bird_animation()

	screen.blit(background_image,(0,0))

	if game_active:
		bird_movement+=gravity
		rotated_bird=rotate_bird(bird_surface)
		bird_rect.centery += bird_movement
		screen.blit(rotated_bird,bird_rect)
		game_active=check_collision(pipe_list)

		pipe_list=move_pipes(pipe_list)
		pipe_list=remove_pipes(pipe_list)
		draw_pipes(pipe_list)

		score+=0.01
		score_display("main_game")


	else:
		screen.blit(game_over_surface,game_over_rect)
		high_score=update_score(score,high_score)
		score_display("game_over")

	floor_x_pos-=1
	draw_floor()
	if floor_x_pos<=-576:
		floor_x_pos=0
	

	pygame.display.update()
	clock.tick(90)

