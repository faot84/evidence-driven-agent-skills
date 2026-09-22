---
name: test-tenant-isolation
description: Verify by execution that, in a system where several customers share one database, no tenant can read or change another tenant's data. Use for multi-tenant or SaaS applications with row-level security, tenant_id columns, memberships, or per-organization roles, before accepting a delivery, before showing it to a real customer, and whenever policies, roles, or permissions change. Requires querying as each role instead of reading policies, and distinguishing "nothing happened" from "it is protected". Do not use for general application security or for judging a delivery against its full contract.
---

# Test tenant isolation

## Purpose

In a shared database, the failure that ends a product is not an outage. It is tenant A seeing a row that belongs to tenant B. It cannot be rolled back, because nobody can undo that someone saw something.

That failure is **not found by reading policies**. Reading tells you what the author intended; only execution tells you what the policies do. A review that reads policies correctly can still miss permissions that appear as soon as a query runs while impersonating a tenant administrator.

## The trap that makes most row-level security audits useless

**Zero rows does not prove that a defense works.**

| Check | Result | What it seemed to show | What actually happened |
|---|---|---|---|
| `DELETE FROM accounts` as a normal user | 0 rows | the anti-delete trigger works | row-level security filtered the rows first; the trigger never ran |
| `UPDATE audit_log` as a normal user | 0 rows | the audit log is immutable | same |

Both defenses may still be correct, but that is only known after repeating the check with a role that actually reaches the trigger.

**Hard rule: when a check returns zero rows, state which mechanism produced it**: the permission prevented it, or the defense fired. They are different mechanisms and fail independently. If you cannot tell, the row is **unverified**.

## Method

### 1. Build a minimal, unequal scenario

The test data must make the failure possible. A scenario where everyone has the same rights proves nothing. At minimum:

- two tenants with their own, distinguishable data;
- two users in the same tenant with different roles, such as administrator and operator;
- a second administrator in the same tenant, who reveals abuse between peers;
- a user with no membership;
- an outsider nobody invited;
- a tenant in each possible state, such as active, suspended, and archived.

### 2. Execute as the user, not as yourself

This is the step that is skipped and the one that makes everything else meaningful. Connecting as a database administrator and filtering in your own query proves your `WHERE` clause, not the policy.

In PostgreSQL with a JWT-based platform such as Supabase, one pattern is:

~~~sql
BEGIN;
SET LOCAL ROLE authenticated;
SELECT set_config('request.jwt.claim.sub', '<user id>', true);
SELECT set_config('request.jwt.claims',
  '{"sub": "<user id>", "role": "authenticated"}', true);
-- the query under test
ROLLBACK;
~~~

Set both settings. The single `claim.sub` value feeds only the user-id helper; policies that read the whole token (for example through `auth.jwt()`, including role, app metadata, or assurance level) see nothing and deny, which produces a false "0 rows" pass. Put in the claims JSON every field your policies read.

Always roll back, so each check starts from the same state. Adapt the role and claim names to your platform, and confirm the impersonation works by running one query the user **is** allowed to run and seeing their own rows.

If no real environment is available, create a disposable local database and emulate what the platform provides: the roles, the authentication schema, and a user-id function that reads the same setting. **Always state that the environment is emulated and what it does not cover.** It tests policies, not authentication, storage, or the HTTP layer.

### 3. Sixteen questions

The first five are the boundary between tenants. The rest are the ones rarely written down, and where the interesting defects usually are.

**Between tenants**

1. Can a user of tenant A see any row of tenant B in the core tenant tables (accounts, users, memberships, and the main business records)?
2. Can they fetch it by exact identifier, without going through a list?
3. Can they write, modify, or delete anything of tenant B?
4. Can they create something **attributed** to tenant B?
5. Can they move one of their own rows **into** tenant B by changing its tenant identifier?

**Within one tenant**

6. Can an operator do what only an administrator should?
7. Can an administrator demote, remove, or impersonate **another administrator** of the same tenant?
8. Can an existing membership be reassigned to a different person? Changing a row's owner erases who held it before; removing access should be done by deactivation, which leaves a trace.
9. Can someone grant themselves, or a third party, a higher role than they hold?

**Escalation and audit trail**

10. Can anyone promote themselves to a platform-level role by editing their own profile?
11. Can anyone write to the audit log, or alter what is already there?
12. Is there a path that bypasses the policies, such as a route using a service key, a `SECURITY DEFINER` procedure, or a function that does not filter?

**States**

13. Do suspended and archived tenants actually lose access, or are they merely hidden?
14. Does a deactivated membership actually lose access?

**Apparent protection**

15. Does any **other** table, including lookup, log, and helper tables, return foreign rows when queried as a tenant A user? A common pattern is row-level security enabled with a `USING (true)` policy: it looks protected in the schema and is readable by everyone. Find it by **querying every table**, not by reading policies, so the scenario must cover every table, not only the core ones.
16. Do stored files follow the same boundary as rows? A public bucket, or one with a looser policy, leaks documents even when the database is perfect. Test by downloading, as a tenant A user, a tenant B file through its direct URL.

### 4. Confirm that permitted actions still work

An audit that only tests prohibitions happily approves a system where nobody can do anything. After each fix, repeat the legitimate operations: the platform administrator still sees everything, and a tenant administrator can still add and deactivate an operator. Report both sides in the same run: the abuse now returns zero rows or an error, and each legitimate operation still affects one row.

### 5. Leave a rerunnable test bench

The deliverable is not only a report. It is a file that can be run again. Give each check an identifier, a description, the expected result, the observed result, and a verdict. Without it, the next policy change requires auditing from scratch.

## Look beyond the policies

Policies can be flawless and govern nothing:

- **Routes using a service key.** If the application writes or uploads with a key that bypasses row-level security, the policies are decoration there. The real authorization is in the route code. Find every use and check which permission it requires first.
- **Authorization in one place, filtering in another.** If authorization lives in the database, in middleware, and in handlers with different criteria, the loosest one wins.
- **`SECURITY DEFINER` functions** run with their owner's rights. They skip row-level security when that owner can: a role with `BYPASSRLS`, or the table owner when the table does not use `FORCE ROW LEVEL SECURITY`. On hosted platforms the usual owner often can. Check the owner of each such function; each needs its own justification and its own fixed `search_path`.
- **An `UPDATE` that matches nothing does not error.** It returns zero rows and the interface reports success. Every write should check how many rows changed.
- **`USING` clauses that only check the tenant.** In an `UPDATE`, `USING` sees the old row and `WITH CHECK` sees the new one, and neither can compare them. Preventing a field from changing value needs a trigger or column-level privileges (`GRANT UPDATE (column)`), not a policy.

## Report

One row per question and a plain verdict:

~~~text
| # | What was tested | Expected | Observed | Verdict |
|---|---|---|---|---|
| 02 | Tenant A operator fetches a tenant B account by id | 0 rows | 0 rows, own account visible in the same session | pass |
| 07 | Tenant A admin demotes another tenant A admin | 0 rows or error | 1 row affected | FAIL |
~~~

Always end with three things: what could not be tested and why, whether the environment was real or emulated, and what lies outside the emulated scope. A fully green table does not mean the system is isolated. It means these questions, and only these, found nothing.

## Limits

This skill does not cover general application security, does not judge a delivery against its whole contract, and does not replace testing against the real platform. It answers exactly one question: whether one tenant can reach another tenant's data.
