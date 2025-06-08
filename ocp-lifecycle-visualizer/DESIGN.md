# OpenShift Lifecycle Visualizer Design

## Purpose
Create a tool to visualize and track the lifecycle of OpenShift clusters, focusing on:
- Version progression and update paths
- Support status and EOL dates

## Core Features

### 1. Lifecycle Tracking
- Current version and status
- Available update paths
- EOL dates and support windows
- Platform compatibility matrix
- Upgrade recommendations

### 2. Data Sync/Import
- Import additional records since the previous run
- Database connection pooling for efficient queries
- OAuth2 authentication for secure access

### 3. Visualization
- Timeline views of version progression
- Support status indicators
- Platform compatibility matrix
- Risk level indicators
- Upgrade path diagrams

## Technical Design

### Input Data
- SupportSense cluster exports
- Version compatibility matrix
- Platform support information
- Known issues database

### Database Connection
1. **Authentication**
   - OAuth2 authentication with Trino
   - Username provided via CLI or interactive prompt
   - Secure connection handling

2. **Connection Management**
   - Connection pooling for efficient resource usage
   - Automatic connection health checks
   - Proper resource cleanup
   - Thread-safe session handling

3. **Error Handling**
   - Connection retry logic
   - Session rollback on errors
   - Comprehensive error logging

### Processing
1. **Data Collection**
   - Get cluster information from SQL queries
   - Validate version data
   - Check platform compatibility
   - Assess support status

2. **Analysis**
   - Determine available update paths
   - Calculate risk levels
   - Identify potential issues
   - Generate recommendations

3. **Visualization**
   - Generate timeline views
   - Create status reports
   - Produce compatibility matrices
   - Build upgrade path diagrams

### Output Formats
1. **TBD**

## Development Roadmap

### Phase 1: Foundation
- [x] Project structure
- [x] Basic module setup
- [x] Core data structures
- [x] Input parsing
- [x] Source Database connectivity
- [x] Target Database connectivity
- [x] OAuth2 authentication
- [x] Connection pooling

### Phase 2: Analysis Engine
- [ ] Version compatibility checking
- [ ] Platform support validation
- [ ] Risk assessment logic
- [ ] Upgrade path calculation

### Phase 3: Visualization
- [ ] Timeline generation
- [ ] Status indicators
- [ ] Compatibility matrices
- [ ] Upgrade path diagrams

### Phase 4: Enhancement
- [ ] Interactive features
- [ ] Advanced visualizations
- [ ] Export capabilities
- [ ] Performance optimization

## Future Considerations
1. Integration with other Red Hat tools
2. Custom visualization templates

## Program Flow

1. **CLI Entry Point**
   - Parse command line arguments
   - Set up logging
   - Get EBS account number
   - Get database username
   - Initialize database connection
   - Call appropriate functions

2. **Function Organization**
   - Core functions are stored in `modules/functions.py`
   - Database management in `modules/database.py`
   - Configuration in `modules/config.py`
   - Main script (`ocp-lifecycle-visualizer.py`) remains clean and focused
   - Each function has a single responsibility
   - Functions are well-documented and reusable

3. **Data Flow**
   - Input validation
   - Database connection and authentication
   - Data processing
   - Output generation

## CLI Design

### Command Structure

- Uses Click's command groups for better organization
- Global options:
  - `--debug`: Enable debug logging
  - `--ebs-account`: EBS Account number
  - `--username`: Database username for OAuth2 authentication

### Inputs
- `ebs-account`: (Optional) pass in the EBS Account number
- `username`: (Optional) pass in the database username

## Logging Design

### Log Levels
- ERROR: Critical issues that prevent program execution
- INFO: Important program flow and status updates
- DEBUG: Detailed information for troubleshooting

### Log Categories
1. **Database Operations**
   - Connection status
   - Query execution
   - Data retrieval results
   - Sync operations
   - Authentication status

2. **Data Processing**
   - Input validation
   - Data transformation
   - Record processing
   - Aggregation results

3. **CLI Operations**
   - Command execution
   - Parameter validation
   - User input handling

### Log Format
```
%(asctime)s - %(levelname)s - [%(category)s] - %(message)s
```

### Log Output
- Console output for INFO and ERROR
- Debug logs to file when --debug flag is used
- Log rotation for debug files
