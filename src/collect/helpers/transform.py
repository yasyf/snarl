import numpy as np

FIRST_CODE = 48
LAST_CODE = 90
ONE_HOT_SIZE = LAST_CODE - FIRST_CODE + 1
TIME_DIFF_THRESHOLD = 300
HOLD_THRESHOLD = 150

def str_to_idxs(s):
  return map(lambda c: ord(c.upper()) - FIRST_CODE, s)

def idxs_to_str(idxs):
  return ''.join(map(lambda i: chr(i + FIRST_CODE).lower(), idxs))

def chars_to_idxs(chars):
  return [c['keyCode'] - FIRST_CODE for c in chars]

def encode_chars(chars):
  return [list(one_hot(c)) for c in chars if is_valid_char(c)]

def filter_valid(obj):
  return [[c for c in w['characters'] if is_valid_char(c)] for w in obj['words'] if w['characters']]

def one_hot_to_ind(x):
  return np.flatnonzero(x)[0]

def one_hot(char):
  one_hot = np.zeros(ONE_HOT_SIZE)
  one_hot[char['keyCode'] - FIRST_CODE] = 1
  return one_hot

def is_valid_char(char):
  return FIRST_CODE <= char['keyCode'] <= LAST_CODE

def is_valid_idx(idx):
  return FIRST_CODE <= idx <= LAST_CODE

def release_time_diff(c1, c2):
  return min(max(0, c2['timeReleased'] - c1['timeReleased']), TIME_DIFF_THRESHOLD)

def time_held(c):
  return min(max(0, c['timeReleased'] - c['timePressed']), HOLD_THRESHOLD)

def transform(obj):
  words = filter_valid(obj)
  X = np.empty(len(words), dtype=np.object)
  Y = np.empty(len(words), dtype=np.object)
  Z = np.empty(len(words), dtype=np.object)
  for i, word in enumerate(words):
    chars = [(j, x) for j, x in enumerate(word) if is_valid_char(x)]
    if not chars:
      X[i] = Y[i] = Z[i] = np.empty(0)
      continue
    x = np.empty((len(chars), ONE_HOT_SIZE), dtype=np.float)
    y = np.empty(len(chars) - 1, dtype=np.float)
    z = np.empty(len(chars), dtype=np.float)
    for k, (j, char) in enumerate(chars):
      x[k,:] = one_hot(char)
      z[k] = time_held(char)
      if k == 0:
        continue
      y[k-1] = release_time_diff(word[j-1], char)
    X[i] = x
    Y[i] = y
    Z[i] = z
  return X, Y, Z
