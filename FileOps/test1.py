import pickle

filehash = r"manifest\0a0c2d9e85967ab336a9ef48ce191f5156292b32b8bd3e0b02c21df999cff248"
try:
    unpickle = open(filehash,'rb') 
    file_info = pickle.load(unpickle)
except Exception as e:
    print(f"Erreur lors de la recuperation du hash: {e}")
finally:
    unpickle.close()
print(file_info)