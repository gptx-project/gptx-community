# Bettercorp Contributor Portal - Common Tasks

This document outlines common repetitive tasks that follow established patterns in the project. Each task includes the files that need to be modified, step-by-step instructions, and important considerations.

## Add New Badge Type

**Files to modify:**
- `/client/src/components/badges/BadgeTypes.js` - Add badge definition
- `/client/src/components/badges/BadgeIcon.jsx` - Add icon mapping
- `/server/app/services/gamification/badge_definitions.py` - Add server-side definition
- `/contracts/src/BadgeNFT.sol` - Add badge metadata if using blockchain

**Steps:**
1. Define the new badge type with properties (name, description, criteria, icon)
2. Add the badge icon component or import the asset
3. Implement the badge awarding logic in the gamification service
4. Update the smart contract if the badge is represented as an NFT
5. Add tests for the badge awarding conditions

**Important notes:**
- Ensure badge criteria are measurable and can be tracked automatically
- Consider retroactive awarding for existing users who meet criteria
- Update documentation for users explaining how to earn the badge

## Integrate New Taiga API Endpoint

**Files to modify:**
- `/server/app/taiga/taiga_client.py` - Add new API method
- `/server/app/services/project_sync/sync_service.py` - Use the new endpoint
- `/server/app/api/controllers/project_controller.py` - Expose data if needed
- `/client/src/services/api/projectApi.js` - Add client method if needed

**Steps:**
1. Add the new API endpoint method to the Taiga client
2. Implement data transformation to match internal models
3. Update the sync service to use the new data
4. Add API endpoint to expose the data if needed
5. Update client-side API service if the data needs to be displayed
6. Add tests for the new functionality

**Important notes:**
- Check Taiga API documentation for rate limits and pagination
- Handle authentication and error cases properly
- Consider caching strategies for frequently accessed data

## Add New Smart Contract Feature

**Files to modify:**
- `/contracts/src/[ContractName].sol` - Add new soul-bound contract or modify existing
- `/server/app/blockchain/contracts/[contract_name].py` - Add Python class for contract interface
- `/server/app/services/blockchain/[feature_name]_service.py` - Implement service
- `/client/src/services/blockchain/[featureName]Service.js` - Add client integration

**Steps:**
1. Implement and test the smart contract feature
2. Generate Python classes for the contract ABI
3. Implement server-side service to interact with the contract
4. Add API endpoints to expose the functionality
5. Implement client-side service to use the API
6. Add UI components to interact with the feature
7. Write tests for all layers

**Important notes:**
- Always test on testnet before deploying to mainnet
- Consider gas costs and optimization
- Implement proper error handling for failed transactions
- Ensure soul-bound tokens are properly non-transferable
- Consider users without blockchain wallets (fallback mechanisms)
- Implement verification mechanisms for soul-bound credentials

## Add New Gamification Element

**Files to modify:**
- `/server/app/services/gamification/elements/[element_name].py` - Add element logic
- `/server/app/db/models/[element_name].py` - Add database model
- `/client/src/components/gamification/[ElementName].jsx` - Add UI component
- `/client/src/pages/Dashboard.jsx` - Integrate the element

**Steps:**
1. Define the gamification element (points, levels, challenges, etc.)
2. Implement the database model and migrations
3. Create the server-side logic for tracking and awarding
4. Add API endpoints to expose the data
5. Implement UI components to display the element
6. Integrate the components into relevant pages
7. Add animations or effects for user engagement
8. Write tests for all functionality

**Important notes:**
- Focus on user motivation and engagement
- Ensure the element aligns with project goals
- Consider balance to prevent gaming the system
- Get user feedback before full implementation

## Deploy New Version

**Files to modify:**
- `/version.txt` - Update version number
- `/CHANGELOG.md` - Document changes
- `/docker-compose.yml` - Update image versions if needed
- CI/CD configuration files

**Steps:**
1. Ensure all tests pass in the CI pipeline
2. Update version numbers in relevant files
3. Create a new release tag in git
4. Update the changelog with new features and fixes
5. Deploy to staging environment first
6. Run smoke tests on staging
7. Deploy to production using blue/green deployment
8. Monitor logs and metrics after deployment

**Important notes:**
- Schedule deployments during low-traffic periods
- Have a rollback plan ready
- Update documentation for any API or UI changes
- Notify users of significant changes