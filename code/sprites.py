import pygame 
from settings import *
from random import choice, randint

class BG(pygame.sprite.Sprite):
	"""
	Class for the background sprite
	"""
	def __init__(self, groups, scale_factor) -> None:
		"""
		Initialize images and display settings for the background
		"""
		super().__init__(groups)
		bg_image = pygame.image.load('../graphics/environment/background.png').convert()

		full_height = bg_image.get_height() * scale_factor
		full_width = bg_image.get_width() * scale_factor
		full_sized_image = pygame.transform.scale(bg_image, (full_width, full_height))
		
		self.image = pygame.Surface((full_width * 2, full_height))
		self.image.blit(full_sized_image, (0, 0))
		self.image.blit(full_sized_image, (full_width, 0))

		self.rect = self.image.get_rect(topleft=(0, 0))
		self.pos = pygame.math.Vector2(self.rect.topleft)

	def update(self, dt) -> None:
		"""
		Refreshes background on screen
		"""
		self.pos.x -= 300 * dt
		if self.rect.centerx <= 0:
			self.pos.x = 0
		self.rect.x = round(self.pos.x)


class Ground(pygame.sprite.Sprite):
	"""
	Class for the ground sprite
	"""
	def __init__(self, groups, scale_factor) -> None:
		"""
		Initialize images and display settings for the ground
		"""
		super().__init__(groups)
		self.sprite_type = 'ground'
		
		# image
		ground = pygame.image.load('../graphics/environment/ground.png').convert_alpha()
		self.image = pygame.transform.scale(ground, pygame.math.Vector2(ground.get_size()) * scale_factor)
		
		# position
		self.rect = self.image.get_rect(bottomleft=(0, WINDOW_HEIGHT))
		self.pos = pygame.math.Vector2(self.rect.topleft)
		self.pos = pygame.math.Vector2(self.rect.topleft)

		# mask
		self.mask = pygame.mask.from_surface(self.image)

	def update(self, dt) -> None:
		"""
		Refreshes ground on screen
		"""
		self.pos.x -= 360 * dt
		if self.rect.centerx <= 0:
			self.pos.x = 0

		self.rect.x = round(self.pos.x)


class Cookie(pygame.sprite.Sprite):
	"""
	Class for the cookie sprite
	"""
	def __init__(self, groups, scale_factor) -> None:
		"""
		Initialize images, display settings, movement, and sound for cookie
		"""
		super().__init__(groups)

		# image 
		self.import_frames(scale_factor)
		self.frame_index = 0
		self.image = self.frames[self.frame_index]

		# rect
		self.rect = self.image.get_rect(midleft = (WINDOW_WIDTH / 20,WINDOW_HEIGHT / 2))
		self.pos = pygame.math.Vector2(self.rect.topleft)

		# movement
		self.gravity = 600
		self.direction = 0

		# mask
		self.mask = pygame.mask.from_surface(self.image)

		# sound
		self.jump_sound = pygame.mixer.Sound('../sounds/jump.wav')
		self.jump_sound.set_volume(0.3)

	def import_frames(self, scale_factor):
		"""
		Code for multiple cookie sprites
		"""
		self.frames = []
		for i in range(3):
			cookie = pygame.image.load(f'../graphics/cookie/cookie{i}.png').convert_alpha()
			scaled_cookie = pygame.transform.scale(cookie, pygame.math.Vector2(cookie.get_size()) * scale_factor)
			self.frames.append(scaled_cookie)

	def apply_gravity(self, dt) -> None:
		"""
		Creates gravity
		"""
		self.direction += self.gravity * dt
		self.pos.y += self.direction * dt
		self.rect.y = round(self.pos.y)

	def jump(self) -> None:
		"""
		Allows cookie to jump
		"""
		self.jump_sound.play()
		self.direction = -400

	def animate(self, dt) -> None:
		"""
		Animates sprite
		"""
		self.frame_index += 10 * dt
		if self.frame_index >= len(self.frames):
			self.frame_index = 0
		self.image = self.frames[int(self.frame_index)]

	def rotate(self) -> None:
		"""
		Method to make the cookie rotate
		"""
		rotate_cookie = pygame.transform.rotozoom(self.image, -self.direction * 0.03, 1)
		self.image = rotate_cookie
		self.mask = pygame.mask.from_surface(self.image)

	def update(self, dt) -> None:
		"""
		Method for refreshing the cookie on the screen
		"""
		self.apply_gravity(dt)
		self.animate(dt)
		self.rotate()


class Obstacle(pygame.sprite.Sprite):
	def __init__(self, groups, scale_factor) -> None:
		"""
		Initialize images and display settings for obstacle
		"""
		super().__init__(groups)
		self.sprite_type = 'obstacle'

		orientation = choice(('up', 'down'))
		obstacle = pygame.image.load(f'../graphics/obstacles/{choice((0,1))}.png').convert_alpha()
		self.image = pygame.transform.scale(obstacle, pygame.math.Vector2(obstacle.get_size()) * scale_factor)
		
		x = WINDOW_WIDTH + randint(40, 100)

		if orientation == 'up':
			y = WINDOW_HEIGHT + randint(10, 50)
			self.rect = self.image.get_rect(midbottom=(x, y))
		else:
			y = randint(-50, -10)
			self.image = pygame.transform.flip(self.image, False, True)
			self.rect = self.image.get_rect(midtop=(x, y))

		self.pos = pygame.math.Vector2(self.rect.topleft)

		# mask
		self.mask = pygame.mask.from_surface(self.image)

	def update(self, dt) -> None:
		"""
		Refreshes obstacle on the screen
		"""
		self.pos.x -= 400 * dt
		self.rect.x = round(self.pos.x)
		if self.rect.right <= -100:
			self.kill()
