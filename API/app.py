import json
import http.server
import socketserver
import base64
import getpass
from urllib.parse import urlparse, parse_qs
from datetime import datetime

# JSON file storage
TRANSACTIONS_FILE = "transactions.json"
LOGS_FILE = "logs.json"
API_KEY_FILE = ".api_key"
RATE_LIMIT = 1000  # requests per minute (By defaults to 1000 requests/minute)

# Global variables
stored_api_key = None  # Store the Base64 encoded version
request_counts = {}

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

def setup_api_key():
    """Get plain API key from user, encode it, and store the Base64 version"""
    global stored_api_key
    
    try:
        # Try to load existing API key (Base64 encoded)
        with open(API_KEY_FILE, 'r') as f:
            stored_api_key = f.read().strip()
        print("Loaded existing API key")
        return
    except FileNotFoundError:
        pass
    
    # Get new API key from user
    print("\nAPI Security Setup")
    print("Enter your secret API key\n")
    
    while True:
        user_key = getpass.getpass("Your API key: ").strip()
        if user_key:
            # Encode to Base64 and store the encoded version
            stored_api_key = base64.b64encode(user_key.encode()).decode()
            
            # Save the Base64 encoded version for future runs
            with open(API_KEY_FILE, 'w') as f:
                f.write(stored_api_key)
            
            print("API key saved successfully!")
            break
        else:
            print("API key cannot be empty. Try again.")

class Security:
    @staticmethod
    def authenticate(incoming_key_plain):
        """Encode the incoming plain key and compare with stored Base64 version"""
        global stored_api_key
        try:
            # Encode the incoming plain key to Base64
            incoming_encoded = base64.b64encode(incoming_key_plain.encode()).decode()
            
            # Compare with our stored Base64 key
            return stored_api_key == incoming_encoded
        except:
            return False
    
    @staticmethod
    def rate_limit(client_ip):
        """Simple IP-based rate limiting"""
        current_minute = datetime.now().minute
        
        if client_ip not in request_counts:
            request_counts[client_ip] = {"minute": current_minute, "count": 1}
            return True
        
        if request_counts[client_ip]["minute"] != current_minute:
            request_counts[client_ip] = {"minute": current_minute, "count": 1}
            return True
        
        request_counts[client_ip]["count"] += 1
        return request_counts[client_ip]["count"] <= RATE_LIMIT

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
    
    def _security_check(self):
        """Security gateway for all requests"""
        api_key_plain = self.headers.get('X-API-Key')  # User sends plain text
        client_ip = self.client_address[0]
        
        # Authentication - user sends plain text, we encode and compare with stored Base64
        if not api_key_plain or not Security.authenticate(api_key_plain):
            self._send_error(401, "Invalid API key")
            return False
        
        # Rate limiting
        if not Security.rate_limit(client_ip):
            self._send_error(429, "Rate limit exceeded")
            return False
        
        return True
    
    def _set_headers(self, status_code=200):
        self.send_response(status_code)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type, X-API-Key')
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
    
    # Transactions endpoints - ORIGINAL LOGIC PRESERVED
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
                required_fields = ['type', 'amount', 'sender', 'receiver', 'timestamp']
                for field in required_fields:
                    if field not in transaction_data:
                        self._send_error(400, f"Missing required field: {field}")
                        return
                
                transactions = JSONHandler.read_json(TRANSACTIONS_FILE)
                new_transaction = {
                        'id': JSONHandler.get_next_id(transactions),
                        'type': transaction_data['type'],
                        'amount': transaction_data['amount'],
                        'sender': transaction_data['sender'],
                        'receiver': transaction_data['receiver'],
                        'timestamp': transaction_data['timestamp']
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
                        'id': transaction_id,
                        'type': transaction_data['type'],
                        'amount': transaction_data['amount'],
                        'sender': transaction_data['sender'],
                        'receiver': transaction_data['receiver'],
                        'timestamp': transaction_data['timestamp']
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
            
            # Security check for all requests
            if not self._security_check():
                return
            
            endpoint = path_parts[0]
            
            if endpoint == 'transactions':
                self.handle_transactions(path_parts, method)
            else:
                self._send_error(404, "Endpoint not found")
        except Exception as e:
            self._send_error(500, f"Internal server error: {str(e)}")

def run_server(port=8000):
    # Setup API key first
    setup_api_key()
    
    # Decode to show user what their plain text key is
    plain_key = base64.b64decode(stored_api_key).decode()
    
    with socketserver.TCPServer(("", port), APIHandler) as httpd:
        print(f"\nServer running on port {port}")
        print(f"Rate limit: {RATE_LIMIT} requests/minute per IP")
        print(f"Security: API Key authentication enabled")
        print(f"Available endpoints:")
        print(f"  GET    /transactions")
        print(f"  GET    /transactions/{{id}}")
        print(f"  POST   /transactions")
        print(f"  PUT    /transactions/{{id}}")
        print(f"  DELETE /transactions/{{id}}")
        print(f"\nRequired header for all requests:")
        print(f"\nYour plain text API key: {plain_key}")
        print(f"\nExample curl command:")
        print(f'curl -H "X-API-Key: {plain_key}" http://localhost:{port}/transactions')
        httpd.serve_forever()

if __name__ == "__main__":
    run_server()