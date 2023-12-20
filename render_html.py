from flask import Flask, url_for,redirect,render_template, request,session,flash
import mysql.connector
from flask_mysqldb import MySQL
from flask_sqlalchemy import SQLAlchemy
from os import path
from sqlalchemy import desc
from helpers import get_ten_danh_muc
app = Flask(__name__)
app.config["SECRET_KEY"] = "bexuanmailonto"
app.config['SQLALCHEMY_DATABASE_URI'] ='sqlite:///test.db'
# app.config ['MYSQL_HOST'] = 'localhost'
# app.config  ['MYSQL_USER'] = 'root'
# app.config  ['MYSQL_PASSWORD'] = ''
# app.config  ['MYSQL_DB'] = 'webtintuc'
# app.config['SQLALCHEMY_DATABASE_URI'] ='sql'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
# mysql = MySQL(app)

class User(db.Model):
    user_id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(125))
    email = db.Column(db.String(125))
    def __init__(self,name,email):
        self.name = name
        self.email = email

class QuanLyBaiViet(db.Model):
    id_bai = db.Column(db.Integer, primary_key=True, autoincrement=True)
    tieu_de = db.Column(db.String(255), nullable=False)
    noi_dung = db.Column(db.Text, nullable=False)
    hinh_anh = db.Column(db.String(255), nullable=False)
    ngay_tao_BV = db.Column(db.DateTime(), default=db.func.now())
    so_luot_xem = db.Column(db.Integer,default=0)
    trangthai = db.Column(db.Boolean,default=True)
    danhmuc_id = db.Column(db.Integer, db.ForeignKey('danh_muc_bai_viet.id_DM'))

    def __init__(self, tieu_de, noi_dung,hinh_anh, danhmuc_id):
        self.tieu_de = tieu_de
        self.noi_dung = noi_dung
        self.hinh_anh = hinh_anh
        self.danhmuc_id = danhmuc_id
        # 
        # self.ngay_tao_BV = ngay_tao_BV
        # self.so_luot_xem = so_luot_xem
        # self.trangthai = trangthai
class DanhMucBaiViet(db.Model):
    id_DM = db.Column(db.Integer, primary_key=True, autoincrement=True)
    ten_DM = db.Column(db.String(255), nullable=False)
    hinh_anh_DM = db.Column(db.String(255), nullable=False)
    ngay_tao_DM = db.Column(db.DateTime(), default=db.func.now())
    bai_viets = db.relationship('QuanLyBaiViet', backref='danh_muc_bai_viet', lazy=True, primaryjoin="DanhMucBaiViet.id_DM == QuanLyBaiViet.danhmuc_id")

    def __init__(self, ten_DM,hinh_anh_DM):
        self.ten_DM = ten_DM
        self.hinh_anh_DM = hinh_anh_DM

class contact(db.Model):
    id_khach = db.Column(db.Integer, primary_key=True, autoincrement=True)
    ten_khach = db.Column(db.String(255), nullable=False)
    email_khach = db.Column(db.String(255), nullable=False)
    sdt_khach = db.Column(db.String(255), nullable=False)
    noidung = db.Column(db.String(255), nullable=False)

    def __init__(self, ten_khach,email_khach,sdt_khach,noidung):
        self.ten_khach = ten_khach
        self.email_khach = email_khach
        self.sdt_khach = sdt_khach
        self.noidung = noidung


@app.route('/')
def index():
    # return '<h1>Hello World!</h1>'
    danh_muc_bai_viets = DanhMucBaiViet.query.all()    
    danh_sach_bai_viet = QuanLyBaiViet.query.all()
    danh_sach_bai_viet_gioihan = QuanLyBaiViet.query.order_by(QuanLyBaiViet.ngay_tao_BV.desc()).limit(5).all()
    danh_sach_bai_viet_gioihan_4 = QuanLyBaiViet.query.order_by(QuanLyBaiViet.ngay_tao_BV.desc()).limit(4).all()
    danh_sach_bai_viet_gioihan_10 = QuanLyBaiViet.query.order_by(QuanLyBaiViet.ngay_tao_BV.desc()).limit(10).all()
    return render_template('index.html' ,danh_muc_bai_viets=danh_muc_bai_viets,danh_sach_bai_viet = danh_sach_bai_viet,gioihan = danh_sach_bai_viet_gioihan,
                           gioihan4 =danh_sach_bai_viet_gioihan_4
                           ,gioihan10 = danh_sach_bai_viet_gioihan_10)
# @app.route('/contact', methods = ["POST", "GET"])
# def contact():
#     # return '<h1>Hello World!</h1>'
#     danh_muc_bai_viets = DanhMucBaiViet.query.all()
#     return render_template('contact.html' ,danh_muc_bai_viets=danh_muc_bai_viets)


@app.route('/contact', methods = ["POST", "GET"])
def contact_page():
    if request.method == "POST":
        ten = request.form['ten']
        email = request.form['email']
        sdt = request.form['sdt']
        noidung = request.form['noidung']
        # session.permanent = True
        try:
            with app.app_context():
                lienhe = contact(ten,email,sdt,noidung)
                db.session.add(lienhe)
                db.session.commit()                                                                                                                 
                flash('Thêm danh mục thành công', 'success')
        except Exception as e:
            flash(f'Lỗi khi thêm danh mục: {e}', 'error')
            db.session.rollback()    
    else:
        flash('Thêm danh mục thất bại', 'failed')
    danh_muc_bai_viets = DanhMucBaiViet.query.all()
    return render_template('contact.html' ,danh_muc_bai_viets=danh_muc_bai_viets)

@app.route('/admin/contact', methods = ["POST", "GET"])
def listcontact():
    lienhe = contact.query.all()
    return render_template('list_contact.html' ,lienhe=lienhe)

@app.route('/admin/edit_contact/<int:id>', methods=['GET', 'POST'])
def edit_contact(id):
    lienhe = contact.query.get(id)
    return render_template('view_contact.html', lienhe=lienhe)
@app.route('/admin/delete_contact/<int:id>', methods=['GET', 'POST'])
def delete_contact(id):
    lienhe = contact.query.get(id)

    if lienhe:
        db.session.delete(lienhe)
        db.session.commit()
        flash('Xóa liên hệ thành công', 'success')
    else:
        flash('Không tìm thấy liên hệ', 'error')

    return redirect(url_for('listcontact'))
@app.route('/chitiet')
def chitiet():
    danh_muc_bai_viets = DanhMucBaiViet.query.all()
    return render_template('single.html', danh_muc_bai_viets=danh_muc_bai_viets)
@app.route('/bai_viet/<int:id>')
def chi_tiet_bai_viet(id):
    bai_viet = QuanLyBaiViet.query.get(id)
    if bai_viet:
        return render_template('single.html', bai_viet=bai_viet)
    else:
        flash('Bài viết không tồn tại', 'error')
        return redirect(url_for('index'))
    
@app.route('/admin/xemchitiet_bai')
def xemchitiet_bai():
    return render_template('view_baiviet.html')

@app.route('/login', methods = ["POST", "GET"])
def login_user():
    if request.method == "POST":
        user_name = request.form['name']
        if user_name:
            session["user"] = user_name
            # flash("duong cu bu vc","info")
            found_user = User.query.filter_by(name = user_name).first()
            if found_user:
                session['email'] = found_user.email
            else:
                user = User(user_name,"asdsa@gmail.com")
                db.session.add(user)
                db.session.commit()
            flash("tao thanh cong","info")
            return redirect(url_for('user',name=user_name) )
            
            # return render_template('user.html',user=user_name)
    if "user" in session:
        name = session["user"]
        flash("duong cu bu vc","message")
        # return '<h1>Hello World! User: {}</h1>'.format(name)
        return redirect(url_for('user',name=name) )
        # return render_template('user.html',user=name)
    return render_template('login.html')
    # return '<h1>Hello World!</h1>'
    # return render_template('index.html')


@app.route('/user', methods = ["POST", "GET"])
def user():
    email = None
    if "user" in session:
        name = session["user"]
        # return '<h1>Hello World222222222222222222222222</h1>'
        # return '<h1>Hello World! User: {}</h1>'.format(name)

        if request.method == "POST":
            if not request.form['email'] and request.form['name']:    
                User.query.filter_by(name = name).delete()
                flash("anh duong bay mau","message")
                db.session.commit()
                return redirect(url_for('logout_user'))

            else:
                email = request.form['email']
                session['email'] = email
                found_user = User.query.filter_by(name = name).delete()
                found_user.email = email
                db.session.commit()
        elif "email" in session:
            email = session['email']
        return render_template('user.html',user=name, email= email)
    else:
        flash("tra tien để dc bucu a dương","message")
        return redirect(url_for('login_user'))
    
@app.route('/admin', methods = ["POST", "GET"])
def login_admin():
    return render_template('dashboard.html')
    
    
@app.route('/admin/dashboard')
def dashboard():
    return render_template('dashboard.html')    

@app.route('/admin/themdanhmuc', methods = ["POST", "GET"])
def themdanhmuc():
    if request.method == "POST":
        ten_DMuc = request.form['ten_DM']
        hinh_DM = request.form['img_DM']
        # session.permanent = True
        try:
            with app.app_context():
                DMuc = DanhMucBaiViet(ten_DM=ten_DMuc,hinh_anh_DM=hinh_DM)
                db.session.add(DMuc)
                db.session.commit()                                                                                                                 
                flash('Thêm danh mục thành công', 'success')
        except Exception as e:
            flash(f'Lỗi khi thêm danh mục: {e}', 'error')
            db.session.rollback()    
    else:
        flash('Thêm danh mục thất bại', 'failed')
    return render_template('themDM.html')




@app.route('/admin/listDM')
def listDM():
    danh_muc_bai_viets = DanhMucBaiViet.query.all()
    return render_template('list_DM.html', danh_muc_bai_viets=danh_muc_bai_viets)

@app.route('/danhmuc')
def danhmuc():
    danh_muc_bai_viets = DanhMucBaiViet.query.all()
    return render_template('category.html', danh_muc_bai_viets=danh_muc_bai_viets)



@app.route('/admin/xoa_danh_muc/<int:id>', methods=['GET', 'POST'])
def xoa_danh_muc(id):
    danh_muc_bai_viet = DanhMucBaiViet.query.get(id)       
    if danh_muc_bai_viet: 
        db.session.rollback()    
        db.session.delete(danh_muc_bai_viet)
        db.session.commit()
                             
        flash('Xóa thành công', 'success')
                
    else:
        flash('Không tìm thấy Danh Mục Bài Viết', 'error')
    return redirect(url_for('listDM'))

@app.route('/admin/sua_danh_muc/<int:id>', methods=['GET', 'POST'])
def sua_danh_muc(id):
    danh_muc_bai_viet = DanhMucBaiViet.query.get(id)
    
    if danh_muc_bai_viet:
        if request.method == 'POST':
            danh_muc_bai_viet.ten_DM = request.form['ten_DM']
            db.session.commit()
            flash('Cập nhật thành công', 'success')
            return redirect(url_for('listDM'))
        
        return render_template('View_DM.html', danh_muc_bai_viet=danh_muc_bai_viet)
    else:
        flash('Không tìm thấy Danh Mục Bài Viết', 'error')
        return redirect(url_for('listDM'))
    

@app.route('/admin/listbaiviet')
def listbaiviet():
    danh_sach_bai_viet = QuanLyBaiViet.query.all()
    return render_template('list_baiviet.html',danh_sach_bai_viet = danh_sach_bai_viet)
@app.route('/admin/thembai', methods=['GET', 'POST'])
def thembaiviet():
    if request.method == "POST":
        tieude = request.form['title_bai']
        hinhanh = request.form['img_bai']
        danhmuc_id = request.form['category']
        noidung = request.form['noidung_bai']
        try:
            with app.app_context():
                bai_viet  = QuanLyBaiViet(tieu_de=tieude, noi_dung=noidung,hinh_anh=hinhanh, danhmuc_id=danhmuc_id)
                db.session.add(bai_viet)
                db.session.commit()
                flash('Thêm danh mục thành công', 'success')
        except Exception as e:
            flash(f'Lỗi khi thêm danh mục: {e}', 'error')
            db.session.rollback()    
    else:
        flash('Thêm bài thất bại', 'failed')
    danh_sach_danh_muc = DanhMucBaiViet.query.all()
    return render_template('thembaiAD.html', danh_sach_danh_muc=danh_sach_danh_muc) 
    

@app.route('/danhmuc/<int:danhmuc_id>')
def hienthi_theo_danhmuc(danhmuc_id):
    danh_muc = DanhMucBaiViet.query.get(danhmuc_id)
    danh_muc_bai_viets = DanhMucBaiViet.query.all()
    if danh_muc:
        bai_viets = QuanLyBaiViet.query.filter_by(danhmuc_id=danhmuc_id).all()
        return render_template('category.html',danh_muc_bai_viets=danh_muc_bai_viets, danh_muc=danh_muc, bai_viets=bai_viets)
    else:
        flash('Không tìm thấy danh mục', 'error')
        return redirect(url_for('index'))
    


@app.route('/baiviet/<int:baiviet_id>')
def hienthi_chitiet_baiviet(baiviet_id):
    bai_viet = QuanLyBaiViet.query.get(baiviet_id)
    danh_muc_bai_viets = DanhMucBaiViet.query.all()    

    if bai_viet:
        return render_template('single.html', bai_viet=bai_viet,danh_muc_bai_viets=danh_muc_bai_viets)
    else:
        flash('Không tìm thấy bài viết', 'error')
        return redirect(url_for('index'))

@app.route('/admin/xoa_bai_viet/<int:id>', methods=['GET', 'POST'])
def xoa_bai_viet(id):
    bai_viet = QuanLyBaiViet.query.get(id)

    if bai_viet:
        db.session.delete(bai_viet)
        db.session.commit()
        flash('Xóa bài viết thành công', 'success')
        return redirect(url_for('listbaiviet'))

        # return render_template('xoa_bai_viet.html', bai_viet=bai_viet)
    else:
        flash('Không tìm thấy bài viết', 'error')
    return redirect(url_for('listbaiviet'))

@app.route('/admin/sua_bai_viet/<int:id>', methods=['GET', 'POST'])
def sua_bai_viet(id):
    bai_viet = QuanLyBaiViet.query.get(id)

    if bai_viet:
        if request.method == 'POST':
            bai_viet.tieu_de = request.form['title_bai']
            bai_viet.noi_dung = request.form['noidung_bai']
            # bai_viet.hinh_anh = request.form['hinh_anh']
            bai_viet.danhmuc_id = request.form['category']
            db.session.commit()
            flash('Cập nhật bài viết thành công', 'success')
            return redirect(url_for('listbaiviet'))

        danh_sach_danh_muc = DanhMucBaiViet.query.all()
        return render_template('view_baiviet.html', bai_viet=bai_viet, danh_sach_danh_muc=danh_sach_danh_muc)
    else:
        flash('Không tìm thấy bài viết', 'error')
        return redirect(url_for('listbaiviet'))





















if __name__ == '__main__':
    if not path.exists("webtintuc.db"):
    # db.create_all()
        with app.app_context():
            db.create_all()
        print("Đã tạo database")
    app.run(debug=True)     