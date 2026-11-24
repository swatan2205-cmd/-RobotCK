param([string]$ReportPath = 'report\bao_cao_robot.docx')
$resolvedReport = (Resolve-Path -LiteralPath $ReportPath).Path
$pdfPath = [IO.Path]::ChangeExtension($resolvedReport, '.pdf')
$wordApp = New-Object -ComObject Word.Application
$wordApp.Visible = $false
$wordApp.DisplayAlerts = 0
try {
    $document = $wordApp.Documents.Open($resolvedReport, $false, $false)
    $document.Fields.Update() | Out-Null
    $document.Save()
    $document.ExportAsFixedFormat($pdfPath, 17)
    $document.Close(0)
} finally {
    $wordApp.Quit()
    [Runtime.InteropServices.Marshal]::ReleaseComObject($wordApp) | Out-Null
}
Write-Output $pdfPath
