# Examples

Sample input files for manual testing and for CI.

`params.json` holds the `--param`/`--params-json` values `cauldron job run` uses against this
plugin's inputs (see `plugin.yaml`'s `inputs:` section, or run
`cauldron plugin inputs lysoip-organelle-specificity` once installed). CI runs this automatically via
`.github/workflows/test-plugin.yml`.

```json
{
  "differential_expression_file": "examples/differential_expression.tsv",
  "organelle_list": "LSD + Lysosome"
}
```
