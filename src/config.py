"""Config file."""

from collections import OrderedDict


# Path to each raw lexicon
LEXICON_PATHS = {'english': ['data/raw/english/celex_all.csv', '\\'],
				 'french': ['data/raw/french/french_lexique.txt', '\t'],
				 'spanish': ['data/raw/spanish/spanish_subtlex.txt', None],
				 'german': ['data/raw/german/celex_german_all.csv', '\\'],
				 'mandarin': ['data/raw/mandarin/mandarin_with_tones_seg1.csv', None], 
				 'mandarin_cld': ['data/raw/mandarin_cld/chineselexicaldatabase2.1.csv', None], 
				 'japanese': ['data/raw/japanese/japanese_labeled_columns.csv', None],
				 'dutch': ['data/raw/dutch/celex_dutch.csv', '\\']
				 }

## Final mapping between each language and n-phone model 
LANGUAGES_N = [
               ('english', 5),
               ('german', 5),
               ('dutch', 5),
               ('french', 4),
               ('mandarin', 4),
               ('mandarin_cld', 4),
               ('japanese', 4),
               ]

# try different n-phone models
MODEL_INFO = {'n': 4, 'smoothing': .01, 
			  'match_on': 'sylls', # phones vs. sylls
			  }

# http://www.iub.edu/~psyling/papers/celex_eug.pdf
# See pg. 179
VOWEL_SETS = {'german': set("i#a$u3y)eo|o1246WBXIYE/{&AVOU@^cq0~"), 
			  'english': set("i#$u312456789IE{QVU@cq0~"),
			  'dutch': set("i!auy()*<e|oKLMIEAO}@"),
		  	  'french': set("i5§yEO9a°e@2uo"),
		  	  'mandarin': set('aeiouəɪuɛɨʊUIAEOy'),
		  	  'mandarin_cld': set('vuoiaeWPUAKLMIOVQEYCB'), 
		  	  'japanese': set("aeiouEOIU12345YN") # Japanese includes "N", placeless nasal coda
		  		} 


PHON_COLUMN = {'german': 'PhonDISC',
			   'english': 'PhonDISC',
			   'mandarin_cld': 'phonetic_remapped', 
			   'dutch': 'PhonDISC',
			   'mandarin': 'phonetic_remapped', 
			   'japanese': 'phonetic_remapped', # Requires remapping double-characters
			   'french': '2_phon'}

WORD_COLUMN = {'german': 'Word',
			   'english': 'Word',
			   'dutch': 'Word',
			   'mandarin': 'word',
			   'mandarin_cld': 'Word',
			   'japanese': 'orth_form_romaji',
			   'french': '3_lemme'}	



# Remap double characters to single characters, where necessary
PHONETIC_REMAPPINGS = {
	'japanese': {
		'ky': 'K', # Already converted in pronuncation field
		'gy': 'G', # Already converted in pronuncation field
		'sh': 'S', # Already converted in pronuncation field
		'ch': 'C', # Already converted in pronuncation field
		'ts': 'c', # Already converted in pronuncation field
		'ny': 'Y', # Already converted in pronuncation field
		'hy': 'H', # Already converted in pronuncation field
		'by': 'B', # Already converted in pronuncation field
		'py': 'P', # Already converted in pronuncation field
		'my': 'M', # Already converted in pronuncation field
		'ry': 'R', # Already converted in pronuncation field
		'ee': 'E', # Represents result of conversion from romaji to pronunciation field
		'oo': 'O', # Represents result of conversion from romaji to pronunciation field
		'ji': 'I', # Represents result of conversion from romaji to pronunciation field
		'zu': 'U', # Represents result of conversion from romaji to pronunciation field
		'ue': '1', # Represents result of conversion from romaji to pronunciation field
		'ui': '2', # Represents result of conversion from romaji to pronunciation field
		'uo': '3', # Represents result of conversion from romaji to pronunciation field
		'ua': '4', # Represents result of conversion from romaji to pronunciation field
		'ie': '5', # Represents result of conversion from romaji to pronunciation field
		'yu': 'Y', # Represents result of conversion from romaji to pronunciation field
		'?': '9' # Replace for REGEX check
		},
	'mandarin': OrderedDict({'uo': 'U', ## Should be ordered
                          'aɪ': 'I', 
                          'aʊ': 'A',
                          'eɪ': 'E',
                          'oʊ': 'O',
                          "tɕ'": 'Q', # sampa  
                          "tʂ'": 'C', # sampa  
                          "ts'": 'c', # sampa  
                          "tʂ": 'Z',
                          "ts": 'z',
                          'tɕ': 'J', # sampa
                          "p'": 'P',
                          "k'": 'K',
                          # "tʻ": 'T',
                          "t'": 'T'
        }),
	'mandarin_cld': OrderedDict({
		'iao': 'W',
		'uai': 'P',
		'ua': 'U',
		'ai': 'A',
		'iu': 'K',
		'ia': 'L',
		'ie': 'M', 
		'ui': 'I',
		'uo': 'O',
		'ou': 'V',
		'ue': 'C',
		've': 'B',
		'ao': 'Q',
		'ei': 'E',
		'io': 'Y'
		}),
    'english': {},
    'french': {},
    'german': {
    ')': '9', # replace for REGEX check
    '+': '8', # replace for REGEX check
    '|': '7'
    },
    'dutch': {
    ')': '9', # replace for REGEX check
    '+': '8', # replace for REGEX check
    '|': '7', # replace for REGEX check
    '*': '6' # replace for REGEX check (6 not a symbol in Dutch, but is for English/German)
    }
}		


