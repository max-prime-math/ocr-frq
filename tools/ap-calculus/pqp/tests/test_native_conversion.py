"""Regression checks for content-preserving native AP prompt conversion."""
from pathlib import Path
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import re

from build_native_typst_candidates import compile_body, convert_many, prepare, safe_clean, tidy


class NativeConversionTests(unittest.TestCase):
    def convert(self, source):
        source, replacements = prepare(source, [])
        self.assertFalse(replacements)
        result = safe_clean(convert_many([source])[0])
        self.assertIsNone(compile_body(result, []), result)
        return result

    def test_grouped_square_root_is_not_simplified(self):
        body = self.convert(r'$\left(\sqrt{x}\right)^2$')
        self.assertIn('sqrt(', body)
        self.assertIn('^(2)', body)
        self.assertIn('lr(', body)

    def test_nested_and_indexed_roots(self):
        body = self.convert(r'$\sqrt{1+\sqrt{x}}+\sqrt[3]{x}$')
        self.assertEqual(body.count('sqrt('), 2)
        self.assertIn('root(3,', body)

    def test_substack_preserves_both_conditions(self):
        body = self.convert(r'$\lim_{\substack{x \to 0 \\ x>0}} f(x)$')
        self.assertIn('mat(delim: #none,', body)
        self.assertIn('->', body)
        self.assertIn('x > 0', body)
        self.assertIn(';', body)

    def test_native_table_retains_values_and_avoids_hardbreaks(self):
        body = self.convert(r'\begin{tabular}{c|c} $x$ & $f(x)$ \\ \hline 0 & 1 \\ 2 & 3 \end{tabular}')
        self.assertIn('#table(', body)
        for value in range(4):
            self.assertIn(f'[{value}]', body)
        self.assertNotIn('[]', body)
        self.assertNotIn('\n', body)

    def test_subpart_labels_survive_list_wrappers(self):
        body = self.convert(r'\begin{enumerate}\item[(a)] Find $f(0)$.\item[(b)] Explain.\end{enumerate}')
        self.assertIn('(a) Find', body)
        self.assertIn('(b) Explain.', body)

    def test_image_requires_declared_source(self):
        with self.assertRaisesRegex(ValueError, 'Unresolved OCR image'):
            prepare(r'\includegraphics{missing.png}', [])
        raw, replacements = prepare(r'Before \includegraphics{diagram.png} after.', [{'name': 'diagram.png', 'path': '/tmp/diagram.png'}])
        self.assertEqual(len(replacements), 1)
        self.assertIn('/imgs/diagram.png', next(iter(replacements.values())))
        self.assertIn(next(iter(replacements)), raw)
        self.assertIn('Before', raw)
        self.assertIn('after.', raw)

    def test_spatial_subparts_get_paragraphs_but_inline_references_do_not(self):
        body = self.convert('Let $f(x)=x^2$.\n(a) Find $f(0)$.\n(b) Explain the answer in part (a).')
        self.assertIn('\n\n(a) Find', body)
        self.assertIn('\n\n(b) Explain', body)
        self.assertIn('part (a).', body)
        self.assertEqual(body.count('\n\n'), 2)

    def test_terminal_layout_break_cannot_escape_testgen_wrapper(self):
        original = 'Find the area.\\'
        self.assertIsNotNone(compile_body(original, []))
        cleaned = safe_clean(original)
        self.assertEqual(cleaned, 'Find the area.')
        self.assertIsNone(compile_body(cleaned, []))
        self.assertEqual(safe_clean('A literal slash: \\\\'), 'A literal slash: \\\\')

    def test_table_row_terminator_cell_and_repeated_rules_are_dropped(self):
        body = self.convert('\\begin{tabular}{|c|c|}\n\\hline $x$ & 1 \\\\\n\\hline $y$ & 2 \\\\\n\\hline\n\\end{tabular}')
        cells = re.findall(r'\[[^\]]*\]', body.split('columns', 1)[1])
        self.assertEqual(len(cells), 4, body)
        self.assertNotRegex(body, r'(table\.hline\([^)]*\)), \1')

    def test_wrapped_header_cell_is_one_label(self):
        body = self.convert(r'\begin{tabular}{|c|c|}\hline\begin{tabular}{c}$t$ \\ (minutes) \\\end{tabular} & 0 \\\hline\end{tabular}')
        self.assertIn('[$t$ (minutes)]', body)
        self.assertEqual(body.count('#table('), 1)

    def test_table_is_its_own_paragraph(self):
        body = self.convert('\\begin{tabular}{c|c} 0 & 1 \\end{tabular}\nThe table above gives values.')
        self.assertIn(');\n\nThe table above', body)

    def test_exam_logistics_are_removed_but_math_notes_kept(self):
        body = self.convert('Sketch it. (Note: Use the axes provided in the pink test booklet.) (Note: The volume of a cone is $V$.)\n(a) Go. Write your responses to this question only on the designated pages in the separate Free Response booklet. Write your solution to each part in the space provided for that part.')
        self.assertNotIn('booklet', body)
        self.assertIn('(Note: The volume of a cone is $V$.)', body)
        self.assertTrue(body.endswith('(a) Go.'), body)

    def test_math_spacing_and_primes_are_tidied_without_changing_calls(self):
        body = self.convert(r"$f^{\prime}(x) + g^{\prime \prime}(2) + \sin (x) + 3 \cdot (x+1)$")
        self.assertIn("f'(x)", body)
        self.assertIn("g''(2)", body)
        self.assertIn('sin(x)', body)
        self.assertNotIn('dot(', body)

    def test_script_parentheses_stay_escaped(self):
        self.assertIn(r'^\(', tidy(r'$e^\(x \)$'))
        self.assertEqual(tidy(r'$f \(x \)$'), '$f(x)$')

    def test_prose_escapes_removed_except_before_minus(self):
        self.assertEqual(tidy(r'On \(-5, 4\)\, see \(a\)\; ft\/sec costs dollar 15.'), r'On \(-5, 4), see (a); ft/sec costs \$15.')
        self.assertEqual(tidy('is $dollar 11$ and $dollar 0.05 $.'), r'is \$11 and \$0.05.')

    def test_figure_caption_becomes_its_own_paragraph(self):
        self.assertEqual(tidy('Graph of $f$\\ The figure above shows $f$.'), 'Graph of $f$\n\nThe figure above shows $f$.')

    def test_tidy_is_idempotent(self):
        body = self.convert(r'\begin{tabular}{c|c} $x$ & $f(x)$ \\ \hline 0 & 1 \\ \end{tabular} Let $f^{\prime}(x)=\sin (x)$.')
        self.assertEqual(tidy(body), body)

    def test_roman_numeral_items_get_line_breaks(self):
        body = self.convert('Requirements.\n(i) First is 0 , and more.\n(ii) Second is 1 .\n(a) Find it.')
        self.assertIn('Requirements.\\ (i) First is 0, and more.\\ (ii) Second is 1.', body)
        self.assertIn('\n\n(a) Find it.', body)


if __name__ == '__main__':
    unittest.main()
