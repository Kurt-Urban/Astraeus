from Asteroids import game_logic as ast


def human():
    game = ast.AsteroidsGame()
    game.run()


def ai():
    game = ast.AsteroidsGame()
    game.ai_run()
