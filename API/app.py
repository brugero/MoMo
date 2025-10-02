import json
import http.server
import socketserver
from urllib.parse import urlparse, parse_qs
from datetime import datetime

# JSON file storage
TRANSACTIONS_FILE = "transactions.json"
LOGS_FILE = "logs.json"

# Initialize JSON files if they don't exist
def init_json_files():
    for file in [TRANSACTIONS_FILE, LOGS_FILE]:
        try:
            with open(file, 'r') as f:
                json.load(f)
        except FileNotFoundError:
            with open(file, 'w') as f:
                json.dump([], f)

init_json_files()

class JSONHandler:
    @staticmethod
    def read_json(file_path):
        with open(file_path, 'r') as f:
            return json.load(f)

    @staticmethod
    def write_json(file_path, data):
        with open(file_path, 'w') as f:
            json.dump(data, f, indent=2)

    @staticmethod
    def find_by_id(data_list, item_id):
        return next((item for item in data_list if item.get('TransactionId') == item_id), None)

    @staticmethod
    def get_next_id(data_list):
        if not data_list:
            return 1
        return max(item.get('TransactionId', 0) for item in data_list) + 1

class APIHandler(http.server.BaseHTTPRequestHandler):
    
    def _set_headers(self, status_code=200):
        self.send_response(status_code)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
    
    def do_OPTIONS(self):
        self._set_headers(200)
    
    def _parse_path(self):
        parsed_path = urlparse(self.path)
        path_parts = parsed_path.path.strip('/').split('/')
        query_params = parse_qs(parsed_path.query)
        return path_parts, query_params
    
    def _read_body(self):
        content_length = int(self.headers.get('Content-Length', 0))
        return self.rfile.read(content_length).decode('utf-8')
    
    def _send_error(self, status_code, message):
        self._set_headers(status_code)
        response = {'detail': message}
        self.wfile.write(json.dumps(response).encode('utf-8'))
    
    def _send_json(self, data, status_code=200):
        self._set_headers(status_code)
        self.wfile.write(json.dumps(data).encode('utf-8'))
    
    # Transactions endpoints
    def handle_transactions(self, path_parts, method):
        if method == 'GET':
            if len(path_parts) > 1:
                # GET /transactions/{transaction_id}
                try:
                    transaction_id = int(path_parts[1])
                    transactions = JSONHandler.read_json(TRANSACTIONS_FILE)
                    transaction = JSONHandler.find_by_id(transactions, transaction_id)
                    if transaction:
                        self._send_json(transaction)
                    else:
                        self._send_error(404, "Transaction not found")
                except ValueError:
                    self._send_error(400, "Invalid transaction ID")
            else:
                # GET /transactions
                transactions = JSONHandler.read_json(TRANSACTIONS_FILE)
                self._send_json(transactions)
        
        elif method == 'POST':
            # POST /transactions
            try:
                body = self._read_body()
                transaction_data = json.loads(body)
                
                # Validate required fields
                required_fields = ['Fee', 'Amount', 'balance', 'initialBalance', 'senderUserId', 
                                 'receiverUserId', 'transactionDate', 'categoryId', 'TransactionReference']
                for field in required_fields:
                    if field not in transaction_data:
                        self._send_error(400, f"Missing required field: {field}")
                        return
                
                transactions = JSONHandler.read_json(TRANSACTIONS_FILE)
                new_transaction = {
                    'TransactionId': JSONHandler.get_next_id(transactions),
                    'Fee': transaction_data['Fee'],
                    'Amount': transaction_data['Amount'],
                    'balance': transaction_data['balance'],
                    'initialBalance': transaction_data['initialBalance'],
                    'senderUserId': transaction_data['senderUserId'],
                    'receiverUserId': transaction_data['receiverUserId'],
                    'transactionDate': transaction_data['transactionDate'],
                    'categoryId': transaction_data['categoryId'],
                    'TransactionReference': transaction_data['TransactionReference']
                }
                
                transactions.append(new_transaction)
                JSONHandler.write_json(TRANSACTIONS_FILE, transactions)
                
                # Create system log
                logs = JSONHandler.read_json(LOGS_FILE)
                new_log = {
                    'logId': f"LOG-{new_transaction['TransactionId']:03d}",
                    'status': "TRANSACTION_CREATED",
                    'transactionId': new_transaction['TransactionId'],
                    'timestamp': datetime.now().isoformat()
                }
                logs.append(new_log)
                JSONHandler.write_json(LOGS_FILE, logs)
                
                self._send_json(new_transaction, 201)
            except json.JSONDecodeError:
                self._send_error(400, "Invalid JSON")
        
        elif method == 'PUT':
            # PUT /transactions/{transaction_id}
            if len(path_parts) > 1:
                try:
                    transaction_id = int(path_parts[1])
                    body = self._read_body()
                    transaction_data = json.loads(body)
                    
                    transactions = JSONHandler.read_json(TRANSACTIONS_FILE)
                    transaction_index = next((i for i, t in enumerate(transactions) if t.get('TransactionId') == transaction_id), None)
                    
                    if transaction_index is None:
                        self._send_error(404, "Transaction not found")
                        return
                    
                    # Update transaction
                    updated_transaction = {
                        'TransactionId': transaction_id,
                        'Fee': transaction_data['Fee'],
                        'Amount': transaction_data['Amount'],
                        'balance': transaction_data['balance'],
                        'initialBalance': transaction_data['initialBalance'],
                        'senderUserId': transaction_data['senderUserId'],
                        'receiverUserId': transaction_data['receiverUserId'],
                        'transactionDate': transaction_data['transactionDate'],
                        'categoryId': transaction_data['categoryId'],
                        'TransactionReference': transaction_data['TransactionReference']
                    }
                    
                    transactions[transaction_index] = updated_transaction
                    JSONHandler.write_json(TRANSACTIONS_FILE, transactions)
                    self._send_json(updated_transaction)
                except (ValueError, json.JSONDecodeError):
                    self._send_error(400, "Invalid data")
        
        elif method == 'DELETE':
            # DELETE /transactions/{transaction_id}
            if len(path_parts) > 1:
                try:
                    transaction_id = int(path_parts[1])
                    transactions = JSONHandler.read_json(TRANSACTIONS_FILE)
                    transaction_index = next((i for i, t in enumerate(transactions) if t.get('TransactionId') == transaction_id), None)
                    
                    if transaction_index is None:
                        self._send_error(404, "Transaction not found")
                        return
                    
                    del transactions[transaction_index]
                    JSONHandler.write_json(TRANSACTIONS_FILE, transactions)
                    self._send_json({'detail': 'Transaction deleted successfully'})
                except ValueError:
                    self._send_error(400, "Invalid transaction ID")
    
    def do_GET(self):
        path_parts, query_params = self._parse_path()
        self._route_request(path_parts, 'GET')
    
    def do_POST(self):
        path_parts, query_params = self._parse_path()
        self._route_request(path_parts, 'POST')
    
    def do_PUT(self):
        path_parts, query_params = self._parse_path()
        self._route_request(path_parts, 'PUT')
    
    def do_DELETE(self):
        path_parts, query_params = self._parse_path()
        self._route_request(path_parts, 'DELETE')
    
    def _route_request(self, path_parts, method):
        try:
            if not path_parts:
                self._send_error(404, "Endpoint not found")
                return
            
            endpoint = path_parts[0]
            
            if endpoint == 'transactions':
                self.handle_transactions(path_parts, method)
            else:
                self._send_error(404, "Endpoint not found")
        except Exception as e:
            self._send_error(500, f"Internal server error: {str(e)}")

def run_server(port=8000):
    with socketserver.TCPServer(("", port), APIHandler) as httpd:
        print(f"Server running on port {port}")
        print(f"Available endpoints:")
        print(f"  GET    /transactions")
        print(f"  GET    /transactions/{{id}}")
        print(f"  POST   /transactions")
        print(f"  PUT    /transactions/{{id}}")
        print(f"  DELETE /transactions/{{id}}")
        httpd.serve_forever()

if __name__ == "__main__":
    run_server()