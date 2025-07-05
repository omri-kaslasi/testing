{{- define "common.pod.template.tpl" -}}
{{- $top := first . }}
{{- $pod := index . 1 }}
{{- $serviceAccount := index . 2 }}
metadata:
  annotations:
    {{- with $pod.podAnnotations }}
      {{- include "common.utils.tplYaml" (list . $top) | nindent 4 }}
    {{- end }}
  labels:
    {{- include "common.labels" (list $top $pod ) | nindent 4 }}
spec:
  imagePullSecrets:
    - name: "regcred"
  {{- if $serviceAccount.create }}
  serviceAccountName: {{ tpl $serviceAccount.name $top }}
  {{- end }}
  {{- with $pod.securityContext }}
  securityContext:
    {{- toYaml $pod.podSecurityContext | nindent 4 }}
  {{- end }}
  dnsConfig:
    options:
      - name: ndots
        value: "1"
  {{- with $pod.nodeSelector }}
  nodeSelector:
    {{- toYaml . | nindent 4 }}
  {{- end }}
  {{- with $pod.affinity }}
  affinity:
    {{- include "common.utils.tplYaml" (list . $top) | nindent 4 }}
  {{- end }}
  {{- with $pod.priorityClassName }}
  priorityClassName: {{ . }}
  {{- end }}
  {{- with $pod.tolerations }}
  tolerations:
    {{- toYaml . | nindent 4 }}
  {{- end }}
  volumes:
  {{- with $pod.persistentVolume }}
  {{- range .volumes }}
  {{- $volumeName := tpl .name $top }}
  {{- $pvName := tpl $pod.persistentVolume.name $top }}
  - name: {{ required "volume name value is required!" $volumeName }}
    persistentVolumeClaim:
      claimName: {{ required "persistentVolume name value is required!" $pvName }}
  {{- end }}
  {{- end }}
  containers:
  - {{- include "common.container" (list $top $pod) | indent 4 }}
{{- end -}}

{{- define "common.pod.template" -}}
{{- include "common.utils.merge" (append . "common.pod.template.tpl") }}
{{- end }}
