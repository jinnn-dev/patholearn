production_file=docker-compose.prod.yml
echo "Building initial slide_api image"
docker-compose -f $production_file build slide_api
echo "Starting production environment"
docker-compose -f $production_file up
