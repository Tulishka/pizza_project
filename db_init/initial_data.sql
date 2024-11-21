
INSERT OR IGNORE INTO categories (id, title) VALUES (1, 'Овощи'), (2, 'Мясо'), (3, 'Сыр');

INSERT OR IGNORE INTO ingredients (name,title,serving_size,measure_unit,price,category_id,weight, auto_place_method)
    VALUES 
    ('mozzarella','Моцарелла', 4, 'шт.', 89, 3, 40, 'circle'),
    ('mozzarella_mini','Моцарелла мини', 6, 'шт.', 89, 3, 39, 'random'),
    ('olive','Оливки', 8, 'шт.', 69, 1, 24, 'random'),
    ('pepperoni','Пепперони', 6, 'шт.', 89, 2, 48, 'mosaic'),
    ('pineapple','Ананасы', 7, 'шт.', 69, 1, 56, 'random'),
    ('shrimp_royal','Королевские креветки', 3, 'шт.', 189, 2, 75, 'circle'),
    ('shrimp','Креветки', 5, 'шт.', 119, 2, 50, 'circle'),
    ('sweet_pepper','Сладкий перец', 3, 'шт.', 79, 1, 110, 'mosaic'),
    ('pickled_cucumbers','Маринованные огурцы', 6, 'шт.', 79, 1, 29, 'random'),
    ('oregano','Орегано', 5, 'шт.', 79, 1, 18, 'random'),
    ('onion','Лук', 3, 'шт.', 79, 1, 38, 'random'),
    ('jalapeno_pepper','Перец халапеньо', 6, 'шт.', 79, 1, 35, 'random'),
    ('ham','Ветчина', 5, 'шт.', 89, 2, 125, 'circle'),
    ('garlic','Чеснок', 8, 'шт.', 69, 1, 28, 'random'),
    ('chicken_breast','Куринная грудка', 4, 'шт.', 89, 2, 128, 'circle'),
    ('cheddar_cheese','Сыр чеддер', 4, 'шт.', 89, 3, 79, 'circle'),
    ('champignons','Шампиньоны', 6, 'шт.', 69, 1, 65, 'random'),
    ('bacon','Бекон', 5, 'шт.', 89, 2, 48, 'circle'),
    ('tomato','Томаты', 5, 'шт.', 79, 1, 130, 'circle');
                           
INSERT OR IGNORE INTO dough_types (id, title, unit_weight, img) 
    VALUES 
    (1, 'Традиционная', 1, 'pizza_big_base.png'), 
    (2, 'Тонкое тесто', 0.9, 'pizza_small_base.png');
            
INSERT OR IGNORE INTO souses (id, title, unit_weight, img)
    VALUES 
    (1, 'Томатный', 1, 'tomato_souse.png'), 
    (2, 'Сливочный', 1, 'creamy_souse.png');
           
INSERT OR IGNORE INTO base_prices (dought_tipe_id, souse_id, size, price)
    VALUES 
    (1, 1, 25, 419),
    (1, 2, 25, 419),
    (2, 1, 25, 419),
    (2, 2, 25, 419),
    (1, 1, 30, 569),
    (1, 2, 30, 569),
    (2, 1, 30, 569),
    (2, 2, 30, 569),
    (1, 1, 35, 719),
    (1, 2, 35, 719),
    (2, 1, 35, 719),
    (2, 2, 35, 719),
    (1, 1, 40, 869),
    (1, 2, 40, 869),
    (2, 1, 40, 869),
    (2, 2, 40, 869)
    
