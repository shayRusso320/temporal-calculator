{{/*
Common labels
*/}}
{{- define "calculator.labels" -}}
app.kubernetes.io/managed-by: {{ .Release.Service }}
{{- end }}