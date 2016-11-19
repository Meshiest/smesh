import pygame, random, os

print(os.getcwd())

# Load an image from provided path
def load(path):
  if not path or len(path) == 0:
    return None

  # Default image path
  path = "./public/res/img/" + path
  
  # Return none if the file does not exist
  if not (os.path.exists(path) and os.path.isfile(path)):
    return None

  # Return pygame loading the image with proper transparency
  return pygame.image.load(os.path.abspath(path)).convert_alpha()

# Get a random element from an array
def sample(arr):
  return arr[int(random.random()*len(arr))]

def sampleIndex(arr):
  return int(random.random()*len(arr))

# Base body image
head_base = load("head_base.png")
hand_base = load("hand_base.png")
arm_base = load("arm_base.png")
leg_base = load("leg_base.png")
torso_base = load("torso_base.png")

# Face Images
faces = [
  load("face/face_shakunetsu_koyori.png"),
  load("face/face_shakunetsu_munemune.png"),
  load("face/face_shakunetsu_hanabi.png"),
  load("face/face_shakunetsu_itsumo.png"),
  load("face/face_shakunetsu_kiruka.png"),
  load("face/face_shakunetsu_agari.png"),
  load("face/face_sao_asuna.png"),
  load("face/face_sao_suguha.png"),
  load("face/face_angelbeats_yuri.png"),
  load("face/face_angelbeats_tachibana.png"),
  load("face/face_angelbeats_yui.png"),
  load("face/face_clannad_nagisa.png"),
  load("face/face_clannad_kyou.png"),
  load("face/face_clannad_fuka.png"),
  load("face/face_clannad_kotomi.png"),
  load("face/face_clannad_tomoyo.png"),
  load("face/face_sgdc_isaac.png"),
  load("face/face_sgdc_jake.png"),
  load("face/face_sgdc_james.png"),
  load("face/face_sgdc_adam.png"),
  load("face/face_sgdc_katie.png"),
  load("face/face_sgdc_nick.png"),
  load("face/face_sgdc_noah.png"),
  load("face/face_sgdc_alex.png"),
  load("face/face_nichijou_mio.png"),
  load("face/face_nichijou_yuuko.png"),
  load("face/face_nichijou_mai.png"),
  load("face/face_teacher_chem.png"),
  load("face/face_oreimo_kirino.png"),
  load("face/face_snk_sasha.png"),
  load("face/face_snk_mikasa.png"),
  load("face/face_eva_rei.png"),
  load("face/face_eva_asuka.png"),
  load("face/face_miko_himeko.png"),
  load("face/face_miko_chikane.png"),
  load("face/face_franken_fran.png"),
  load("face/face_streetfighter_chunli.png"),
  load("face/face_akuma_haru.png"),
  load("face/face_akuma_tokaku.png"),
  load("face/face_smash_rosalina.png"),
  load("face/face_smash_peach.png"),
  load("face/face_black_taki.png"),
  load("face/face_lbg_miko.png"),
  load("face/face_katawa_rin.png"),
  load("face/face_otomi_sakuragi.png"),
  load("face/face_smash_zelda.png"),
  load("face/face_spice_holo.png"),
  load("face/face_pokemon_joy.png"),
  load("face/face_haganai_yukino.png"),
  load("face/face_gurren_yoko.png"),
  load("face/face_mirai_yuno.png"),
]

# Torso Images
torsos = [
  load("torso/torso_angelbeats.png"),
  load("torso/torso_angelbeats_tachibana.png"),
  load("torso/torso_shakunetsu.png"),
  load("torso/torso_sgdc_isaac.png"),
  load("torso/torso_mirai_yuno.png"),
  load("torso/torso_dress.png"),
  load("torso/torso_underwear.png"),
  load("torso/torso_clannad_winter.png"),
  load("torso/torso_clannad_summer.png"),
  load("torso/torso_nichijou.png"),
  load("torso/torso_haganai_yukino.png"),
  load("torso/torso_sao_asuna.png"),
  load("torso/torso_eva.png"),
  load("torso/torso_smash_rosalina.png"),
  load("torso/torso_smash_peach.png"),
  load("torso/torso_miko.png"),
  load("torso/torso_akuma_toukaku.png"),
  load("torso/torso_smash_zelda.png"),
  load("torso/torso_pokemon_joy.png"),
  load("torso/torso_katawa.png"),
  load("torso/torso_gurren_yoko.png"),
  load("torso/torso_black.png"),
  load("torso/torso_snk_sasha.png"),
  load("torso/torso_snk_mikasa.png"),
  load("torso/torso_franken_fran.png"),
  load("torso/torso_oreimo.png"),
  load("torso/torso_spice_holo.png"),
  load("torso/torso_miko_mido.png"),
  load("torso/torso_chunli.png"),
]

# Weapon Images and Meta
weapons = [
  {'img': load('weapons/weapon_boat.png'), 'hand': (50, 150)},
  {'img': load('weapons/weapon_candycane.png'), 'hand': (60, 150)},
  {'img': load('weapons/weapon_cardboard.png'), 'hand': (50, 180)},
  {'img': load('weapons/weapon_cleaver.png'), 'hand': (50, 180)},
  {'img': load('weapons/weapon_dagger.png'), 'hand': (50, 190)},
  {'img': load('weapons/weapon_doggy.png'), 'hand': (50, 190)},
  {'img': load('weapons/weapon_doggy2.png'), 'hand': (50, 190)},
  {'img': load('weapons/weapon_lamp.png'), 'hand': (50, 170)},
  {'img': load('weapons/weapon_lovestaff.png'), 'hand': (50, 170)},
  {'img': load('weapons/weapon_maraca.png'), 'hand': (50, 170)},
  {'img': load('weapons/weapon_pregert.png'), 'hand': (50, 100)},
  {'img': load('weapons/weapon_pretzal.png'), 'hand': (50, 130)},
  {'img': load('weapons/weapon_royaldragon.png'), 'hand': (50, 170)},
  {'img': load('weapons/weapon_scimitar.png'), 'hand': (50, 160)},
  {'img': load('weapons/weapon_scythe.png'), 'hand': (50, 170)},
  {'img': load('weapons/weapon_umbrella.png'), 'hand': (50, 170)},
  {'img': load('weapons/weapon_guardian.png'), 'hand': (50, 160)},
  {'img': load('weapons/weapon_echo.png'), 'hand': (40, 170)},
  {'img': load('weapons/weapon_pan.png'), 'hand': (50, 180)},
  {'img': load('weapons/weapon_bread.png'), 'hand': (50, 180)},
  {'img': load('weapons/weapon_skullstaff.png'), 'hand': (50, 140)},
  {'img': load('weapons/weapon_horse.png'), 'hand': (50, 180)},
  {'img': load('weapons/weapon_rose.png'), 'hand': (50, 180)},
  {'img': load('weapons/weapon_snk.png'), 'hand': (25, 146)},
  {'img': load('weapons/weapon_stick.png'), 'hand': (42, 170)},
  {'img': load('weapons/weapon_swordred.png'), 'hand': (42, 175)},
  {'img': load('weapons/weapon_emeraldstaff.png'), 'hand': (20, 170)},
  {'img': load('weapons/weapon_swordpink.png'), 'hand': (23, 160)},
  {'img': load('weapons/weapon_swordorb.png'), 'hand': (21, 165)},
  {'img': load('weapons/weapon_swordsanic.png'), 'hand': (26, 173)},
  {'img': load('weapons/weapon_scalpel.png'), 'hand': (15, 152)},
]

# Foot Images
feet = [
  load("foot/foot_bare.png"),
  load("foot/foot_boot.png"),
  load("foot/foot_sock_sandal.png"),
  load("foot/foot_waterbottle.png"),
  load("foot/foot_sandal.png"),
  load("foot/foot_bunnyslipper.png"),
  load("foot/foot_cowboy.png"),
  load("foot/foot_snakeboot.png"),
  load("foot/foot_dick_1.png"),
  load("foot/foot_dick_2.png"),
  load("foot/foot_gordon.png"),
  load("foot/foot_sock.png"),
  load("foot/foot_loafer.png"),
  load("foot/foot_shark.png"),
  load("foot/foot_sneakerboot.png"),
  load("foot/foot_heel.png"),
]

def generateFace(index=-1):
  if index < 0:
    index = sampleIndex(faces)
  surface = pygame.Surface((100, 100), pygame.SRCALPHA, 32).convert_alpha()
  surface.blit(head_base, surface.get_rect())
  surface.blit(faces[index],surface.get_rect())
  return surface

def generateTorso():
  torso = sample(torsos)
  surface = pygame.Surface((100, 150), pygame.SRCALPHA, 32).convert_alpha()
  surface.blit(torso_base, surface.get_rect())
  surface.blit(torso, surface.get_rect())
  return surface

def generateFoot():
  foot = sample(feet)
  surface = pygame.Surface((34, 34), pygame.SRCALPHA, 32).convert_alpha()
  surface.blit(foot, surface.get_rect())
  return surface

def generateWeapon():
  weapon = sample(weapons)
  surface = pygame.Surface((weapon['img'].get_width(), weapon['img'].get_height()), pygame.SRCALPHA, 32).convert_alpha()
  surface.blit(weapon['img'], surface.get_rect())
  handWidth = hand_base.get_width()
  handHeight = hand_base.get_height()
  handPos = weapon['hand']
  surface.blit(hand_base, (handPos[0]-handWidth/2, handPos[1]-handHeight/2, handWidth, handHeight))
  return {'img': surface, 'hand': (surface.get_width() - handPos[0], surface.get_height() - handPos[1])}