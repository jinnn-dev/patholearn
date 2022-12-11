#!/bin/bash

while [ $# -gt 0 ]
do
    case $1 in
        -d|--directory)
            DIRECTORY="$2"
            shift
            shift
            ;;
        -i|--image)
            IMAGE="$2"
            shift
            shift
            ;;
        -t|--tag)
            TAG="$2"
            shift
            shift
            ;;
        -m|--mode)
            MODE="$2"
            shift
            shift
            ;;
        -*|--*)
            echo "Unkown option $1"
            exit 1
            ;;
    esac
done

if [ -z "$DIRECTORY" ]
then
    echo "You must give a directory (-d or --directory)"
    exit -1
fi
if [ -z "$IMAGE" ]
then
    echo "You must give an image name (-i or --image)"
    exit -1
fi
if [ -z "$TAG" ]
then
    echo "No tag given. Using default value 'latest'"
    TAG="latest"
fi
# if [ -z "$MODE"]
# then
#     echo "No mode given. Using default value 'prod'"
#     MODE="prod"
# fi
cd $DIRECTORY
dockerfile="${MODE}.dockerfile"
echo $dockerfile
docker buildx build --tag hafen.noxz.dev/patholearn/$IMAGE:$TAG -o type=image --platform=linux/amd64 --push -f $dockerfile .

echo 'Build and publish of docker image'