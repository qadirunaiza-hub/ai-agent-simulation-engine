#!/usr/bin/env bash
# Deploy mirofish-qa — SSHes into 172.25.2.181, pulls branch image, restarts container.
# Usage: ./deploy-qa.sh [branch]   (default: current git branch)

set -euo pipefail

IMAGE_BASE="registry.ird.mu-sigma.com/devops/devops-2026/mirofish/mirofish-offline-musigma"
CONTAINER="mirofish-qa"
NETWORK="mirofish-offline_default"
ENV_FILE="/home/dolores/mirofish-offline/.env"
PORT_FRONT="3011"
PORT_BACK="5004"
DEPLOY_HOST="172.25.2.181"
DEPLOY_USER="dolores"
DEPLOY_PASSWORD="Infr@3214."

BRANCH="${1:-$(git -C "$(dirname "$0")" rev-parse --abbrev-ref HEAD)}"
BRANCH_SLUG=$(echo "$BRANCH" | tr '/' '-' | tr '[:upper:]' '[:lower:]' | sed 's/[^a-z0-9-]/-/g')
IMAGE_TAG="${IMAGE_BASE}:${BRANCH_SLUG}"

echo "Branch  : $BRANCH"
echo "Image   : $IMAGE_TAG"
echo "Target  : ${DEPLOY_USER}@${DEPLOY_HOST}:${PORT_FRONT} (front) / ${PORT_BACK} (back)"
echo ""

export SSHPASS="${DEPLOY_PASSWORD}"
sshpass -e ssh -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null \
  "${DEPLOY_USER}@${DEPLOY_HOST}" bash -s << ENDSSH
  docker pull ${IMAGE_TAG}
  docker stop ${CONTAINER} 2>/dev/null || true
  docker rm   ${CONTAINER} 2>/dev/null || true
  docker run -d \
    --name ${CONTAINER} \
    --network ${NETWORK} \
    --env-file ${ENV_FILE} \
    -e NEO4J_URI=bolt://mirofish-neo4j:7687 \
    -p ${PORT_FRONT}:3000 \
    -p ${PORT_BACK}:5010 \
    --restart unless-stopped \
    ${IMAGE_TAG}
  echo "mirofish-qa live at http://${DEPLOY_HOST}:${PORT_FRONT}"
ENDSSH
