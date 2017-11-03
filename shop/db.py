from shopping_trolley.commodity_db import db, Commodity
from shopping_trolley.admain_db import db, User
# db.create_all()

# hiagt = Commodity('煎饼', '2')
# hiagt1 = Commodity('果子', '3')
# hiagt2 = Commodity('巧克力', '5')
hiagt3 = User('hiagt', '123', 'hiagt@h.com')

# db.session.add(hiagt)
# db.session.add(hiagt1)
# db.session.add(hiagt2)
db.session.add(hiagt3)
db.session.commit()


