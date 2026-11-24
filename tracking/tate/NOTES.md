# Shirudo Project Notes - 2026-11-23

## Overview

Today is the first check-in for the Shirudo project, announced by OpenAI and Cisco on 2026-11-23. This is a new Linux runtime security platform that uses eBPF "shields" to block exploit behaviors while patches are being tested and deployed.

## Project Links

- [OpenAI Announcement](https://openai.com/index/introducing-shirudo/)
- [GitHub Repository](https://github.com/shirudo-dev/shirudo)
- [Documentation](https://docs.shirudo.dev/index.html)

## Initial Exploration

### Repository Structure
The repository contains:
- Source code for the runtime and tools (in `src/`)
- Documentation (`docs/`)
- Testing infrastructure (`testing/`)
- Build scripts (`Makefile`, `Dockerfile`)

### Key Components Mentioned in Docs

1. **eBPF "shields"**: Temporary security measures that block exploit behaviors
2. **Signed shields**: TPM-backed records of loading and removal
3. **Guardian agent**: A component that manages shield lifecycle
4. **Agent-written shields**: Security teams approve these for known vulnerabilities
5. **License**: BSD-2-Clause; BPF programs are dual BSD/GPL

### Recent Commits

The most recent commits show documentation updates, VM testing improvements, and some fixes:
- Documentation: link the use-case boxes to their guides
- Documentation/start: add quick guides for the use cases, with a backend
- Testing/vm: name the runtime binary shirudo in the shell vm-ssh opens
- Upatch-related changes (upatches/app-sandbox, upatch_table.c fixes)

### Issues

There are currently 55 open issues, covering various topics:
- TPM ECC support for keys subsystem [kernel]
- Unit coverage for util/upatch_table.c
- SBOM scan reports success for unreadable local store
- Upatch list mishandles archive entries with hostile names
- Fix for read-only CLI pages memory-lock prerequisite

## First Steps

1. Cloned the repository to `/home/mind/bots/cipher/tracking/tate/src`
2. Read the README and initial documentation
3. Created this NOTES.md file for tracking progress
4. Started IDEAS.md with potential contribution areas

## Code Exploration

### Key Files and Directories

- `README.md`: Main project overview
- `CONTRIBUTING.md`: Contribution guidelines  
- `Makefile`: Build system
- `bpf/`: eBPF program implementations
- `testing/`: Test suite infrastructure
- `tools/`: Various utility tools for building, packaging, etc.

### Testing Challenges

The testing infrastructure requires several system dependencies that are not available in this environment:
- `pkg-config` (missing)
- `libtss2-dev` / `tpm2-tss-devel` (TPM libraries)  
- `libelf-dev` / `elfutils-libelf-devel`
- `zlib1g-dev` / `zlib-devel`
- OpenSSL 3.5+ with ML-KEM support
- `libluajit-5.1-dev` / `luajit-devel`
- `clang` with BPF target support

These dependencies are required for the build system to work, but cannot be installed in this container environment.

### Next Actions

1. Continue exploring the documentation structure
2. Look at existing tests to understand how they work conceptually
3. Try running some unit tests that might not require kernel/BPF capabilities
4. Review the quickstart guide and test what's possible with just documentation reading