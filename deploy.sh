#!/bin/bash

# CyberTrap-AI Deployment Script

set -e

echo "Starting CyberTrap-AI deployment..."

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo -e "${RED}Docker is not installed${NC}"
    exit 1
fi

echo -e "${GREEN}✓ Docker is installed${NC}"

# Check if Docker Compose is installed
if ! command -v docker-compose &> /dev/null; then
    echo -e "${RED}Docker Compose is not installed${NC}"
    exit 1
fi

echo -e "${GREEN}✓ Docker Compose is installed${NC}"

# Create .env file if it doesn't exist
if [ ! -f .env ]; then
    echo -e "${YELLOW}Creating .env file from .env.example${NC}"
    cp .env.example .env
    echo -e "${YELLOW}Please update .env with your configuration${NC}"
fi

echo -e "${YELLOW}Starting services...${NC}"

# Start services
docker-compose up -d

echo -e "${YELLOW}Waiting for services to start...${NC}"
sleep 10

echo -e "${YELLOW}Initializing database...${NC}"

# Initialize database
docker-compose exec -T web flask init-db

echo -e "${YELLOW}Seeding database...${NC}"

# Seed database
docker-compose exec -T web flask seed-db

echo -e "${GREEN}✓ Deployment completed!${NC}"
echo ""
echo "Services:"
echo "  Web UI:     http://localhost"
echo "  API:        http://localhost/api/v1"
echo "  Database:   localhost:5432"
echo "  Redis:      localhost:6379"
echo ""
echo "Default credentials:"
echo "  Username: admin"
echo "  Password: Admin@123456"
