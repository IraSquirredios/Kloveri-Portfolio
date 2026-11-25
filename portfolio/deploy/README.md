# Official test deployment

The pipeline follows Wiki `exploitation/mnt/cicd/frontend` and the frontend/react
reference template, adapted for portfolio_frontend, npm/Node 24 and API proxies.
It uses runner tag `docker` and internship init project `cloveri.start/cicd/env-init`.
It does not use the legacy runner tag `own` or the Swarm service on port 6060.

## Required project settings (maintainer)

- SERVICE_DOMAIN: allocated DNS hostname only, without scheme or path.
- INIT_TOKEN: existing project API access token for the environment init project.
  Do not commit its value, and do not create/expand credentials without approval.
- ENV_FILE: GitLab variable of type File, containing public frontend settings:

```dotenv
VITE_PROJECT_ID=<project-uuid>
VITE_ACCOUNT_ID=<account-uuid>
VITE_API_URL=/api
VITE_DIRECTORY_API_URL=/directory-api
```

VITE_* values are bundled into browser code. Never put passwords/access tokens
in this file. The temporary .env.production is included only in the build stage.
No runtime env file or local FastAPI is required.

The environment-init pipeline supplies shared SSH, registry and mirror settings
including SSH_CONF, GATE_KEY, HOST_KEY and DOCKER_HUB_MIRROR. These are not stored
in the repository. The documented SERVICE_IP algorithm supplies an internal
container address; the deployment binds it on :8080 and installs the external
nginx virtual host from deploy/nginx-template.conf.

## Pipeline

Runs on feat/portfolio-products-api and dev. Preflight validates required settings
without printing values; init_vars triggers the internship environment initializer.
Build uses immutable commit-SHA image tags and runs nginx -t before pushing.
Deploy is manual, serialized by resource_group, and records https://SERVICE_DOMAIN
in the dev environment. Confirm the assigned domain/target host before starting it.
Master and production deployments are disabled in this configuration.

The root Dockerfile/docker-compose.yml remain legacy files. This pipeline explicitly
uses Dockerfile.portfolio and deploy/compose.yml. deploy/portfolio-review.compose.yml
is the retired experimental Swarm configuration and is no longer used by CI.

After deployment, verify the environment URL, /healthz, login, products and categories.
Successful local frontend tests do not verify remote Docker/SSH/DNS availability.
