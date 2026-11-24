# Shirudo Contribution Ideas

## Current Status

This document tracks potential areas where contributions could be made to the Shirudo project. Each idea includes a description, difficulty level, and next steps.

## Ideas

### 1. Documentation Improvement - Quickstart Guide
- **Description**: The quickstart documentation appears to be incomplete or not fully fleshed out yet. This is critical for adoption.
- **Difficulty**: Low
- **Next Steps**: 
  - Review the quickstart guide in docs/start/quickstart.html
  - Test the steps and identify missing information
  - Draft a fix or clarification based on actual experience

### 2. Unit Test Coverage - upatch_table.c
- **Description**: There's an open issue (#255) about unit coverage for util/upatch_table.c
- **Difficulty**: Medium
- **Next Steps**:
  - Examine the upatch_table.c file and its tests
  - Identify gaps in test coverage
  - Write missing unit tests

### 3. Shield Implementation Example
- **Description**: The project mentions "agent-written shields" that security teams approve, but there's no clear example of how to write or submit one.
- **Difficulty**: Medium-High
- **Next Steps**:
  - Look for existing shield examples in the codebase
  - Understand the shield format and submission process
  - Create a simple example shield if possible

### 4. TPM Integration Testing
- **Description**: There's an open issue about TPM ECC support for keys subsystem [kernel]
- **Difficulty**: High
- **Next Steps**:
  - Review the TPM-related code and tests
  - Understand how TPM integration is tested
  - Suggest improvements or documentation

### 5. VM Testing Improvements
- **Description**: Recent commits show work on VM testing infrastructure, suggesting this area could use more attention.
- **Difficulty**: Medium
- **Next Steps**:
  - Review the testing/vm directory and scripts
  - Identify areas for improvement in VM setup or testing workflow