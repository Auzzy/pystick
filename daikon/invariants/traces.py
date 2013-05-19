import sys
from os.path import abspath, dirname, pardir, join as path_join
sys.path.append(abspath(path_join(dirname(__file__),pardir,pardir)))
from util import *


traces = [
{ ('Exit', 1):{'num5': Void(), 'num6': Void(), 'num2': Void(), 'num3': Void(), 'num21': Void(), 'num9': Void(), 'num14': Void(), 'num': Void(), 'num12': Void()},
('Loop', 8):{'num5': Void(), 'num6': Void(), 'num2': Void(), 'num3': Void(), 'num21': Void(), 'num9': 4, 'num14': 0, 'num': 4, 'num12': open("test.txt")},
('Exit', 7):{'num5': Void(), 'num6': Void(), 'num2': Void(), 'num3': Void(), 'num21': Void(), 'num9': Void(), 'num14': Void(), 'num': Void(), 'num12': Void()},
('Loop', 5):{'num5': Void(), 'num6': Void(), 'num2': Void(), 'num3': Void(), 'num21': Void(), 'num9': Void(), 'num14': Void(), 'num': Void(), 'num12': Void()},
('Enter', 1):{'num5': Void(), 'num6': Void(), 'num2': Void(), 'num3': Void(), 'num21': Void(), 'num9': Void(), 'num14': Void(), 'num': 4, 'num12': Void()},
('Exit', 16):{'num5': Void(), 'num6': 4, 'return': type(None), 'num2': Void(), 'num3': 123, 'num21': 0, 'num9': 4, 'num14': 0, 'num': 4, 'num12': open("test.txt")},
},

{ ('Exit', 1):{'num5': Void(), 'num6': Void(), 'num2': Void(), 'num3': Void(), 'num21': Void(), 'num9': Void(), 'num14': Void(), 'num': Void(), 'num12': Void()},
('Loop', 8):{'num5': Void(), 'num6': Void(), 'num2': Void(), 'num3': Void(), 'num21': Void(), 'num9': 9, 'num14': 0, 'num': 9, 'num12': open("test.txt")},
('Exit', 7):{'num5': Void(), 'num6': Void(), 'num2': Void(), 'num3': Void(), 'num21': Void(), 'num9': Void(), 'num14': Void(), 'num': Void(), 'num12': Void()},
('Loop', 5):{'num5': Void(), 'num6': Void(), 'num2': Void(), 'num3': Void(), 'num21': Void(), 'num9': Void(), 'num14': Void(), 'num': Void(), 'num12': Void()},
('Enter', 1):{'num5': Void(), 'num6': Void(), 'num2': Void(), 'num3': Void(), 'num21': Void(), 'num9': Void(), 'num14': Void(), 'num': 9, 'num12': Void()},
('Exit', 16):{'num5': Void(), 'num6': 4, 'return': type(None), 'num2': Void(), 'num3': 123, 'num21': 0, 'num9': 9, 'num14': 0, 'num': 9, 'num12': open("test.txt")},
},

{ ('Exit', 1):{'num5': Void(), 'num6': Void(), 'num2': Void(), 'num3': Void(), 'num21': Void(), 'num9': Void(), 'num14': Void(), 'num': Void(), 'num12': Void()},
('Loop', 8):{'num5': Void(), 'num6': Void(), 'num2': Void(), 'num3': Void(), 'num21': Void(), 'num9': 0, 'num14': 0, 'num': 0, 'num12': open("test.txt")},
('Exit', 7):{'num5': Void(), 'num6': Void(), 'num2': Void(), 'num3': Void(), 'num21': Void(), 'num9': Void(), 'num14': Void(), 'num': Void(), 'num12': Void()},
('Loop', 5):{'num5': Void(), 'num6': Void(), 'num2': Void(), 'num3': Void(), 'num21': Void(), 'num9': Void(), 'num14': Void(), 'num': Void(), 'num12': Void()},
('Enter', 1):{'num5': Void(), 'num6': Void(), 'num2': Void(), 'num3': Void(), 'num21': Void(), 'num9': Void(), 'num14': Void(), 'num': 0, 'num12': Void()},
('Exit', 16):{'num5': Void(), 'num6': 4, 'return': type(None), 'num2': Void(), 'num3': 123, 'num21': 0, 'num9': 0, 'num14': 0, 'num': 0, 'num12': open("test.txt")},
},

{ ('Exit', 1):{'num5': Void(), 'num6': 5, 'return': type(Void()), 'num2': Void(), 'num3': Void(), 'num21': 0, 'num9': 7, 'num14': 0, 'num': 7, 'num12': open("test.txt")},
('Loop', 8):{'num5': Void(), 'num6': Void(), 'num2': Void(), 'num3': Void(), 'num21': Void(), 'num9': 7, 'num14': 0, 'num': 7, 'num12': open("test.txt")},
('Exit', 7):{'num5': Void(), 'num6': Void(), 'num2': Void(), 'num3': Void(), 'num21': Void(), 'num9': Void(), 'num14': Void(), 'num': Void(), 'num12': Void()},
('Loop', 5):{'num5': Void(), 'num6': Void(), 'num2': Void(), 'num3': Void(), 'num21': Void(), 'num9': Void(), 'num14': Void(), 'num': Void(), 'num12': Void()},
('Enter', 1):{'num5': Void(), 'num6': Void(), 'num2': Void(), 'num3': Void(), 'num21': Void(), 'num9': Void(), 'num14': Void(), 'num': 7, 'num12': Void()},
('Exit', 16):{'num5': Void(), 'num6': Void(), 'num2': Void(), 'num3': Void(), 'num21': Void(), 'num9': Void(), 'num14': Void(), 'num': Void(), 'num12': Void()},
},

{ ('Exit', 1):{'num5': Void(), 'num6': Void(), 'num2': Void(), 'num3': Void(), 'num21': Void(), 'num9': Void(), 'num14': Void(), 'num': Void(), 'num12': Void()},
('Loop', 8):{'num5': Void(), 'num6': Void(), 'num2': Void(), 'num3': Void(), 'num21': Void(), 'num9': -6, 'num14': 0, 'num': -6, 'num12': open("test.txt")},
('Exit', 7):{'num5': Void(), 'num6': Void(), 'num2': Void(), 'num3': Void(), 'num21': Void(), 'num9': Void(), 'num14': Void(), 'num': Void(), 'num12': Void()},
('Loop', 5):{'num5': Void(), 'num6': Void(), 'num2': Void(), 'num3': Void(), 'num21': Void(), 'num9': Void(), 'num14': Void(), 'num': Void(), 'num12': Void()},
('Enter', 1):{'num5': Void(), 'num6': Void(), 'num2': Void(), 'num3': Void(), 'num21': Void(), 'num9': Void(), 'num14': Void(), 'num': -6, 'num12': Void()},
('Exit', 16):{'num5': Void(), 'num6': 4, 'return': type(None), 'num2': Void(), 'num3': 123, 'num21': 0, 'num9': -6, 'num14': 0, 'num': -6, 'num12': open("test.txt")},
},

{ ('Exit', 1):{'num5': Void(), 'num6': Void(), 'num2': Void(), 'num3': Void(), 'num21': Void(), 'num9': Void(), 'num14': Void(), 'num': Void(), 'num12': Void()},
('Loop', 8):{'num5': Void(), 'num6': Void(), 'num2': Void(), 'num3': Void(), 'num21': Void(), 'num9': 1, 'num14': 0, 'num': 1, 'num12': open("test.txt")},
('Exit', 7):{'num5': Void(), 'num6': Void(), 'num2': Void(), 'num3': Void(), 'num21': Void(), 'num9': Void(), 'num14': Void(), 'num': Void(), 'num12': Void()},
('Loop', 5):{'num5': Void(), 'num6': Void(), 'num2': Void(), 'num3': Void(), 'num21': Void(), 'num9': Void(), 'num14': Void(), 'num': Void(), 'num12': Void()},
('Enter', 1):{'num5': Void(), 'num6': Void(), 'num2': Void(), 'num3': Void(), 'num21': Void(), 'num9': Void(), 'num14': Void(), 'num': 1, 'num12': Void()},
('Exit', 16):{'num5': Void(), 'num6': 4, 'return': type(None), 'num2': Void(), 'num3': 123, 'num21': 0, 'num9': 1, 'num14': 0, 'num': 1, 'num12': open("test.txt")}}]


traces2 = [
{ ('Exit', 1):{'num5': Void(), 'num6': Void(), 'num2': Void(), 'num3': Void(), 'num21': Void(), 'num9': Void(), 'num14': Void(), 'num': Void(), 'num12': Void()},
('Loop', 8):{'num5': Void(), 'num6': Void(), 'num2': Void(), 'num3': Void(), 'num21': Void(), 'num9': 4, 'num14': 0, 'num': 4, 'num12': open("test.txt")},
('Exit', 7):{'num5': Void(), 'num6': Void(), 'num2': Void(), 'num3': Void(), 'num21': Void(), 'num9': Void(), 'num14': Void(), 'num': Void(), 'num12': Void()},
('Loop', 5):{'num5': Void(), 'num6': Void(), 'num2': Void(), 'num3': Void(), 'num21': Void(), 'num9': Void(), 'num14': Void(), 'num': Void(), 'num12': Void()},
('Enter', 1):{'num5': Void(), 'num6': Void(), 'num2': Void(), 'num3': Void(), 'num21': Void(), 'num9': Void(), 'num14': Void(), 'num': 4, 'num12': Void()},
('Exit', 16):{'num5': Void(), 'num6': 4, 'return': type(None), 'num2': Void(), 'num3': 123, 'num21': 0, 'num9': 4, 'num14': 0, 'num': 4, 'num12': open("test.txt")},
},

{ ('Exit', 1):{'num5': Void(), 'num6': Void(), 'num2': Void(), 'num3': Void(), 'num21': Void(), 'num9': Void(), 'num14': Void(), 'num': Void(), 'num12': Void()},
('Loop', 8):{'num5': Void(), 'num6': Void(), 'num2': Void(), 'num3': Void(), 'num21': Void(), 'num9': 9, 'num14': 0, 'num': 9, 'num12': open("test.txt")},
('Exit', 7):{'num5': Void(), 'num6': Void(), 'num2': Void(), 'num3': Void(), 'num21': Void(), 'num9': Void(), 'num14': Void(), 'num': Void(), 'num12': Void()},
('Loop', 5):{'num5': Void(), 'num6': Void(), 'num2': Void(), 'num3': Void(), 'num21': Void(), 'num9': Void(), 'num14': Void(), 'num': Void(), 'num12': Void()},
('Enter', 1):{'num5': Void(), 'num6': Void(), 'num2': Void(), 'num3': Void(), 'num21': Void(), 'num9': Void(), 'num14': Void(), 'num': 9, 'num12': Void()},
('Exit', 16):{'num5': Void(), 'num6': 4, 'return': type(None), 'num2': Void(), 'num3': 123, 'num21': 0, 'num9': 9, 'num14': 0, 'num': 9, 'num12': open("test.txt")},
},

{ ('Exit', 1):{'num5': Void(), 'num6': Void(), 'num2': Void(), 'num3': Void(), 'num21': Void(), 'num9': Void(), 'num14': Void(), 'num': Void(), 'num12': Void()},
('Loop', 8):{'num5': Void(), 'num6': Void(), 'num2': Void(), 'num3': Void(), 'num21': Void(), 'num9': -6, 'num14': 0, 'num': -6, 'num12': open("test.txt")},
('Exit', 7):{'num5': Void(), 'num6': Void(), 'num2': Void(), 'num3': Void(), 'num21': Void(), 'num9': Void(), 'num14': Void(), 'num': Void(), 'num12': Void()},
('Loop', 5):{'num5': Void(), 'num6': Void(), 'num2': Void(), 'num3': Void(), 'num21': Void(), 'num9': Void(), 'num14': Void(), 'num': Void(), 'num12': Void()},
('Enter', 1):{'num5': Void(), 'num6': Void(), 'num2': Void(), 'num3': Void(), 'num21': Void(), 'num9': Void(), 'num14': Void(), 'num': -6, 'num12': Void()},
('Exit', 16):{'num5': Void(), 'num6': 4, 'return': type(None), 'num2': Void(), 'num3': 123, 'num21': 0, 'num9': -6, 'num14': 0, 'num': -6, 'num12': open("test.txt")},
}]



traces3 = [
{ ('Exit', 1):{'num5': Void(), 'num6': Void(), 'num2': Void(), 'num3': Void(), 'num21': Void(), 'num9': Void(), 'num14': Void(), 'num': Void(), 'num12': Void()},
('Loop', 8):{'num5': Void(), 'num6': Void(), 'num2': Void(), 'num3': Void(), 'num21': Void(), 'num9': 4, 'num14': 0, 'num': 4, 'num12': open("test.txt")},
('Exit', 7):{'num5': Void(), 'num6': Void(), 'num2': Void(), 'num3': Void(), 'num21': Void(), 'num9': Void(), 'num14': Void(), 'num': Void(), 'num12': Void()},
('Loop', 5):{'num5': Void(), 'num6': Void(), 'num2': Void(), 'num3': Void(), 'num21': Void(), 'num9': Void(), 'num14': Void(), 'num': Void(), 'num12': Void()},
('Enter', 1):{'num5': Void(), 'num6': Void(), 'num2': Void(), 'num3': Void(), 'num21': Void(), 'num9': Void(), 'num14': Void(), 'num': 4, 'num12': Void()},
('Exit', 16):{'num5': Void(), 'num6': 4, 'return': type(None), 'num2': Void(), 'num3': 123, 'num21': 0, 'num9': 4, 'num14': 0, 'num': 4, 'num12': open("test.txt")},
},

{ ('Exit', 1):{'num5': Void(), 'num6': Void(), 'num2': Void(), 'num3': Void(), 'num21': Void(), 'num9': Void(), 'num14': Void(), 'num': Void(), 'num12': Void()},
('Loop', 8):{'num5': Void(), 'num6': Void(), 'num2': Void(), 'num3': Void(), 'num21': Void(), 'num9': 9, 'num14': 0, 'num': 9, 'num12': open("test.txt")},
('Exit', 7):{'num5': Void(), 'num6': Void(), 'num2': Void(), 'num3': Void(), 'num21': Void(), 'num9': Void(), 'num14': Void(), 'num': Void(), 'num12': Void()},
('Loop', 5):{'num5': Void(), 'num6': Void(), 'num2': Void(), 'num3': Void(), 'num21': Void(), 'num9': Void(), 'num14': Void(), 'num': Void(), 'num12': Void()},
('Enter', 1):{'num5': Void(), 'num6': Void(), 'num2': Void(), 'num3': Void(), 'num21': Void(), 'num9': Void(), 'num14': Void(), 'num': 9, 'num12': Void()},
('Exit', 16):{'num5': Void(), 'num6': 4, 'return': type(None), 'num2': Void(), 'num3': 123, 'num21': 0, 'num9': 9, 'num14': 0, 'num': 9, 'num12': open("test.txt")}}]
