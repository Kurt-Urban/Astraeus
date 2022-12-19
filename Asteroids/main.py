from Asteroids import game_logic as ast


def human():
    game = ast.AsteroidsGame()
    game.run()


def ai_game() -> ast.AsteroidsGame:
    return ast.AsteroidsGame()
