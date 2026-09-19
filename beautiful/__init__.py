"""beautiful — a mathematical beauty score (1..100) for any image, from pixels alone."""
from .core import beauty, beauty_score, WEIGHTS, MODES
from .symmetry import symmetry_score, symmetry_report

__all__ = ["beauty", "beauty_score", "symmetry_score", "symmetry_report", "WEIGHTS", "MODES"]
__version__ = "0.4.1"
