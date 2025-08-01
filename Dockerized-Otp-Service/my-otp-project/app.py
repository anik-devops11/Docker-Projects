import os
import random
import redis
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS

app = Flask(__name__, static_folder='frontend') # ফ্লাস্ককে বলে দিচ্ছি আমাদের স্ট্যাটিক ফাইলগুলো কোথায় আছে।

CORS(app)

# Redis-এর সাথে সংযোগ স্থাপন। 'redis' হোস্টনেমটি docker-compose.yml ফাইলে সংজ্ঞায়িত করা হয়েছে।
redis_host = os.environ.get('REDIS_HOST', 'redis')
r = redis.Redis(host=redis_host, port=6379, db=0)

# নতুন রুট যা index.html ফাইলটি সার্ভ করবে।
@app.route('/')
def serve_index():
    return send_from_directory(app.static_folder, 'index.html')

# এটি style.css এবং script.js-এর মতো অন্যান্য স্ট্যাটিক ফাইল সার্ভ করবে।
@app.route('/<path:path>')
def serve_static(path):
    return send_from_directory(app.static_folder, path)

@app.route('/generate-otp', methods=['POST'])
def generate_otp():
    """একটি OTP তৈরি করে এবং ৫ মিনিটের মেয়াদের জন্য Redis-এ সংরক্ষণ করে।"""
    data = request.json
    phone_number = data.get('phone_number')
    if not phone_number:
        return jsonify({"error": "Phone number is required"}), 400

    otp = str(random.randint(100000, 999999))
    
    # OTP-কে Redis-এ 300 সেকেন্ডের (5 মিনিট) জন্য সংরক্ষণ করা হলো।
    r.setex(phone_number, 300, otp)
    
    return jsonify({"message": f"OTP sent to {phone_number}", "otp": otp})

@app.route('/verify-otp', methods=['POST'])
def verify_otp():
    """ব্যবহারকারীর OTP-কে Redis-এ সংরক্ষিত OTP-এর সাথে যাচাই করে।"""
    data = request.json
    phone_number = data.get('phone_number')
    otp_from_user = data.get('otp')

    if not phone_number or not otp_from_user:
        return jsonify({"error": "Phone number and OTP are required"}), 400

    stored_otp = r.get(phone_number)
    
    if stored_otp and stored_otp.decode('utf-8') == otp_from_user:
        # OTP সঠিক হলে, পুনরায় ব্যবহার ঠেকাতে Redis থেকে এটি মুছে ফেলা হবে।
        r.delete(phone_number)
        return jsonify({"message": "OTP verification successful"}), 200
    else:
        return jsonify({"error": "Invalid OTP"}), 401

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)