#!/bin/bash
set -e
echo "Starting  production deployment..."

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color
print_status() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

if ! command -v docker &> /dev/null; then
    print_error "Docker is not installed. Please install Docker first."
    exit 1
fi

if ! command -v docker-compose &> /dev/null; then
    print_error "Docker Compose is not installed. Please install Docker Compose first."
    exit 1
fi
if [[ $EUID -eq 0 ]]; then
    print_warning "Running as root. This is okay but consider using a dedicated user."
fi
print_status "Stopping existing containers..."
docker-compose -f docker-compose.prod.yml down --remove-orphans || true
print_status "Cleaning up old Docker images..."
docker system prune -f
print_status "Building and starting services..."
docker-compose -f docker-compose.prod.yml up --build -d
print_status "Waiting for services to be ready..."
sleep 10

print_status "Checking service health..."
if docker-compose -f docker-compose.prod.yml ps | grep -q "Up"; then
    print_status "Services are running successfully!"

    echo ""
    print_status "   Your application should be available at:"
    print_status "   Frontend: https://ayushjayaswal.xyz/tangerines/"
    print_status "   API: https://ayushjayaswal.xyz/api/"
    echo ""

    print_status "  Service Status:"
    docker-compose -f docker-compose.prod.yml ps

    echo ""
    print_status "  To view logs:"
    print_status "   docker-compose -f docker-compose.prod.yml logs -f"

    echo ""
    print_status "  To stop services:"
    print_status "   docker-compose -f docker-compose.prod.yml down"

else
    print_error "  Some services failed to start. Check the logs:"
    docker-compose -f docker-compose.prod.yml logs
    exit 1
fi
