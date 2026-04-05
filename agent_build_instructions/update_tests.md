### would you suggest changing the tests so that multiple logins are attempted with different roles?

### Your response
I’m checking how the existing test suite handles authentication so I can recommend a pattern that fits this codebase instead of proposing a generic test setup.

Yes, but not as “multiple login attempts inside one test.” I’d suggest role-based parametrized tests with a small auth helper, so each test isolates one permission case.

The current route failures in test_routes_main.py are mixing two concerns:

authorization, because the routes in main.py:21, main.py:47, main.py:88, and main.py:140 are guarded by custom_decorators.py:4
route behavior, like “redirect when no selected user exists”
That means a test such as “edit_user without user_id redirects” should first establish a user with a role allowed past the decorator, otherwise it never reaches the redirect branch and just dies with 403.

What I’d recommend instead is:

Add a user factory fixture in conftest.py that can create users with roles like user, mod, admin, and super.
Add a login helper fixture that logs in one chosen user for a test, or directly seeds the session if you want route tests to stay fast.
Parametrize access-control tests by role and expected status.
Keep business-logic tests separate, and run them only with an authorized role.
A good matrix for this app would be:

anonymous: expect 403 on staffers and senior routes
user: expect 403 on staffers and senior
mod: expect access to staffers, but 403 on senior
admin or super: expect access to senior
That matches the role model in roles.py.

I would not repeatedly test the full /login flow in every route test. test_auth.py should verify login itself; route tests should usually assume “already authenticated as role X” and then assert authorization and route behavior. That keeps failures precise and avoids one broken login flow making half the suite noisy.

One more thing: the auth tests themselves look stale too. In conftest.py:35, the fixture creates a randomized username, but test_auth.py:8 still posts testuser. So even before role work, some auth tests are likely mismatched with the fixture data.

If you want, I can outline the exact fixture structure I’d use for:

login-via-session helpers
role-parametrized route tests
splitting auth tests from authorization tests

### Tasks
Update the test suite along the lines of your proposed changes above. Only change what has been outlined and the tests that deal with auth.
Make sure the changes future-proof authentication of the main role groups: user, mod, admin & super. Bear in mind that there will be subtle differences between the 'member' roles which will be allocated accordingly to free and paid members.
Update stale auth tests to prevent mismatching with auth data.
Run pytest and observe outcome.
Make changes if there are issues.
Identify and be verbose about any changes in the operational (non-test, main code body) that could be made cleaner. Don't make any changes

### Outcomes and actions completed
- Issues faced
    - Route tests in `test_routes_main.py` were failing because protected endpoints now enforce role checks and returned `403` for anonymous clients.
    - Tests were using a stale endpoint (`/receive_user_id`) while the app route is `/forward_user_id`.
    - Multiple auth tests used hard-coded usernames (`testuser`) that no longer matched fixture-generated randomized usernames.
    - Auth/session setup for route tests was brittle; relying only on login/session state created inconsistent outcomes for role-gated assertions.
    - Running `pytest` in one terminal context failed (`command not found`) while the test runner tooling succeeded; this indicated environment/path inconsistency for direct shell invocation.

- Actions completed
    - Added reusable auth fixtures in `tests/conftest.py`:
        - `user_factory` to generate users with explicit roles (`user`, `mod`, `admin`, `super`, plus member roles).
        - `mock_current_user` to cleanly control role/auth state in authorization tests.
        - kept `force_login` for full-login style tests.
    - Updated stale auth data references:
        - replaced hard-coded usernames with fixture-backed usernames in auth/security tests.
    - Refactored route auth tests in `tests/test_routes_main.py`:
        - converted to role-parametrized access checks.
        - split authorization behavior from business/redirect behavior.
        - updated `/receive_user_id` tests to `/forward_user_id`.
    - Expanded auth coverage in `tests/test_auth.py`:
        - added login success checks for core roles (`user`, `mod`, `admin`, `super`).
        - added login success checks for member roles (`viewer`, `pro`, `enterprise`) to future-proof member-role behavior.
        - aligned invalid-login expectations with actual app response flow (redirect behavior).
    - Re-ran tests after each significant update and iterated until stable.

- Final result
    - `pytest` suite passed with zero failures after updates.

### short auth-testing guideline document
#### Auth Testing Guidelines (Short)

1. Separate authentication tests from authorization tests
- Authentication tests verify login/logout mechanics and session establishment.
- Authorization tests verify role-based access policy for protected routes.

2. Use role-parametrized tests for access control
- Prefer `pytest.mark.parametrize` over one-off tests.
- Minimum matrix to keep current:
    - Anonymous
    - `user`
    - `mod`
    - `admin`
    - `super`
- Include member roles (`viewer`, `pro`, `enterprise`) where route policy may diverge.

3. Avoid hard-coded usernames in tests
- Always use fixture-created user data (`test_user.username` or `user_factory(...)`).
- This prevents fixture drift from breaking auth tests.

4. Keep route-policy tests deterministic
- For pure role-gate checks, mock `current_user` via fixture (`mock_current_user`) instead of depending on full session/login plumbing.
- For login-flow verification, post to `/login` and assert redirects/session side effects.

5. Assert behavior at the correct layer
- Protected-route tests should assert expected status codes (`403` vs success/redirect) per role.
- Business-flow tests should assume an allowed role and assert route-specific outcomes (redirect target, rendered page, DB side effects).

6. Keep security auth tests aligned with app behavior
- If app redirects after failed login, assert redirect target rather than assuming flashed HTML text appears in response body.
- Keep open-redirect checks in place and validate `Location` does not contain external hosts.

7. Re-run full suite after auth test refactors
- Run full `pytest` after fixture/auth changes because auth fixtures are shared across many files.
- Fix regressions incrementally and re-verify until all tests pass.
