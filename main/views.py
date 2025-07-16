# main/views.py (Versi dengan Supabase)
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
import json
import requests
from datetime import datetime
import uuid
from .supabase_client import db

def index(request):
    """View untuk halaman utama"""
    # Ambil data dari Supabase
    pesawat_list = db.get_all_pesawat()
    hotel_list = db.get_all_hotel()
    
    # Fallback ke data dummy jika Supabase tidak tersedia
    if not pesawat_list:
        pesawat_list = [
            {
                'id': 1,
                'nama_penerbangan': 'GA-123',
                'maskapai_penerbangan': 'Garuda Indonesia',
                'waktu_keberangkatan': '2025-07-01T08:00:00',
                'durasi_penerbangan': 120,
                'bandara_berangkat': 'CGK - Soekarno Hatta',
                'bandara_tiba': 'DPS - Ngurah Rai',
                'harga_tiket': 1500000
            },
            {
                'id': 2,
                'nama_penerbangan': 'ID-456',
                'maskapai_penerbangan': 'Batik Air',
                'waktu_keberangkatan': '2025-07-01T10:30:00',
                'durasi_penerbangan': 130,
                'bandara_berangkat': 'CGK - Soekarno Hatta',
                'bandara_tiba': 'DPS - Ngurah Rai',
                'harga_tiket': 1200000
            },
            {
                'id': 3,
                'nama_penerbangan': 'QZ-789',
                'maskapai_penerbangan': 'AirAsia',
                'waktu_keberangkatan': '2025-07-01T14:15:00',
                'durasi_penerbangan': 125,
                'bandara_berangkat': 'CGK - Soekarno Hatta',
                'bandara_tiba': 'DPS - Ngurah Rai',
                'harga_tiket': 950000
            }
        ]
    
    if not hotel_list:
        hotel_list = [
            {
                'id': 1,
                'nama_hotel': 'The Mulia Resort',
                'waktu_tersedia': '2025-07-01',
                'harga_per_malam': 2500000,
                'rating': 95,
                'bintang': 5
            },
            {
                'id': 2,
                'nama_hotel': 'Grand Hyatt Bali',
                'waktu_tersedia': '2025-07-01',
                'harga_per_malam': 1800000,
                'rating': 90,
                'bintang': 5
            },
            {
                'id': 3,
                'nama_hotel': 'Ibis Styles Denpasar',
                'waktu_tersedia': '2025-07-01',
                'harga_per_malam': 600000,
                'rating': 85,
                'bintang': 3
            }
        ]
    
    context = {
        'pesawat_list': json.dumps(pesawat_list),
        'hotel_list': json.dumps(hotel_list)
    }
    return render(request, 'main/index.html', context)

@csrf_exempt
@require_http_methods(["POST"])
def send_chat(request):
    """View untuk mengirim chat ke n8n webhook"""
    try:
        data = json.loads(request.body)
        
        # Validasi data yang diperlukan
        required_fields = ['nama', 'usia', 'nik', 'kewarganegaraan', 'chat', 'id']
        for field in required_fields:
            if not data.get(field):
                return JsonResponse({
                    'error': f'Field {field} harus diisi'
                }, status=400)
        
        chat_id = data['id']
        user_message = data['chat']
        
        # Ambil chat yang ada atau buat baru
        chat_data = db.get_chat_by_id(chat_id)
        if not chat_data:
            # Buat chat baru jika tidak ada
            chat_data = {
                'id': chat_id,
                'title': f"Chat {datetime.now().strftime('%d/%m/%Y %H:%M')}",
                'chat': []
            }
            db.create_chat(chat_data)
        
        # Kirim request ke n8n webhook
        webhook_url = 'https://n8n-elrsppnn.n8x.web.id/webhook-test/29b9ae51-f0e7-4136-aea0-d4da26667194'
        
        payload = {
            'nama': data['nama'],
            'usia': data['usia'],
            'nik': data['nik'],
            'kewarganegaraan': data['kewarganegaraan'],
            'chat': user_message,
            'id': chat_id
        }
        
        response = requests.post(webhook_url, json=payload, timeout=60)
        
        if response.status_code == 200:
            chat_data['chat'].append(f"User: {user_message}")
            try:
                response_json = response.json()
                # Ambil output untuk history, tapi simpan seluruh response_json
                if isinstance(response_json, list) and len(response_json) > 0 and 'output' in response_json[0]:
                    bot_output = response_json[0]['output']
                elif isinstance(response_json, dict) and 'output' in response_json:
                    bot_output = response_json['output']
                else:
                    bot_output = response_json.get('response', 'Terima kasih atas pesan Anda!')
            except Exception as e:
                bot_output = response.text if response.text else 'Terima kasih atas pesan Anda!'
                response_json = {'output': bot_output}
            # Simpan seluruh objek response n8n sebagai JSON string
            chat_data['chat'].append(f"Bot: {json.dumps(response_json)}")
            db.update_chat(chat_id, {'chat': chat_data['chat']})
            return JsonResponse({
                'success': True,
                'response': response_json,  # Kirim seluruh response n8n ke frontend!
                'chat_id': chat_id
            })
        else:
            return JsonResponse({
                'error': 'Gagal mengirim pesan ke server'
            }, status=500)
            
    except requests.exceptions.Timeout:
        return JsonResponse({
            'error': 'Timeout - Server tidak merespons'
        }, status=408)
    except requests.exceptions.RequestException as e:
        return JsonResponse({
            'error': f'Kesalahan koneksi: {str(e)}'
        }, status=500)
    except json.JSONDecodeError:
        return JsonResponse({
            'error': 'Format data tidak valid'
        }, status=400)
    except Exception as e:
        return JsonResponse({
            'error': f'Terjadi kesalahan: {str(e)}'
        }, status=500)

@csrf_exempt
@require_http_methods(["POST"])
def new_chat(request):
    """View untuk membuat chat baru"""
    try:
        chat_id = str(uuid.uuid4())
        chat_data = {
            'id': chat_id,
            'title': f"Chat Baru {datetime.now().strftime('%d/%m/%Y %H:%M')}",
            'chat': []
        }
        
        created_chat = db.create_chat(chat_data)
        
        if created_chat:
            return JsonResponse({
                'success': True,
                'chat_id': chat_id,
                'title': chat_data['title']
            })
        else:
            return JsonResponse({
                'error': 'Gagal membuat chat baru'
            }, status=500)
    except Exception as e:
        return JsonResponse({
            'error': f'Gagal membuat chat baru: {str(e)}'
        }, status=500)

@csrf_exempt
@require_http_methods(["POST"])
def delete_chat(request):
    """View untuk menghapus chat"""
    try:
        data = json.loads(request.body)
        chat_id = data.get('chat_id')
        
        if not chat_id:
            return JsonResponse({
                'error': 'Chat ID diperlukan'
            }, status=400)
        
        success = db.delete_chat(chat_id)
        
        if success:
            return JsonResponse({'success': True})
        else:
            return JsonResponse({
                'error': 'Chat tidak ditemukan atau gagal dihapus'
            }, status=404)
    except Exception as e:
        return JsonResponse({
            'error': f'Gagal menghapus chat: {str(e)}'
        }, status=500)

@require_http_methods(["GET"])
def get_chat_history(request):
    """View untuk mendapatkan daftar chat"""
    try:
        chats = db.get_all_chats()
        
        chat_list = []
        for chat in chats:
            chat_list.append({
                'id': chat['id'],
                'title': chat['title']
            })
        
        return JsonResponse({
            'success': True,
            'chats': chat_list
        })
    except Exception as e:
        return JsonResponse({
            'error': f'Gagal mengambil history chat: {str(e)}'
        }, status=500)

@require_http_methods(["GET"])
def get_chat_detail(request, chat_id):
    """View untuk mendapatkan detail chat"""
    try:
        chat_data = db.get_chat_by_id(chat_id)
        
        if chat_data:
            return JsonResponse({
                'success': True,
                'chat': chat_data
            })
        else:
            return JsonResponse({
                'error': 'Chat tidak ditemukan'
            }, status=404)
    except Exception as e:
        return JsonResponse({
            'error': f'Gagal mengambil detail chat: {str(e)}'
        }, status=500)

@csrf_exempt
@require_http_methods(["POST"])
def rename_chat(request):
    """View untuk mengubah nama chat"""
    try:
        data = json.loads(request.body)
        chat_id = data.get('chat_id')
        new_title = data.get('new_title')
        
        if not chat_id or not new_title:
            return JsonResponse({
                'error': 'Chat ID dan nama baru diperlukan'
            }, status=400)
        
        # Update title chat di Supabase
        updated_chat = db.update_chat(chat_id, {'title': new_title})
        
        if updated_chat:
            return JsonResponse({'success': True})
        else:
            return JsonResponse({
                'error': 'Chat tidak ditemukan atau gagal diupdate'
            }, status=404)
    except Exception as e:
        return JsonResponse({
            'error': f'Gagal mengubah nama chat: {str(e)}'
        }, status=500)

def book_plane(request, plane_id):
    return render(request, 'main/booking_plane.html', {'plane_id': plane_id})

def book_hotel(request, hotel_id):
    return render(request, 'main/booking_hotel.html', {'hotel_id': hotel_id})