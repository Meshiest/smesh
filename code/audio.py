import pygame, time

END_MUSIC_EVENT = pygame.USEREVENT + 0

pygame.mixer.music.set_endevent(END_MUSIC_EVENT)

lobby_loop = 'public/res/audio/lobby_loop.wav'
lobby_start = 'public/res/audio/lobby_start.wav'

melee_opening = 'public/res/audio/melee_opening_8bit.mp3'
elevator_loop = 'public/res/audio/elevator_loop.mp3'
brawl_opening = 'public/res/audio/smash_opening.mp3'

menu_select = pygame.mixer.Sound('public/res/audio/menu_select.wav')
win_cheer = pygame.mixer.Sound('public/res/audio/win_cheer.wav')
explosion = pygame.mixer.Sound('public/res/audio/explosion.wav')