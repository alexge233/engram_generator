# Benchmark Results

Results from models trained on the Engram Generator curriculum. Each JSON file in this directory is one experiment.

## Submitting results

1. Fork this repository
2. Create a JSON file in `results/` named `{model_family}_{params}_{date}.json` (e.g. `baseline_18M_2026-06-11.json`)
3. Validate against `schema.json`
4. Open a pull request

### Validation

```bash
pip install jsonschema
python -c "
import json, jsonschema
schema = json.load(open('results/schema.json'))
result = json.load(open('results/your_file.json'))
jsonschema.validate(result, schema)
print('Valid')
"
```

### Required fields

- **model**: name, family, version (+ optional huggingface URL, repo, description)
- **architecture**: type, d_model, num_layers (+ tokenizer, memory slots, iterations)
- **parameters**: total and trainable count
- **training**: steps, effective batch size, learning rate, loss strategy, hardware
- **dataset**: generator version, number of generators, difficulty range
- **metrics**: val_loss, exact_match (+ optional per-difficulty, per-domain, OOD)
- **submitted**: date and submitter

### Naming convention

`{family}_{params}_{date}.json`

Examples:
- `baseline_18M_2026-06-11.json`
- `engram_13M_2026-06-15.json`
- `llama2_7B_finetune_2026-07-01.json`
