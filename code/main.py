import pygame
import sys
import time
from settings import *
from sprites import BG, Ground, Cookie, Obstacle

# https://www.youtube.com/watch?v=VUFvY349ess&t=427s

class Game:
	def __init__(self) -> None:
		"""
		Method to set up the window, sprites, and music
		"""
		# window setup
		pygame.init()
		self.display = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
		pygame.display.set_caption('Flappy Cookie')
		self.clock = pygame.time.Clock()
		self.active = True

		# sprite groups
		self.all_sprites = pygame.sprite.Group()
		self.collision_sprites = pygame.sprite.Group()

		# background
		bg_height = pygame.image.load('../graphics/environment/background.png').get_height()
		self.scale_factor = WINDOW_HEIGHT / bg_height

		# sprite setup
		BG(self.all_sprites, self.scale_factor)
		Ground([self.all_sprites, self.collision_sprites], self.scale_factor)
		self.cookie = Cookie(self.all_sprites, self.scale_factor / 1.7)

		# timer
		self.obstacle_timer = pygame.USEREVENT + 1
		pygame.time.set_timer(self.obstacle_timer, 1500)

		# text
		self.font = pygame.font.Font('../graphics/font/BD_Cartoon_Shout.ttf', 30)
		self.score = 0
		self.start_offset = 0

		# menu
		self.menu = pygame.image.load('../graphics/ui/menu.png').convert_alpha()
		self.menu_rect = self.menu.get_rect(center=(WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2))

		# music
		self.music = pygame.mixer.Sound('../sounds/music.wav')
		self.music.play(loops=-1)

	def collisions(self) -> None:
		"""
		Method to check for collisions with the obstacles
		"""
		if pygame.sprite.spritecollide(self.cookie, self.collision_sprites, False, pygame.sprite.collide_mask) or self.cookie.rect.top <= 0:
			for sprite in self.collision_sprites.sprites():
				if sprite.sprite_type == 'obstacle':
					sprite.kill()
			self.active = False
			self.cookie.kill()

	def display_score(self) -> None:
		"""
		Method for displaying the score
		"""
		if self.active:
			self.score = (pygame.time.get_ticks() - self.start_offset) // 1500
			y = WINDOW_HEIGHT / 10
		else:
			y = WINDOW_HEIGHT / 2 + (self.menu_rect.height / 1.5)

		score_text = self.font.render(str(self.score), True, 'black')
		score_rect = score_text.get_rect(midtop=(WINDOW_WIDTH / 2, y))
		self.display.blit(score_text, score_rect)

	def display_pause(self) -> None:
		"""
		Method for displaying the pause button
		"""
		pause = self.font.render('ESC', True, 'black')
		pause_rect = pause.get_rect(midtop=(400, 30))
		self.display.blit(pause, pause_rect)

	def main_menu(self) -> None:
		"""
		Method for setting up the main menu
		"""
		text_active = False
		click = False
		self.display = pygame.display.set_mode((300, 500))
		while True:
			self.display.fill((38, 161, 191))
			mx, my = pygame.mouse.get_pos()

			# Code for play button
			play_button = pygame.Rect(50, 100, 200, 50)
			font = pygame.font.SysFont(None, 40)
			play_text = font.render('Play Game', 1, (255, 255, 255))
			play_rect = play_text.get_rect()
			play_rect.midtop = (150, 100)

			# Code for help button
			help_button = pygame.Rect(50, 200, 200, 50)
			help_text = font.render('HELP', 1, (255, 255, 255))
			help_rect = help_text.get_rect()
			help_rect.midtop = (150, 200)

			# Checks for button clicks
			if play_button.collidepoint((mx, my)):
				if click:
					game.run()
					pygame.time.delay(5000)
			if help_button.collidepoint((mx, my)):
				if click:
					font1 = pygame.font.SysFont(None, 20)
					jump_text = font.render('Tap to jump', 1, (255, 255, 255))
					jump_rect = jump_text.get_rect()
					jump_rect.midtop = (150, 300)
					obstacle_text = font.render('Jump past obstacles', 1, (255, 255, 255))
					obstacle_rect = obstacle_text.get_rect()
					obstacle_rect.midtop = (150, 350)
					time_text = font.render('Time Alive = Score', 1, (255, 255, 255))
					time_rect = obstacle_text.get_rect()
					time_rect.midtop = (175, 400)
					text_active = True

			# displays text
			pygame.draw.rect(self.display, (143, 93, 39), play_button)
			pygame.draw.rect(self.display, (143, 93, 39), help_button)
			self.display.blit(play_text, play_rect)
			self.display.blit(help_text, help_rect)
			if text_active:
				self.display.blit(jump_text, jump_rect)
				self.display.blit(obstacle_text, obstacle_rect)
				self.display.blit(time_text, time_rect)
			click = False

			# event loop
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					pygame.quit()
					sys.exit()
				if event.type == pygame.KEYDOWN:
					if event.key == pygame.K_ESCAPE:
						pygame.quit()
						sys.exit()
				if event.type == pygame.MOUSEBUTTONDOWN:
					if event.button == 1:
						click = True
			self.clock.tick(0)
			pygame.display.update()

	def run(self) -> None:
		"""
		Method used to run the main game
		"""
		self.display = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
		last_time = time.time()
		while True:

			# difference in time
			dt = time.time() - last_time
			last_time = time.time()

			# event loop
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					pygame.quit()
					sys.exit()
				if event.type == pygame.MOUSEBUTTONDOWN:
					if self.active:
						self.cookie.jump()
					else:
						self.cookie = Cookie(self.all_sprites, self.scale_factor / 1.5)
						self.active = True
						self.start_offset = pygame.time.get_ticks()
				if event.type == pygame.KEYDOWN:
					if event.key == pygame.K_ESCAPE:
						game.main_menu()

				if event.type == self.obstacle_timer and self.active:
					Obstacle([self.all_sprites, self.collision_sprites], self.scale_factor * 1.1)

			# game logic
			self.display.fill('black')
			self.all_sprites.update(dt)
			self.all_sprites.draw(self.display)
			self.display_score()
			self.display_pause()

			if self.active:
				self.collisions()
			else:
				self.display.blit(self.menu, self.menu_rect)

			pygame.display.update()


if __name__ == '__main__':
	game = Game()
	game.main_menu()