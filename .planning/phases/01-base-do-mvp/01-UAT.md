# 01 UAT

## Environment
- Docker Compose stack running: `db`, `backend`, `frontend`
- Backend available at `http://localhost:8000`
- Frontend available at `http://localhost:3000`

## Tests executed
1. User registration and login via API
   - `POST /api/register/` created a new user
   - `POST /api/login/` returned valid access and refresh JWT tokens
   - Result: **PASS**

2. Investment CRUD flow via API
   - Authenticated request created an investment record
   - Authenticated request listed the same investment for the logged-in user
   - `lucro_prejuizo` was calculated correctly
   - Result: **PASS**

3. Frontend page rendering
   - `GET /login` returned an HTML page containing the login form
   - `GET /investments` returned the investments page shell and client scripts
   - Result: **PASS**

## Findings
- The backend is functionally serving auth and investment APIs.
- The frontend is serving the expected Next.js pages.

## Issue identified
- Backend startup logs show a Django migration warning:
  - `Your models in app(s): 'users' have changes that are not yet reflected in a migration`
- Confirmed by running `python manage.py makemigrations --dry-run --check` inside the backend container.
- It reports a pending migration: `users/migrations/0002_alter_user_options_alter_user_managers.py`

## Impact
- Current user and investment flows work in this session.
- However, the backend schema state is inconsistent with the current `users` model definition.
- This may cause future schema drift, deployment instability, or missing data model changes.

## Fix plan
1. Generate and commit the missing migration for the `users` app.
   - `docker compose exec backend python manage.py makemigrations users`
2. Apply the migration in the running backend:
   - `docker compose exec backend python manage.py migrate --noinput`
3. Re-run the UAT flow to confirm the warning is gone and the API remains functional.

## Next step
- This issue is ready for `/gsd-execute-phase` as a fix task before the phase is considered fully verified.
