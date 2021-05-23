# Julia Fernanda Ramirez Oviedo
# Silvestre Martinez Cervantes

# Informe de ejecución
$path = Get-Location
$reporte = $path.Path+"\Servicios.txt"
$reporte_2 = $path.Path+"\Procesos.txt"

# Obtener la lista de servicios
$servicios = Get-Service


# Recorrer cada elemento de la lista de servicios
try{
    Start-Transcript -Path $reporte
    Write-Host "===ESTATUS DE SERVICIOS===="
    foreach ($elemento in $servicios){
    #verificar si esta en ejecucion o no
    if ($elemento.Status -eq "Running"){
        Write-Host $elemento.Name "is" $elemento.Status -ForegroundColor Green
    } elseif ($elemento.Status -ne "Running"){
        Write-Host $elemento.Name "is" $elemento.Status -ForegroundColor Red
    }
    }
    Stop-Transcript
    Write-Host "`n===INFORMACION DE PROCESOS==="
    Start-Transcript -Path $reporte_2 
    Get-Process
    Stop-Transcript
}catch{
    $_.Exception.Message
}