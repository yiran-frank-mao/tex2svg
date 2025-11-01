import subprocess
import tempfile
import os

def latex_to_svg(latex_snippet):
    """
    Converts a LaTeX snippet to an SVG image.

    Args:
        latex_snippet: The LaTeX code to be converted.

    Returns:
        The SVG content as a string.
    """
    with open('template.tex', 'r') as f:
        template = f.read()

    latex_code = template.replace('%{INPUTS}', latex_snippet)

    with tempfile.TemporaryDirectory() as tempdir:
        tex_filepath = os.path.join(tempdir, 'input.tex')
        with open(tex_filepath, 'w') as f:
            f.write(latex_code)

        # Compile LaTeX to PDF
        process = subprocess.run(
            ['pdflatex', '-interaction=nonstopmode', '-output-directory', tempdir, tex_filepath],
            capture_output=True,
            text=True
        )

        if process.returncode != 0:
            raise RuntimeError(f"pdflatex failed: {process.stderr}\\n{process.stdout}")

        pdf_filepath = os.path.join(tempdir, 'input.pdf')
        svg_filepath = os.path.join(tempdir, 'output.svg')

        # Convert PDF to SVG
        process = subprocess.run(
            ['pdf2svg', pdf_filepath, svg_filepath],
            capture_output=True,
            text=True
        )

        if process.returncode != 0:
            raise RuntimeError(f"pdf2svg failed: {process.stderr}")

        with open(svg_filepath, 'r') as f:
            svg_content = f.read()

    return svg_content

def test_latex_to_svg():
    """
    Tests the latex_to_svg function.
    """
    tikz_code = r"""
\begin{tikzcd}
    A \arrow[r, "f"] \arrow[d, "g"'] & B \arrow[d, "h"] \\
    C \arrow[r, "k"'] & D
\end{tikzcd}
"""
    try:
        svg_output = latex_to_svg(tikz_code)
        assert svg_output.strip().startswith('<?xml')
        assert svg_output.strip().endswith('</svg>')
        with open('output.svg', 'w') as f:
            f.write(svg_output)
        print("Test passed: Successfully generated output.svg")
    except (RuntimeError, AssertionError) as e:
        print(f"Test failed: {repr(e)}")

if __name__ == '__main__':
    test_latex_to_svg()
