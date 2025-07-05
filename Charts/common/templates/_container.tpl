{{- define "common.container.tpl" -}}
{{- $top := first . }}
{{- $container := index . 1 }}
name: {{ $container.role }} 
{{- with $container.command }}
command:
   {{- toYaml . | nindent 2 }}
{{- end }}
{{- with $container.args }}
args:
   {{- toYaml . | nindent 2 }}
{{- end }}
{{- with $container.securityContext }}
securityContext:
  {{- toYaml $container.securityContext | nindent 2 }}
{{- end }}
image: "{{ $container.image.repository }}:{{ $container.image.version | default "Latest" }}"
imagePullPolicy: {{ $container.image.pullPolicy | default "IfNotPresent" }}
resources:
  {{- toYaml (required "resources value is required!" $container.resources) | nindent 2 }}
{{- with $container.startupProbe }}
startupProbe:
  {{- toYaml . | nindent 2 }}
{{- end }}
{{- with $container.livenessProbe }}
livenessProbe:
  {{- toYaml . | nindent 2 }}
{{- end }}
{{- with $container.readinessProbe }}
readinessProbe:
  {{- toYaml . | nindent 2 }}
{{- end }}
volumeMounts:
{{- range $container.volumeMounts }}
{{- $mountPath := .mountPath }}
{{- $name := .name }}
{{- $readOnly := .readOnly | default false}}
  - name: {{ $name }}
    mountPath: {{ $mountPath }}
    readOnly:  {{ $readOnly }}
{{- end }}
{{- with $container.persistentVolume }}
{{- range $container.persistentVolume.volumes }}
{{- $volumeName := tpl .name $top }}
  {{- range .mounts }}
  - name: {{ (required "volumes[].name value is required!" $volumeName) }}
  {{- with .subPath }}
    subPath: {{ . }}
  {{- end }}
    readOnly: {{ .readOnly | default false}}
    mountPath: {{ .mountPath }}
  {{- end }}
{{- end -}}
{{- end -}}
{{- with $container.environmentVariables }}
env:
{{- range $k, $v := . }}
- name: {{ $k }}
  value: {{ tpl $v $top }}
{{- end -}}
{{- end -}}
{{- end -}}

{{- define "common.container" -}}
{{- include "common.utils.merge" (append . "common.container.tpl") -}}
{{- end -}}