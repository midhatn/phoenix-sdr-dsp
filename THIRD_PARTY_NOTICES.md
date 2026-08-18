# Third-party notices and provenance

This file inventories third-party material distributed in this repository. It
does not change the repository-wide MIT license for original Phoenix SDR-DSP
work; files carrying their own notices remain subject to those notices.

## Distributed source

| Path | Origin and provenance | License / notice |
|---|---|---|
| `kernels/fft_stockham_f32.cc` | Adapted from AMD-authored [`diacccc/FFT_R4_AIE`](https://github.com/diacccc/FFT_R4_AIE), as identified in the file header and [`CITATION.cff`](CITATION.cff). | Apache License 2.0 with LLVM Exceptions; retain the file-level copyright, SPDX identifier, and attribution. The Apache 2.0 text is included in [`LICENSES/Apache-2.0.txt`](LICENSES/Apache-2.0.txt). |

## Test-vector provenance

The ML-KEM and ML-DSA JSON vectors under `tests/m32_mlkem/vectors/` and
`tests/m33_mldsa/vectors/` are retained test data from the
[NIST ACVP-Server Gen/Vals repository](https://github.com/usnistgov/ACVP-Server).
Their exact upstream commit/tree hash and distribution manifest are not yet
recorded in this repository. Do not infer an OSI license from this provenance
note; release work must record the upstream revision, vector hashes, and
applicable notice before representing the data as a reproducible release
artifact.

## Dependencies not redistributed

MLIR-AIE/IRON, XRT, LLVM-AIE/Peano, `kyber-py`, and `dilithium-py` are obtained
externally by the bootstrap or user environment and are not copied into this
repository. Their versions and acquisition URLs are recorded in
[`toolchain.yaml`](toolchain.yaml) and
[`requirements/toolchain-versions.md`](requirements/toolchain-versions.md);
their licenses must be reviewed from their upstream distributions.

## Maintenance policy

When adding imported code or test data:

1. retain upstream copyright and license notices in the imported file;
2. add its path, immutable origin URL/revision, and license expression here;
3. add the license text under `LICENSES/` when the license requires or
   benefits from local redistribution; and
4. do not replace a file-specific SPDX expression with the project-wide MIT
   identifier.

SPDX guidance on file-level identifiers:
https://spdx.dev/learn/handling-license-info/
