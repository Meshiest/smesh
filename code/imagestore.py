import pygame, random, os

print(os.getcwd())

# Load an image from provided path
def load(path):
  # Default image path
  path = "./public/res/img/" + path
  
  # Return none if the file does not exist
  if not os.path.exists(path):
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
]

# Torso Images
torsos = [
  load("torso/torso_base.png")
]

def generateFace(index=-1):
  global faces
  if index < 0:
    index = sampleIndex(faces)
  surface = pygame.Surface((100, 100), pygame.SRCALPHA, 32).convert_alpha()
  surface.blit(head_base, surface.get_rect())
  surface.blit(faces[index],surface.get_rect())
  return surface