# EXAMPLE: Extension README

This is an example of what your extension README should look like after customization.
**Delete this file and replace README.md with content similar to this.**

---

# My Extension

<!-- CUSTOMIZE: Replace with your extension description -->

Brief description of what your extension does and why it's useful.

## Features

<!-- CUSTOMIZE: List key features -->

- Feature 1: Description
- Feature 2: Description
- Feature 3: Description

## Installation

```bash
# Install from catalog
<extension-manager> add my-extension

# Or install from local development directory
<extension-manager> add --dev /path/to/my-extension
```

## Configuration

1. Create configuration file:

   ```bash
   cp .lanyant/extensions/my-extension/config-template.yml \
      .lanyant/extensions/my-extension/my-extension-config.yml
   ```

2. Edit configuration:

   ```bash
   vim .lanyant/extensions/my-extension/my-extension-config.yml
   ```

3. Set required values:
   <!-- CUSTOMIZE: List required configuration -->
   ```yaml
   connection:
     url: "https://api.example.com"
     api_key: "your-api-key"

   project:
     id: "your-project-id"
   ```

## Usage

<!-- CUSTOMIZE: Add usage examples -->

### Command: example

Description of what this command does.

```bash
# In Claude Code
> lanyant.my-extension.example
```

**Prerequisites**:

- Prerequisite 1
- Prerequisite 2

**Output**:

- What this command produces
- Where results are saved

## Configuration Reference

<!-- CUSTOMIZE: Document all configuration options -->

### Connection Settings

| Setting | Type | Required | Description |
|---------|------|----------|-------------|
| `connection.url` | string | Yes | API endpoint URL |
| `connection.api_key` | string | Yes | API authentication key |

### Project Settings

| Setting | Type | Required | Description |
|---------|------|----------|-------------|
| `project.id` | string | Yes | Project identifier |
| `project.workspace` | string | No | Workspace or organization |

## Environment Variables

Override configuration with environment variables:

```bash
# Override connection settings
export LANYANT_MY_EXTENSION_CONNECTION_URL="https://custom-api.com"
export LANYANT_MY_EXTENSION_CONNECTION_API_KEY="custom-key"
```

## Examples

<!-- CUSTOMIZE: Add real-world examples -->

### Example 1: Basic Workflow

```bash
# Step 1: Create specification
> lanyant.spec

# Step 2: Generate tasks
> lanyant.tasks

# Step 3: Use extension
> lanyant.my-extension.example
```

## Troubleshooting

<!-- CUSTOMIZE: Add common issues -->

### Issue: Configuration not found

**Solution**: Create config from template (see Configuration section)

### Issue: Command not available

**Solutions**:

1. Check extension is installed: `<extension-manager> list`
2. Restart AI agent
3. Reinstall extension

## License

MIT License - see LICENSE file

## Support

- **Issues**: <https://github.com/your-org/project-toolkit-my-extension/issues>
- **the project toolkit Docs**: <https://github.com/statsperform/project-toolkit>

## Changelog

See [CHANGELOG.md](CHANGELOG.md) for version history.

---

*Extension Version: 1.0.0*
*the project toolkit: >=0.1.0*
