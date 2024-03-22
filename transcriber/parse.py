import stanza
from stanza.pipeline.core import DownloadMethod
import uuid
import os
from dotenv import load_dotenv
from helper import *
from functools import partial

load_dotenv()

OUTPUT_FILE_PATH = os.getenv("OUTPUT_FILE_PATH")
PARSE_OUTPUT_PATH = os.getenv("PARSE_OUTPUT_PATH")

transcriptions = read_csv(OUTPUT_FILE_PATH)
def map_doc(doc):
    doc['title'] = doc['id']
    doc['id'] = uuid.uuid4()
    doc['raw'] = doc['text']
    doc.pop('text', None)
    return doc

docs = list(map(map_doc, transcriptions))
tokens = []
sentences = []

def map_token(sentence_id, token):
    token['index'] = token['id']
    token['id'] = uuid.uuid4()
    token['sentence_id'] = sentence_id
    return token

def parse_tree_to_dict(tree):
    if len(tree.children) < 1:
        return {
            'label': tree.label,
        }
    return {
        'label': tree.label,
        'children': [parse_tree_to_dict(child) for child in tree.children]
    }


nlp = stanza.Pipeline(lang='es', 
                      processors='tokenize,mwt,pos,lemma,depparse,constituency', 
                      model_dir='.cache/stanza',
                      download_method=DownloadMethod.REUSE_RESOURCES
                      )
for raw_doc in docs:
    doc = nlp(raw_doc['raw'])
    for i, sentence in enumerate(doc.sentences):
        sentence_id = uuid.uuid4()
        sentences.append({
            'id': sentence_id,
            'index': i,
            'doc_id': raw_doc['id'],
            'raw': sentence.text,
            'constituency' : str(parse_tree_to_dict(sentence.constituency))
        })
        map_token_partial = partial(map_token, str(sentence_id))
        tokens += map(map_token_partial, sentence.to_dict())

print("Saving...")

os.makedirs(PARSE_OUTPUT_PATH, exist_ok=True)

write_csv(os.path.join(PARSE_OUTPUT_PATH, "documents.csv"), docs)
write_csv(os.path.join(PARSE_OUTPUT_PATH, "sentences.csv"), sentences)
write_csv(os.path.join(PARSE_OUTPUT_PATH, "tokens.csv"), tokens)

print("Done!")

