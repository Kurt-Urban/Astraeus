from Asteroids import game_logic as ast
import sys


def human():
    game = ast.AsteroidsGame(False)
    game.run()


def ai():
    pass


if __name__ == "__main__":
    globals()[sys.argv[1]]()
