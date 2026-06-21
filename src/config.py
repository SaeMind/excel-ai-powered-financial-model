"""Configuration helpers for the financial model."""

from __future__ import annotations

import os
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path


@dataclass(frozen=True)
class ModelConfig:
    """Runtime configuration for model generation.

    Attributes:
        output_dir: Directory where timestamped outputs are written.
        timestamp: Timestamp suffix for generated output files.
    """

    output_dir: Path
    timestamp: str

    @classmethod
    def from_env(cls, output_dir: str | None = None) -> "ModelConfig":
        """Build configuration from arguments and environment variables.

        Parameters:
            output_dir: Optional output directory override.

        Returns:
            ModelConfig with resolved output path and timestamp.
        """
        resolved_output_dir = Path(output_dir or os.getenv("OUTPUT_DIR", "outputs"))
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        return cls(output_dir=resolved_output_dir, timestamp=timestamp)

    def output_path(self, stem: str, suffix: str) -> Path:
        """Create a timestamped output path.

        Parameters:
            stem: File name stem.
            suffix: File extension including leading dot.

        Returns:
            Path in the configured output directory.
        """
        return self.output_dir / f"{stem}_{self.timestamp}{suffix}"
