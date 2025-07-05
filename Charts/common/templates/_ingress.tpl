{{/* ALB condition values hard limit is 5.
The first is taken by the "path" and the other four are used by the source IPs */}}
{{- define "condition-limit" -}}
{{- int 4 -}}
{{- end -}}

{{/* Returns the number of ALB rules that will be created ("source-ips-rule-count" * number of servie ports) */}}
{{- define "rule-count" }}
{{- $sourceIpsCount := index . 0 -}}
{{- $servicePortsCount := index . 1 -}}
{{- $sourceIpsRulesCount := include "source-ips-rule-count" $sourceIpsCount | int }}
{{- int (mul $servicePortsCount $sourceIpsRulesCount) -}}
{{- end -}}

{{/* Returns the number of ALB rules thaat are required for each service port */}}
{{- define "source-ips-rule-count" -}}
{{- $length := . -}}
{{- $coditionValues := include "condition-limit" . | int -}}
{{- $count := div $length $coditionValues -}}
{{- if gt (mod $length $coditionValues) 0 -}}
{{- $count = add1 $count -}}
{{- end -}}
{{- int $count -}}
{{- end -}}

{{/*
The function uses a nested loop to generate ALB ingress annotations for each combination of source IP and service port.
It iterates over each service port and creates rules for the source IP addresses.
For each combination, it generates ALB annotations for actions and conditions.
 */}}
{{- define "common.source-ips-annotations" -}}
{{- $sourceIps := index . 0 }}
{{- $service := index . 1 }}
{{- $serviceName := $service.name -}}
{{- $servicePorts := $service.ports -}}
{{- $servicePortsCount := len $servicePorts | int }}
{{- $coditionValues := include "condition-limit" . | int -}}
{{- $totalRulesCount := include "rule-count" (list (len $sourceIps) $servicePortsCount) | int -}}

{{- range $i := untilStep 0 $totalRulesCount $servicePortsCount -}}
{{/* mustSlice extracts a subset of elements from $sourceIps based on the specified starting and ending indices. */}}
{{- $s := mustSlice $sourceIps (mul $i $coditionValues) (min (add $coditionValues (mul $i $coditionValues)) (len $sourceIps)) -}}
{{- range $j, $svcPort := $servicePorts }}
alb.ingress.kubernetes.io/actions.rule-ip{{add $i $j}}: '{"type":"forward","forwardConfig":{"targetGroups":[{"serviceName": "{{ $serviceName }}" ,"servicePort":"{{ $svcPort.port }}","weight":20}],"targetGroupStickinessConfig":{"enabled":false}}}'
alb.ingress.kubernetes.io/conditions.rule-ip{{add $i $j}}: '[{"field":"source-ip","sourceIpConfig":{"values": {{ toJson $s }} }}]'
{{- end -}}
{{- end -}}
{{- end -}}

{{- define "common.redirect-rules-annotations" -}}
{{- $redirectRule := . }}
{{- $redirectHost := $redirectRule.host }}
{{- $destinationPath := $redirectRule.destinationPath }}
{{- $redirectPort := $redirectRule.port | default "443" }}
{{- $redirectProtocol := $redirectRule.protocol | default "HTTPS" }}
{{- $redirectQuery := $redirectRule.query | default "#{query}" }}
{{- $redirectStatusCode := $redirectRule.statusCode | default "HTTP_301" }}
alb.ingress.kubernetes.io/actions.redirect-rule: '{"type":"redirect","redirectConfig":{"host":"{{- $redirectHost }}","path":"{{- $destinationPath }}","port":"{{- $redirectPort }}","protocol":"{{- $redirectProtocol }}","query":"{{- $redirectQuery }}","statusCode":"{{- $redirectStatusCode }}"}}'
{{- end -}}