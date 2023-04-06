from flask import Flask, jsonify, request, render_template
from web3 import Web3
import json

# สร้าง Flask App
app = Flask(__name__)

# เชื่อมต่อ Ethereum blockchain ด้วย Web3
w3 = Web3(Web3.HTTPProvider('https:127.0.0.1:8545'))

# อ่าน Smart Contract ABI จากไฟล์ JSON
with open('VotingSystem.json', 'r') as f:
    voting_system_abi = json.load(f)['abi']

# สร้าง Contract Object จาก ABI และ Contract Address
contract_address = '0x892ABA6a2DC41745b85c4AefE1Ca05602286973b'
voting_system_contract = w3.eth.contract(address=contract_address, abi=voting_system_abi)

# สร้างฟังก์ชันสำหรับเรียกใช้ Smart Contract Method ต่าง ๆ
def call_contract_method(method_name, args):
    # สร้าง Transaction Object จาก Method Signature และ Arguments
    method_signature = voting_system_contract.encodeABI(fn_name=method_name, args=args)
    tx = {
        'to': contract_address,
        'data': method_signature,
        'gas': w3.eth.estimateGas({'to': contract_address, 'data': method_signature})
    }
    # ส่ง Transaction ไปยัง Ethereum blockchain
    tx_hash = w3.eth.sendTransaction(tx)
    # รอการ Confirm Transaction จนกว่าจะเสร็จสมบูรณ์
    tx_receipt = w3.eth.waitForTransactionReceipt(tx_hash)
    # คืนค่าผลลัพธ์จาก Smart Contract Method
    return tx_receipt['output']


#สร้าง API Endpoint สำหรับหน้า INDEX
@app.route("/")
def index():
    return render_template('index.html')

# สร้าง API Endpoint สำหรับเพิ่มผู้สมัครเลือกตั้งใหม่
@app.route('/candidates', methods=['POST'])
def add_candidate():
    candidate_name = request.json['name']
    tx_result = call_contract_method('addCandidate', [candidate_name])
    return jsonify({'tx_result': tx_result}), 200

# สร้าง API Endpoint สำหรับลงคะแนนเสียง
@app.route('/votes', methods=['POST'])
def vote():
    voter_address = request.json['address']
    candidate_id = request.json['candidate_id']
    tx_result = call_contract_method('vote', [candidate_id], {'from': voter_address})
    return jsonify({'tx_result': tx_result}), 200

# สร้าง API Endpoint สำหรับแสดงรายชื่อผู้สมัครเลือกตั้ง
@app.route('/candidates', methods=['GET'])
def get_candidates():
    candidates = call_contract_method('getCandidates', [])
    return jsonify({'candidates': candidates}), 200

if __name__ == 'main':
    app.run(debug=True)