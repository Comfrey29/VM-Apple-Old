# Apple VM Launcher 1.1

**Version 1.1** — A graphical launcher for QEMU, designed to run macOS (Snow Leopard, etc.) with persistent configuration.  
Includes: GUI interface, multi-language support (ca, es, en, fr), VM management via `.json`, and direct launch with QEMU.

## Main Features (v1.1)

- Tkinter-based GUI to:
  - Add, edit, delete, and launch virtual machines.
  - View the list of configured VMs.
- Persistent storage in `~/apple_vm_launcher_vms.json`.
- Internationalization with `~/strings.json` (supports Catalan, Spanish, English, French).  
- QEMU boot with:
  - UEFI via OVMF (`OVMF_CODE.fd` / `OVMF_VARS.fd`)
  - Optional OpenCore or installer ISO.
  - SMC key (`isa-applesmc` + OSK).
- Compatible with Python 2.6.1 (built for Snow Leopard) and newer environments.

## Installation

1. Make sure you have `qemu-system-x86_64` installed and accessible in your `PATH`.
2. Create or copy the example configuration files:
   - `~/strings.json` (translations).
   - `~/apple_vm_launcher_vms.json` (VM definitions).

### Example `~/strings.json` (minimum, English)

```json
{
  "en": {
    "title": "Apple VM Launcher 1.1",
    "available_vms": "Available virtual machines:",
    "add": "Add",
    "edit": "Edit",
    "delete": "Delete",
    "launch": "Launch VM",
    "no_selection": "No selection",
    "select_vm": "Please select a virtual machine.",
    "error": "Error",
    "missing_qcow2": "Virtual disk not found: %s",
    "missing_iso": "ISO not found: %s",
    "confirm_delete": "Are you sure you want to delete '%s'?",
    "warning_qemu": "QEMU is not available in PATH: %s"
  }
}
