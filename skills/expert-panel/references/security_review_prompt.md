# Security Review: attacker-led coverage profile

Use for an owned or explicitly authorized web application, API, repository, lab or CTF. Start with `offensive_security.md`: establish engagement scope, then think from the attacker side. This file supplies web-focused attack classes; it is not a passive compliance checklist.

For each class, trace **entry point → attacker-controlled value/action → parsing/normalization → security decision → sensitive sink → observable boundary result**. Record an attack hypothesis, prerequisites, target invariant, bypass idea, evidence that would falsify it, and exploit status: `CONFIRMED`, `CONDITIONAL`, `BLOCKED`, or `REJECTED`. In an authorized local/test environment, validate with the minimum-impact reproducible PoC; do not call a source pattern exploitable without observing the primitive or documenting the exact missing external control.

## Web attack classes

1. **Injection and execution:** SQL/NoSQL/LDAP/template/command injection, unsafe deserialization, expression languages, file inclusion and code-loading boundaries. Follow canonicalization and quoting through every layer; test a harmless marker or dummy record rather than destructive commands.
2. **Browser execution:** reflected/stored/DOM XSS, unsafe HTML/URL/CSS sinks, CSP bypass assumptions, postMessage origin handling, prototype pollution and script gadget composition. Demonstrate controlled execution only in the agreed app/test origin.
3. **Request and network pivoting:** SSRF, request smuggling/splitting, host-header trust, open redirect composition, DNS/rebinding assumptions, internal metadata/control-plane reachability. Stop at a controlled loopback/canary or owner-observed request.
4. **Object and tenant authorization:** IDOR/BOLA/BFLA, mass assignment, role/tenant switching, indirect object references, export/search leakage and batch endpoints. Use dummy principals and cross-tenant fixtures.
5. **Authentication/session/token attacks:** account enumeration, reset/recovery weaknesses, MFA state transitions, session fixation/hijacking, JWT/key confusion, OAuth/OIDC redirect/state/PKCE mistakes and stale/revoked credential handling. Never capture credentials from real users.
6. **CSRF and state-machine abuse:** browser-ambient authority, SameSite/CORS assumptions, replay, duplicate actions, race/TOCTOU, order-dependent workflows, negative quantities, refund/credit abuse and idempotency failures.
7. **File and parser attacks:** traversal, overwrite, archive extraction, polyglot/type confusion, image/document parsers, decompression/resource bombs and unsafe public/private object boundaries. Use bounded fixtures and size/time limits.
8. **Secrets and privilege transitions:** hardcoded/client-exposed secrets, CI logs/artifacts, signing keys, service identities, IAM/ACL delegation, admin routes and cloud metadata. Mask actual secrets; proving exposure does not authorize using them outside the test.
9. **AI/agent attack paths:** indirect prompt injection, confused-deputy tool calls, cross-tenant memory, retrieval poisoning, tool-output injection, excessive agency and secret/data exfiltration. Use synthetic data and controlled tools.
10. **Supply chain and deployment:** dependency confusion/typosquatting signals, build/release trust, artifact substitution, unsafe install hooks, exposed debug/control planes, proxy/header assumptions and environment-dependent controls. Do not publish a poisoned package or compromise a third-party dependency.

## Output

1. **Engagement card:** authorization basis, scope, allowed techniques, excluded targets, stop conditions and tools actually available.
2. **Attack-surface map:** assets, principals, entry points and trust transitions.
3. **Attack hypotheses:** table with path, preconditions, bypass, falsifier and status.
4. **Confirmed findings:** exact location/endpoint, technical mechanism, minimum PoC/reproduction, observed boundary result, impact/likelihood/severity, fix invariant and regression test.
5. **Attack chains:** link only confirmed or explicitly conditional steps; state access gained and missing proof at each transition.
6. **Rejected/blocked hypotheses and coverage gaps:** show what was falsified or could not be validated.

In agent hosts, use separate scoped hunters for distinct attack classes and a fresh exploit verifier. In web chat, use sequential attacker/falsifier passes and state that they are one model. Do not expose hidden chain-of-thought; expose the concise technical rationale and reproducible evidence needed to audit the finding.
