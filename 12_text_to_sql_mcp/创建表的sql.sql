-- 1. 作者表
CREATE TABLE authors (
    id INT PRIMARY KEY AUTO_INCREMENT COMMENT '作者ID',
    name VARCHAR(100) NOT NULL COMMENT '作者姓名',
    country VARCHAR(50) NOT NULL COMMENT '国家',
    birth_year INT DEFAULT NULL COMMENT '出生年份'
) COMMENT '作者信息表';

-- 2. 图书表
CREATE TABLE books (
    id INT PRIMARY KEY AUTO_INCREMENT COMMENT '图书ID',
    author_id INT NOT NULL COMMENT '作者ID',
    title VARCHAR(200) NOT NULL COMMENT '书名',
    category VARCHAR(50) NOT NULL COMMENT '分类',
    price DECIMAL(10,2) NOT NULL COMMENT '价格',
    stock INT NOT NULL DEFAULT 0 COMMENT '库存',
    sold_count INT NOT NULL DEFAULT 0 COMMENT '销量',
    publish_date DATE NOT NULL COMMENT '出版日期',
    publisher VARCHAR(100) DEFAULT NULL COMMENT '出版社',
    CONSTRAINT fk_books_author
        FOREIGN KEY (author_id) REFERENCES authors(id)
        ON DELETE CASCADE
) COMMENT '图书信息表';

-- 插入作者数据
INSERT INTO authors (name, country, birth_year) VALUES
('刘慈欣', '中国', 1963),
('余华', '中国', 1960),
('东野圭吾', '日本', 1958),
('J.K.罗琳', '英国', 1965),
('加西亚·马尔克斯', '哥伦比亚', 1927),
('尤瓦尔·赫拉利', '以色列', 1976),
('史蒂芬·霍金', '英国', 1942),
('当年明月', '中国', 1979),
('Eric Matthes', '美国', 1980);

-- 插入图书数据
INSERT INTO books
(author_id, title, category, price, stock, sold_count, publish_date, publisher)
VALUES
(1, '三体', '科幻', 93.00, 25, 300, '2008-01-01', '重庆出版社'),
(1, '流浪地球', '科幻', 45.00, 40, 180, '2016-01-01', '长江文艺出版社'),
(2, '活着', '文学', 45.00, 50, 200, '2012-08-01', '作家出版社'),
(2, '许三观卖血记', '文学', 39.00, 30, 120, '2012-09-01', '作家出版社'),
(3, '解忧杂货店', '文学', 39.50, 35, 180, '2014-05-01', '南海出版公司'),
(3, '白夜行', '悬疑', 49.50, 28, 160, '2013-01-01', '南海出版公司'),
(4, '哈利·波特与魔法石', '儿童', 69.00, 40, 260, '2000-09-01', '人民文学出版社'),
(4, '哈利·波特与密室', '儿童', 69.00, 38, 240, '2000-10-01', '人民文学出版社'),
(5, '百年孤独', '文学', 55.00, 20, 150, '2011-06-01', '南海出版公司'),
(6, '人类简史', '历史', 68.00, 12, 110, '2014-11-01', '中信出版社'),
(6, '未来简史', '历史', 68.00, 15, 95, '2017-01-01', '中信出版社'),
(7, '时间简史', '科技', 45.00, 18, 70, '2010-04-01', '湖南科学技术出版社'),
(8, '明朝那些事儿', '历史', 299.00, 8, 90, '2011-10-01', '浙江人民出版社'),
(9, 'Python编程 从入门到实践', '计算机', 89.00, 30, 120, '2023-05-01', '人民邮电出版社');