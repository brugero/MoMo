from fastapi import FastAPI, HTTPException
from db import get_db_connection
from schemas import User, UserCreate, Transaction, TransactionCreate, TransactionCategory, TransactionCategoryCreate, SystemLog, SystemLogCreate

app = FastAPI()

@app.get("/users", response_model=list[User])
def get_users():
    conn = get_db_connection()
    with conn.cursor() as cursor:
        cursor.execute("SELECT UserId, FullNames, PhoneNumber, DateCreated FROM user")
        users = cursor.fetchall()
        for user in users:
            if user["DateCreated"] is not None:
                user["DateCreated"] = user["DateCreated"].isoformat()
    conn.close()
    return users

@app.get("/users/{user_id}", response_model=User)
def get_user_by_id(user_id: int):
    conn = get_db_connection()
    with conn.cursor() as cursor:
        cursor.execute("SELECT UserId, FullNames, PhoneNumber, DateCreated FROM user WHERE UserId = %s", (user_id,))
        user = cursor.fetchone()
        if not user:
            conn.close()
            raise HTTPException(status_code=404, detail="User not found")
        if user["DateCreated"] is not None:
            user["DateCreated"] = user["DateCreated"].isoformat()
    conn.close()
    return user

@app.post("/users", response_model=User)
def create_user(user: UserCreate):
    conn = get_db_connection()
    with conn.cursor() as cursor:
        cursor.execute(
            "INSERT INTO user (FullNames, PhoneNumber) VALUES (%s, %s)",
            (user.FullNames, user.PhoneNumber)
        )
        conn.commit()
        user_id = cursor.lastrowid
        cursor.execute("SELECT UserId, FullNames, PhoneNumber, DateCreated FROM user WHERE UserId = %s", (user_id,))
        result = cursor.fetchone()
        if result and result["DateCreated"] is not None:
            result["DateCreated"] = result["DateCreated"].isoformat()
    conn.close()
    return result

@app.get("/categories", response_model=list[TransactionCategory])
def get_categories():
    conn = get_db_connection()
    with conn.cursor() as cursor:
        cursor.execute("SELECT categoryId, TransactionType, paymentType FROM transaction_categories")
        categories = cursor.fetchall()
    conn.close()
    return categories

@app.post("/categories", response_model=TransactionCategory)
def create_category(category: TransactionCategoryCreate):
    conn = get_db_connection()
    with conn.cursor() as cursor:
        cursor.execute(
            "INSERT INTO transaction_categories (TransactionType, paymentType) VALUES (%s, %s)",
            (category.TransactionType, category.paymentType)
        )
        conn.commit()
        category_id = cursor.lastrowid
        cursor.execute("SELECT categoryId, TransactionType, paymentType FROM transaction_categories WHERE categoryId = %s", (category_id,))
        result = cursor.fetchone()
    conn.close()
    return result

@app.get("/transactions", response_model=list[Transaction])
def get_transactions():
    conn = get_db_connection()
    with conn.cursor() as cursor:
        cursor.execute("""
            SELECT TransactionId, Fee, Amount, balance, initialBalance, senderUserId, receiverUserId, transactionDate, categoryId, TransactionReference
            FROM transactions
        """)
        transactions = cursor.fetchall()
        for t in transactions:
            if t["transactionDate"] is not None:
                t["transactionDate"] = t["transactionDate"].isoformat()
    conn.close()
    return transactions

@app.get("/transactions/{transaction_id}", response_model=Transaction)
def get_transaction_by_id(transaction_id: int):
    conn = get_db_connection()
    with conn.cursor() as cursor:
        cursor.execute("""
            SELECT TransactionId, Fee, Amount, balance, initialBalance, senderUserId, receiverUserId, transactionDate, categoryId, TransactionReference
            FROM transactions WHERE TransactionId = %s
        """, (transaction_id,))
        transaction = cursor.fetchone()
        if not transaction:
            conn.close()
            raise HTTPException(status_code=404, detail="Transaction not found")
        if transaction["transactionDate"] is not None:
            transaction["transactionDate"] = transaction["transactionDate"].isoformat()
    conn.close()
    return transaction

@app.post("/transactions", response_model=Transaction)
def create_transaction(transaction: TransactionCreate):
    conn = get_db_connection()
    with conn.cursor() as cursor:
        cursor.execute(
            "INSERT INTO transactions (Fee, Amount, balance, initialBalance, senderUserId, receiverUserId, transactionDate, categoryId, TransactionReference) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)",
            (
                transaction.Fee,
                transaction.Amount,
                transaction.balance,
                transaction.initialBalance,
                transaction.senderUserId,
                transaction.receiverUserId,
                transaction.transactionDate,
                transaction.categoryId,
                transaction.TransactionReference
            )
        )
        conn.commit()
        transaction_id = cursor.lastrowid

        # Create a system log for transaction creation
        cursor.execute(
            "INSERT INTO SystemLogs (logId, status, transactionId, timestamp) VALUES (%s, %s, %s, NOW())",
            (f"LOG-{transaction_id:03d}", "TRANSACTION_CREATED", transaction_id)
        )
        conn.commit()

        cursor.execute("""
            SELECT TransactionId, Fee, Amount, balance, initialBalance, senderUserId, receiverUserId, transactionDate, categoryId, TransactionReference
            FROM transactions WHERE TransactionId = %s
        """, (transaction_id,))
        result = cursor.fetchone()
        if result and result["transactionDate"] is not None:
            result["transactionDate"] = result["transactionDate"].isoformat()
    conn.close()
    return result

@app.put("/transactions/{transaction_id}", response_model=Transaction)
def update_transaction(transaction_id: int, transaction: TransactionCreate):
    conn = get_db_connection()
    with conn.cursor() as cursor:
        cursor.execute("""
            UPDATE transactions SET
                Fee = %s,
                Amount = %s,
                balance = %s,
                initialBalance = %s,
                senderUserId = %s,
                receiverUserId = %s,
                transactionDate = %s,
                categoryId = %s,
                TransactionReference = %s
            WHERE TransactionId = %s
        """, (
            transaction.Fee,
            transaction.Amount,
            transaction.balance,
            transaction.initialBalance,
            transaction.senderUserId,
            transaction.receiverUserId,
            transaction.transactionDate,
            transaction.categoryId,
            transaction.TransactionReference,
            transaction_id
        ))
        conn.commit()
        cursor.execute("""
            SELECT TransactionId, Fee, Amount, balance, initialBalance, senderUserId, receiverUserId, transactionDate, categoryId, TransactionReference
            FROM transactions WHERE TransactionId = %s
        """, (transaction_id,))
        updated = cursor.fetchone()
        if not updated:
            conn.close()
            raise HTTPException(status_code=404, detail="Transaction not found")
        if updated["transactionDate"] is not None:
            updated["transactionDate"] = updated["transactionDate"].isoformat()
    conn.close()
    return updated

@app.delete("/transactions/{transaction_id}")
def delete_transaction(transaction_id: int):
    conn = get_db_connection()
    with conn.cursor() as cursor:
        cursor.execute("DELETE FROM transactions WHERE TransactionId = %s", (transaction_id,))
        conn.commit()
        if cursor.rowcount == 0:
            conn.close()
            raise HTTPException(status_code=404, detail="Transaction not found")
    conn.close()
    return {"detail": "Transaction deleted successfully"}

@app.get("/logs", response_model=list[SystemLog])
def get_logs():
    conn = get_db_connection()
    with conn.cursor() as cursor:
        cursor.execute("SELECT logId, status, transactionId, timestamp FROM SystemLogs")
        logs = cursor.fetchall()
        for log in logs:
            if log["timestamp"] is not None:
                log["timestamp"] = log["timestamp"].isoformat()
    conn.close()
    return logs