import pygame, time

print(pygame.USEREVENT)
END_MUSIC_EVENT = pygame.USEREVENT + 0

pygame.mixer.music.set_endevent(END_MUSIC_EVENT)

lobby_loop = pygame.mixer.Sound('public/res/audio/lobby_loop.wav')
lobby_start = pygame.mixer.Sound('public/res/audio/lobby_start.wav')

melee_opening = pygame.mixer.Sound('public/res/audio/melee_opening_8bit.mp3')
brawl_opening = pygame.mixer.Sound('public/res/audio/smash_opening.mp3')