# Shirudo Contribution Ideas

## Current Status
This file tracks potential contribution opportunities for the Shirudo project.

## Ideas

### 1. Documentation Fixes (Low-Hanging Fruit)
- **Issue**: #247 fix(docs): name the memory-lock prerequisite on read-only CLI pages []
- **Difficulty**: Low
- **Status**: Not started
- **Notes**: Fix documentation to properly mention memory locking requirement for read-only CLI pages

### 2. Testing Coverage (Medium)
- **Issue**: #255 testing: unit coverage for util/upatch_table.c (and similar.c) []
- **Difficulty**: Medium
- **Status**: Not started
- **Notes**: Add missing unit tests for upatch_table.c and related utilities

### 3. Build System Improvements (Medium-High)
- **Issue**: #246 fix(packaging): RPM versions omit the zero prefix for digit-leading Git hashes []
- **Difficulty**: Medium
- **Status**: Not started
- **Notes**: Fix RPM packaging to properly handle Git hash prefixes in versioning

### 4. BPF Program Enhancements (High)
- **PR**: #100 wip: add a ksock upatch by mtardy
- **Difficulty**: High
- **Status**: Not started
- **Notes**: Work on adding a new kernel socket upatch capability - requires deep eBPF and kernel knowledge

### 5. Shell Completion Improvements (Low-Medium)
- **Issue**: #242 fix(completion): preserve paths containing spaces in Bash completion []
- **Difficulty**: Low-Medium
- **Status**: Not started
- **Notes**: Improve shell completion to handle paths with spaces properly

## Next Steps
1. Review the current documentation issues more closely
2. Look at testing coverage gaps
3. Consider starting with a simple documentation fix or shell completion improvement
