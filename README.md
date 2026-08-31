# Using this repo as a Copier template

This repository is a [Copier](https://copier.readthedocs.io/) template. The
repo root itself is the template source — that's why paths like
`[[project_slug]]/` and file contents contain Jinja placeholders (using
`[[ ]]` / `[% %]` delimiters instead of the default `{{ }}` / `{% %}`, to
avoid colliding with GitHub Actions' `${{ ... }}` syntax — see `copier.yml`).
It is not meant to be run directly; generate a real project from it first.

## Generate a new project

```bash
pipx install copier   # one-time
copier copy gh:yfnel/svango my-new-app
```

Answer the prompts (`project_name`, `project_slug`, `author_name`,
`use_ldap`, `use_stage`, `use_utils`, ...), or supply them non-interactively:

```bash
copier copy gh:yfnel/svango my-new-app \
  --data project_name="Acme Billing" \
  --data use_ldap=false \
  --defaults
```

Pin a specific template version/branch with `--vcs-ref v1.0.0`.

## Turn the generated output into a real repo

```bash
cd my-new-app
git init && git add -A && git commit -m "Initial commit from svango template"
poetry install --with dev
poetry run pytest
poetry run ruff check .
```

## Pulling in later template updates

Every generated project gets a `.copier-answers.yml` recording which
template version and answers were used. To pull in template improvements
later:

```bash
copier update
```

Conflicts are marked like a git merge conflict for manual resolution.

## Testing the template itself

Since the repo root can't be run directly, validate changes by rendering it
into a throwaway directory and running the real checks there:

```bash
copier copy . /tmp/rendered --defaults
cd /tmp/rendered
poetry install --with dev
poetry run ruff check .
poetry run pytest
```

This is exactly what `.github/workflows/template-selfcheck.yml` does in CI.
