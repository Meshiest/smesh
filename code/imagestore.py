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
]

def generateFace(index=-1):
  global faces
  if index < 0:
    index = sampleIndex(faces)
  surface = pygame.Surface((100, 100), pygame.SRCALPHA, 32).convert_alpha()
  surface.blit(head_base, surface.get_rect())
  surface.blit(faces[index],surface.get_rect())
  return surface

def generateTorso():
  global torsos
  torso = sample(torsos)
  surface = pygame.Surface((100, 150), pygame.SRCALPHA, 32).convert_alpha()
  surface.blit(torso_base, surface.get_rect())
  surface.blit(torso, surface.get_rect())
  return surface