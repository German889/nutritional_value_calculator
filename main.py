from flask import Flask, request, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)
# Настройка SQLAlchemy с SQLite для примера
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///nutrition.db'
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# Определение модели продукта в базе данных
class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    protein = db.Column(db.Float, nullable=False)  # грамм белка на 100 г
    fat = db.Column(db.Float, nullable=False)      # грамм жира на 100 г
    carbohydrate = db.Column(db.Float, nullable=False)  # грамм углеводов на 100 г
    category = db.Column(db.String(50), nullable=False)

    def __repr__(self):
        return f'<Product {self.name}>'

@app.route('/')
def index():
    categories = Product.query.with_entities(Product.category).distinct().all()
    category_dict = {category[0]: Product.query.filter_by(category=category[0]).all() for category in categories}
    products = Product.query.all()
    print(category_dict)
    return render_template('index.html', products=products, category_dict=category_dict)

@app.route('/add-product', methods=['GET', 'POST'])
def add_product():
    if request.method == 'POST':
        # Получение данных из формы
        name = request.form.get('name')
        protein = request.form.get('protein', type=float)
        fat = request.form.get('fat', type=float)
        carbohydrate = request.form.get('carbohydrate', type=float)
        category = request.form.get('category')
        
        # Создание нового объекта продукта
        new_product = Product(name=name, protein=protein, fat=fat, carbohydrate=carbohydrate, category=category)
        
        # Добавление в сессию и сохранение в базу данных
        db.session.add(new_product)
        db.session.commit()
        
        # Перенаправление на главную страницу с формой
        return redirect(url_for('index'))
    
    # Для GET-запроса просто отображаем форму
    return render_template('add_product.html')

@app.route('/process', methods=['POST'])
def process():
    selected_products_ids = request.form.getlist('product')
    selected_products = [Product.query.get(id) for id in selected_products_ids]
    return render_template('selected_products.html', products=selected_products)

@app.route('/calculate', methods=['POST'])
def calculate():
    dish_nutrition = {'protein': 0, 'fat': 0, 'carbohydrate': 0, 'energy_value':0}
    ingredients_nutrition = []

    # Обработка каждого поля формы
    for key in request.form:
        if key.startswith('weight_'):
            # Получение ID продукта
            product_id = key.split('_')[1]
            # Получение продукта по ID
            product = Product.query.get(product_id)
            # Получение количества (веса) продукта из формы
            amount = float(request.form[key])

            if product and amount:
                # Расчет питательной информации
                protein = product.protein * amount / 100
                fat = product.fat * amount / 100
                carbohydrate = product.carbohydrate * amount / 100
                energy_value = 4*protein+9*fat+4*carbohydrate

                # Добавление питательной информации к общему блюду
                dish_nutrition['protein'] += protein
                dish_nutrition['fat'] += fat
                dish_nutrition['carbohydrate'] += carbohydrate
                dish_nutrition['energy_value'] += energy_value
                
                # Сохранение информации о каждом продукте
                ingredients_nutrition.append({
                    'name': product.name,
                    'protein': round(protein, 2),
                    'fat': round(fat, 2),
                    'carbohydrate': round(carbohydrate, 2),
                    'energy_value': round(energy_value, 2),
                    'amount': amount
                })

    # Возвращение результатов расчета
    return render_template('results.html', dish_nutrition=dish_nutrition, ingredients=ingredients_nutrition)

if __name__ == '__main__':
    db.create_all() # Создайте таблицы
    app.run(debug=True)
