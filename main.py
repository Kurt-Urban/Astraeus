from Asteroids import game_logic as ast
import sys


def human():
    game = ast.AsteroidsGame()
    game.run()


def ai():
    game = ast.AsteroidsGame()
    game.ai_run()


if __name__ == "__main__":
    globals()[sys.argv[1]]()
