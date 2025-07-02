instructions

- When importing from Python files in the `src` directory, use absolute imports starting with `src`. For example: `from src.discord_bot import bot`.
- the python evrironment starts inside api, do not start imports with `api.`
- when refactoring functions and interfaces, verify you didn't break other packages with `source /app/api/.venv/bin/activate.fish; cd /app/api; pyright`

- When installing javascript packages, use `pnpm`. Install them in the `client` directory. For example: `cd client && pnpm install package-name`.
- Get all icons from the `@fortawesome/fontawesome-free` package.