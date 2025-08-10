#!/usr/bin/env bash
set -euo pipefail
DEPLOY="$1"
NAMESPACE="${2:-default}"
echo "Waiting for rollout: $DEPLOY ($NAMESPACE)"
kubectl -n "$NAMESPACE" rollout status deploy/"$DEPLOY" --timeout=180s
