# Sudoku Solver

A fun little project I decided to build because I play Sudoku almost every day (mostly on NYT) and wanted to see if I could solve one programmatically.

It started as a simple backtracking solver, but somewhere along the way it turned into a computer vision project. Instead of manually entering the puzzle, the program now detects the Sudoku board from an image, extracts the grid, recognizes the digits, and solves it automatically.

## Features

- Detects Sudoku boards from images using OpenCV
- Corrects perspective distortion
- Splits the board into 81 cells
- Recognizes digits using OCR
- Solves the puzzle using a backtracking algorithm

## Tech Stack

- Python
- OpenCV
- NumPy
- OCR (Tesseract)
- Backtracking Algorithm

## Current Progress

- [x] Sudoku board detection
- [x] Perspective transformation
- [x] Cell extraction
- [X] OCR integration
- [X] Sudoku solving
- [X] Overlay solved board back onto the original image
- [] Train CNN classifier and integrate it

## Why?

Mostly because I enjoy Sudoku and wanted to build something that combines computer vision with a classic algorithm. It also turned out to be a great excuse to learn OpenCV from scratch.

## Some notes

I used tesseract OCR for this but it's unable to detect the number properly and reliably, I have tweaked with the config multiple times but it's always unable to properply recognize a "1" or sometimes even "8", as such I have decided to train a tiny CNN classifier for this purpose.