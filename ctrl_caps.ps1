# ctrl_caps.ps1: Ensure Caps Lock and Left Ctrl are swapped on Windows
# Requires: PowerShell 5+, admin rights for registry edits

# Get current keyboard layout
$layout = Get-WinUserLanguageList | Select-Object -First 1
Write-Host "Current keyboard layout: $($layout.InputMethodTip)"

# Registry path for scancode map
$regPath = "HKLM:\SYSTEM\CurrentControlSet\Control\Keyboard Layout"
$scancodeMap = (Get-ItemProperty -Path $regPath -Name 'Scancode Map' -ErrorAction SilentlyContinue)."Scancode Map"

# Scancode map for swapping Caps Lock (0x3A) and Left Ctrl (0x1D)
$swap = ([byte[]](
    0x00,0x00,0x00,0x00, # header
    0x00,0x00,0x00,0x00, # header
    0x03,0x00,0x00,0x00, # 3 entries (including null)
    0x1D,0x00,0x3A,0x00, # CapsLock -> LCtrl
    0x3A,0x00,0x1D,0x00, # LCtrl -> CapsLock
    0x00,0x00,0x00,0x00  # null terminator
))

# Check if swap is already set
if ($scancodeMap -and ($scancodeMap -eq $swap)) {
    Write-Host "Caps Lock and Left Ctrl are already swapped."
} else {
    Write-Host "Applying swap (Caps Lock <-> Left Ctrl)..."
    Set-ItemProperty -Path $regPath -Name 'Scancode Map' -Value $swap
    Write-Host "Swap applied. Please reboot or log off for changes to take effect."
}
