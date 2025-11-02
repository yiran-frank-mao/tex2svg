import unittest
from main import latex_to_svg

class TestLatexToSvg(unittest.TestCase):
    def test_simple_lambda(self):
        """
        Tests that a simple lambda expression is correctly converted to an SVG.
        """
        latex_snippet = r"$\lambda$"
        svg_output = latex_to_svg(latex_snippet)
        self.assertTrue(svg_output.strip().startswith('<?xml'))
        self.assertTrue(svg_output.strip().endswith('</svg>'))

if __name__ == '__main__':
    unittest.main()
