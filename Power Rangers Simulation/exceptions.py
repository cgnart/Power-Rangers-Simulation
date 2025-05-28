"""
Custom exceptions for the Power Rangers Enhanced Game
"""

class GameException(Exception):
    """Base exception for all game-related errors"""
    pass

class InvalidMove(GameException):
    """Raised when player attempts an invalid move"""
    pass

class InsufficientFunds(GameException):
    """Raised when player doesn't have enough gold for a transaction"""
    pass

class MarketException(GameException):
    """Raised when there's an error in the stock market system"""
    pass

class SaveError(GameException):
    """Raised when there's an error saving the game"""
    pass

class LoadError(GameException):
    """Raised when there's an error loading the game"""
    pass

class SkillError(GameException):
    """Raised when there's an error with skill usage"""
    pass

class BattleException(GameException):
    """Raised when there's an error in the battle system"""
    pass

class CharacterException(GameException):
    """Raised when there's an error with character operations"""
    pass

class MissionException(GameException):
    """Raised when there's an error with mission operations"""
    pass
