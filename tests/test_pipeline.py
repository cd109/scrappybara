import unittest

from scrappybara.pipeline.pipeline import Pipeline

_PIPE = Pipeline()


class TestPipeline(unittest.TestCase):

    def test_chunk_nouns(self):
        text = 'Infant mortality is low.'

        stuples = _PIPE([text])[0].stuples
        stuple_strs = [str(stuple) for stuple in stuples]
        self.assertTrue('NCA(infant mortality, be, low)' in stuple_strs)
        self.assertFalse('NCA(mortality, be, low)' in stuple_strs)

        stuples = _PIPE([text], chunk_common_nouns=False)[0].stuples
        stuple_strs = [str(stuple) for stuple in stuples]
        self.assertFalse('NCA(infant mortality, be, low)' in stuple_strs)
        self.assertTrue('NCA(mortality, be, low)' in stuple_strs)

    def test_empty_list(self):
        self.assertListEqual([], _PIPE([]))

    def test_empty_texts(self):
        self.assertListEqual([], _PIPE([''])[0].stuples)
        self.assertListEqual([], _PIPE(['', '', ''])[1].stuples)
        self.assertListEqual([], _PIPE(['', 'Infant mortality is low.', ''])[0].stuples)
        self.assertListEqual([], _PIPE(['', 'Infant mortality is low.', ''])[2].stuples)
        self.assertEqual(1, len(_PIPE(['', 'Infant mortality is low.', ''])[1].stuples))
        self.assertEqual(1, len(_PIPE(['Infant mortality is low.', '', ''])[0].stuples))


if __name__ == '__main__':
    unittest.main()
