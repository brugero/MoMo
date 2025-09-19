-- database/database_setup.sql
-- MoMo Transaction Analyzer Database Schema - Users & Transactions Module
-- Team: Data Pioneers
-- Implemented by: Selena ISIMBI

SET foreign_key_checks = 1;
SET sql_mode = 'STRICT_TRANS_TABLES,ERROR_FOR_DIVISION_BY_ZERO,NO_AUTO_CREATE_USER,NO_ENGINE_SUBSTITUTION';

-- Drop tables if they exist for clean setup
DROP TABLE IF EXISTS transactions;
DROP TABLE IF EXISTS user;

-- Temporary table for categories - will be replaced by Beulla's implementation
CREATE TABLE IF NOT EXISTS transaction_categories (
    categoryId INT AUTO_INCREMENT PRIMARY KEY,
    TransactionType VARCHAR(50) NOT NULL,
    paymentType VARCHAR(50) NOT NULL
) ENGINE=InnoDB;

-- Users table implementation by Selena ISIMBI
CREATE TABLE IF NOT EXISTS user (
    UserId INT AUTO_INCREMENT PRIMARY KEY,
    FullNames VARCHAR(250) NOT NULL,
    PhoneNumber VARCHAR(15) NOT NULL,
    DateCreated TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE KEY uk_user_phone (PhoneNumber),
    CONSTRAINT chk_phone_not_empty CHECK (PhoneNumber != ''),
    CONSTRAINT chk_names_not_empty CHECK (FullNames != '')
) ENGINE=InnoDB;

-- Transactions table implementation by Selena ISIMBI
CREATE TABLE IF NOT EXISTS transactions (
    TransactionId INT AUTO_INCREMENT PRIMARY KEY,
    Fee DECIMAL(15,2) NOT NULL DEFAULT 0.00,
    Amount DECIMAL(15,2) NOT NULL,
    balance DECIMAL(15,2) NOT NULL,
    initialBalance DECIMAL(15,2) NOT NULL,
    senderUserId INT NOT NULL,
    receiverUserId INT NOT NULL,
    transactionDate DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    categoryId INT NOT NULL,
    TransactionReference VARCHAR(50),
    FOREIGN KEY (senderUserId) REFERENCES user(UserId) ON DELETE RESTRICT ON UPDATE CASCADE,
    FOREIGN KEY (receiverUserId) REFERENCES user(UserId) ON DELETE RESTRICT ON UPDATE CASCADE,
    FOREIGN KEY (categoryId) REFERENCES transaction_categories(categoryId) ON DELETE RESTRICT ON UPDATE CASCADE,
    CONSTRAINT chk_sender_receiver_diff CHECK (senderUserId != receiverUserId),
    CONSTRAINT chk_amount_positive CHECK (Amount > 0),
    CONSTRAINT chk_fee_non_negative CHECK (Fee >= 0),
    CONSTRAINT chk_balance_non_negative CHECK (balance >= 0),
    CONSTRAINT chk_initial_balance_non_negative CHECK (initialBalance >= 0),
    UNIQUE KEY uk_transaction_ref (TransactionReference)
) ENGINE=InnoDB;

-- Performance indexes created by Selena ISIMBI
CREATE INDEX idx_transactions_sender ON transactions (senderUserId);
CREATE INDEX idx_transactions_receiver ON transactions (receiverUserId);
CREATE INDEX idx_transactions_category ON transactions (categoryId);
CREATE INDEX idx_transactions_date ON transactions (transactionDate);
CREATE INDEX idx_transactions_sender_date ON transactions (senderUserId, transactionDate);
CREATE INDEX idx_transactions_receiver_date ON transactions (receiverUserId, transactionDate);
CREATE INDEX idx_transactions_amount_date ON transactions (Amount, transactionDate);
CREATE INDEX idx_user_phone ON user (PhoneNumber);
CREATE INDEX idx_user_names ON user (FullNames);

-- Sample categories data - temporary implementation
INSERT INTO transaction_categories (TransactionType, paymentType) VALUES
('Transfer', 'Personal'),
('Transfer', 'Business'),
('Deposit', 'Cash'),
('Withdrawal', 'Cash'),
('Payment', 'Airtime'),
('Payment', 'Shopping');

-- Sample users data inserted by Selena ISIMBI
INSERT INTO user (FullNames, PhoneNumber) VALUES
('Alice Kagwa', '256712345678'),
('Bob Ssebatta', '256772345678'),
('SuperMart Ltd', '256782345678'),
('Airtime Provider', '256752345678'),
('David Okello', '256762345678'),
('Grace Nakato', '256792345678'),
('Tech Solutions Ltd', '256702345678');

-- Sample transactions data with balanced calculations
INSERT INTO transactions (Fee, Amount, balance, initialBalance, senderUserId, receiverUserId, transactionDate, categoryId, TransactionReference) VALUES
(500.00, 50000.00, 449500.00, 500000.00, 1, 2, '2023-10-25 14:30:00', 1, 'REF001'),
(0.00, 25000.00, 474500.00, 449500.00, 3, 1, '2023-10-25 16:45:00', 2, 'REF002'),
(1000.00, 100000.00, 373500.00, 474500.00, 1, 4, '2023-10-26 09:15:00', 5, 'REF003'),
(500.00, 75000.00, 298000.00, 373500.00, 1, 3, '2023-10-26 12:30:00', 6, 'REF004'),
(0.00, 50000.00, 348000.00, 298000.00, 5, 1, '2023-10-27 11:20:00', 1, 'REF005'),
(300.00, 50000.00, 149700.00, 200000.00, 2, 6, '2023-10-27 14:15:00', 1, 'REF006');

-- Testing queries to verify implementation works correctly
SELECT 'Users and Transactions tables created successfully' as Status;

SELECT COUNT(*) as users_count FROM user;
SELECT COUNT(*) as transactions_count FROM transactions;

-- Verify whether relationships and constraints are working
SELECT 
    t.TransactionId,
    t.Amount,
    t.Fee,
    sender.FullNames as SenderName,
    receiver.FullNames as ReceiverName,
    t.transactionDate
FROM transactions t
JOIN user sender ON t.senderUserId = sender.UserId
JOIN user receiver ON t.receiverUserId = receiver.UserId  
ORDER BY t.transactionDate DESC;

-- Check foreign key setup
SELECT 
    'Foreign Key Constraints:' as Info,
    TABLE_NAME,
    COLUMN_NAME,
    CONSTRAINT_NAME,
    REFERENCED_TABLE_NAME,
    REFERENCED_COLUMN_NAME
FROM information_schema.KEY_COLUMN_USAGE 
WHERE REFERENCED_TABLE_SCHEMA = DATABASE() 
AND TABLE_NAME IN ('user', 'transactions')
AND REFERENCED_TABLE_NAME IS NOT NULL;
