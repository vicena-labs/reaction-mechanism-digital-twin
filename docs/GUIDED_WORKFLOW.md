# Guided Reaction Mechanism Analysis Workflow

Part of the [Vicena Research Twins collection](https://vicena.ai).

This repository is an analysis and validation starter. It provides a safe, auditable route from a reaction definition to a validated interpretation of supplied or newly generated results. It does not run the full quantum-chemistry ladder automatically.

## Stage 1: Define the chemical system

Required inputs:

- reactants and products,
- mapped atom ordering,
- total charge and multiplicity,
- phase, temperature, pressure, solvent, concentration, and standard state when relevant,
- native coordinate provenance,
- experimental or literature comparison targets.

Completion gate: every required field is explicit, with no guessed metadata.

## Stage 2: Validate composition and mapping

Run:

```bash
python scripts/validate_reaction.py reactions/<case>/reaction.json
```

Checks include element conservation, mapping permutation, element-compatible mapping, charge, and multiplicity.

Completion gate: deterministic validation passes and the intended forming and breaking bonds are documented.

## Stage 3: Generate and optimize endpoint conformers

Local screening may use RDKit or similar geometry generation. High-fidelity endpoint preparation may use an authorized Rowan conformer search and optimization ladder.

The bundled example contains one completed Rowan product conformer search. It does not contain an equivalent real reactant endpoint workflow.

Completion gate: endpoint structures have coordinates, provenance, charge, multiplicity, atom order, method, and optimization status.

## Stage 4: Authorize the quantum-chemistry method

Before paid work, record:

- workflow type,
- method, engine, basis or model,
- solvent treatment,
- convergence mode,
- constraints,
- expected scientific purpose,
- maximum Vicena credit cap.

Completion gate: the user has explicitly authorized the method and budget. Submission remains outside notebooks.

## Stage 5: Search transition-state candidates

Possible routes include coordinate scans, double-ended transition-state searches, or a justified transition-state guess followed by optimization.

Every candidate must retain its UUID, settings, input structures, warnings, status, and raw result, including failures.

Completion gate: at least one candidate geometry exists. This is not yet a validated transition state.

## Stage 6: Validate frequencies and IRC

A candidate is accepted only when:

- exactly one relevant imaginary frequency is present,
- the displacement matches intended bond changes,
- geometry and atom mapping remain plausible,
- the backward and forward paths connect the intended endpoint regions.

Completion gate: frequency and bidirectional path evidence pass at a scientifically compatible level of theory.

## Stage 7: Preserve failed candidates

Do not delete failed searches, rejected saddles, disconnected IRC paths, or provider warnings. Record the reason each candidate was rejected.

Completion gate: the evidence package explains both accepted and rejected candidates.

## Stage 8: Compare uncertainty and method sensitivity

Compare only compatible quantities and conditions. Report method sensitivity, conformer dependence, thermochemical assumptions, standard states, experimental uncertainty, and known missing corrections.

Completion gate: the final report separates calculated evidence, experimental evidence, assumptions, and unresolved uncertainty.

## Status labels

Use these labels consistently:

- `implemented-local`: executable without external compute,
- `executed-remote`: a real collected remote result exists,
- `synthetic-fixture`: test data only,
- `documented-not-executed`: workflow guidance exists but no result was generated,
- `validated`: the stated scientific acceptance gate was passed with real evidence.
