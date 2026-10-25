#!/usr/bin/env python3
"""Clue Hunt — A Secret Global Race Game."""

import sys
import os

# Ensure the game package is importable
sys.path.insert(0, os.path.dirname(__file__))

from game.engine import GameEngine


def main():
    engine = GameEngine()
    engine.run()


if __name__ == "__main__":
    main()
