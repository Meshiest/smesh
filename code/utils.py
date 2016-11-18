
def clamp(number, minimum, maximum):
  return min(max(number, minimum), maximum)

def lerp(start, end, cap):
  return start + clamp(end - start, -cap, cap)