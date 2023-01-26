# import json

import sqlalchemy as sq
from sqlalchemy.orm import declarative_base, relationship, sessionmaker

engine = sq.create_engine('postgresql://postgres:7355608@localhost:5432/netology_db')

Session = sessionmaker(bind=engine)
session = Session()

Base = declarative_base()


class Publisher(Base):
    __tablename__ = 'publisher'

    id = sq.Column(sq.Integer, primary_key=True)
    name = sq.Column(sq.String(250), nullable=False)

    book = relationship('Book', back_populates='publisher')


class Book(Base):
    __tablename__ = 'book'

    id = sq.Column(sq.Integer, primary_key=True)
    title = sq.Column(sq.String(250), nullable=False)
    id_publisher = sq.Column(sq.Integer, sq.ForeignKey('publisher.id'), nullable=False)

    publisher = relationship('Publisher', back_populates='book')
    stock1 = relationship('Stock', back_populates='books')


class Shop(Base):
    __tablename__ = 'shop'
    
    id = sq.Column(sq.Integer, primary_key=True)
    name = sq.Column(sq.String(250), nullable=False)

    stock2 = relationship('Stock', back_populates='shop')


class Stock(Base):
    __tablename__ = 'stock'

    id = sq.Column(sq.Integer, primary_key=True)
    id_book = sq.Column(sq.Integer, sq.ForeignKey('book.id'), nullable=False)
    id_shop = sq.Column(sq.Integer, sq.ForeignKey('shop.id'), nullable=False)
    count = sq.Column(sq.Integer)

    books = relationship('Book', back_populates='stock1')
    shop = relationship('Shop', back_populates='stock2')
    sale = relationship('Sale', back_populates='stock3')


class Sale(Base):
    __tablename__ = 'sale'

    id = sq.Column(sq.Integer, primary_key=True)
    price = sq.Column(sq.Float, nullable=False)
    date_sale = sq.Column(sq.Date, nullable=False)
    id_stock = sq.Column(sq.Integer, sq.ForeignKey('stock.id'), nullable=False)
    count = sq.Column(sq.Integer)

    stock3 = relationship('Stock', back_populates='sale')


Base.metadata.create_all(engine)


# with open('fixtures.json', 'r', encoding='utf-8') as file:
#     data = json.load(file)

# for record in data:
#     model = {
#         'publisher': Publisher,
#         'shop': Shop,
#         'book': Book,
#         'stock': Stock,
#         'sale': Sale,
#     }[record.get('model')]
#     session.add(model(id=record.get('pk'), **record.get('fields')))
# session.commit()


def orders_info_by_author(name):
    data = session.query(Book, Shop, Sale).join(Publisher, Publisher.id == Book.id_publisher)\
        .join(Stock, Stock.id_book == Book.id).join(Shop, Shop.id == Stock.id_shop)\
            .join(Sale, Sale.id_stock == Stock.id).filter(Publisher.name == name).all()
    for book, shop, sale in data:
        print(book.title, ' | ', shop.name, ' | ', sale.price, ' | ', sale.date_sale)


def main():
    name = input('Введите имя автора: ')
    orders_info_by_author(name)
    session.close()


if __name__ == '__main__':
    main()
