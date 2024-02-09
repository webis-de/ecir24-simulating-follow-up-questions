# Simulating Follow-up Questions in Conversational Search

## Setup

### Authentication
For building models only

1. The LLama2 model needs access permissions to their repository. Hence, you need to have a Hugging Face account with an access token (can be created [here](https://huggingface.co/settings/tokens)). Fill out [this Meta-AI form](https://ai.meta.com/resources/models-and-libraries/llama-downloads/) and request permission to their models [here](https://huggingface.co/meta-llama/Llama-2-7b-hf).
2. The Alpaca model requires an Chatnoir API token which can be requested [here](https://www.chatnoir.eu/apikey).

Then
```bash
make auth
```

### General
This will also download the dataset
```bash
make clean install
```


## Generate Follow-up Questions
1. Configure which dataset, model and prompt type should be used
   ```bash
   make configure
   ```
2. Activate the virtual environment and run the experiment.
   ```bash
   source venv/bin/activate
   python src/python/generate_followup_questions.py
   ```


## Generate Tables

### Automated Comparison (Table 1)

This computation may take a while depending on your hardware. A GPU is preferred for this experiment.

```bash
source venv/bin/activate
python src/python/compute_automatic_comparison.py
```

### Human Assessment (Table 2)

```bash
source venv/bin/activate
python src/python/compute_human_assessment.py
```

### User Modeling (Table 3)

```bash
source venv/bin/activate
python src/python/compute_user_model.py
```

### Compute top-k most-frequent leading bigrams (Appendix)

```bash
source venv/bin/activate
python src/python/compute_leading_bigrams_frequency.py
```

### Calculate Kappa

```bash
# setup
Rscript -e 'dir.create(Sys.getenv("R_LIBS_USER"), showWarnings=FALSE);install.packages("irr", lib=Sys.getenv("R_LIBS_USER"))'

# run
cat data/corpus-webis-follow-up-questions-24/simulation-annotations.json.gz \
  | gunzip \
  | python3 src/python/parse-label-studio-human-assessment-for-kappa.py /dev/stdin \
  | sed 's/not_generic/specific/' \
  > data/simulation-single-annotations.tsv
./src/r/kappa.R  data/simulation-single-annotations.tsv
```
