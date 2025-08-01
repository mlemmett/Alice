# Set root directory
$root = "D:\Alice"
New-Item -Path $root -ItemType Directory -Force

# Define folder structure
$folders = @(
    "Alice-neuralnet\memory",
    "Alice-neuralnet\emotion",
    "Alice-neuralnet\identity",
    "Alice-neuralnet\utils",
    "modules\empathy",
    "modules\curiosity",
    "modules\grace",
    "modules\truth",
    "modules\love",
    "interface\voice",
    "interface\text",
    "interface\api",
    "data\embeddings",
    "data\transcripts",
    "data\feedback",
    "income\subscriptions",
    "income\api_tokens",
    "income\sustainability",
    "config\dev",
    "config\prod",
    "config\secrets",
    "tests\core",
    "tests\modules",
    "tests\interface",
    "docs"
)

# Create folders and placeholder README files
foreach ($folder in $folders) {
    $fullPath = Join-Path $root $folder
    New-Item -Path $fullPath -ItemType Directory -Force
    New-Item -Path (Join-Path $fullPath "README.md") -ItemType File -Force
}

# Create VS Code workspace file
$workspace = @{
    folders = $folders | ForEach-Object { @{ path = $_ } }
    settings = @{}
}
$workspaceJson = $workspace | ConvertTo-Json -Depth 3
$workspacePath = Join-Path $root "Alice.code-workspace"
$workspaceJson | Out-File -FilePath $workspacePath -Encoding UTF8

Write-Host "✅ Alice setup complete. Workspace file created at: $workspacePath"

