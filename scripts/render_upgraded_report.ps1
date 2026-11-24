$reportFile=(Resolve-Path -LiteralPath 'report\bao_cao_robot_cap_nhat.docx').Path
$wordRevision=New-Object -ComObject Word.Application
$wordRevision.Visible=$false
$wordRevision.DisplayAlerts=0
try {
 $reportDocument=$wordRevision.Documents.Open($reportFile,$false,$false)
 $reportDocument.Repaginate()
 $reportDocument.Fields.Update() | Out-Null
 foreach($toc in $reportDocument.TablesOfContents){$toc.Update()}
 $reportDocument.Repaginate()
 foreach($toc in $reportDocument.TablesOfContents){$toc.UpdatePageNumbers()}
 $reportDocument.Save()
 $reportDocument.ExportAsFixedFormat([IO.Path]::ChangeExtension($reportFile,'.pdf'),17)
 $reportDocument.Close(0)
} finally {
 $wordRevision.Quit()
 [Runtime.InteropServices.Marshal]::ReleaseComObject($wordRevision) | Out-Null
}
Write-Output 'Updated equations, fields and PDF.'
