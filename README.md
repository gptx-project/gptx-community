# Bettercorp Contributor Portal

The Bettercorp Contributor Portal is a central hub for project collaborators, enabling developers, designers, and stakeholders to coordinate, contribute, and track progress efficiently.

## Features

- User authentication and profile management
- Project and task management with Taiga integration
- Contribution tracking and verification
- Blockchain-based tokenization of contributions
- Soul-bound tokens for badges and achievements
- Gamification elements for community engagement

## Technology Stack

- **Frontend**: React.js with Redux Toolkit, Material-UI/Chakra UI
- **Backend**: FastAPI with Python, PostgreSQL with SQLAlchemy
- **Blockchain**: Ethereum/Polygon with Solidity for Soul-Bound Tokens
- **DevOps**: Docker, Docker Compose

## Getting Started

### Prerequisites

- Docker and Docker Compose
- Python 3.12+ (for local development)
- Node.js 16+ (for frontend development)
- PostgreSQL (for local development without Docker)
- Redis (for local development without Docker)

### Setup with Docker

1. Clone the repository:
   ```bash
   git clone https://github.com/your-organization/bettercorp-contributor-portal.git
   cd bettercorp-contributor-portal
   ```

2. Create environment files:
   ```bash
   cp server/.env.example server/.env
   ```

3. Start the services with Docker Compose:
   ```bash
   docker-compose up -d
   ```

4. Access the API at http://localhost:8000 and the API documentation at http://localhost:8000/api/docs

### Local Development Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/your-organization/bettercorp-contributor-portal.git
   cd bettercorp-contributor-portal
   ```

2. Set up the backend:
   ```bash
   cd server
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   cp .env.example .env  # Edit the .env file with your configuration
   ```

3. Run the backend:
   ```bash
   cd server
   python run.py
   ```

4. Access the API at http://localhost:8000 and the API documentation at http://localhost:8000/api/docs

## API Testing

You can test the API using the provided test script:

```bash
cd server
python test_api.py
```

## Project Structure

```
/
├── client/                 # Frontend application (to be implemented)
│   ├── public/             # Static assets
│   ├── src/                # Source code
│   └── tests/              # Frontend tests
│
├── server/                 # Backend application
│   ├── src/                # Source code
│   │   ├── api/            # API routes and controllers
│   │   ├── blockchain/     # Blockchain integration
│   │   ├── config/         # Configuration
│   │   ├── db/             # Database models and migrations
│   │   ├── services/       # Business logic
│   │   ├── taiga/          # Taiga API integration
│   │   └── utils/          # Utility functions
│   └── tests/              # Backend tests
│
├── contracts/              # Smart contracts for blockchain
│   ├── src/                # Contract source code
│   └── tests/              # Contract tests
│
└── docs/                   # Documentation
    ├── api/                # API documentation
    ├── architecture/       # Architecture documentation
    └── user/               # User documentation
```

## Contributing

Please read [CONTRIBUTING.md](CONTRIBUTING.md) for details on our code of conduct and the process for submitting pull requests.

## License

This project is licensed under the [LICENSE](LICENSE) - see the LICENSE file for details.
