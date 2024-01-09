from DBPackage.DBclass import DBMethods


class Paginator:
    #TODO: пропиши доку плз (какой метод для чего применяется, типизация данных
    def __init__(self, telegram_id):
        # Getting card values if card has no attribute "learned"
        self.card_values = [i for i in DBMethods.get_active_collection_cards(telegram_id) if i[2] == 0]
        self.cur_pos = 1

    def get_start(self):
        return self.card_values[self.cur_pos - 1][0]

    def get_card_fwd(self):
        self.cur_pos += 1
        return self.card_values[self.cur_pos - 1][0]

    def get_card_bck(self):
        self.cur_pos -= 1
        return self.card_values[self.cur_pos + 1][0]

    def get_response(self):
        return self.card_values[self.cur_pos][1]

    def set_learned(self):
        # Setting learned status for card
        DBMethods.set_card_learned_status(self.card_values[self.cur_pos][3])
        # Deleting card from local list
        del self.card_values[self.cur_pos]
        # Setting pointer for previous position if current not exists
        self.cur_pos = self.cur_pos - 1 if len(self.card_values) < self.cur_pos + 1 else self.cur_pos

    def get_len(self):
        return len(self.card_values)

    def get_pos(self):
        return self.cur_pos
