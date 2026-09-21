# Sandbox and Isolation Technology Research
Status: Current supporting research
Last updated: 20 September 2026
Role: Non-authoritative evidence for `../architecture/Deployment and Execution Architecture.md` and `../architecture/Security Privacy and Data Boundaries.md`
Current scope note: the first internal 'On this Mac' slice deliberately uses supervised same-user processes and non-sensitive fixtures; it does not claim hostile-code containment. Local browser operation is now part of the first usable release. Local generated-code containment and session protection must be qualified before external use; cloud providers below remain later deployment options and are not an implicit local-mode fallback. This research informs those gates without selecting a containment implementation.
## Purpose
Evaluate the practical isolation technologies available when the platform crosses the internal same-user prototype boundary and identify the smallest credible posture for executing AI-generated code, Builder harnesses, and hostile browser content in cloud or otherwise isolated workers.
This document is research rather than architecture. Adopted choices belong in the architecture decision register and the isolation architecture.
## Decision question
The platform needs to execute broad, user-generated Python applications and a powerful coding harness without allowing generated code to acquire control-plane access, durable credentials, raw production data, unrestricted network access, or authority outside one exact Build or Run.
The first qualified isolation provider must support:
- a strong boundary for arbitrary generated code;
- disposable per-workload environments;
- bounded CPU, memory, disk, process, time, and network use;
- fast enough startup for interactive internal Apps;
- resumable Builder work;
- complete termination and cleanup;
- outbound-network control enforced outside the guest;
- separate browser execution;
- a credible future path to a private or customer-controlled runtime;
- provider substitution without changing App packages.
## Evaluation criteria
| Criterion | Why it matters |
|---|---|
| Isolation boundary | Generated code and browser content are adversarial inputs even when the user is trusted. |
| Startup and lifecycle | User-created Apps need interactive execution as well as background jobs. |
| Network enforcement | Raw internet access would bypass the Capability, credential, approval, and evidence model. |
| State and checkpoint behavior | Builds must resume; approval waits must not retain compute indefinitely. |
| Operational burden | v0 should not begin as a virtualization or Kubernetes operations company. |
| Compatibility | Python packages, build tools, Chromium, and coding harnesses need ordinary Linux behavior. |
| Portability | The platform must not encode one provider's session or snapshot model into App semantics. |
| Observability and termination | The control plane needs usage, health, cancellation, cleanup, and incident evidence. |
| Private-runtime path | The original vision includes future local, private, and customer-controlled runners. |
## Candidate summary
| Candidate | Isolation | Lifecycle fit | Operational burden | Main limitation | Assessment |
|---|---|---|---|---|---|
| Ordinary Linux containers | Shared host kernel | Fast and familiar | Low to medium | Insufficient primary boundary for hostile generated code | Reject as the only v0 boundary |
| Self-managed Firecracker | Dedicated guest kernel in a microVM | Strong and fast with snapshot support | Very high | Host hardening, jailer, networking, images, patching, scheduling, and snapshot security become platform responsibilities | Preserve as a future provider, do not operate first |
| gVisor `runsc` | Userspace application kernel with a reduced host syscall surface | OCI-compatible; checkpoint/restore available | Medium to high | Compatibility and performance variance; still requires worker-cluster operations | Strong fallback or later self-managed provider |
| AWS ECS/Fargate task per workload | Managed task isolation; each Fargate task receives a dedicated instance | Good for asynchronous and longer tasks | Medium | No native pause/resume and relatively poor fit for low-latency interactive sessions or mutable Builder workspaces | Useful infrastructure option, not the preferred universal v0 sandbox |
| Managed Firecracker sandbox service | One microVM per sandbox with lifecycle APIs | Designed for agent sessions, pause/resume, templates, metrics, and browser/desktop workloads | Low initial burden | Vendor dependency and provider semantics must not become platform semantics | Recommended first cloud-isolation implementation behind an adapter |
## Firecracker
Firecracker supplies a purpose-built virtual machine monitor using KVM. It offers a materially stronger separation than an ordinary container because a workload receives a guest kernel rather than sharing the host kernel directly.
Its production documentation also makes clear that Firecracker is not a complete hosted sandbox by itself. A secure production host requires the jailer, seccomp filtering, cgroups, namespace isolation, dropped privileges, host firewalling, unique identities, resource limits, host patching, and careful CPU configuration. Firecracker recommends one process per single-tenant workload. It does not itself filter guest network traffic.
Snapshot support can make restoration fast, but a snapshot combines guest memory and emulated-device state while disk files are managed separately. Network and vsock connections do not reliably survive restoration. Snapshot inputs must be authenticated and protected externally. Restoring one snapshot more than once can duplicate state that software assumed was unique, including tokens or identifiers.
### Architectural implication
Firecracker is an appropriate isolation primitive. Running Firecracker securely is a separate infrastructure product. The platform should first consume it through a managed provider when the cloud or stronger-containment track begins and retain a provider seam for future self-operation or customer-controlled deployment.
Memory snapshots may accelerate a session. They cannot be the only durable representation of a Build or Run.
Official references:
- [Firecracker production host setup](https://github.com/firecracker-microvm/firecracker/blob/main/docs/prod-host-setup.md)
- [Firecracker snapshot support](https://github.com/firecracker-microvm/firecracker/blob/main/docs/snapshotting/snapshot-support.md)
## gVisor
gVisor interposes a userspace application kernel, called the Sentry, between an application and the host kernel. The Sentry handles most Linux system calls and itself runs with seccomp, namespaces, cgroups, a pivoted root, and minimal capabilities. The default Systrap platform can operate inside a virtual machine; a KVM platform is also available.
This substantially reduces the host-kernel attack surface relative to an ordinary container while retaining OCI integration. gVisor recommends separating different customers into different sandboxes. It does not claim to solve application bugs or all side channels.
gVisor supports checkpoint and restore, root-filesystem snapshots, and background restore. Its documentation notes compatibility requirements between source and destination CPU features. Connected host-network sockets reset on restore and applications must reconnect.
### Architectural implication
gVisor is the strongest practical fallback for a self-managed OCI worker pool. It is particularly attractive if managed-sandbox economics, data placement, or provider limits become unacceptable. It still introduces cluster, kernel-compatibility, image, CNI, patching, scheduling, and checkpoint operations that are not differentiating v0 product work.
Official references:
- [gVisor security model](https://gvisor.dev/docs/architecture_guide/security/)
- [gVisor architecture introduction](https://gvisor.dev/docs/architecture_guide/intro/)
- [gVisor checkpoint and restore](https://gvisor.dev/docs/user_guide/checkpoint_restore/)
## AWS ECS on Fargate
AWS documents that every Fargate task runs on its own dedicated instance and requires explicit CPU and memory sizing. Privileged containers are not supported. Fargate removes direct host management and is a credible strong managed boundary for task-shaped work.
Fargate does not provide the agent-session lifecycle required here as a first-class abstraction: there is no native pause/resume session, filesystem checkpoint, or memory snapshot. A mutable Builder workspace therefore needs external storage and reconstruction, and approval suspension always requires application-level continuation. Starting a new task for every interactive query also introduces latency and task/image orchestration overhead.
### Architectural implication
Fargate remains a plausible provider for longer asynchronous Runs, validation jobs, or a future provider adapter. It is not selected as the one universal v0 sandbox because it fits batch tasks better than interactive Builder and App sessions.
Official reference:
- [Amazon ECS task and container security best practices](https://docs.aws.amazon.com/AmazonECS/latest/developerguide/security-tasks-containers.html)
## E2B as the first managed microVM candidate
E2B currently presents each sandbox as an isolated Linux VM and states that each session runs in its own Firecracker microVM. Its current lifecycle supports create, connect, pause, resume, automatic pause, timeout, kill, templates, filesystem and memory persistence, and CPU, memory, and disk metrics. Desktop sandboxes support graphical browser automation and authenticated streaming.
Current network controls include:
- disabling all outbound internet access;
- per-sandbox IP, CIDR, and domain allow and deny rules;
- disabling unauthenticated public traffic to sandbox URLs;
- blocking common private and link-local ranges outside the guest;
- routing allowed traffic through a customer proxy;
- egress-time secret or workload-identity injection in newer features.
The documentation explicitly warns that domain allowlisting is a routing control rather than a strict security boundary when multiple hostnames share infrastructure. It recommends a controlled proxy when a strict boundary is required. This supports the platform design: the sandbox should reach only a dedicated platform gateway or egress proxy, and that trusted service should evaluate final destinations and credentials.
E2B cloud is the lowest-operations candidate when the isolated-worker track begins. E2B also documents AWS/GCP BYOC, an Apache-2.0 self-hosted infrastructure option, and a common SDK/API across deployment modes. BYOC is a managed Enterprise deployment rather than self-hosting.
### Important limitations
- Public sandbox URLs are accessible by default unless public traffic is disabled.
- Some identity and request-transform features are beta and should not be required for v0 correctness.
- Provider memory snapshots may contain sensitive process state and open connections may need reconstruction.
- Domain filters alone are not a sufficient strict egress boundary.
- Provider APIs, quotas, pricing, retention, regions, support, and lifecycle semantics may change.
- A provider outage or account suspension must not erase canonical platform state.

### Architectural implication

E2B is the recommended first 'SandboxProvider' candidate for the later isolated cloud-worker track, not part of the App Contract and not a dependency of the first local slice. The adapter must fail closed by explicitly denying general outbound access and public ingress. The platform supplies its own short-lived workload token, gateway, egress policy, durable checkpoints, artifacts, Run state, and evidence rather than relying on beta provider identity or secret features.

Official references:
- [E2B documentation and sandbox model](https://docs.e2b.dev/)
- [E2B sandbox lifecycle](https://docs.e2b.dev/sandbox)
- [E2B sandbox persistence](https://docs.e2b.dev/sandbox/persistence)
- [E2B internet-access controls](https://docs.e2b.dev/network/internet-access)
- [E2B public-access controls](https://docs.e2b.dev/network/restrict-public-access)
- [E2B workload identity](https://docs.e2b.dev/iam/workload-identity)
- [E2B sandbox metrics](https://docs.e2b.dev/sandbox/metrics)
- [E2B computer-use environment](https://docs.e2b.dev/use-cases/computer-use)
- [E2B BYOC and self-hosting comparison](https://docs.e2b.dev/byoc)
- [E2B security and deployment overview](https://e2b.dev/enterprise)

## Why ordinary containers are insufficient

The platform intends to execute code generated from natural-language requests, third-party packages, Builder tools, and content retrieved from adversarial websites. That workload should be treated as hostile even when neither the user nor Builder is malicious.

Namespaces, seccomp, cgroups, non-root users, read-only filesystems, and dropped capabilities are necessary defense-in-depth controls. They do not turn a shared-kernel container into the preferred primary tenant boundary for arbitrary code. An escape from an ordinary container reaches a host shared with other tenants. A microVM or gVisor-class intermediary adds a distinct boundary before the host kernel.

Ordinary containers remain useful inside a microVM, for trusted services, for local development, and as a package format. They are not selected as the sole v0 production boundary.

## Profile fit

### Build

A Build needs a mutable filesystem, compiler and test tools, a Builder harness, package retrieval, incremental work, and pause/resume. A managed microVM session fits this directly. A canonical content checkpoint must still exist outside the provider so Builds survive provider loss and can move to another provider.

### Run

A Run needs a clean, short-lived environment containing only one immutable execution closure and one narrow platform SDK identity. The Run should reconstruct from package, input, Context, and durable Run state rather than a prior VM. A fresh microVM per active execution segment is the clearest boundary.

### Browser

A browser processes hostile pages and, when authenticated, highly sensitive session state. It should not run in the same VM as arbitrary App code. A separate browser-profile sandbox can use the same physical provider while having a different image, identity, network proxy, retention, process model, and evidence policy.

### Custom interface

A custom TypeScript interface executes in the user's browser, not in a compute sandbox. It requires an isolated origin, restrictive content-security policy, sandboxed embedding, and the App UI Bridge. Its isolation technology is therefore a browser-origin boundary rather than Firecracker.

## Recommended technology posture

1. Define a provider-neutral 'SandboxProvider' contract owned by the Runner Manager.
2. Require an independent-kernel microVM boundary for arbitrary Build and generated Python execution. Permit a gVisor-class provider only after equivalent qualification against the platform threat model.
3. Evaluate E2B Cloud as the first isolated cloud-provider candidate because it supplies Firecracker microVMs and the needed session lifecycle without requiring a virtualization platform team.
4. Use separate Build, Run, and browser profiles and a fresh sandbox for every active untrusted trust unit.
5. Deny public ingress and general outbound internet explicitly at sandbox creation. Route allowed traffic only through dedicated platform gateways and proxies.
6. Keep canonical state, authority, evidence, and checkpoints in platform-owned services. Provider snapshots are optional acceleration only.
7. Do not self-host Firecracker, introduce a Kubernetes/gVisor cluster, or combine multiple execution providers before qualification or operating evidence requires it.
8. Retain a gVisor-based worker pool and E2B BYOC or self-hosting as future substitution paths, not v0 dependencies.

## Provider qualification conditions

The E2B adapter is eligible for production only if a proof demonstrates all of the following against the exact SDK, API, template, region, and account tier:

- one Firecracker microVM or equivalent independent-kernel boundary per sandbox;
  - fail-closed creation with outbound deny, public ingress deny, and explicit resource limits;


## Screenshot 122 (Image 2)

- no provider credential or durable platform credential inside the guest;
- reachability only to dedicated platform gateway or proxy endpoints;
- blocked metadata, private, loopback-externalization, and link-local destinations;
- non-root Run execution and no host mounts, privileged mode, device exposure, or nested runtime socket;
- immutable App package enforcement or pre/post-execution digest verification;
- deterministic kill, timeout, provider-list reconciliation, and orphan cleanup;
- metrics and lifecycle evidence sufficient for metering and incident analysis;
- encrypted storage and documented snapshot, log, deletion, and regional behavior;
- account, project, and template separation appropriate to development and production;
- quota, concurrency, rate, support, and outage behavior tested under load;
- provider failure cannot authorize stale work or lose canonical Build and Run state;
- a second implementation can satisfy the same conformance suite without changing App code.

## Rejected shortcuts

| Shortcut | Reason rejected |
|---|---|
| Give the Builder or Run a general cloud IAM role | It would bypass the Capability and credential brokers and greatly expand compromise impact. |
| Put durable secrets in environment variables | Generated code, subprocesses, crash logs, snapshots, and package scripts could read them. |
| Allow outbound internet and rely on application policy | Compromised code could exfiltrate data or bypass evidence and approval. |
| Keep one long-lived VM per App | It creates mutable snowflakes, weakens version reproducibility, increases idle cost, and enlarges persistence of compromise. |
| Reuse a dirty sandbox between tenant or Runs | Files, process state, caches, tokens, and side channels can cross trust units. |
| Depend on memory snapshots for approval resume | Connections expire, snapshots contain sensitive state, duplicate restore can duplicate unique state, and provider loss would break correctness. |
| Run authenticated browser sessions in the App-code VM | Page compromise or App code could reach browser credentials and session data. |
| Self-host Firecracker immediately | The necessary host, image, network, scheduling, snapshot, patching, and incident work would dominate v0 without differentiating the product. |

## Remaining evidence to collect before implementation

- Exact E2B data-processing, deletion, regional, encryption, incident, SLA, quota, and subprocessor terms.
- Measured cold-start, package staging, browser startup, pause/resume, and kill latencies.
- Cost per fixture under realistic Build, Run, browser, and idle patterns.
- Compatibility of Python 3.13 compiled dependencies and Chromium with the selected templates.
- Behavior when E2B creation, resume, metrics, network update, or kill calls time out.
- Whether exact network and public-ingress controls are available in the contracted tier and region.
- Whether platform-controlled proxying remains fail-closed during DNS rebinding, redirect, websocket, HTTP/2, and TLS edge cases.
- A minimal gVisor or second managed-provider conformance run proving that the abstraction is real rather than nominal.


