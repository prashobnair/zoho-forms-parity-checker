import copy
import json
import unittest
from pathlib import Path
from parity import evaluate, compare

SPEC = json.loads(Path(__file__).with_name('examples.json').read_text())

class ParityTests(unittest.TestCase):
    def test_expected_one_mismatch(self):
        report = compare(SPEC)
        self.assertFalse(report['all_pass'])
        self.assertEqual([True, False, True], [c['pass'] for c in report['cases']])
        self.assertEqual('600', report['cases'][1]['source']['output']['estimate'])
        self.assertEqual('203', report['cases'][1]['target']['output']['estimate'])
        self.assertEqual(0, report['form_submissions'])

    def test_corrected_target_passes(self):
        spec = copy.deepcopy(SPEC)
        spec['target_fields'][4]['operation'] = 'multiply'
        self.assertTrue(compare(spec)['all_pass'])

    def test_hidden_required_not_triggered(self):
        result = evaluate(SPEC['source_fields'], {'service':'delivery','seats':1,'rate':2,'name':'X'})
        self.assertNotIn('details', result['output'])
        self.assertEqual([], result['issues'])

    def test_visible_required_fails(self):
        result = evaluate(SPEC['source_fields'], {'service':'audit','name':'X'})
        self.assertIn({'field':'details','code':'required_missing'}, result['issues'])

    def test_invalid_choice(self):
        result = evaluate(SPEC['source_fields'], {'service':'other','name':'X'})
        self.assertIn({'field':'service','code':'invalid_choice'}, result['issues'])

    def test_duplicate_field_rejected(self):
        with self.assertRaises(ValueError):
            evaluate([SPEC['source_fields'][0],SPEC['source_fields'][0]], {})

if __name__ == '__main__':
    unittest.main()
