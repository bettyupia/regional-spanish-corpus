# Regional Spanish Corpus in Peru

## Transcriber & Parser
### Setups
* Navigate to `transcriber` folder
* Python version used: `3.11.8`
* Set up a python venv and install all dependencies in `requirements.txt`
* `cp .env.dev .env`
* Set up OpenAPI Whisper according to [here](https://github.com/openai/whisper)

### How to use transcriber
1. Toggle settings in `.env`
2. Activate venv
3. Run `python transcribe.py` to transcribe audio first
4. Run `python parse.py` to parse transcribed result
