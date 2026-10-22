# Security Policy

## Supported versions

Only the latest commit on the default branch is supported with security fixes.

## Reporting a vulnerability

Please **do not** open a public issue for a security problem.

Report privately through GitHub's
[Report a vulnerability](../../security/advisories/new) form, or by email to
the maintainer, **Dr Abdulmalek Al-Husseini**.

Include:

- a description of the issue and its impact,
- the affected file path or dependency,
- reproduction steps or a proof of concept,
- any suggested remediation.

## What to expect

| Stage | Target |
|---|---|
| Acknowledgement of the report | 3 working days |
| Initial assessment and severity | 7 working days |
| Fix or mitigation plan | 30 days for high/critical |

## Scope

In scope: credentials or secrets committed to this repository, dependency
vulnerabilities, injection and authentication flaws, and unsafe handling of
uploaded files or user data.

Out of scope: findings that require a compromised local machine, social
engineering, and missing hardening headers on non-production deployments.

## Handling of leaked credentials

If you discover a credential in this repository, report it privately as above
rather than opening an issue. The maintainer will revoke and rotate it, then
remove it from the working tree. Note that a revoked credential remains
readable in commit history, which is why rotation always comes first.
