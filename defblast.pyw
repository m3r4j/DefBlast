import pygame
import os # Used to join paths
import random # Used to generate the y axis for the nuke and when to launch the nukes
import sys # Used to terminate the program

# All the rgb colors
white = (255, 255, 255)
black = (0, 0, 0)
brown = (139, 69, 19)
grey = (169, 169, 169)
red = (255, 0, 0)

# Initialize all pygame features that are needed for the game
pygame.mixer.init()
pygame.font.init()

# Make a (default) font
font = pygame.font.SysFont(None, 40)

# Create a sound class and make functions that just play sounds
class sound:
	# Whenever the user wants to fire then make the fire_gun sound effect
	def fire_gun():
		pygame.mixer.music.load(os.path.join('audio', 'fire_gun.mp3'))
		pygame.mixer.music.play()

	# Whenever it is round over make this noise
	def round_over():
		pygame.mixer.music.load(os.path.join('audio', 'round_over.wav'))
		pygame.mixer.music.play()

	# Whenever the player loses then make the game over noise
	def game_over():
		pygame.mixer.music.load(os.path.join('audio', 'game_over.wav'))
		pygame.mixer.music.play()


# Show a message to the screen with given parameters / arguements
def message_to_screen(text, font, x, y, color):
	text = font.render(text, True, color) # Create the text so it can be put onto the screen
	window.blit(text, (x, y)) # Put it onto the screen

# This will draw the bullets with the bull array
def draw_bullets(bullets):
	index = 0
	for i in bullets:
		if i.x > width: # If the bullet has gone through the screen (to the end) then get rid of that bullet
			del bullets[index]
		window.blit(bullet, (i)) # Put the bullet onto the screen
		i.x += bullet_speed # Add to its speed
		index += 1

# This generates random nukes
def generate_nukes(amount_of_nukes):
	if random.random() < 0.01:
		global nukes, nuke_rect

		for nuke_amount in range(amount_of_nukes): # Loop over a given amount of times
			nuke_y = random.randint(1, height - nuke_height) # Generate the nukes y axis
			nuke_rect = pygame.Rect(nuke_x, nuke_y, nuke_width, nuke_height) # Create the nuke rect object
			nukes.append(nuke_rect) # Save it to nukes



# With nukes in the nukes list then we now have to launch them
def launch_nukes(nukes):
	global game_over
	index = 0
	for i in nukes:
		if i.x < 0: # If the nuke goes off the screen then get rid of it
			del nukes[index]
			game_over = True
		window.blit(nuke, i)
		i.x -= nuke_speed # Keep making it go left with the given speed
		index += 1




# This is the logic behind handling the tanks movement
def handle_tank_movement(keys):
	global tank_x, tank_y

	if keys[pygame.K_d] and tank_x + tank_speed <= width - tank_width: # If the tank wants to go right
		tank_x += tank_speed

	elif keys[pygame.K_a] and tank_x - tank_speed >= 0: # If the tank wants to go left
		tank_x -= tank_speed

	elif keys[pygame.K_w] and tank_y - tank_speed >= 0: # If the tank wants to go up
		tank_y -= tank_speed

	elif keys[pygame.K_s] and tank_y + tank_speed <= height - tank_height: # And if the tank wants to go left
		tank_y += tank_speed

# Initialize pygame
pygame.init()

# Set a width and height (can be changed, but should stay as 800x600)
width, height = 800, 400

# Create the window
window = pygame.display.set_mode((width, height))

# Set the title to "Defblast"
pygame.display.set_caption('Defblast')

# Load in the game icon or get the surface object
game_icon = pygame.image.load('icon.png')

# Display this onto the screen
pygame.display.set_icon(game_icon)

clock = pygame.time.Clock() # The clock to tick it to the fps count (variable)

# The nukes width and height
nuke_width = 50
nuke_height = 100

# The nukes coordinates (x, y)
nuke_x = width - 100
nuke_y = random.randint(1, height - nuke_height)

# The nuke surface object
nuke = pygame.image.load(os.path.join('sprites', 'nuke.png'))
nuke = pygame.transform.scale(nuke, (nuke_width, nuke_height)) # Resize it to the width and height
nuke = pygame.transform.rotate(nuke, 90) # Rotate it so its facing left because it comes from that direction

# The tanks size (width, height)
tank_width = 100
tank_height = 50

# Load in the tank (surface object) and resize it to its value
tank = pygame.image.load(os.path.join('sprites', 'tank.png'))
tank = pygame.transform.scale(tank, (tank_width, tank_height))

# The tanks coordinates
tank_x = 50
tank_y = height // 2

# Bullets width and height
bullet_width = 50
bullet_height = 50

# The bullet surface object and resize it to given width and height
bullet = pygame.image.load(os.path.join('sprites', 'bullet.png'))
bullet = pygame.transform.scale(bullet, (bullet_width, bullet_height))

# Coordinates for the bullet, in this case it must be right next to the scope becaause thats where it fires from
bullet_x = tank_x + 90
bullet_y = tank_y - 10

# Rect object which tells the program where this bullet is headed
bullet_rect = pygame.Rect(bullet_x, bullet_y, bullet_width, bullet_height)

# Rect object which tells the program where the nuke is headed
nuke_rect = pygame.Rect(nuke_x, nuke_y, nuke_width, nuke_height)

# Some constants which are used to update the game or round
tank_speed_add = 1 # The amount that the tank speed will add to
nuke_speed_add = 1 # The amount that the nuke speed will add to
round_add = 1 # Every time a round goes up then add it by this number

amount_of_nukes = 1 # This is the amount of nukes that get generated, usually it should be set to "1"


def game_loop():
	global nukes, bullets, tank_speed, bullet_speed, nuke_speed, tank_x, tank_y, game_over

	# The tanks coordinates
	tank_x = 50
	tank_y = height // 2

	# The bullets coordinates
	bullet_x = tank_x + 90
	bullet_y = tank_y - 10

	# The nukes coordinates
	nuke_x = width - 100 # Start
	nuke_y = random.randint(1, height - nuke_height) # Generate a random y axis for the nuke

	game_over = False # Check if the game is over

	running = True # Check if the game is running

	fps = 60 # This is the fps count (should stay at 60 fps)

	tank_speed = 5 # The tank speed which can go high or low

	nuke_speed = 1 # The speed that the nukes are going at

	bullet_speed = 10 # The speed that the bullets are firing at

	shots_fired = 0 # The amount of shots fired

	score = 0 # The current score for the user (the amount of nukes destroyed)

	scores = [] # Get all the scores of the user (only if its a multiple of ten)

	rounds = 1 # The amount of rounds, usually every ten scores it becomes one round and makes a noise

	# Bullets and nukes are gonna be stored so they're all drawn out with seperate functions, they take in its rect objects
	bullets = []
	nukes = []


	# The mainloop to run the game
	while running:
		# Run the event loop on a given fps
		clock.tick(fps)

		# Check if the game is over, if so then make the game_over sound
		if game_over == True:
			sound.game_over()

		# This checks if it is game over
		while game_over:
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					pygame.quit()
					sys.exit()

				if event.type == pygame.KEYDOWN:
					if event.key == pygame.K_q:
						pygame.quit()
						sys.exit()

					elif event.key == pygame.K_c:
						game_loop()

			# The display can be much more nicer than just this
			window.fill(white)
			message_to_screen('Press Q to quit or C to play again', font, width // 4.5, height // 2.5, red)
			pygame.display.update()

		# Check events
		for event in pygame.event.get():
			if event.type == pygame.QUIT: # Checks for the quit event
				running = False

			if event.type == pygame.KEYDOWN: # Checks if a key was pushed
				if event.key == pygame.K_SPACE: # If the space key was pushed down
					bullet_rect = pygame.Rect(bullet_x, bullet_y, bullet_width, bullet_height)
					bullets.append(bullet_rect) # Add it to the bullets list
					shots_fired += 1 # Adds to the amount of shots fired
					sound.fire_gun() # Makes the sound effect when a bullet is shot


		keys = pygame.key.get_pressed() # Get all the keys pressed
		window.fill(brown) # Set the background color or fill the screen

		# The bullet will have to be right next to the tanks scope so always worry about that
		bullet_x = tank_x + 90
		bullet_y = tank_y - 10

		tank_sprite = window.blit(tank, (tank_x, tank_y)) # Display the tank

		# Show the messages onto the screen
		message_to_screen('Score: ' + str(score), font, 0, 0, grey) # Show the users score
		message_to_screen('Round: ' + str(rounds), font, 200, 0, grey) # Show what round it is currently on
		message_to_screen('Shots: ' + str(shots_fired), font, 400, 0, grey) # Show the amount of shots the user has fired
		message_to_screen('Speed: ' + str(tank_speed), font, 600, 0, grey) # Show the speed of the player or tank

		if score % 10 == 0 and score not in scores and score != 0: # Check if its a multiple of 10 and it doesn't equal to zero
			# Update the scores
			sound.round_over() # Make the round over noise
			rounds += round_add # Go to the next round
			nuke_speed += nuke_speed_add # Increase the speed of the nuke
			tank_speed += tank_speed_add # Increase the speed of the tank
			scores.append(score) # Add it to scores so it gets blocked

		# Check if the bullet has hit the nuke
		for i in bullets:
			for c in nukes: # Go through all the nukes
				if i.x in range(c.x, c.x + nuke_width - nuke_speed) and i.y in range(c.y - 20, c.y + 20): # Check if it hit in that area
					if c in nukes:
						nukes.remove(c) # Remove the nuke from the current (incoming) nukes

					if i in bullets:
						bullets.remove(i) # Make the bullet dissapear once it has hit

					score += 1 # Update the score when a nuke is hit

		# Check if the nuke hits the tank, if so then it is game over
		for i in nukes:
			if tank_x in range(i.x - 80, i.x + 20) and tank_y in range(i.y - 40, i.y + 20):
				nukes.remove(i)
				game_over = True



		# Game logic
		handle_tank_movement(keys) # This gives life to the movement of the tank
		draw_bullets(bullets) # This draws all the bullets and shows the firing of it
		launch_nukes(nukes) # This launches any nukes that are in the nukes list
		generate_nukes(amount_of_nukes) # Generates one nuke every single time

		pygame.display.update() # Updates the screen every time

game_loop()
pygame.quit()
sys.exit()
