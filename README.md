This is a simple and modular Library Management System built with:
Python
Streamlit (for UI)
Services layer for business logic (Books, Friends, Loaning)
Database layer for schema + storage

## Features
+ Book Management
  - Add new books
  - Edit or delete existing books
  - List all available books
+ Friends Management
  - Add friends who can borrow books
  - Track who is active or blocked
+ Loan System
  - Loan a book to a friend
  - Return a book
  - Track due dates
+ Streamlit UI
  - Clean and interactive frontend
  - Works in any browser
  - Easy to deploy
 ## DB config
  + add .env file in the main directory
  + enter your creditentials :
  +    
        MYSQL_HOST=localhost
        MYSQL_USER=root
        MYSQL_PASSWORD=yourpassword
        MYSQL_DATABASE=your_database
        MYSQL_PORT=yourPort
  + connect to your sql server
  +      
 ## Instalation

 + clone repos: 
   git clone https://github.com/<your-username>/<your-repo>.git
   cd <your-repo>
 + create virtual envirement
   python3 -m venv venv
   source venv/bin/activate   # On Windows: venv\Scripts\activate
 + pip install -r requirements.txt
 
 + Run APP
    - streamlit run Streamlit/app.py

