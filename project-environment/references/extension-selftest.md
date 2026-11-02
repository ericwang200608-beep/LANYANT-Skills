# Extension Self-Test: `<user request>`

This command drives a self-test simulating the developer experience with the `<user request>` extension.

## Goal

Validate the end-to-end lifecycle (discovery, installation, registration) for the extension: `<user request>`.
If `<user request>` is empty, you must tell the user to provide an extension name, for example: `lanyant.selftest.extension linear`.

## Steps

### Step 1: Catalog Discovery Validation

Check if the extension exists in the the configured extension catalog.
Execute this command and verify that it completes successfully and that the returned extension ID exactly matches `<user request>`. If the command fails or the ID does not match `<user request>`, fail the test.

```bash
<extension-manager> info "<user request>"
```

### Step 2: Simulate Installation

First, try to add the extension to the current workspace configuration directly. If the catalog provides the extension as `install_allowed: false` (discovery-only), this step is *expected* to fail.

```bash
<extension-manager> add "<user request>"
```

Then, simulate adding the extension by installing it from its catalog download URL, which should bypass the restriction.
Obtain the extension's `download_url` from the catalog metadata (for example, via a catalog info command or UI), then run:

```bash
<extension-manager> add "<user request>" --from "<download_url>"
```

### Step 3: Registration Verification

Once the `add` command completes, verify the installation by checking the project configuration.
Use terminal tools (like `cat`) to verify that the following file contains a record for `<user request>`.

```bash
cat .lanyant/extensions/.registry/<user request>.json
```

### Step 4: Verification Report

Analyze the standard output of the three steps.
Generate a terminal-style test output format detailing the results of discovery, installation, and registration. Return this directly to the user.

Example output format:
```text
============================= test session starts ==============================
collected 3 items

test_selftest_discovery.py::test_catalog_search [PASS/FAIL]
  Details: [Provide execution result of <extension-manager> search]

test_selftest_installation.py::test_extension_add [PASS/FAIL]
  Details: [Provide execution result of <extension-manager> add]

test_selftest_registration.py::test_config_verification [PASS/FAIL]
  Details: [Provide execution result of registry record verification]

============================== [X] passed in ... ==============================
```


## Runtime and authorization binding

Before running, bind `<extension-manager>` to a real installed catalog/package manager and inspect its supported flags. The placeholders are adapter slots, not installed LANYANT commands. If discovery, install-from-URL, or registry inspection has no real equivalent, mark that exact step environment-blocked and leave the overall lifecycle test unverified. Never print PASS from prose or a mock installation. Use an isolated disposable project and a trusted archive. A discovery-only catalog entry is expected to reject ordinary installation; install-from-URL tests an explicitly authorized source, not a way to evade a security policy. Publishing or external messages remain separately authorized. Record command output, exact requested/returned ID, installed version/digest, registry path and elapsed time, including every expected and unexpected failure. Do not remove the test installation or repository without applicable cleanup authorization.
