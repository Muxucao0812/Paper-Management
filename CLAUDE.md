# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository Overview

This is an academic research paper repository focused on:
- **Homomorphic Encryption (HE)** - Various papers on FHE schemes, implementations, and hardware acceleration
- **Hardware Verification** - Formal verification methods, testing frameworks, and hardware design validation
- **Neural Networks with FHE** - Privacy-preserving machine learning using homomorphic encryption
- **Hardware Accelerators** - FPGA and custom chip designs for cryptographic operations

## Repository Structure

### Core Research Areas
- `HE/` - Homomorphic encryption papers and research documents
- `Hardware Verfication/` - Hardware verification methodologies and tools
- `Neural Network with FHE/` - Privacy-preserving ML with homomorphic encryption
- `61DAC/` - DAC conference proceedings with hundreds of research papers
- `DATE2025-Proceedings/` - DATE conference proceedings

### Key Paper Categories
- **BFV/CKKS Schemes** - Core FHE implementations and optimizations
- **NTT (Number Theoretic Transform)** - Hardware acceleration for polynomial operations
- **RNS (Residue Number System)** - Efficient arithmetic for FHE
- **FPGA Accelerators** - Hardware implementations (F1, Poseidon, ReMCA, HEAP)
- **Bootstrapping** - Key operation for maintaining FHE functionality

## Working with This Repository

### Paper Analysis Tasks
When analyzing papers in this repository:
- Focus on **security/defensive aspects** only - vulnerability analysis, attack detection, defensive architectures
- Papers cover hardware acceleration, cryptographic implementations, and verification methods
- Look for implementation details, performance metrics, and architectural insights

### File Organization
- Papers are organized by research domain in themed directories
- Many files use academic naming conventions with DOI numbers
- Conference proceedings contain hundreds of individual papers
- Some directories contain associated images and figures

### Research Context
This repository represents cutting-edge research in:
- Privacy-preserving computation
- Hardware security acceleration
- Formal verification methods
- Cryptographic algorithm optimization

Note: This is a research repository containing academic papers and conference proceedings. No executable code or build processes are present.