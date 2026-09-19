"""beautiful — a mathematical beauty number (1..100) for any image, from pixels alone."""
from .core import beauty, beauty_score, WEIGHTS
from .symmetry import symmetry_score, symmetry_report

__all__ = ["beauty", "beauty_score", "symmetry_score", "symmetry_report", "WEIGHTS"]
__version__ = "0.1.0"
