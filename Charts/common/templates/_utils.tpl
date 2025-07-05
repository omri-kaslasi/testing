{{/* vim: set filetype=mustache: */}}

{{/*
Merge one or more YAML templates and output the result.
This takes an list of values:
- the top context
- [optional] zero or more template args
- [optional] the template name of the overrides (destination)
- the template name of the base (source)
*/}}
{{- define "common.utils.merge" -}}
{{- $top := first . }}
{{- $tplName := last . }}
{{- $args := initial . }}
{{- if typeIs "string" (last $args) }}
  {{- $overridesName := last $args }}
  {{- $args = initial $args }}
  {{- $tpl := fromYaml (include $tplName $args) | default (dict) }}
  {{- $overrides := fromYaml (include $overridesName $args) | default (dict) }}
  {{- toYaml (merge $overrides $tpl) }}
{{- else }}
  {{- include $tplName $args }}
{{- end }}
{{- end }}

{{/*
A utility for converting data to YAML format, supporting both direct conversion of non-string types using toYaml
and template-based conversion for strings using tpl.
It takes two parameters:
- $input: The data to be converted to YAML format. This can be either a string or any other data type.
- $tplContext: The template context, which is a set of values and functions available for use within the template.

The function is useful when dealing with multiline values that require template rendering.
If the type of $input is a string, the function uses the Helm tpl function to apply the template defined by the string
to the given context ($tplContext). This allows for dynamic templating within string values.
If the type of $input is not a string, it uses the toYaml function to convert the data to YAML format.
*/}}
{{- define "common.utils.tplYaml" -}}
{{- $input := index . 0 }}
{{- $tplContext := index . 1 }}
{{- if typeIs "string" $input }}
{{- tpl $input $tplContext }}
{{- else }}
{{- toYaml $input }}
{{- end }}
{{- end }}

{{- define "common.name" -}}
{{- default .Chart.Name .Values.nameOverride | trunc 63 | trimSuffix "-" }}
{{- end }}

{{- define "common.labels" -}}
{{- $top := first . -}}
{{- $isWorkloadResource := index . 1 | default false -}}
{{- $object := last . -}}
region: {{ required ".Values.global.region is required!" $top.Values.global.region }}
env: {{ required ".Values.global.env is required!" $top.Values.global.env }}
role: {{ $top.Chart.Name }}
tenant: {{ required ".Values.global.tenant is required!" $top.Values.global.tenant }}
{{ include "common.selectorLabels" (list $top $object)}}
{{- end }}

{{/*
Selector labels
*/}}
{{- define "common.selectorLabels" -}}
{{- $top := first . -}}
{{- $object := last . -}}
app.kubernetes.io/name: {{ include "common.name" $top }}
{{- with $object.selectorLabels }}
{{ toYaml . }}
{{- end }}
{{- end }}

{{- define "common.objectName" }}
{{- $top := first . -}}
{{- $object := last . -}}
{{- if hasKey $object "name" }}
    {{- tpl $object.name $top }}
{{- else }}
    {{- include "common.name" $top }}
    {{- end }}
{{- end }}

{{/*
For more information about Kubernetes Workload Resources check: https://kubernetes.io/docs/reference/kubernetes-api/workload-resources/
*/}}
{{- define "common.metadata.tpl" -}}
{{- $top := first . -}}
{{- $isWorkloadResource := index . 1 | default false -}}
{{- $object := last . -}}
name: {{ $object.name }}
labels:
  {{- include "common.labels" (list $top $isWorkloadResource $object) | nindent 2 }}
{{- end }}

{{/*
Create a standard metadata header
*/}}
{{- define "common.metadata" -}}
{{- include "common.utils.merge" (append . "common.metadata.tpl") }}
{{- end }}
