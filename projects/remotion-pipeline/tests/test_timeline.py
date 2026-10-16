import importlib.util,unittest
from pathlib import Path
spec=importlib.util.spec_from_file_location('timeline',Path(__file__).resolve().parents[1]/'scripts/timeline.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
class TimelineTests(unittest.TestCase):
 def fixture(self,offset=0):return [{'sourceId':'s','audioOffsetSeconds':offset,'words':[{'text':'Do','start':1,'end':1.2},{'text':'not','start':1.2,'end':1.4},{'text':'rush.','start':1.4,'end':1.8}],'speechRegions':[{'start':.9,'end':1.9}]}]
 def clip(self,**kwargs):return {'id':'c','sourceId':'s','sourceIn':1,'sourceOut':2,'timelineStart':5,'rate':1,**kwargs}
 def test_basic_mapping(self):self.assertEqual(m.map_analysis(self.fixture(),[self.clip()])['words'][0]['start'],5)
 def test_rate_mapping(self):self.assertAlmostEqual(m.map_analysis(self.fixture(),[self.clip(rate=2)])['words'][-1]['end'],5.4)
 def test_offset(self):self.assertEqual(m.map_analysis(self.fixture(.5),[self.clip(sourceIn=1.5,sourceOut=3)])['words'][0]['start'],5)
 def test_negative_offset(self):self.assertAlmostEqual(m.map_analysis(self.fixture(-.5),[self.clip(sourceIn=.5)])['words'][0]['start'],5)
 def test_partial_word_flagged(self):r=m.map_analysis(self.fixture(),[self.clip(sourceIn=1.1)]);self.assertTrue(r['issues']);self.assertEqual(r['words'][0]['text'],'not')
 def test_speech_clipped(self):r=m.map_analysis(self.fixture(),[self.clip(sourceIn=1.1,sourceOut=1.7)]);self.assertEqual(r['speechRegions'][0]['start'],5);self.assertAlmostEqual(r['speechRegions'][0]['end'],5.6)
 def test_reordered_duplicate_source(self):r=m.map_analysis(self.fixture(),[self.clip(id='c1',timelineStart=10),self.clip(id='c2',timelineStart=0)]);self.assertEqual(len(r['words']),6);self.assertEqual(r['words'][0]['start'],0)
 def test_missing_source(self):self.assertRaises(ValueError,m.map_analysis,self.fixture(),[self.clip(sourceId='missing')])
 def test_invalid_rate(self):self.assertRaises(ValueError,m.map_analysis,self.fixture(),[self.clip(rate=0)])
 def test_reversed_range(self):self.assertRaises(ValueError,m.map_analysis,self.fixture(),[self.clip(sourceOut=.5)])
 def test_duplicate_clip(self):self.assertRaises(ValueError,m.map_analysis,self.fixture(),[self.clip(),self.clip()])
 def test_duplicate_source(self):self.assertRaises(ValueError,m.map_analysis,self.fixture()*2,[self.clip()])
 def test_missing_offset(self):a=self.fixture();del a[0]['audioOffsetSeconds'];self.assertRaises(ValueError,m.map_analysis,a,[self.clip()])
 def test_invalid_word_flagged(self):a=self.fixture();a[0]['words'][0]['start']=None;self.assertTrue(m.map_analysis(a,[self.clip()])['issues'])
 def test_negation_preserved(self):r=m.map_analysis(self.fixture(),[self.clip()]);self.assertEqual(m.caption_phrases(r['words'])[0]['text'],'Do not rush.')
 def test_phrase_word_limit(self):r=m.map_analysis(self.fixture(),[self.clip()]);self.assertEqual(len(m.caption_phrases(r['words'],max_words=1)),3)
 def test_phrase_gap(self):w=[{'text':'a','start':0,'end':.2},{'text':'b','start':2,'end':2.2}];self.assertEqual(len(m.caption_phrases(w)),2)
 def test_phrase_clip_boundary(self):w=[{'text':'a','start':0,'end':.2,'clipId':'a'},{'text':'b','start':.2,'end':.4,'clipId':'b'}];self.assertEqual(len(m.caption_phrases(w)),2)
 def test_bad_phrase_settings(self):self.assertRaises(ValueError,m.caption_phrases,[],max_words=0)
 def test_empty_input(self):self.assertEqual(m.map_analysis([],[])['words'],[])
if __name__=='__main__':unittest.main()
