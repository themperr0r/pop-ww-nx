# Recompiler Research Notes

## 1. Objective

The objective is to investigate a native Nintendo Switch port of the original Xbox version of Prince of Persia: Warrior Within.

The selected approach is static recompilation.

The original Xbox executable contains x86 machine code. The long-term plan is to decode this code, translate its behavior into an intermediate representation (IR), and eventually generate ARM64 code suitable for the Nintendo Switch.

Xbox-specific system functionality will need to be implemented separately through compatibility layers.

This is an early research prototype, not a functioning recompiler.

## 2. Current Pipeline

The experimental workflow currently consists of:

1. Read the XBE executable.
2. Parse the XBE header.
3. Parse the XBE section table.
4. Map virtual addresses to file offsets.
5. Decode x86 instructions with Capstone.
6. Convert a limited instruction subset into an initial IR.
7. Inspect direct calls and referenced addresses.

ARM64 code generation has not been implemented.

## 3. XBE Structure

The analyzed executable is `default.xbe`.

Current observations:

| Property | Value |
|---|---:|
| XBE base address | `0x00010000` |
| Entry point | `0x003D674C` |
| Section table VA | `0x00010370` |
| Section table file offset | `0x00000370` |
| Section entry size | 56 bytes |
| Number of sections | 35 |

The XBE section table is essential because virtual addresses cannot be mapped to file offsets using one universal subtraction formula.

For a file-backed address inside a section, the mapping is:

    file_offset = raw_offset + (virtual_address - virtual_address_start)

The address must fall inside the file-backed range of the section. A virtual address may refer to memory that has no corresponding bytes in the executable file.

## 4. Entry-Point Analysis

The entry point is `0x003D674C`.

The initial Capstone disassembly produced 42 instructions.

The routine performs several operations, including:

- Reads and updates global values.
- Calculates an aligned memory-related value.
- Pushes arguments onto the stack.
- Calls three internal addresses.
- Checks the return value of the first call.
- Restores registers and returns.

The three direct call targets are:

| Call instruction | Target |
|---|---|
| `0x003D67A0` | `0x003D1A6A` |
| `0x003D67B0` | `0x003D7C1C` |
| `0x003D67B6` | `0x003D1793` |

All three targets map into the executable's first section.

Their complete behavior and function boundaries still require further analysis.

## 5. Initial IR Prototype

The current prototype converts a limited set of decoded x86 instructions into an intermediate representation.

The first experiment processed 42 instructions and reported zero unsupported instructions within its implemented instruction subset.

This does not mean that all x86 instructions are supported.

Important missing or incomplete areas include:

- Accurate x86 flag behavior.
- Memory operand semantics.
- Stack and calling convention behavior.
- Conditional branches and control-flow reconstruction.
- Indirect calls and jumps.
- Floating-point and SIMD instructions.
- Function boundary discovery.

The current IR output is an analysis artifact and is not executable game code.

## 6. Important Implementation Considerations

### Address Mapping

The XBE section table must be used to resolve virtual addresses.

The mapper must distinguish:

- File-backed addresses.
- Memory-only addresses.
- Unmapped addresses.

### Instruction Semantics

Instructions cannot be translated by simply replacing x86 mnemonics with ARM64 mnemonics.

The implementation must preserve the behavior of registers, flags, memory accesses, stack operations and control flow.

### Xbox Compatibility

The original game relies on Xbox-specific system functionality.

A native port will need implementations or equivalents for the required kernel, filesystem, threading, synchronization, graphics, audio and input interfaces.

The exact set of required interfaces is still under investigation.

## 7. Current Limitations

- Only the entry-point routine has been processed by the current IR experiment.
- The instruction translator supports a limited subset.
- Function discovery is not automated.
- Import and thunk identification is incomplete.
- ARM64 code generation does not exist yet.
- Xbox compatibility layers do not exist yet.
- No playable port is available.

## 8. Next Research Steps

1. Inspect and validate the three direct call targets.
2. Develop section-aware function discovery.
3. Build a call graph for reachable functions.
4. Improve IR generation using Capstone's structured operand data.
5. Implement accurate x86 flags and memory semantics.
6. Identify required Xbox kernel imports.
7. Design the ARM64 code-generation stage.

## 9. Reproducibility

The experimental scripts are located in the repository's `recompiler/` directory.

Install dependencies from the repository root:

    python3 -m venv .venv
    source .venv/bin/activate
    pip install -r requirements.txt

Place `default.xbe` in the repository root, then run the entry-point analysis scripts from `recompiler/`.

Generated files such as `entry_instructions.json` and `entry_ir.json` are local analysis outputs and are not intended to be committed.
