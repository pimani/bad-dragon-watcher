"""Enum for bad-dragon toy hardness."""
from option import Option

ConditionSet = {  # Set creation.
    Option("unknown", "UNKNOWN", "unknown"),
    Option("ready_made", "READY_MADE", "ready_made"),
    Option("flop", "FLOP", "flop")
}
