# Extension Template

Starter template for creating a the project toolkit extension.

## Quick Start

1. **Copy this template**:

   ```bash
   cp -r extensions/template my-extension
   cd my-extension
   ```

2. **Customize `extension.yml`**:
   - Change extension ID, name, description
   - Update author and repository
   - Define your commands

3. **Create commands**:
   - Add command files in `commands/` directory
   - Use Markdown format with YAML frontmatter

4. **Create config template**:
   - Define configuration options
   - Document all settings

5. **Write documentation**:
   - Update README.md with usage instructions
   - Add examples

6. **Test locally**:

   ```bash
   cd /path/to/project-toolkit-project
   <extension-manager> add --dev /path/to/my-extension
   ```

7. **Publish** (optional):
   - Create GitHub repository
   - Create release
   - Submit to catalog (see the [Extension Publishing Guide](../../references/extension-authoring.md))

## Files in This Template

- `extension.yml` - Extension manifest (CUSTOMIZE THIS)
- `config-template.yml` - Configuration template (CUSTOMIZE THIS)
- `commands/example.md` - Example command (REPLACE THIS)
- `README.md` - Extension documentation (REPLACE THIS)
- `LICENSE` - MIT License (REVIEW THIS)
- `CHANGELOG.md` - Version history (UPDATE THIS)
- `.gitignore` - Git ignore rules

## Customization Checklist

- [ ] Update `extension.yml` with your extension details
- [ ] Change extension ID to your extension name
- [ ] Update author information
- [ ] Define your commands
- [ ] Create command files in `commands/`
- [ ] Update config template
- [ ] Write README with usage instructions
- [ ] Add examples
- [ ] Update LICENSE if needed
- [ ] Test extension locally
- [ ] Create git repository
- [ ] Create first release

## Need Help?

- **Development Guide**: See [Extension Development Guide](../../references/extension-authoring.md)
- **API Reference**: See the [Extension API Reference](../../references/extension-authoring.md)
- **Publishing Guide**: See the [Extension Publishing Guide](../../references/extension-authoring.md)
- **User Guide**: See the [Extension User Guide](../../references/extension-authoring.md)

## Template Version

- Version: 1.0.0
- Last Updated: 2026-01-28
- Compatible with the project toolkit: >=0.1.0
