# Prince of Persia: Warrior Within — Nintendo Switch

An educational reverse-engineering and native porting research project focused on the original Xbox version of Prince of Persia: Warrior Within.

## Project Goal

Investigate the original Xbox executable (XBE), understand its code and dependencies, and explore a native Nintendo Switch port through static recompilation.

The intended approach is to translate original x86 game code into ARM64-compatible code and implement the required Xbox platform functionality through compatibility layers.

This is not an emulator project.

## Current Status

### Resource Research
- [x] Extracted and indexed resources from the game's BF archive.
- [x] Conducted preliminary BF resource analysis.

### XBE Analysis
- [x] Inspected the XBE header and entry point.
- [x] Parsed the XBE section table (35 sections).
- [x] Implemented section-aware virtual-address to file-offset mapping.
- [x] Disassembled the entry-point routine using Capstone.
- [x] Processed 42 instructions in the initial IR experiment.
- [x] Generated an initial x86 intermediate representation.
- [x] Identified three direct calls from the entry-point routine.
- [ ] Automate function discovery and call-graph analysis.
- [ ] Expand Xbox kernel import and thunk analysis.
- [ ] Analyze additional game functions.

### Recompiler
- [x] Created initial x86 instruction decoding prototypes.
- [x] Created an initial x86-to-IR translation prototype.
- [ ] Implement complete x86 instruction semantics.
- [ ] Implement x86 flags, stack and memory behavior.
- [ ] Generate ARM64 code.
- [ ] Implement Xbox kernel and XDK compatibility layers.

### Native Nintendo Switch Port
- [ ] Implement graphics compatibility.
- [ ] Implement audio and input compatibility.
- [ ] Implement filesystem compatibility.
- [ ] Integrate recompiled game code.
- [ ] Build and test a native Nintendo Switch application.

The project is currently in the research and prototyping stage. No playable port is available yet.

## Repository Structure

- `docs/` — Technical documentation and research notes.
- `tools/` — Binary and BF archive analysis tools.
- `recompiler/` — XBE decoding and initial IR translation prototypes.
- `research/` — Research findings and analysis.
- `source/` — Native port implementation.
- `tests/` — Tests and experiments.

## Requirements

- Python 3
- Capstone 5 or newer

Install dependencies from the repository root:

    python3 -m venv .venv
    source .venv/bin/activate
    pip install -r requirements.txt

Place a legally obtained `default.xbe` in the repository root. The executable is excluded from version control.

## Running the Experimental Recompiler Tools

After installing the requirements and placing your legally obtained
`default.xbe` in the repository root, run the experimental tools from
the `recompiler/` directory:

    cd recompiler
    python translate_ir_6.py
    python decode_entry_2.py
    python translate_ir_5.py

The tools perform three separate tasks:

- `translate_ir_6.py` parses the XBE section table and tests virtual-address to file-offset mapping.
- `decode_entry_2.py` disassembles the entry-point routine and writes `entry_instructions.json`.
- `translate_ir_5.py` converts the decoded instructions into an initial IR and writes `entry_ir.json`.

Generated JSON files are local analysis outputs and are not intended to be committed.

These scripts are experimental prototypes, not a complete static recompiler.
See `docs/recompiler.md` for the current architecture and research findings.

## Legal Notice

This repository does not contain the original game executable, game assets, or copyrighted resources.

The project is an independent educational research effort and is not affiliated with or endorsed by Ubisoft.
