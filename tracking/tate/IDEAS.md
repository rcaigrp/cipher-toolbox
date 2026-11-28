# Shirudo Contribution Ideas

## Status: Tracking

### 1. Java Shield Documentation Improvement
- **Issue**: #368, #366, #370 - Java shield issues related to retransformation and XXE handling
- **Status**: In progress (PRs #368, #371)
- **Difficulty**: Medium
- **First Step**: Review PRs for the Java XMLDecoder shield (#371) and Base64 guard fix (#368) to understand current implementation

### 2. Quickstart Documentation Gap
- **Issue**: Previously noted gap in checkout directory handling
- **Status**: Needs verification if still exists
- **Difficulty**: Low
- **First Step**: Check quickstart guide against actual repo structure and workflow

### 3. Unit Test Coverage for upatch_table.c
- **Issue**: #255 - Unit test gap reported
- **Status**: Needs verification
- **Difficulty**: Medium
- **First Step**: Examine current test setup and confirm if test exists

### 4. VM Build Issue Resolution
- **Issue**: #360 - VM build problems
- **Status**: Needs tracking
- **Difficulty**: Medium
- **First Step**: Review issue details and related PRs

### 5. TPM and Authorization Clarifications
- **Issue**: #379 - Questions about signed tree operations and authorization
- **Status**: Open question
- **Difficulty**: High (requires design understanding)
- **First Step**: Read up on TPM integration and security model

### 6. Completion Space Preservation Fix
- **Issue**: #251 - Preserve spaces in filesystem path completion
- **Status**: In PR (#251) 
- **Difficulty**: Low
- **First Step**: Review implementation to understand impact

## Potential Future Ideas

### 7. Add Shield Examples
- **Status**: Not yet implemented
- **Difficulty**: Medium
- **First Step**: Review current docs for existing examples and assess gaps

### 8. Expand BPF Program Documentation
- **Status**: Not yet implemented  
- **Difficulty**: High
- **First Step**: Analyze bpf/ directory structure and documentation needs

## Notes
- Most Java-related issues are being actively worked on in PRs
- Documentation improvements continue to be a focus area
- Some gaps may not be actionable due to container limitations (kernel access)