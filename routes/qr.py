from flask import request, send_from_directory
from flask_restx import Resource, Namespace
import qrcode
import os
from models import db, QRimage, Receipt

QR = Namespace('QR')

IMAGE_DIR = os.path.abspath('./static/images')

@QR.route('')
@QR.route('/')
class ReceiptQR(Resource):
    def post(self):
        # 프론트에 호출하는 url넣기 
        receipt_id = request.json.get('receipt_id')
        receipt = Receipt.query.filter_by(id=receipt_id).first()
        if receipt:
            qr = QRimage.query.filter_by(receipt=receipt_id).first()
            if qr:
                return {"error":"이미 해당하는 영수증에 대한 QR이 있음"}, 400
            url = f'https://www.google.com/?receiptId={receipt_id}'
            qr_url = qrcode.make(url)
            file_name = f"receipt-{receipt_id}-qr.png"
            qr_path = os.path.join(IMAGE_DIR, file_name)
            qr_url.save(qr_path)
            qr_obj = QRimage(receipt=receipt.id, QRpath=file_name)
            db.session.add(qr_obj)
            db.session.commit()
            if qr_obj.id:
                return {"result":file_name}, 200
            else:
                return {"error":"DB에 저장되지 않음"}, 500
        else:
            return {"error":"영수증 데이터가 없음"}, 400


@QR.route('/<path:path>')
class QRImage(Resource):
    def get(self, path):
        # 조회 시 사용자 번호 저장 추가해야 됨
        return send_from_directory(IMAGE_DIR,path)
