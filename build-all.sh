#!/bin/bash

while [ $# -gt 0 ]
do
    case $1 in
        -t|--tag)
            TAG="$2"
            shift
            shift
            ;;
        -*|--*)
            echo "Unkown option $1"
            exit 1
            ;;
    esac
done

if [ -z "$TAG" ]
then
    echo "No tag given. Using default value 'latest'"
    TAG="latest"
fi

folders=("ai-api" "ai-worker" "auth" "frontend" "learn-api" "slide-api")

length=${#folders[@]}
i=0
while [ $i -lt $length ]
do
    echo "${folders[$i]}"
    current=${folders[$i]}
    cd ./${current}
    docker buildx build --tag hafen.noxz.dev/patholearn-ai/$current:$TAG -o type=image --platform=linux/amd64 --push -f prod.dockerfile .
    cd ../
    ((i++))
done

# cd $DIRECTORY
# dockerfile="${MODE}.dockerfile"
# echo $dockerfile
# docker buildx build --tag hafen.noxz.dev/patholearn-ai/$IMAGE:$TAG -o type=image --platform=linux/amd64 --push -f $dockerfile .

# echo 'Build and publish of docker image'

# docker buildx build --tag hafen.noxz.dev/patholearn-ai/$IMAGE:$TAG -o type=image --platform=linux/amd64 --push -f $dockerfile .
