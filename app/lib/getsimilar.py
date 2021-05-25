from PyDictionary import PyDictionary

from pickle import load as pickle_load
from pathlib import Path


# Initialize
with open(f'{Path(__file__).parent.parent}/ml_model/wikitext-103-raw.model-25.wv.pkl', 'rb') as pkl_file:
	# Load a gensim.models.fasttext.FastTextKeyedVectors object.
	wv = pickle_load(pkl_file)
dictionary=PyDictionary()


def get_similar(text: str, topn: int = 10) -> list:
	"""Returns a list of the words most similar to the passed word.
	NOTE: Only supports a single word at the moment.
	"""
	most_similar = wv.most_similar(text, topn=topn)
	if len(most_similar) == 0 or most_similar[0][1] < 0.01:
		synonyms = dictionary.synonym(text)
		if synonyms is not None:
			return [
				{'text': synonym, 'similarity': None} for synonym in synonyms
			]
	return [
		{'text': t, 'similarity': s} for t, s in most_similar
	]
