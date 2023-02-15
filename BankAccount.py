class BankAccount:

    def __init__(self):
        self.account_txt = open("bank_account.txt", 'r')
        self.account_dict = {}
        while True:
            line = self.account_txt.readline()
            if not line:
                break
            line = line.split(" : ")
            self.account_dict[line[0].strip()] = line[1].strip()

        self.account_txt.close()

    def get_bank_account(self, name):
        acc = self.account_dict.get(name)
        if acc is None:
            return "없다"
        else:
            return name + " : " + acc


