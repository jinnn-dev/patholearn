dev_file=docker-compose.dev.yml
echo "Building initial slide_api image"
docker-compose -f $dev_file build slide_api
echo "Starting development environment"
docker-compose -f $dev_file up --build
