"""Fast regression checks; the staging CLI also compiles the complete bank."""
import json
import unittest
from types import SimpleNamespace
from unittest.mock import patch
from manitoba_typst_conversion import clean, convert_many, prepare, apply_reviewed_overrides


class ConversionTests(unittest.TestCase):
    def converted(self, text):
        return patch('manitoba_typst_conversion.subprocess.run', return_value=SimpleNamespace(stdout=json.dumps([{'text': text}])))

    def test_no_silent_latex_fallback(self):
        with self.converted(r'$\frac{1}{2}$'):
            with self.assertRaisesRegex(RuntimeError, 'LaTeX command remains'):
                convert_many(['input'])

    def test_typst_escaped_delimiters_are_preserved(self):
        text = r'$\(x + 1\)$'
        with self.converted(text):
            self.assertEqual(convert_many(['input']), [text])

    def test_wasm_error_is_not_published(self):
        result = SimpleNamespace(stdout=json.dumps([{'error': 'unreachable'}]))
        with patch('manitoba_typst_conversion.subprocess.run', return_value=result):
            with self.assertRaisesRegex(RuntimeError, 'MiTeX conversion failed'):
                convert_many(['input'])

    def test_alignment_keeps_escaped_parentheses(self):
        self.assertEqual(clean(r'$aligned(x &= \(1\))$'), r'$x &= \(1\)$')

    def test_inline_equation_and_decimal(self):
        self.assertEqual(clean('#math.equation(block: false, $1 . 2 3$);'), '$1.23$')

    def test_native_helpers(self):
        self.assertEqual(clean('$mitexsqrt(x)$'), '$sqrt(x)$')
        self.assertEqual(clean(r'$mitexsqrt(\[3\],x)$'), '$root(3,x)$')
        self.assertEqual(clean('$mitexarray(arg0: cc, x,y;z,w)$'), '$mat(delim: #none,  x,y;z,w)$')

    def test_table_hint_removed(self):
        self.assertNotIn('[t]', prepare(r'\begin{tabular}[t]{cc}a&b\\\end{tabular}'))

    def test_editorial_override_keeps_original(self):
        doc = {'text': '', 'extensions': {'latexSource': 'original'}}
        package = {'questions': [{'id': 'mb-pc40s-2013-jan-q32', 'content': {'solution': doc}}]}
        apply_reviewed_overrides(package)
        self.assertTrue(doc['text'])
        self.assertEqual(doc['format'], 'typst')
        self.assertEqual(doc['extensions']['latexSource'], 'original')
        self.assertEqual(doc['extensions']['source'], 'editorial-repair')


if __name__ == '__main__':
    unittest.main()
