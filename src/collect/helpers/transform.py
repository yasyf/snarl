import numpy as np

FIRST_CODE = 48
LAST_CODE = 90
ONE_HOT_SIZE = LAST_CODE - FIRST_CODE + 1

def one_hot(char):
  one_hot = np.zeros(ONE_HOT_SIZE)
  one_hot[char['keyCode'] - FIRST_CODE] = 1
  return one_hot

def is_valid_char(char):
  return FIRST_CODE <= char['keyCode'] <= LAST_CODE

def release_time_diff(c1, c2):
  return c2['timeReleased'] - c1['timeReleased']

def transform(obj):
  words = [x for x in obj['words'] if x['characters']]
  X = np.empty(len(words), dtype=np.object)
  Y = np.empty(len(words), dtype=np.object)
  for i, word in enumerate(words):
    chars = [x for x in word['characters'] if is_valid_char(x)]
    x = np.empty((len(chars), ONE_HOT_SIZE), dtype=np.float)
    y = np.empty((len(chars) - 1,), dtype=np.float)
    for j, char in enumerate(chars):
      x[j,:] = one_hot(char)
      if j == 0:
        continue
      y[j-1] = release_time_diff(chars[j-1], char)
    X[i] = x
    Y[i] = y
  return X, Y
