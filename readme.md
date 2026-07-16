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
- [ ] OCR integration
- [ ] Sudoku solving
- [ ] Overlay solved board back onto the original image

## Why?

Mostly because I enjoy Sudoku and wanted to build something that combines computer vision with a classic algorithm. It also turned out to be a great excuse to learn OpenCV from scratch.