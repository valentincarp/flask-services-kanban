import ctypes
import os
import platform

_ext = '.so'
if platform.system() == 'Darwin':
    _ext = '.dylib'
elif platform.system() == 'Windows':
    _ext = '.dll'

_lib_path = os.path.join(os.path.dirname(__file__), 'lib', f'stats{_ext}')

if not os.path.exists(_lib_path):
    raise FileNotFoundError(
        f'Bibliothèque C introuvable : {_lib_path}\n'
        'Exécutez ./compile.sh pour compiler stats.c'
    )

_lib = ctypes.CDLL(_lib_path)

_DoublePtr = ctypes.POINTER(ctypes.c_double)

_lib.calcul_moyenne.argtypes  = [_DoublePtr, ctypes.c_int]
_lib.calcul_moyenne.restype   = ctypes.c_double
_lib.calcul_variance.argtypes = [_DoublePtr, ctypes.c_int]
_lib.calcul_variance.restype  = ctypes.c_double
_lib.calcul_ecart_type.argtypes = [_DoublePtr, ctypes.c_int]
_lib.calcul_ecart_type.restype  = ctypes.c_double
_lib.calcul_mediane.argtypes  = [_DoublePtr, ctypes.c_int]
_lib.calcul_mediane.restype   = ctypes.c_double
_lib.calcul_min.argtypes      = [_DoublePtr, ctypes.c_int]
_lib.calcul_min.restype       = ctypes.c_double
_lib.calcul_max.argtypes      = [_DoublePtr, ctypes.c_int]
_lib.calcul_max.restype       = ctypes.c_double
_lib.produit_scalaire.argtypes = [_DoublePtr, _DoublePtr, ctypes.c_int]
_lib.produit_scalaire.restype  = ctypes.c_double

def _to_c_array(python_list):
    arr = (ctypes.c_double * len(python_list))(*python_list)
    return arr, len(python_list)

def moyenne(valeurs):
    arr, n = _to_c_array(valeurs)
    return round(_lib.calcul_moyenne(arr, n), 6)

def variance(valeurs):
    arr, n = _to_c_array(valeurs)
    return round(_lib.calcul_variance(arr, n), 6)

def ecart_type(valeurs):
    arr, n = _to_c_array(valeurs)
    return round(_lib.calcul_ecart_type(arr, n), 6)

def mediane(valeurs):
    arr, n = _to_c_array(valeurs)
    return round(_lib.calcul_mediane(arr, n), 6)

def minimum(valeurs):
    arr, n = _to_c_array(valeurs)
    return round(_lib.calcul_min(arr, n), 6)

def maximum(valeurs):
    arr, n = _to_c_array(valeurs)
    return round(_lib.calcul_max(arr, n), 6)

def dot_product(v1, v2):
    if len(v1) != len(v2):
        raise ValueError('Les deux vecteurs doivent avoir la même longueur')
    a1, n = _to_c_array(v1)
    a2, _ = _to_c_array(v2)
    return round(_lib.produit_scalaire(a1, a2, n), 6)