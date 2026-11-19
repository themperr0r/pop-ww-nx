
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
