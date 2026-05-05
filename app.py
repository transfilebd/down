from flask import Flask, request, jsonify
from flask_cors import CORS
import yt_dlp
import os

app = Flask(__name__)
CORS(app)

@app.route('/')
def home():
    return "CSM Downloader API is Live and Secure!"

@app.route('/api/getlink', methods=['POST'])
def get_link():
    data = request.json or {}
    url = data.get('url')
    
    if not url:
        return jsonify({'error': 'URL is required'}), 400

    try:
        # ইউটিউবের বট চেকিং এড়াতে প্লেয়ার ক্লায়েন্ট কনফিগারেশন
        ydl_opts = {
            'extractor_args': {
                'youtube': {
                    'player_client': ['web', 'android']
                }
            },
            'noplaylist': True
        }
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            
            # সরাসরি ডাউনলোড লিংক বের করা
            direct_url = info.get('url') or (info.get('formats', [])[-1]['url'] if info.get('formats') else '')
            
            return jsonify({
                'success': True,
                'title': info.get('title', 'Unknown Title'),
                'direct_url': direct_url,
                'uploader': info.get('uploader', 'Unknown'),
                'duration': info.get('duration', 0)
            })
            
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

if __name__ == '__main__':
    app.run(port=int(os.environ.get('PORT', 5000)))
