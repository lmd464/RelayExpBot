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

    def add_bank_account(self, name, acc):
        self.account_dict[name] = acc

        # 파일에 추가
        self.account_txt = open("bank_account.txt", 'a')
        new_acc = name + " : " + acc
        self.account_txt.write("\n" + new_acc)
        self.account_txt.close()
        return "추가완료"

    def delete_bank_account(self, name):
        self.account_dict.pop(name)

        # 새 텍스트파일로 갱신
        self.account_txt = open("bank_account.txt", 'w')
        for key, value in self.account_dict:
            self.account_txt.write(key + " : " + value)
        self.account_txt.close()
        return "삭제완료"


