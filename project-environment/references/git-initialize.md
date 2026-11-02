# Initialize Git Repository

Initialize a Git repository in the current project directory if one does not already exist.

## Execution

Run the appropriate script from the project root:

- **Bash**: `<this-skill>/scripts/initialize_repo.py`
- **PowerShell**: `<this-skill>/scripts/initialize_repo.py`

Run `python3 <this-skill>/scripts/initialize_repo.py` from the actual project root. It initializes Git only by default, retains existing repositories, and never stages files. To make an authorized initial commit, inspect and stage the intended files and commit them explicitly. `--initial-commit` can create an empty initial commit during initialization; it does not stage the working tree. Failure is reported rather than disguised as a complete setup.

## Customization

Replace the script to add project-specific Git initialization steps:
- Custom `.gitignore` templates
- Default branch naming (`git config init.defaultBranch`)
- Git LFS setup
- Git hooks installation
- Commit signing configuration
- Git Flow initialization

## Output

On success:
- `[OK] Git repository initialized`

## Graceful Degradation

If Git is not installed:
- Warn the user
- Skip repository initialization
- The project continues to function without Git (specs can still be created under `specs/`)

If Git is installed but an authorized Git operation fails:
- Surface the error to the user
- Stop this command rather than continuing with a partially initialized repository
