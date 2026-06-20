#!/bin/bash
set -e

SRC_DIR="src"
LIB_DIR="lib"
SRC_FILE="${SRC_DIR}/stats.c"
OUT_FILE="${LIB_DIR}/stats.so"

mkdir -p "${LIB_DIR}"

echo "[1/2] Compilation de ${SRC_FILE}..."
gcc \
    -shared \
    -fPIC \
    -O2 \
    -Wall \
    -lm \
    -o "${OUT_FILE}" \
    "${SRC_FILE}"

echo "[2/2] Bibliothèque créée : ${OUT_FILE}"
echo "Compilation réussie !"