import os
from datetime import datetime


class ExportUtils:

    def __init__(self):
        """Create export folder"""
        self.output_dir = "exports"
        os.makedirs(self.output_dir, exist_ok=True)

    def export_solution(self, equation, steps, final_answer):
        """
        Export solution to TXT file
        """

        filename = f"{self.output_dir}/solution_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"

        with open(filename, "w", encoding="utf-8") as file:

            file.write("AI Math Tutor Solution\n")
            file.write("=" * 40 + "\n\n")

            file.write(f"Equation:\n{equation}\n\n")

            file.write("Step-by-Step Solution:\n")
            file.write("-" * 30 + "\n")

            if isinstance(steps, list):
                for step in steps:
                    file.write(str(step) + "\n")

            file.write("\nFinal Answer:\n")
            file.write(str(final_answer) + "\n")

        return filename