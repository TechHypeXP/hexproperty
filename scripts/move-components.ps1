$sourceDir = "src"
$targetDir = "src/interface/web/components"

# Create arrays of file moves
$moves = @(
    @{
        Source = "$sourceDir/components/molecules/Cards/CardStats.tsx"
        Target = "$targetDir/molecules/cards/CardStats.tsx"
    },
    @{
        Source = "$sourceDir/components/molecules/Cards/CardTable.tsx"
        Target = "$targetDir/molecules/cards/CardTable.tsx"
    },
    @{
        Source = "$sourceDir/components/molecules/Cards/CardBarChart.tsx"
        Target = "$targetDir/molecules/cards/CardBarChart.tsx"
    },
    @{
        Source = "$sourceDir/components/molecules/Cards/CardSocialTraffic.tsx"
        Target = "$targetDir/molecules/cards/CardSocialTraffic.tsx"
    },
    @{
        Source = "$sourceDir/components/molecules/Dropdowns/UserDropdown.tsx"
        Target = "$targetDir/molecules/dropdowns/UserDropdown.tsx"
    },
    @{
        Source = "$sourceDir/components/organisms/Navbars/AdminNavbar.tsx"
        Target = "$targetDir/organisms/navbars/AdminNavbar.tsx"
    },
    @{
        Source = "$sourceDir/components/organisms/Headers/HeaderStats.tsx"
        Target = "$targetDir/organisms/headers/HeaderStats.tsx"
    }
)

# Function to ensure target directory exists
function EnsureDirectory {
    param($path)
    if (-not (Test-Path $path)) {
        New-Item -ItemType Directory -Force -Path $path | Out-Null
    }
}

# Move each file
foreach ($move in $moves) {
    if (Test-Path $move.Source) {
        $targetDir = Split-Path -Parent $move.Target
        EnsureDirectory $targetDir
        Move-Item -Path $move.Source -Destination $move.Target -Force
        Write-Host "Moved $($move.Source) to $($move.Target)"
    } else {
        Write-Host "Source file not found: $($move.Source)"
    }
}

# Clean up empty directories
Get-ChildItem -Path $sourceDir/components -Recurse -Directory | 
    Where-Object { (Get-ChildItem -Path $_.FullName -Recurse -File).Count -eq 0 } |
    Remove-Item -Recurse -Force
