import stanza
import uuid
import os
from dotenv import load_dotenv
from helper import *
from functools import partial

load_dotenv()

OUTPUT_FILE_PATH = os.getenv("OUTPUT_FILE_PATH")
PARSE_OUTPUT_PATH = os.getenv("PARSE_OUTPUT_PATH")

transcriptions = read_csv(OUTPUT_FILE_PATH)

docs = [{'id': uuid.uuid4(), 'title': t['id'], 'raw': t['text']} for t in transcriptions]
tokens = []
sentences = []

def map_token(sentence_id, token):
    token['index'] = token['id']
    token['id'] = uuid.uuid4()
    token['sentence_id'] = sentence_id
    return token

nlp = stanza.Pipeline(lang='es', processors='tokenize,mwt,pos,lemma,depparse,constituency', model_dir='.cache/stanza')
for raw_doc in docs:
    doc = nlp(raw_doc['raw'])
    for i, sentence in enumerate(doc.sentences):
        sentence_id = uuid.uuid4(),
        sentences.append({
            'id': uuid.uuid4(),
            'index': i,
            'doc_id': raw_doc['id'],
            'raw': sentence.text,
            'constituency' : str(sentence.constituency)
        })
        map_token_partial = partial(map_token, sentence_id)
        tokens += map(map_token_partial, sentence.to_dict())

print("Saving...")

os.makedirs(PARSE_OUTPUT_PATH, exist_ok=True)

write_csv(os.path.join(PARSE_OUTPUT_PATH, "documents.csv"), docs)
write_csv(os.path.join(PARSE_OUTPUT_PATH, "sentences.csv"), sentences)
write_csv(os.path.join(PARSE_OUTPUT_PATH, "tokens.csv"), tokens)

print("Done!")

