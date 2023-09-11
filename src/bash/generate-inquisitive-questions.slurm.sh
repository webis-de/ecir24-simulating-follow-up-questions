#!/bin/bash -e

#SBATCH --job-name="generate-inquisitive-questions"
#SBATCH --output="/mnt/ceph/storage/data-tmp/current/kipu5728/log-%x-%j.txt"
#SBATCH --gres=gpu:ampere

CONTAINER_NAME="generate-inquisitive-questions"
IMAGE_SQSH="${CONTAINER_NAME}.sqsh"
IMAGE="docker://registry.webis.de#code-lib/public-images/simulation-by-question-under-discussion:latest"

echo "Check container"

mapfile -t AVAILABLE_CONTAINER < <( enroot list )

if [[ ! " ${AVAILABLE_CONTAINER[*]} " =~ ${CONTAINER_NAME} ]]; then
  if [ ! -f "$IMAGE_SQSH" ]; then
    echo "Can't find image \"${IMAGE_SQSH}\"..."
    enroot import -o ${IMAGE_SQSH} "${IMAGE}"
  fi

  echo "Create container \"${CONTAINER_NAME}\"..."
  enroot create --name ${CONTAINER_NAME} ${IMAGE_SQSH}
fi

enroot start -w -r ${CONTAINER_NAME}

