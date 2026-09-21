# Application Package Layout

Specification version: 0.1, revision 3
Status: Accepted design baseline
Last updated: 21 September 2026

## Purpose

This specification defines the portable handoff from a Builder to the platform compiler and the immutable package stored for an App Version.

The package boundary lets any compatible builder harness create applications without controlling publication, permissions, credentials, production providers, or runtime infrastructure.

The keywords MUST, MUST NOT, SHOULD, SHOULD NOT, and MAY are normative.

Revision 3 aligns the TypeScript dependency lock with the qualified pnpm runtime profile. Portable native-view and agent shapes remain valid package vocabulary, but the v0 runtime profile accepts only the React/TypeScript/Vite micro-frontend Surface path plus the trusted no-Surface fallback.

## Core decision

There are four different artifacts. They must not be collapsed into one mutable folder.

| Artifact | Mutable | Owner | Purpose |
|---|---:|---|---|
| Build working tree | Yes | Builder sandbox | Implementation workspace, logs, caches, and intermediate files |
| Source App Package | No after handoff | Builder produces; compiler consumes | Portable source declaration and referenced content |
| Sealed App Version Package | No | Package service | Validated, compiled, content-addressed application version |
| Run projection | Ephemeral | Runner | Minimum files and declarations needed for one Entrypoint |

The Builder submits a Source App Package. It never writes a live App Version or production filesystem.

## Source App Package

The Source App Package is a directory tree rooted at `app.yaml`.

```text
app.yaml
schemas/
components/
ui/
agents/
tests/
assets/
```

Only `app.yaml` and files referenced directly or transitively by the Source App Manifest are required. Empty directories are not retained.

### Top-level ownership

| Path | Owner | Allowed content |
|---|---|---|
| `app.yaml` | Builder | Source App Manifest |
| `schemas/` | Builder | JSON Schemas and UI-schema hints |
| `components/` | Builder | Python handler bundles and their dependency locks |
| `ui/` | Builder | Native-view declarations, TypeScript micro-frontend sources, and UI dependency locks |
| `agents/` | Builder | Declarative bounded-agent definitions |
| `tests/` | Builder | Unit, fixture, outcome, health, and test-data files |
| `assets/` | Builder | Passive images, fonts, and documents used by the App |
| `app.resolved.json` | Platform only | Canonical Resolved App Manifest |
| `package.index.json` | Platform only | Complete sealed-package inventory |
| `.platform/` | Platform only | Compiler-generated executable artifacts |

A Source App Package MUST NOT contain `app.resolved.json`, `package.index.json`, or `.platform/`. Any other top-level path is rejected in v0.

## Sealed App Version Package

The package service validates the source package, compiles generated artifacts, adds platform-owned files, and seals the result.

```text
app.yaml
app.resolved.json
package.index.json
schemas/
components/
ui/
agents/
tests/
assets/
.platform/
  artifacts/
    <component-id>/
      <content-digest>/
        <runtime artifact>
```

The sealed package retains source declarations and tests for audit, repair, and reproducibility. Production workers receive only a Run projection, not the complete package.

### Generated artifacts

- A `handler-bundle` may be copied unchanged when it is already in the platform's accepted executable bundle format. Otherwise the compiler produces a normalized Python artifact.
- A `micro-frontend` is compiled from TypeScript into a browser bundle plus required static assets.
- An `agent` or `native-view` is validated and copied into a normalized declarative artifact.
- Generated paths are content-addressed beneath `.platform/artifacts/` and referenced by digest from `app.resolved.json`.
- Builder-authored code MUST NOT write into `.platform/`.

## Path rules

Every package path MUST:

- be relative to the package root;
- use `/` separators;
- be valid UTF-8 normalized to Unicode NFC;
- contain no empty segment, `.` segment, `..` segment, control character, or NUL;
- remain at or below the package root after normalization;
- avoid case-folding collisions with every other path;
- avoid Windows device-name segments and trailing spaces or periods;
- be no longer than 512 bytes in UTF-8.

Symbolic links, hard links, sockets, named pipes, devices, mount points, and sparse-file tricks are forbidden. Every retained item is a regular file or directory.

The following content is always excluded or rejected:

- `.git`, editor metadata, caches, temporary files, and operating-system metadata;
- virtual environments, `node_modules`, downloaded package caches, and mutable dependency directories;
- environment files, credential stores, browser profiles, cookies, tokens, and private keys;
- platform control-plane clients or direct provider credentials;
- Builder-supplied native binaries. A runtime profile may allow the platform to build and scan exact hashed native dependencies from approved registries.

## Reachability and file roles

Every file in a sealed package appears once in `package.index.json` with a role.

Supported v0 roles are:

- `source-manifest`
- `resolved-manifest`
- `schema`
- `component-source`
- `component-artifact`
- `dependency-lock`
- `agent-definition`
- `ui-definition`
- `test`
- `test-fixture`
- `asset`

Executable behavior MUST be reachable from a declared Component root or compiler-generated artifact. An unreferenced script, import root, executable archive, or configuration file that could alter runtime behavior is rejected.

Passive assets and test fixtures may be indirectly referenced, but the compiler must prove and record their owning Component or test. Unreachable passive files are omitted from the sealed package.

Package-retained fixtures MUST be synthetic, sanitised, or otherwise approved for immutable retention. Real Workspace records, uploaded customer files, production extracts, browser captures, and preview samples MUST remain outside the package as access-controlled Build or validation artifacts. The App Version references their validation result set, not their bytes.

## Dependency locks

Every executable `handler-bundle` and `micro-frontend` requires one dependency lock, as already declared by the App Contract.

The Component registry defines accepted lock formats. The v0 direction is:

| Component | Preferred lock | Minimum requirement |
|---|---|---|
| Python handler | `pylock.toml` or a compiler-normalized equivalent | Exact package versions, artifact hashes, Python compatibility, source index, and no editable or local-path dependency |
| TypeScript micro-frontend | `pnpm-lock.yaml` in the lock format qualified by the runtime profile | Exact resolved package identities, integrity hashes, and no mutable Git branch or local-path dependency |

The compiler MUST reject:

- version ranges that remain unresolved;
- dependencies without an integrity hash;
- mutable VCS references;
- undeclared registries or direct arbitrary download URLs;
- lockfiles inconsistent with imported packages;
- install scripts or native extensions not permitted by the runtime profile;
- a build whose dependency graph differs from the declared lock.

The sealed package records both the original lock and the exact resolved dependency graph used to build each artifact.

## `package.index.json`

The package index is generated after `app.resolved.json`. It contains:

```json
{
  "apiVersion": "alpha.platform.package/v0.1",
  "kind": "AppPackageIndex",
  "sourceManifest": {
    "path": "app.yaml",
    "digest": "sha256:<raw-file-digest>",
    "canonicalDigest": "sha256:<canonical-parsed-manifest-digest>"
  },
  "resolvedManifest": {
    "path": "app.resolved.json",
    "digest": "sha256:<canonical-resolved-manifest-digest>"
  },
  "files": [
    {
      "path": "schemas/input.schema.json",
      "mediaType": "application/schema+json",
      "sizeBytes": 1234,
      "digest": "sha256:<file-digest>",
      "role": "schema",
      "owner": "entrypoint:refresh"
    }
  ]
}
```

Rules:

1. `files` contains every sealed-package file except `package.index.json` itself.
2. Entries are sorted lexicographically by normalized path.
3. A path appears exactly once.
4. `digest` is SHA-256 over the exact file bytes.
5. `sizeBytes` is the exact uncompressed byte size.
6. `mediaType` is authoritative and validated against content; extensions are not trusted.
7. `owner` identifies the logical declaration responsible for the file.
8. `app.yaml` and `app.resolved.json` appear in `files` as well as in their named summary fields; the values must match.

The **package digest** is SHA-256 over the RFC 8785 canonical JSON bytes of `package.index.json`. The index does not contain its own digest, avoiding a recursive hash. The App Version record stores the package digest.

`source.fileSetDigest` in the Resolved App Manifest is SHA-256 over the RFC 8785 canonical JSON array of all Builder-owned file entries, sorted by path, excluding `app.resolved.json`, `package.index.json`, and `.platform/`. Each entry contains exactly `path`, `mediaType`, `sizeBytes`, `digest`, `role`, and `owner`.

This descriptor shape is intentionally compatible with content-addressable artifact stores, but v0 does not require one particular archive registry or OCI deployment.

## Canonical source-manifest digest

`source_manifest_digest` is not the digest of YAML formatting. The compiler:

1. parses `app.yaml` using the YAML 1.2 JSON-compatible scalar subset;
2. rejects duplicate keys, anchors, aliases, merge keys, custom tags, timestamps, binary scalars, non-finite numbers, and implicit implementation-specific types;
3. converts the result to a JSON data model;
4. normalizes all strings to Unicode NFC;
5. serializes using RFC 8785 JSON Canonicalization Scheme;
6. computes SHA-256 over those bytes.

Equivalent supported YAML formatting therefore produces the same source-manifest digest. Exact source-file bytes remain separately recorded in the package index.

## Deterministic sealing

Given identical source bytes, compiler version, registry snapshot, SDK resolution, approved build profile, and dependency artifacts, sealing MUST produce identical:

- compiler-generated artifact bytes;
- `app.resolved.json` bytes;
- `package.index.json` bytes;
- package digest.

Compiler-generated outputs MUST exclude wall-clock timestamps, random identifiers, absolute build paths, usernames, hostnames, non-normalized archive metadata, and nondeterministic file order.

When a transport archive is used, it MUST normalize entry order, ownership, permissions, timestamps, and compression settings. The package digest remains based on `package.index.json`, not transport bytes.

## Provenance and attestation

After successful validation, the platform records an immutable App Version provenance record binding:

- package digest;
- resolved-manifest digest;
- source-manifest digest;
- compiler identity and version;
- registry snapshot;
- validation-set identity;
- Builder and Build identity;
- creation principal.

The provenance record is control-plane metadata, not a mutable file inside the package. v0 integrity relies on content digests, protected control-plane records, and immutable storage. The platform MAY cryptographically sign the record, but signing is not required until packages cross a platform trust boundary. Third-party and marketplace signatures remain deferred.

## Run projection

The Runner receives a read-only projection for one Entrypoint containing only:

- the exact resolved-manifest execution closure;
- the implementing Component artifact;
- its locked dependency environment or image identity;
- referenced input and output schemas;
- referenced passive assets;
- the platform SDK client required by the runtime profile.

Tests, unrelated Components, Builder files, source credentials, other Entrypoints, and package-wide write access are absent. Runtime Resources, Context snapshots, Capability tokens, configuration, and Connection use are injected through typed platform interfaces; they are not written into the projection.

## Validation pipeline

The Package Service performs these ordered gates:

1. Safely extract and normalize the incoming package.
2. Validate path, file-kind, count, and size limits.
3. Parse and structurally validate `app.yaml`.
4. Resolve logical references and determine file ownership and reachability.
5. Validate dependency locks and reproduce dependency resolution.
6. Scan secrets, content, archives, imports, binaries, and network behavior.
7. Compile Components into platform-owned artifacts.
8. Resolve the App Contract against the pinned registry snapshot.
9. Create and schema-validate `app.resolved.json`.
10. Execute required static, unit, fixture, outcome, and preview gates.
11. Generate `package.index.json` and verify every digest from clean bytes.
12. Rebuild in a clean environment when reproducibility verification is required.
13. Seal the package and create the immutable App Version record and attestation.

No preview or active Release may execute an unsealed Build working tree.

## Standard errors

| Code | Meaning |
|---|---|
| `PKG_ROOT_INVALID` | Required root or `app.yaml` is missing or duplicated |
| `PKG_RESERVED_PATH` | Builder content uses a platform-owned path |
| `PKG_PATH_INVALID` | A path violates normalization or containment rules |
| `PKG_LINK_FORBIDDEN` | A link, device, socket, pipe, or special file is present |
| `PKG_CASE_COLLISION` | Two paths collide under case folding |
| `PKG_FILE_UNREACHABLE` | A behavior-affecting file is not owned by a declaration |
| `PKG_CONTENT_FORBIDDEN` | Disallowed binary, archive, script, or active asset is present |
| `PKG_SECRET_DETECTED` | Credential-like material is present |
| `PKG_DEPENDENCY_UNLOCKED` | A dependency is not reproducibly locked |
| `PKG_DEPENDENCY_MISMATCH` | Imports or built dependencies differ from the lock |
| `PKG_BUILD_NONDETERMINISTIC` | Clean builds produce different artifacts |
| `PKG_INDEX_INVALID` | The package index is incomplete, duplicated, or inconsistent |
| `PKG_DIGEST_MISMATCH` | Recorded digest or size does not match content |
| `PKG_ATTESTATION_INVALID` | The App Version attestation is missing or invalid |

## Compatibility

- The package-index `apiVersion` governs index structure and digest semantics.
- A package may be recompiled only into a new App Version; a sealed package never changes in place.
- Runtime profile or compiler upgrades do not mutate old packages.
- A Release may activate an old package only while its contract, SDK, runtime profile, dependencies, and policy metadata remain supported.
- Storage transport and registry implementation may change without changing package identity, provided file bytes and `package.index.json` remain unchanged.

## Security invariants

1. A package contains no Workspace bindings, Grants, raw secrets, production configuration values, or provider credentials.
2. Generated code cannot influence its own validation, resolved metadata, package inventory, digest, or attestation.
3. Release binding may reduce authority but cannot add undeclared Capabilities or Resources.
4. Runtime never resolves an omitted dependency or default dynamically.
5. Workers verify package and Component digests before execution.
6. Only the Package Service writes platform-owned paths.
7. Real Workspace or user data is never sealed into an App Version as a test fixture.

## Accepted decisions

1. Use a content-addressed logical file tree rather than making Docker or OCI the public App Package format.
2. Reserve `.platform/` for compiler-generated artifacts.
3. Define package identity as the digest of canonical `package.index.json`, independent of archive encoding.
4. Retain source and tests in the sealed package, but execute only a minimal per-Entrypoint projection.
5. Require platform provenance records in v0; defer mandatory cryptographic signing and third-party signatures until packages cross a trust boundary.

## External standards referenced

- [RFC 8785 JSON Canonicalization Scheme](https://www.rfc-editor.org/rfc/rfc8785.html)
- [Open Container Initiative image specification](https://specs.opencontainers.org/image-spec/?v=v1.1.1), used only as inspiration for digest descriptors and transport compatibility
- [Python reproducible environment lock-file specification](https://packaging.python.org/en/latest/specifications/pylock-toml/)
