import unittest

from scrappybara.langmodel.language_model import LanguageModel
from scrappybara.pipeline.logic_pipeline import LogicPipeline

_PIPE = LogicPipeline(LanguageModel(1, 1))


def _strs(sample):
    stuples = _PIPE.test_sample(sample)
    return [str(stuple) for stuple in stuples]


class TestLogicPipeline(unittest.TestCase):

    def test_1(self):
        # In the last scene , Tamara drops her skepticism toward Sasha and allows him to fall asleep with his head
        # resting on her lap .
        sample = [('In', 'PREP', 'MARK', 3), ('the', 'DET', 'ART', 3), ('last', 'ADJ', 'CPL', 3),
                  ('scene', 'NOUN', 'CPL', 6), (',', 'PUNCT', 'NODEP', -1), ('Tamara', 'PROPN', 'SUBJ', 6),
                  ('drops', 'VERB', 'ROOT', -1), ('her', 'DET', 'ART', 8), ('skepticism', 'NOUN', 'OBJ', 6),
                  ('toward', 'PREP', 'MARK', 10), ('Sasha', 'PROPN', 'CPL', 8), ('and', 'CONJ', 'NODEP', -1),
                  ('allows', 'VERB', 'AND', 6), ('him', 'PRON', 'SUBJ', 15), ('to', 'FRAG', 'PART', 15),
                  ('fall', 'VERB', 'OBJ', 12), ('asleep', 'FRAG', 'PART', 15), ('with', 'PREP', 'MARK', 20),
                  ('his', 'DET', 'ART', 19), ('head', 'NOUN', 'SUBJ', 20), ('resting', 'VERB', 'CPL', 15),
                  ('on', 'PREP', 'MARK', 23), ('her', 'DET', 'ART', 23), ('lap', 'NOUN', 'CPL', 20),
                  ('.', 'PUNCT', 'NODEP', -1)]
        # print(_strs(sample))
        self.assertCountEqual([
            'NCA(scene, be, last)',
            'PTN(tamara, drop, skepticism)',
            'NCL(skepticism, be, dropped)',
            'PTOI(tamara, allow, he, fall asleep)',
            'NI(head, rest)'
        ], _strs(sample))

    def test_2(self):
        # Everyone avoids and hates him .
        sample = [('-', 'PUNCT', 'NODEP', -1), ('Everyone', 'PRON', 'SUBJ', 2), ('avoids', 'VERB', 'ROOT', -1),
                  ('and', 'CONJ', 'NODEP', -1), ('hates', 'VERB', 'AND', 2), ('him', 'PRON', 'OBJ', 2),
                  ('.', 'PUNCT', 'NODEP', -1)]
        # print(_strs(sample))
        self.assertCountEqual([
            'OTO(everyone, avoid, he)',
            'OCL(he, be, avoided)',
            'OTO(everyone, hate, he)',
            'OCL(he, be, hated)'
        ], _strs(sample))

    def test_3(self):
        # But do n't confuse Whodom with obscurity or viral fame .
        sample = [('But', 'CONJ', 'MARK', 3), ('do', 'MAT', 'AUX', 3), ("n't", 'ADV', 'NEG', 3),
                  ('confuse', 'VERB', 'ROOT', -1), ('Whodom', 'PROPN', 'OBJ', 3), ('with', 'FRAG', 'PART', 3),
                  ('obscurity', 'NOUN', 'IOBJ', 3), ('or', 'CONJ', 'NODEP', -1), ('viral', 'ADJ', 'CPL', 9),
                  ('fame', 'NOUN', 'OR', 6), ('.', 'PUNCT', 'NODEP', -1)]
        # print(_strs(sample))
        self.assertCountEqual([
            'PCL(whodom, NOT be, confused with)',
            'NCA(fame, be, viral)'
        ], _strs(sample))

    def test_4(self):
        # Are n't you apologetic at all , Harry ?
        sample = [('Are', 'VERB', 'ROOT', -1), ("n't", 'ADV', 'NEG', 0), ('you', 'PRON', 'SUBJ', 0),
                  ('apologetic', 'ADJ', 'PROP', 0), ('at', 'ADV', 'CPL', 3), ('all', 'ADV', 'FLAT', 4),
                  (',', 'PUNCT', 'NODEP', -1), ('Harry', 'PROPN', 'CALLEE', 0), ('?', 'PUNCT', 'NODEP', -1)]
        # print(_strs(sample))
        self.assertCountEqual([
            'OCA(you, NOT be, apologetic)',
        ], _strs(sample))

    def test_5(self):
        # Lock up your sleepless portals .
        sample = [('Lock', 'VERB', 'ROOT', -1), ('up', 'FRAG', 'PART', 0), ('your', 'DET', 'ART', 4),
                  ('sleepless', 'ADJ', 'CPL', 4), ('portals', 'NOUN', 'OBJ', 0), ('.', 'PUNCT', 'NODEP', -1)]
        # print(_strs(sample))
        self.assertCountEqual([
            'NCA(portal, be, sleepless)',
            'NCL(portal, be, locked up)'
        ], _strs(sample))

    def test_6(self):
        # The things i did to you were beyond inexcusable .
        sample = [('The', 'DET', 'ART', 1), ('things', 'NOUN', 'SUBJ', 6), ('i', 'PRON', 'SUBJ', 3),
                  ('did', 'VERB', 'CPL', 1), ('to', 'PREP', 'MARK', 5), ('you', 'PRON', 'CPL', 3),
                  ('were', 'VERB', 'ROOT', -1), ('beyond', 'ADV', 'CPL', 8), ('inexcusable', 'ADJ', 'PROP', 6),
                  ('.', 'PUNCT', 'NODEP', -1)]
        # print(_strs(sample))
        self.assertCountEqual([
            'NCA(thing, be, inexcusable)',
            'OTN(i, do, thing)',
            'NCL(thing, be, done)'
        ], _strs(sample))

    def test_7(self):
        # I made her swim .
        sample = [('I', 'PRON', 'SUBJ', 1), ('made', 'VERB', 'ROOT', -1), ('her', 'PRON', 'SUBJ', 3),
                  ('swim', 'VERB', 'OBJ', 1), ('.', 'PUNCT', 'NODEP', -1)]
        # print(_strs(sample))
        self.assertCountEqual([
            'OTOI(i, make, she, swim)',
        ], _strs(sample))

    def test_8(self):
        # The insurance company will pay at least 175 .
        sample = [('The', 'DET', 'ART', 2), ('insurance', 'NOUN', 'CPL', 2), ('company', 'NOUN', 'SUBJ', 4),
                  ('will', 'MAT', 'AUX', 4), ('pay', 'VERB', 'ROOT', -1), ('at', 'ADV', 'CPL', 7),
                  ('least', 'ADV', 'FLAT', 5), ('175', 'NUM', 'OBJ', 4), ('.', 'PUNCT', 'NODEP', -1)]
        # print(_strs(sample))
        self.assertCountEqual([
            'NTU(insurance company, pay, 175)',
            'UCL(175, be, paid)'
        ], _strs(sample))

    def test_9(self):
        # Does Tar Sand Oil Increase the Risk of Pipeline Spills ?
        sample = [('Does', 'MAT', 'AUX', 4), ('Tar', 'NOUN', 'CPL', 2), ('Sand', 'NOUN', 'CPL', 3),
                  ('Oil', 'NOUN', 'SUBJ', 4), ('Increase', 'VERB', 'ROOT', -1), ('the', 'DET', 'ART', 6),
                  ('Risk', 'NOUN', 'OBJ', 4), ('of', 'PREP', 'MARK', 9), ('Pipeline', 'NOUN', 'CPL', 9),
                  ('Spills', 'NOUN', 'CPL', 6), ('?', 'PUNCT', 'NODEP', -1)]
        # print(_strs(sample))
        self.assertCountEqual([
            'NTN(tar sand oil, increase, risk)',
            'NCL(risk, be, increased)'
        ], _strs(sample))

    def test_10(self):
        # Heritage Auctions will offer the 1951 Fender Guitar Sunday .
        sample = [('Heritage', 'PROPN', 'SUBJ', 3), ('Auctions', 'PROPN', 'FLAT', 0), ('will', 'MAT', 'AUX', 3),
                  ('offer', 'VERB', 'ROOT', -1), ('the', 'DET', 'ART', 7), ('1951', 'NUM', 'CPL', 7),
                  ('Fender', 'PROPN', 'CPL', 7), ('guitar', 'NOUN', 'OBJ', 3), ('Sunday', 'PROPN', 'CPL', 3),
                  ('.', 'PUNCT', 'NODEP', -1)]
        # print(_strs(sample))
        self.assertCountEqual([
            'PTN(heritage auctions, offer, 1951 fender guitar)',
            'NCL(1951 fender guitar, be, offered)'
        ], _strs(sample))

    def test_11(self):
        # Call me Brandon .
        sample = [('Call', 'VERB', 'ROOT', -1), ('me', 'PRON', 'OBJ', 0), ('Brandon', 'PROPN', 'IPROP', 0),
                  ('.', 'PUNCT', 'NODEP', -1)]
        # print(_strs(sample))
        self.assertCountEqual([
            'OCP(i, be called, brandon)'
        ], _strs(sample))

    def test_12(self):
        # They call them light sabers .
        sample = [('They', 'PRON', 'SUBJ', 1), ('call', 'VERB', 'ROOT', -1), ('them', 'PRON', 'OBJ', 1),
                  ('light', 'NOUN', 'CPL', 4), ('sabers', 'NOUN', 'IPROP', 1), ('.', 'PUNCT', 'NODEP', -1)]
        # print(_strs(sample))
        self.assertCountEqual([
            'OCN(they, be called, light saber)'
        ], _strs(sample))

    def test_13(self):
        # Paul is as nice as John .
        sample = [('Paul', 'PROPN', 'SUBJ', 1), ('is', 'VERB', 'ROOT', -1), ('as', 'ADV', 'CPL', 3),
                  ('nice', 'ADJ', 'PROP', 1), ('as', 'PREP', 'CMARK', 5), ('John', 'PROPN', 'CPL', 3),
                  ('.', 'PUNCT', 'NODEP', -1)]
        # print(_strs(sample))
        self.assertCountEqual([
            'PCA(paul, be, nice)',
            'PCA(john, be, nice)'
        ], _strs(sample))

    def test_14(self):
        # My computer is as powerful as hers , if not more .
        sample = [('My', 'DET', 'ART', 1), ('computer', 'NOUN', 'SUBJ', 2), ('is', 'VERB', 'ROOT', -1),
                  ('as', 'ADV', 'CPL', 4), ('powerful', 'ADJ', 'PROP', 2), ('as', 'PREP', 'CMARK', 6),
                  ('hers', 'PRON', 'CPL', 4), (',', 'PUNCT', 'NODEP', -1), ('if', 'ADV', 'CPL', 4),
                  ('not', 'ADV', 'FLAT', 8), ('more', 'ADV', 'FLAT', 9), ('.', 'PUNCT', 'NODEP', -1)]
        # print(_strs(sample))
        self.assertCountEqual([
            'NCA(computer, be, powerful)',
            'OCA(hers, be, powerful)'
        ], _strs(sample))

    def test_15(self):
        # Are you affected by the collapse of Carillion ?
        sample = [('Are', 'VERB', 'ROOT', -1), ('you', 'PRON', 'SUBJ', 0), ('affected', 'ADJ', 'PROP', 0),
                  ('by', 'PREP', 'MARK', 5), ('the', 'DET', 'ART', 5), ('collapse', 'NOUN', 'CPL', 2),
                  ('of', 'PREP', 'MARK', 7), ('Carillion', 'PROPN', 'CPL', 5), ('?', 'PUNCT', 'NODEP', -1)]
        # print(_strs(sample))
        self.assertCountEqual([
            'OCL(you, be, affected)',
            'NTO(collapse, affect, you)'
        ], _strs(sample))

    def test_16(self):
        # Children have had limbs amputated because of cluster bombs .
        sample = [('Children', 'NOUN', 'SUBJ', 2), ('have', 'MAT', 'AUX', 2), ('had', 'VERB', 'ROOT', -1),
                  ('limbs', 'NOUN', 'OBJ', 2), ('amputated', 'ADJ', 'CPL', 3), ('because', 'PREP', 'MARK', 8),
                  ('of', 'PREP', 'FLAT', 5), ('cluster', 'NOUN', 'CPL', 8), ('bombs', 'NOUN', 'CPL', 4),
                  ('.', 'PUNCT', 'NODEP', -1)]
        # print(_strs(sample))
        self.assertCountEqual([
            'NTN(child, have, limb)',
            'NCL(limb, be, amputated)'
        ], _strs(sample))

    def test_17(self):
        # In May , 2017 , a twenty two year old Dutch entrepreneur named Boyan Slat unveiled a contraption that
        # he believed would rid the oceans of plastic .
        sample = [('In', 'PREP', 'MARK', 1), ('May', 'PROPN', 'CPL', 15), (',', 'PUNCT', 'NODEP', -1),
                  ('2017', 'NUM', 'CPL', 1), (',', 'PUNCT', 'NODEP', -1), ('a', 'DET', 'ART', 11),
                  ('twenty', 'NUM', 'ART', 8), ('two', 'NUM', 'AND', 6), ('year', 'NOUN', 'CPL', 9),
                  ('old', 'ADJ', 'CPL', 10), ('Dutch', 'ADJ', 'CPL', 11), ('entrepreneur', 'NOUN', 'SUBJ', 15),
                  ('named', 'ADJ', 'CPL', 11), ('Boyan', 'PROPN', 'PROP', 12), ('Slat', 'PROPN', 'FLAT', 13),
                  ('unveiled', 'VERB', 'ROOT', -1), ('a', 'DET', 'ART', 17), ('contraption', 'NOUN', 'OBJ', 15),
                  ('that', 'PRON', 'SUBJ', 22), ('he', 'PRON', 'SUBJ', 20), ('believed', 'VERB', 'CPL', 22),
                  ('would', 'MAT', 'MODAL', 22), ('rid', 'VERB', 'CPL', 17), ('the', 'DET', 'ART', 24),
                  ('oceans', 'NOUN', 'OBJ', 22), ('of', 'PREP', 'MARK', 26), ('plastic', 'NOUN', 'CPL', 22),
                  ('.', 'PUNCT', 'NODEP', -1)]
        # print(_strs(sample))
        self.assertCountEqual([
            'NCA(entrepreneur, be, dutch)',
            'NCL(entrepreneur, be, named)',
            'NCP(entrepreneur, be named, boyan slat)',
            'NTN(entrepreneur, unveil, contraption)',
            'NCL(contraption, be, unveiled)',
            'OI(he, believe)',
            'NTN(contraption, rid, ocean)',
            'NCL(ocean, be, rid)',
        ], _strs(sample))

    def test_18(self):
        # I think the strength and power that I bring at this weight overwhelms a lot of people .
        sample = [('I', 'PRON', 'SUBJ', 1), ('think', 'VERB', 'ROOT', -1), ('the', 'DET', 'ART', 3),
                  ('strength', 'NOUN', 'SUBJ', 12), ('and', 'CONJ', 'NODEP', -1), ('power', 'NOUN', 'AND', 3),
                  ('that', 'PRON', 'OBJ', 8), ('I', 'PRON', 'SUBJ', 8), ('bring', 'VERB', 'CPL', 3),
                  ('at', 'PREP', 'MARK', 11), ('this', 'DET', 'ART', 11), ('weight', 'NOUN', 'CPL', 8),
                  ('overwhelms', 'VERB', 'OBJ', 1), ('a', 'DET', 'ART', 14), ('lot', 'DET', 'ART', 16),
                  ('of', 'PREP', 'MARK', 14), ('people', 'NOUN', 'OBJ', 12), ('.', 'PUNCT', 'NODEP', -1)]
        # print(_strs(sample))
        self.assertCountEqual([
            'OTN(i, bring, strength)',
            'NCL(strength, be, brought)',
            'OTN(i, bring, power)',
            'NCL(power, be, brought)',
            'OTNTN(i, think, strength, overwhelm, people)',
            'OTNTN(i, think, power, overwhelm, people)',
            'NCL(people, be, overwhelmed)',
        ], _strs(sample))

    def test_19(self):
        # The hive takes care of itself .
        sample = [('The', 'DET', 'ART', 1), ('hive', 'NOUN', 'SUBJ', 2), ('takes', 'VERB', 'ROOT', -1),
                  ('care', 'FRAG', 'PART', 2), ('of', 'FRAG', 'PART', 2), ('itself', 'PRON', 'OBJ', 2),
                  ('.', 'PUNCT', 'NODEP', -1)]
        # print(_strs(sample))
        self.assertCountEqual([
            'NTN(hive, take care of, hive)',
            'NCL(hive, be, taken care of)'
        ], _strs(sample))

    def test_20(self):
        # - Why is Robbie 's zipper down ?
        sample = [('-', 'PUNCT', 'NODEP', -1), ('Why', 'ADV', 'CPL', 2), ('is', 'VERB', 'ROOT', -1),
                  ('Robbie', 'PROPN', 'CPL', 5), ("'s", 'PREP', 'MARK', 3), ('zipper', 'NOUN', 'SUBJ', 2),
                  ('down', 'ADV', 'CPL', 2), ('?', 'PUNCT', 'NODEP', -1)]
        # print(_strs(sample))
        self.assertEqual(0, len(_strs(sample)))

    def test_21(self):
        # McCoy immediately ripped off his helmet and was pounding the turf at Hard Rock Stadium
        # as trainers ran out to examine him , though X-rays later were negative .
        sample = [('McCoy', 'PROPN', 'SUBJ', 2), ('immediately', 'ADV', 'CPL', 2), ('ripped', 'VERB', 'ROOT', -1),
                  ('off', 'FRAG', 'PART', 2), ('his', 'DET', 'ART', 5), ('helmet', 'NOUN', 'OBJ', 2),
                  ('and', 'CONJ', 'NODEP', -1), ('was', 'MAT', 'AUX', 8), ('pounding', 'VERB', 'AND', 2),
                  ('the', 'DET', 'ART', 10), ('turf', 'NOUN', 'OBJ', 8), ('at', 'PREP', 'MARK', 12),
                  ('Hard', 'PROPN', 'CPL', 2), ('Rock', 'PROPN', 'FLAT', 12), ('Stadium', 'PROPN', 'FLAT', 13),
                  ('as', 'PREP', 'MARK', 17), ('trainers', 'NOUN', 'SUBJ', 17), ('ran', 'VERB', 'CPL', 2),
                  ('out', 'ADV', 'CPL', 17), ('to', 'FRAG', 'PART', 20), ('examine', 'VERB', 'CPL', 17),
                  ('him', 'PRON', 'OBJ', 20), (',', 'PUNCT', 'NODEP', -1), ('though', 'CONJ', 'MARK', 26),
                  ('X-rays', 'NOUN', 'SUBJ', 26), ('later', 'ADV', 'CPL', 26), ('were', 'VERB', 'CPL', 20),
                  ('negative', 'ADJ', 'PROP', 26), ('.', 'PUNCT', 'NODEP', -1)]
        # print(_strs(sample))
        self.assertCountEqual([
            'PTN(mccoy, rip off, helmet)',
            'NCL(helmet, be, ripped off)',
            'OCL(he, be, examined)',
            'PTN(mccoy, pound, turf)',
            'NCL(turf, be, pounded)',
            'NI(trainer, run)',
            'NCA(x-ray, be, negative)'
        ], _strs(sample))

    def test_22(self):
        # What the Kings did is similar to what happened in 2016
        # as they 've helped shine a light on an important issue related to race and justice .
        sample = [('What', 'PRON', 'OBJ', 3), ('the', 'DET', 'ART', 2), ('Kings', 'PROPN', 'SUBJ', 3),
                  ('did', 'VERB', 'SUBJ', 4), ('is', 'VERB', 'ROOT', -1), ('similar', 'ADJ', 'PROP', 4),
                  ('to', 'PREP', 'MARK', 8), ('what', 'PRON', 'SUBJ', 8), ('happened', 'VERB', 'CPL', 5),
                  ('in', 'PREP', 'MARK', 10), ('2016', 'NUM', 'CPL', 8), ('as', 'PREP', 'MARK', 14),
                  ('they', 'PRON', 'SUBJ', 14), ("'ve", 'MAT', 'AUX', 14), ('helped', 'VERB', 'CPL', 4),
                  ('shine', 'VERB', 'OBJ', 14), ('a', 'DET', 'ART', 17), ('light', 'NOUN', 'OBJ', 15),
                  ('on', 'PREP', 'MARK', 21), ('an', 'DET', 'ART', 21), ('important', 'ADJ', 'CPL', 21),
                  ('issue', 'NOUN', 'CPL', 17), ('related', 'ADJ', 'CPL', 21), ('to', 'PREP', 'MARK', 24),
                  ('race', 'NOUN', 'CPL', 22), ('and', 'CONJ', 'NODEP', -1), ('justice', 'NOUN', 'AND', 24),
                  ('.', 'PUNCT', 'NODEP', -1)]
        # print(_strs(sample))
        self.assertCountEqual([
            'OTOTN(they, help, they, shine, light)',
            'PTO(kings, do, what)',
            'OCL(what, be, done)',
            'OI(what, happen)',
            'NCL(light, be, shone)',
            'NCA(issue, be, important)',
            'NCL(issue, be, related)'
        ], _strs(sample))

    def test_23(self):
        # She broke into the safe and took the money and gold that was stored in there .
        sample = [('She', 'PROPN', 'SUBJ', 1), ('broke', 'VERB', 'ROOT', -1), ('into', 'FRAG', 'PART', 1),
                  ('the', 'DET', 'ART', 4), ('safe', 'NOUN', 'OBJ', 1), ('and', 'CONJ', 'NODEP', -1),
                  ('took', 'VERB', 'AND', 1), ('the', 'DET', 'ART', 8), ('money', 'NOUN', 'OBJ', 6),
                  ('and', 'CONJ', 'NODEP', -1), ('gold', 'NOUN', 'AND', 8), ('that', 'PRON', 'SUBJ', 12),
                  ('was', 'VERB', 'CPL', 8), ('stored', 'ADJ', 'PROP', 12), ('in', 'PREP', 'MARK', 15),
                  ('there', 'ADV', 'CPL', 13), ('.', 'PUNCT', 'NODEP', -1)]
        # print(_strs(sample))
        self.assertCountEqual([
            'PTN(she, break into, safe)',
            'NCL(safe, be, broken into)',
            'PTN(she, take, money)',
            'NCL(money, be, taken)',
            'PTN(she, take, gold)',
            'NCL(gold, be, taken)',
            'NCL(money, be, stored)',
            'NCL(gold, be, stored)'
        ], _strs(sample))

    def test_24(self):
        # " Because used-car dealers are doing well ,
        # I guess that implies they continue to be rivals of used-car operations of new-car dealerships . "
        sample = [('"', 'PUNCT', 'NODEP', -1), ('Because', 'CONJ', 'MARK', 5), ('used-car', 'NOUN', 'CPL', 3),
                  ('dealers', 'NOUN', 'SUBJ', 5), ('are', 'MAT', 'AUX', 5), ('doing', 'VERB', 'CPL', 9),
                  ('well', 'ADV', 'CPL', 5), (',', 'PUNCT', 'NODEP', -1), ('I', 'PRON', 'SUBJ', 9),
                  ('guess', 'VERB', 'ROOT', -1), ('that', 'PRON', 'SUBJ', 11), ('implies', 'VERB', 'OBJ', 9),
                  ('they', 'PRON', 'SUBJ', 13), ('continue', 'VERB', 'OBJ', 11), ('to', 'FRAG', 'PART', 15),
                  ('be', 'VERB', 'OBJ', 13), ('rivals', 'NOUN', 'PROP', 15), ('of', 'PREP', 'MARK', 19),
                  ('used-car', 'NOUN', 'CPL', 19), ('operations', 'NOUN', 'CPL', 16), ('of', 'PREP', 'MARK', 22),
                  ('new-car', 'NOUN', 'CPL', 22), ('dealerships', 'NOUN', 'CPL', 19), ('.', 'PUNCT', 'NODEP', -1),
                  ('"', 'PUNCT', 'NODEP', -1)]
        # print(_strs(sample))
        self.assertCountEqual([
            'OTOCN(they, continue, they, be, rival)'
        ], _strs(sample))

    def test_25(self):
        # People on systems like Facebook are increasingly forming into ' echo chambers ' of those who think alike .
        sample = [('People', 'NOUN', 'SUBJ', 7), ('on', 'PREP', 'MARK', 2), ('systems', 'NOUN', 'CPL', 0),
                  ('like', 'PREP', 'MARK', 4), ('Facebook', 'PROPN', 'CPL', 2), ('are', 'MAT', 'AUX', 7),
                  ('increasingly', 'ADV', 'CPL', 7), ('forming', 'VERB', 'ROOT', -1), ('into', 'PREP', 'MARK', 11),
                  ("'", 'PUNCT', 'NODEP', -1), ('echo', 'NOUN', 'CPL', 11), ('chambers', 'NOUN', 'CPL', 7),
                  ("'", 'CONJ', 'NODEP', -1), ('of', 'PREP', 'MARK', 14), ('those', 'PRON', 'CPL', 11),
                  ('who', 'PRON', 'SUBJ', 16), ('think', 'VERB', 'CPL', 14), ('alike', 'ADV', 'CPL', 16),
                  ('.', 'PUNCT', 'NODEP', -1)]
        # print(_strs(sample))
        self.assertCountEqual([
            'NI(people, form)',
            'OI(those, think)'
        ], _strs(sample))

    def test_26(self):
        # I was looking for a strip joint and wandered into a Writers Guild meeting by mistake .
        sample = [('I', 'PRON', 'SUBJ', 2), ('was', 'MAT', 'AUX', 2), ('looking', 'VERB', 'ROOT', -1),
                  ('for', 'FRAG', 'PART', 2), ('a', 'DET', 'ART', 6), ('strip', 'NOUN', 'CPL', 6),
                  ('joint', 'NOUN', 'OBJ', 2), ('and', 'CONJ', 'NODEP', -1), ('wandered', 'VERB', 'AND', 2),
                  ('into', 'PREP', 'MARK', 13), ('a', 'DET', 'ART', 13), ('Writers', 'PROPN', 'CPL', 13),
                  ('Guild', 'PROPN', 'FLAT', 11), ('meeting', 'NOUN', 'CPL', 8), ('by', 'PREP', 'MARK', 15),
                  ('mistake', 'NOUN', 'CPL', 8), ('.', 'PUNCT', 'NODEP', -1)]
        # print(_strs(sample))
        self.assertCountEqual([
            'OTN(i, look for, strip joint)',
            'NCL(strip joint, be, looked for)',
            'OI(i, wander)'
        ], _strs(sample))

    def test_27(self):
        # I heard myself screaming .
        sample = [('I', 'PRON', 'SUBJ', 1), ('heard', 'VERB', 'ROOT', -1), ('myself', 'PRON', 'SUBJ', 3),
                  ('screaming', 'VERB', 'OBJ', 1), ('.', 'PUNCT', 'NODEP', -1)]
        # print(_strs(sample))
        self.assertCountEqual([
            'OTOI(i, hear, i, scream)'
        ], _strs(sample))

    def test_28(self):
        # According to Daily Maverick , they were later allowed into the Mandela home by the Mandela family ,
        # but could not visit the gravesite as the appropriate rituals had not been performed .
        sample = [('According', 'PREP', 'MARK', 2), ('to', 'PREP', 'FLAT', 0), ('Daily', 'PROPN', 'CPL', 6),
                  ('Maverick', 'PROPN', 'FLAT', 2), (',', 'PUNCT', 'NODEP', -1), ('they', 'PRON', 'SUBJ', 6),
                  ('were', 'VERB', 'ROOT', -1), ('later', 'ADV', 'CPL', 8), ('allowed', 'ADJ', 'PROP', 6),
                  ('into', 'PREP', 'MARK', 12), ('the', 'DET', 'ART', 12), ('Mandela', 'PROPN', 'CPL', 12),
                  ('home', 'NOUN', 'CPL', 8), ('by', 'PREP', 'MARK', 16), ('the', 'DET', 'ART', 16),
                  ('Mandela', 'PROPN', 'CPL', 16), ('family', 'NOUN', 'CPL', 8), (',', 'PUNCT', 'NODEP', -1),
                  ('but', 'CONJ', 'MARK', 21), ('could', 'MAT', 'MODAL', 21), ('not', 'ADV', 'NEG', 21),
                  ('visit', 'VERB', 'CPL', 6), ('the', 'DET', 'ART', 23), ('gravesite', 'NOUN', 'OBJ', 21),
                  ('as', 'PREP', 'MARK', 30), ('the', 'DET', 'ART', 27), ('appropriate', 'ADJ', 'CPL', 27),
                  ('rituals', 'NOUN', 'SUBJ', 30), ('had', 'MAT', 'AUX', 30), ('not', 'ADV', 'NEG', 30),
                  ('been', 'VERB', 'CPL', 21), ('performed', 'ADJ', 'PROP', 30), ('.', 'PUNCT', 'NODEP', -1)]
        # print(_strs(sample))
        self.assertCountEqual([
            'OCL(they, be, allowed)',
            'NTO(mandela family, allow, they)',
            'OTN(they, NOT visit, gravesite)',
            'NCL(gravesite, NOT be, visited)',
            'NCA(ritual, be, appropriate)',
            'NCL(ritual, NOT be, performed)'
        ], _strs(sample))

    def test_29(self):
        # We liked the name Alphabet because it means a collection of letters that represent language ,
        # one of humanity 's most important innovations , and is the core of how we index with Google search !
        sample = [('We', 'PRON', 'SUBJ', 1), ('liked', 'VERB', 'ROOT', -1), ('the', 'DET', 'ART', 3),
                  ('name', 'NOUN', 'OBJ', 1), ('Alphabet', 'PROPN', 'CPL', 3), ('because', 'CONJ', 'MARK', 7),
                  ('it', 'PRON', 'SUBJ', 7), ('means', 'VERB', 'CPL', 1), ('a', 'DET', 'ART', 9),
                  ('collection', 'NOUN', 'OBJ', 7), ('of', 'PREP', 'MARK', 11), ('letters', 'NOUN', 'CPL', 9),
                  ('that', 'PRON', 'SUBJ', 13), ('represent', 'VERB', 'CPL', 11), ('language', 'NOUN', 'OBJ', 13),
                  (',', 'PUNCT', 'NODEP', -1), ('one', 'PRON', 'CPL', 14), ('of', 'PREP', 'MARK', 22),
                  ('humanity', 'NOUN', 'CPL', 22), ("'s", 'PREP', 'MARK', 18), ('most', 'ADV', 'CPL', 21),
                  ('important', 'ADJ', 'CPL', 22), ('innovations', 'NOUN', 'CPL', 16), (',', 'PUNCT', 'NODEP', -1),
                  ('and', 'CONJ', 'NODEP', -1), ('is', 'VERB', 'AND', 7), ('the', 'DET', 'ART', 27),
                  ('core', 'NOUN', 'PROP', 25), ('of', 'PREP', 'MARK', 29), ('how', 'ADV', 'CPL', 27),
                  ('we', 'PRON', 'SUBJ', 31), ('index', 'VERB', 'CPL', 29), ('with', 'PREP', 'MARK', 34),
                  ('Google', 'PROPN', 'CPL', 34), ('search', 'NOUN', 'CPL', 31), ('!', 'PUNCT', 'NODEP', -1)]
        # print(_strs(sample))
        self.assertCountEqual([
            'OTN(we, like, name)',
            'NCL(name, be, liked)',
            'OTN(it, mean, collection)',
            'NCL(collection, be, meant)',
            'NTN(letter, represent, language)',
            'NCL(language, be, represented)',
            'NCA(innovation, be, important)',
            'OI(we, index)'
        ], _strs(sample))

    def test_30(self):
        # Is the world safer , or at greater risk than it was a year ago ?
        sample = [('Is', 'VERB', 'ROOT', -1), ('the', 'DET', 'ART', 2), ('world', 'NOUN', 'SUBJ', 0),
                  ('safer', 'ADJ', 'PROP', 0), (',', 'PUNCT', 'NODEP', -1), ('or', 'CONJ', 'NODEP', -1),
                  ('at', 'PREP', 'MARK', 8), ('greater', 'ADJ', 'CPL', 8), ('risk', 'NOUN', 'OR', 3),
                  ('than', 'CONJ', 'CMARK', 11), ('it', 'PRON', 'SUBJ', 11), ('was', 'VERB', 'CPL', 3),
                  ('a', 'DET', 'ART', 13), ('year', 'NOUN', 'CPL', 11), ('ago', 'ADV', 'CPL', 13),
                  ('?', 'PUNCT', 'NODEP', -1)]
        # print(_strs(sample))
        self.assertCountEqual([
            'NCA(world, be, safe)',
            'NCA(risk, be, great)'
        ], _strs(sample))


if __name__ == ' main ':
    unittest.main()
