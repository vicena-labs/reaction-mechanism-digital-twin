# Model card

## Intended use

Reaction definition validation, supplied-result analysis, transition-state evidence gating, kinetics and thermochemistry calculations, uncertainty review, and molecular visualization.

## Maturity

Analysis and validation starter, version 0.2.0.

## Implemented evidence

- deterministic reaction manifest validation,
- archived energy and rate analysis,
- acceptance logic for supplied frequency and IRC results,
- one executed Rowan product conformer search,
- provenance, UUID, failure-preservation, and visualization infrastructure.

## Not implemented or not executed

- end-to-end mechanism computation,
- real transition-state search for the bundled example,
- real frequency and IRC validation for the bundled example,
- consistent computed activation and reaction free energies.

The bundled energies, frequencies, and IRC values are synthetic fixtures. The TS display is a midpoint proxy. They test software behavior and must not be cited as new quantum-chemistry results.

## Limitations

Electronic-structure method error, conformer incompleteness, standard states, entropy, tunneling, anharmonicity, recrossing, solvent treatment, dynamics, multireference character, atom mapping, and experimental-condition mismatch may change conclusions.
