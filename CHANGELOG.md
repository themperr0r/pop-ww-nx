
## v0.2.0 - 2026-11-18

### BF Extraction

- Created initial Python BF unpacker.
- Extracted all 5374 indexed resources.
- Generated manifest.csv.
- Verified extracted file sizes against index metadata.

## v0.3.0 - BF Research Checkpoint / XBE Pivot
Date: 2026-11-18

### BF Archive Research
- Extracted all 5374 indexed resources using bf_unpack.py.
- Identified 1464 unique first-four-byte signatures.
- Compared resource groups by size, content hashes and common prefixes.
- Identified a 322-file group with signature 00 75 06 00.
- Found a shared 12263-byte tail (offset 0x6019-0x8FFF) in 314/322 files.
- Identified 8 tail outliers for further investigation.
- Compared Swyter/poptools Binary Template with the Xbox archive.
- Confirmed a 0x54-byte structural size match, but exact field correspondence remains unresolved.
- BF archive research paused, not abandoned.

### New Reference
- Repository: https://github.com/Swyter/poptools
- Important file: pop_prince_bf.bt
- Template documents BIG archive structures and multiple platform variants.
- Xbox-specific structure still requires independent verification.

### Strategic Direction
- Primary objective remains a native Nintendo Switch port.
- Shift immediate focus from BF resource reverse engineering to XBE analysis.
- Investigate static recompilation / ReXGlue feasibility.
- Preserve original executable logic wherever possible.
- Identify Xbox kernel, graphics, audio, input and filesystem dependencies.
- Do not assume direct ReXGlue compatibility before examining the XBE.

### Next Milestone
- Inspect default.xbe header, entry point, sections and import tables.
- Establish an initial executable analysis report.

## [0.4.0] - 2026-11-22

### Added
- Initial XBE section-table parsing and section-aware address mapping research.
- Entry-point disassembly using Capstone.
- Initial x86 instruction-to-IR translation prototype.
- Recompiler scripts copied into the project repository.
- Python dependency declaration through `requirements.txt`.
- Initial recompiler technical documentation.

### Research Findings
- Identified the XBE entry point at virtual address `0x003D674C`.
- Parsed 35 XBE section entries.
- Confirmed file-backed address mappings for the entry-point code and several referenced addresses.
- Processed 42 instructions in the initial entry-point IR experiment.
- Identified three direct call targets from the entry-point routine:
  - `0x003D1A6A`
  - `0x003D7C1C`
  - `0x003D1793`

### Notes
- The current IR translator supports only a limited instruction subset.
- The zero-unsupported-instructions result applies only to the 42 instructions in this experiment.
- Call classification and function boundaries still require further validation.
- No ARM64 code generation or playable Nintendo Switch port exists yet.


## [0.5.0] - 2026-11-22

### Added
- Recursive XBE code scanning and per-function disassembly output.
- Xbox kernel thunk-table import resolution.
- Indirect kernel API call mapping.
- Callsite-to-function mapping tools.

### Research Findings
- Discovered 74 function-entry candidates and decoded 3,712 unique instructions.
- Located the retail Xbox kernel thunk table at `0x0054B2E0`.
- Resolved all 153 entries in the discovered kernel import table.
- Mapped 46 indirect callsites to kernel APIs; 16 remain unresolved.
- Identified memory allocation APIs including `NtAllocateVirtualMemory` and `NtFreeVirtualMemory`.
- Found two callers of `0x003D4034`.
- Observed returned memory being populated with fields and linked into a data structure, suggesting a possible allocator or memory-pool role.

### Notes
- Function entries are discovered candidates, not fully verified function boundaries.
- The recursive scan covers only reachable code discovered by the current analysis.
- The role of `0x003D4034` remains a hypothesis and requires further investigation.
- No ARM64 code generation or playable Nintendo Switch port exists yet.
