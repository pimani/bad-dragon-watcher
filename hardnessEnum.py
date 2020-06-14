"""Enum for bad-dragon toy hardness."""
from option import Option

HardnessSet = {  # Set creation.
    Option("2", "Extra Soft", "e"),
    Option("3", "Soft", "s"),
    Option("5", "Medium", "m"),
    Option("8", "Firm", "f"),
    Option("3/5", "Soft Shaft, Medium Base", "sm"),
    Option("3/8", "Soft Shaft, Firm Base", "sf"),
    Option("5/3", "Medium Shaft, Soft Base", "ms"),
    Option("5/8", "Med Shaft, Firm Base", "mf"),
    Option("8/3", "Firm Shaft, Soft Base", "fs"),
    Option("8/5", "Firm Shaft, Medium Base", "fm")
}
