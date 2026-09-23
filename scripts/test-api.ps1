param(
    [string]$BaseUrl = "http://localhost:8000"
)

$health = Invoke-RestMethod "$BaseUrl/health"
$body = @{
    study_hours = 7
    attendance = 85
    assignments_completed = 8
} | ConvertTo-Json
$prediction = Invoke-RestMethod `
    -Method Post `
    -Uri "$BaseUrl/predict" `
    -ContentType "application/json" `
    -Body $body

[pscustomobject]@{
    Health = $health.status
    Version = $health.model_version
    Prediction = $prediction.prediction
    Probability = $prediction.probability
} | Format-List

