# Project Description

The MoMo Transaction Analyzer is an enterprise-level fullstack application designed to process Mobile Money (MoMo) SMS data in XML format. The system cleans and categorizes transaction data, stores it in a relational database, and provides a frontend interface for analysis and visualization.


# Team Information:
Team Name: Data Raiders

Team members:
 ## Week 1 Roles
- Albert NIYONSENGA- Github Repository Master & Initial Scaffolder 
- Sonia UMUBYEYI BAYINGANA - System Architect
- Beulla RUGERO - Scrum Master
- Selena ISIMBI- Documentation Lead 
- Ulrich RUKAZAMBUGA - Documentation

  ## Week 2 Roles
- Beulla RUGERO – ERD Design & Documentation  
- Albert NIYONSENGA – SQL Schema Design & Testing  
- Selena ISIMBI – SQL Schema Design & Testing  
- Sonia UMUBYEYI BAYINGANA – JSON & Data Modeling  
- Ulrich RUKAZAMBUGA – JSON & Data Modeling 

# Key features:

XML data parsing and extraction

Data cleaning and normalization

Transaction categorization

SQLite database storage

Dashboard with data visualization

RESTful API (bonus feature)

# Project Links 
Architecture Diagram: View System Architecture 
![System Architecture](docs/architecture.png)

Scrum Board: View Project Progress
You can track our tasks here: [MoMo Scrum Board](https://github.com/users/brugero/projects/2/views/1)


# Project Structure

```
├── README.md # Project overview and setup instructions
├── .env.example # Environment variables template
├── requirements.txt # Python dependencies
├── index.html # Main dashboard page
├── web/ # Frontend assets (styles, chart handling, etc.)
├── data/ # Raw XML + processed data
├── logs/ # ETL and error logs
├── etl/ # Parsing, cleaning, and loading scripts
├── api/ # API layer & schema definitions
├── tests/ # Unit tests for parsing, cleaning, categorization
└── docs/ # Documentation (ERD, design docs, etc.)
```
## 🛠 Week 2 Deliverables: Database & JSON Foundation  

### Database Design  
- Added entities: **Users**, **Transactions**, **Transaction Categories**, **System Logs**, and a junction table for many-to-many relationships.  
- ERD exported and available in `/docs/erd_diagram.png`.  
- Database schema implemented in MySQL with proper data types, constraints, indexes & sample data.  

### JSON & Data Modeling  
- Schemas defined for main entities: `User`, `Transaction_Category`, `Transaction`, `System_Log`.  
- Nested structures to represent relationships: transactions include sender & receiver info; categories map via junction table; logs associated per transaction.  
- Example objects created including a full complex transaction with system logs (saved in `/examples/json_schemas.json`).  


## Getting Started
### Prerequisites  
- MySQL 8+ (or compatible relational DB)  
- Git  

### Database Setup  
1. Clone this repo  
2. Navigate to `/database`  
3. Run `database_setup.sql` in your MySQL instance
  
   ```sh
   mysql -u <username> -p < database_setup.sql
Confirm sample data has been inserted

### Running the server 
1. Run `uvicorn app:app --reload` to expose the endpoints
NB: Make sure all dependencies are installed. Run `pip install fastapi uvicorn pymysql` to install them   
## JSON Examples
Refer to `/examples/json_schemas.json` for JSON schema definitions, examples, and a full transaction object showing nested user / category / log info.

## AI Usage Policy
✅ Permitted: grammar, syntax checking; SQL best-practice research

❌ Not permitted: generating ERD designs, major logic/biz rules, reflection required content

AI usage is logged in /docs/ai_usage_log.md

Scrum Board & Project Management
Weekly sprints with assigned roles and tasks

Week 2 tasks include: ERD finalization, SQL schema implementation, JSON modeling, and documentation updates

Contributions are visible via GitHub commits per member

## License
This project is under the MIT License — see the [LICENSE](./LICENSE) file for details.
